"""WordPress provider.

This provider performs lightweight WordPress checks for the JamesOS public
portfolio site.  It deliberately keeps all shell access behind the provider
boundary so the rest of JamesOS can reason over structured results.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from jamesos.core.models import CheckResult
from jamesos.core.shell import run


class WordPressProvider:
    """Inspect and health-check the WordPress service."""

    name = "wordpress"

    def __init__(
        self,
        container: str | None = None,
        public_url: str | None = None,
    ) -> None:
        self.container = container or os.getenv(
            "JAMESOS_WORDPRESS_CONTAINER",
            "wordpress-wordpress-1",
        )
        self.public_url = (
            public_url
            or os.getenv("JAMESOS_WORDPRESS_URL", "https://jamesallendoerfer.com")
        ).rstrip("/")

    def health(self) -> CheckResult:
        state = self._state()
        if state.get("error"):
            return CheckResult(
                name="WordPress",
                status="fail",
                message="WordPress state could not be read from the container.",
                details=state,
            )

        unexpected_php = self._unexpected_root_php()
        login_integrity = self._wp_login_integrity()
        urls = self._public_urls()

        details: dict[str, Any] = {
            "container": self.container,
            "public_url": self.public_url,
            "state": state,
            "unexpected_root_php": unexpected_php,
            "wp_login_integrity": login_integrity,
            "public_urls": urls,
        }

        failures: list[str] = []
        warnings: list[str] = []

        if unexpected_php:
            failures.append(
                "unexpected PHP file(s) exist in the WordPress web root"
            )

        if login_integrity.get("status") != "ok":
            failures.append("wp-login.php does not match the clean Docker image")

        if str(state.get("blog_public")) != "1":
            failures.append("WordPress is discouraging search engines")

        home = str(state.get("home", ""))
        siteurl = str(state.get("siteurl", ""))
        option_home = str(state.get("option_home", ""))
        option_siteurl = str(state.get("option_siteurl", ""))
        wp_home = str(state.get("wp_home", ""))
        wp_siteurl = str(state.get("wp_siteurl", ""))

        if home and not home.startswith("https://"):
            warnings.append("WordPress home URL is not HTTPS")
        if siteurl and not siteurl.startswith("https://"):
            warnings.append("WordPress site URL is not HTTPS")
        if option_home and not option_home.startswith("https://"):
            warnings.append("WordPress home option is not HTTPS")
        if option_siteurl and not option_siteurl.startswith("https://"):
            warnings.append("WordPress siteurl option is not HTTPS")
        if wp_home and wp_home != "None" and not wp_home.startswith("https://"):
            warnings.append("WordPress WP_HOME constant is not HTTPS")
        if wp_siteurl and wp_siteurl != "None" and not wp_siteurl.startswith("https://"):
            warnings.append("WordPress WP_SITEURL constant is not HTTPS")

        if state.get("disallow_file_edit") is not True:
            warnings.append("DISALLOW_FILE_EDIT is not enabled")
        if state.get("disallow_file_mods") is not True:
            warnings.append("DISALLOW_FILE_MODS is not enabled")

        if urls.get("home") != 200:
            warnings.append("public homepage did not return HTTP 200")
        if urls.get("sitemap") != 200:
            warnings.append("WordPress sitemap did not return HTTP 200")
        if urls.get("xmlrpc") not in {401, 403, 404}:
            warnings.append("XML-RPC is not blocked at the public edge/origin")

        if failures:
            return CheckResult(
                name="WordPress",
                status="fail",
                message="; ".join(failures),
                details=details,
            )

        if warnings:
            return CheckResult(
                name="WordPress",
                status="warn",
                message="; ".join(warnings),
                details=details,
            )

        return CheckResult(
            name="WordPress",
            status="ok",
            message="WordPress core, sitemap, and security checks passed.",
            details=details,
        )

    def inventory(self) -> dict[str, object]:
        return {
            "container": self.container,
            "public_url": self.public_url,
            "state": self._state(),
            "unexpected_root_php": self._unexpected_root_php(),
            "wp_login_integrity": self._wp_login_integrity(),
            "public_urls": self._public_urls(),
        }

    def _state(self) -> dict[str, object]:
        parsed = urllib.parse.urlparse(self.public_url)
        host = parsed.netloc or "jamesallendoerfer.com"

        code = f'''
$_SERVER["HTTPS"] = "on";
$_SERVER["HTTP_X_FORWARDED_PROTO"] = "https";
$_SERVER["HTTP_HOST"] = "{host}";
$_SERVER["SERVER_PORT"] = "443";
require "/var/www/html/wp-load.php";
$out = array(
    "version" => get_bloginfo("version"),
    "home" => home_url("/"),
    "siteurl" => site_url("/"),
    "option_home" => get_option("home"),
    "option_siteurl" => get_option("siteurl"),
    "wp_home" => defined("WP_HOME") ? WP_HOME : null,
    "wp_siteurl" => defined("WP_SITEURL") ? WP_SITEURL : null,
    "disallow_file_edit" => defined("DISALLOW_FILE_EDIT") ? DISALLOW_FILE_EDIT : false,
    "disallow_file_mods" => defined("DISALLOW_FILE_MODS") ? DISALLOW_FILE_MODS : false,
    "blog_public" => get_option("blog_public"),
    "theme" => wp_get_theme()->get("Name"),
    "active_plugins" => get_option("active_plugins"),
);
echo json_encode($out, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
'''
        result = run(["docker", "exec", self.container, "php", "-r", code], timeout=20)
        if not result.ok:
            return {
                "error": "php_state_failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError:
            return {
                "error": "invalid_json",
                "stdout": result.stdout,
            }

    def _unexpected_root_php(self) -> list[str]:
        command = r'''
for f in /var/www/html/*.php; do
    base=$(basename "$f")
    if [ ! -f "/usr/src/wordpress/$base" ] && [ "$base" != "wp-config.php" ]; then
        echo "$base"
    fi
done
'''
        result = run(["docker", "exec", self.container, "sh", "-lc", command], timeout=20)
        if not result.ok:
            return [f"ERROR: {result.stderr or result.stdout}"]
        return [line for line in result.stdout.splitlines() if line.strip()]

    def _wp_login_integrity(self) -> dict[str, object]:
        command = r'''
if [ ! -f /var/www/html/wp-login.php ]; then
    echo missing
    exit 0
fi
if cmp -s /usr/src/wordpress/wp-login.php /var/www/html/wp-login.php; then
    echo ok
else
    echo mismatch
fi
'''
        result = run(["docker", "exec", self.container, "sh", "-lc", command], timeout=20)
        if not result.ok:
            return {
                "status": "error",
                "stderr": result.stderr,
                "stdout": result.stdout,
            }
        status = result.stdout.strip() or "unknown"
        return {"status": status}

    def _public_urls(self) -> dict[str, int]:
        return {
            "home": self._http_status(f"{self.public_url}/"),
            "sitemap": self._http_status(f"{self.public_url}/wp-sitemap.xml"),
            "xmlrpc": self._http_status(f"{self.public_url}/xmlrpc.php"),
        }

    def _http_status(self, url: str) -> int:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "JamesOS/0.2 WordPressProvider"},
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return int(response.status)
        except urllib.error.HTTPError as exc:
            return int(exc.code)
        except Exception:
            return 0

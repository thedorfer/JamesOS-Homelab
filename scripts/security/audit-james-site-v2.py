#!/usr/bin/env python3
# Comprehensive pre-index audit for jamesallendoerfer.com.
# Read-only: this script makes no changes.

import html
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser

BASE = "https://jamesallendoerfer.com"
DOMAIN = "jamesallendoerfer.com"
CONTAINER = "wordpress-wordpress-1"
UA = "Mozilla/5.0 (compatible; JamesSiteAudit/2.0; +https://jamesallendoerfer.com/)"

PASS = []
WARN = []
FAIL = []

def note(kind, text):
    {"PASS": PASS, "WARN": WARN, "FAIL": FAIL}[kind].append(text)

def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)

def docker_php(code):
    r = run(["docker", "exec", CONTAINER, "php", "-r", code])
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip())
    return r.stdout

def fetch(url, timeout=20):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": UA, "Accept": "*/*"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.geturl(), resp.headers, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.geturl(), e.headers, e.read()
    except Exception as e:
        return 0, url, {}, str(e).encode("utf-8", "replace")

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title_parts = []
        self.in_title = False
        self.h1s = []
        self.in_h1 = False
        self.h1_parts = []
        self.description = ""
        self.robots = ""
        self.canonical = ""
        self.links = []
        self.images = []
        self.lang = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang", "").strip()
        elif tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.in_h1 = True
            self.h1_parts = []
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.description = a.get("content", "").strip()
            elif name == "robots":
                self.robots = a.get("content", "").strip()
        elif tag == "link":
            rel = a.get("rel", "")
            if isinstance(rel, str) and "canonical" in rel.lower():
                self.canonical = a.get("href", "").strip()
        elif tag == "a":
            href = a.get("href")
            if href:
                self.links.append(href)
        elif tag == "img":
            self.images.append(
                {
                    "src": a.get("src", ""),
                    "alt_present": "alt" in a,
                    "alt": a.get("alt", ""),
                }
            )

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag == "h1":
            self.in_h1 = False
            text = re.sub(r"\s+", " ", "".join(self.h1_parts)).strip()
            if text:
                self.h1s.append(text)

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self.in_h1:
            self.h1_parts.append(data)

    @property
    def title(self):
        return re.sub(r"\s+", " ", "".join(self.title_parts)).strip()

def normalize_internal(base, href):
    href = html.unescape(href.strip())

    if (
        not href
        or href.startswith("#")
        or href.startswith("mailto:")
        or href.startswith("tel:")
        or href.startswith("javascript:")
        or href.startswith("data:")
    ):
        return None

    absolute = urllib.parse.urljoin(base, href)
    p = urllib.parse.urlsplit(absolute)

    if p.hostname != DOMAIN:
        return None

    # Cloudflare Email Address Obfuscation uses a JavaScript pseudo-link.
    if p.path == "/cdn-cgi/l/email-protection":
        return None

    # Exclude WordPress admin/API paths from the public-link audit.
    if (
        p.path.startswith("/wp-admin")
        or p.path.startswith("/wp-login.php")
        or p.path.startswith("/wp-json/")
    ):
        return None

    return urllib.parse.urlunsplit(
        ("https", DOMAIN, p.path or "/", p.query, "")
    )

print("============================================================")
print(" JAMESALLENDOERFER.COM - PRE-INDEX AUDIT V2")
print("============================================================")
print("Read-only: no files or WordPress settings will be changed.\n")

# --------------------------------------------------------------------
# 1. WORDPRESS LOCAL STATE
# --------------------------------------------------------------------
print("=== 1. WORDPRESS LOCAL STATE ===")

try:
    php_code = r'''
require "/var/www/html/wp-load.php";

$published = get_pages(array(
    "post_status" => "publish",
    "sort_column" => "post_title",
));

$private = get_pages(array(
    "post_status" => "private",
    "sort_column" => "post_title",
));

$out = array(
    "version" => get_bloginfo("version"),
    "home" => home_url("/"),
    "siteurl" => site_url("/"),
    "blog_public" => get_option("blog_public"),
    "active_plugins" => get_option("active_plugins"),
    "published" => array(),
    "private" => array(),
);

foreach ($published as $p) {
    $out["published"][] = array(
        "title" => html_entity_decode(get_the_title($p->ID), ENT_QUOTES | ENT_HTML5, "UTF-8"),
        "slug" => $p->post_name,
        "url" => get_permalink($p->ID),
    );
}

foreach ($private as $p) {
    $out["private"][] = array(
        "title" => html_entity_decode(get_the_title($p->ID), ENT_QUOTES | ENT_HTML5, "UTF-8"),
        "slug" => $p->post_name,
        "url" => get_permalink($p->ID),
    );
}

echo json_encode($out, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
'''
    state = json.loads(docker_php(php_code))

    print(f"WordPress version : {state['version']}")
    print(f"Home URL          : {state['home']}")
    print(f"Site URL          : {state['siteurl']}")
    print(f"Search visibility : {'PUBLIC' if str(state['blog_public']) == '1' else 'DISCOURAGED'}")
    print(f"Active plugins    : {len(state['active_plugins'])}")

    if str(state["blog_public"]) == "1":
        note("PASS", "WordPress search-engine visibility is enabled.")
    else:
        note("FAIL", "WordPress is discouraging search engines (blog_public != 1).")

    published_pages = state["published"]
    private_pages = state["private"]

    print("\nPublished pages:")
    for p in published_pages:
        print(f"  - {p['title']}: {p['url']}")

    print("\nPrivate pages:")
    if private_pages:
        for p in private_pages:
            print(f"  - {p['title']}: {p['url']}")
    else:
        print("  None")

except Exception as e:
    print(f"ERROR reading WordPress state: {e}")
    note("FAIL", f"Could not read WordPress state: {e}")
    published_pages = []
    private_pages = []

print("\nMU plugins:")
r = run([
    "docker", "exec", CONTAINER, "sh", "-lc",
    'find /var/www/html/wp-content/mu-plugins -maxdepth 1 -type f -printf "%f\\n" 2>/dev/null | sort',
])
mu = [x for x in r.stdout.splitlines() if x.strip()]
if mu:
    for f in mu:
        print(f"  - {f}")
else:
    print("  None")

# --------------------------------------------------------------------
# 2. CORE INTEGRITY
# --------------------------------------------------------------------
print("\n=== 2. WORDPRESS CORE INTEGRITY ===")

core_cmd = r'''
set -eu
SRC=/usr/src/wordpress
WEB=/var/www/html

missing=/tmp/audit-missing.txt
modified=/tmp/audit-modified.txt
extra=/tmp/audit-extra.txt
: > "$missing"
: > "$modified"
: > "$extra"

cd "$SRC"

find . -type f \
    ! -path "./wp-content/*" \
    ! -name "wp-config-sample.php" \
    ! -name ".htaccess" \
    -print |
while IFS= read -r rel; do
    target="$WEB/${rel#./}"

    if [ ! -f "$target" ]; then
        echo "${rel#./}" >> "$missing"
        continue
    fi

    sh1=$(sha256sum "$rel" | awk "{print \$1}")
    sh2=$(sha256sum "$target" | awk "{print \$1}")

    if [ "$sh1" != "$sh2" ]; then
        echo "${rel#./}" >> "$modified"
    fi
done

for dir in wp-admin wp-includes; do
    if [ -d "$WEB/$dir" ]; then
        find "$WEB/$dir" -type f -print |
        while IFS= read -r target; do
            rel="${target#"$WEB/"}"
            if [ ! -f "$SRC/$rel" ]; then
                echo "$rel" >> "$extra"
            fi
        done
    fi
done

echo "---MISSING---"
cat "$missing"
echo "---MODIFIED---"
cat "$modified"
echo "---EXTRA---"
cat "$extra"
'''

r = run(["docker", "exec", CONTAINER, "sh", "-lc", core_cmd])
if r.returncode != 0:
    print(r.stderr)
    note("FAIL", "WordPress core integrity check failed to run.")
else:
    text = r.stdout
    missing_part = text.split("---MISSING---", 1)[1].split("---MODIFIED---", 1)[0].strip()
    modified_part = text.split("---MODIFIED---", 1)[1].split("---EXTRA---", 1)[0].strip()
    extra_part = text.split("---EXTRA---", 1)[1].strip()

    missing = [x for x in missing_part.splitlines() if x.strip()]
    modified = [x for x in modified_part.splitlines() if x.strip()]
    extra = [x for x in extra_part.splitlines() if x.strip()]

    print(f"Missing core files    : {len(missing)}")
    print(f"Modified core files   : {len(modified)}")
    print(f"Unexpected core files : {len(extra)}")

    if missing:
        print("\nMissing:")
        for x in missing:
            print(f"  - {x}")
        note("FAIL", f"{len(missing)} WordPress core file(s) are missing.")
    else:
        note("PASS", "No WordPress core files are missing.")

    if modified:
        print("\nModified:")
        for x in modified:
            print(f"  - {x}")
        note("WARN", f"{len(modified)} WordPress core file(s) differ from the Docker image.")
    else:
        note("PASS", "No WordPress core hash mismatches found.")

    if extra:
        print("\nUnexpected files in core directories:")
        for x in extra:
            print(f"  - {x}")
        note("FAIL", f"{len(extra)} unexpected file(s) exist inside wp-admin/wp-includes.")
    else:
        note("PASS", "No unexpected files found inside wp-admin/wp-includes.")

# --------------------------------------------------------------------
# 3. PUBLIC PAGE AUDIT
# --------------------------------------------------------------------
print("\n=== 3. PUBLIC PAGE SEO / CRAWL AUDIT ===")

page_results = []
all_internal_links = set()

for pinfo in published_pages:
    url = pinfo["url"]
    status, final, headers, body = fetch(url)
    ctype = headers.get("Content-Type", "") if hasattr(headers, "get") else ""

    parser = PageParser()
    if "text/html" in ctype.lower():
        try:
            parser.feed(body.decode("utf-8", "replace"))
        except Exception:
            pass

    title = parser.title
    missing_alt_attr = [
        img["src"] for img in parser.images if not img["alt_present"]
    ]
    empty_alt = [
        img["src"]
        for img in parser.images
        if img["alt_present"] and not img["alt"].strip()
    ]

    issues = []

    if status != 200:
        issues.append(f"HTTP {status}")
        note("FAIL", f"{url} returned HTTP {status}.")

    if not title:
        issues.append("NO TITLE")
        note("FAIL", f"{url} has no HTML title.")
    elif len(title) > 70:
        issues.append(f"REVIEW TITLE LENGTH ({len(title)})")
        note("WARN", f"{url} title is {len(title)} characters.")

    if not parser.description:
        issues.append("NO META DESCRIPTION")
        note("WARN", f"{url} has no meta description.")
    elif len(parser.description) < 105:
        issues.append(f"SHORT DESCRIPTION ({len(parser.description)})")
        note("WARN", f"{url} meta description is short ({len(parser.description)} chars).")
    elif len(parser.description) > 165:
        issues.append(f"LONG DESCRIPTION ({len(parser.description)})")
        note("WARN", f"{url} meta description is long ({len(parser.description)} chars).")

    if "noindex" in parser.robots.lower():
        issues.append("NOINDEX")
        note("FAIL", f"{url} contains a noindex directive.")

    if not parser.h1s:
        issues.append("NO H1")
        note("WARN", f"{url} has no H1.")
    elif len(parser.h1s) > 1:
        issues.append(f"{len(parser.h1s)} H1s")
        note("WARN", f"{url} has {len(parser.h1s)} H1 elements.")

    if not parser.canonical:
        issues.append("NO CANONICAL")
        note("WARN", f"{url} has no canonical URL.")
    else:
        expected = final.rstrip("/")
        actual = parser.canonical.rstrip("/")
        if expected != actual:
            issues.append("CANONICAL DIFFERS")
            note("WARN", f"{url} canonical points to {parser.canonical}.")

    if missing_alt_attr:
        issues.append(f"{len(missing_alt_attr)} IMG(S) HAVE NO ALT ATTRIBUTE")
        note("WARN", f"{url} has {len(missing_alt_attr)} image(s) without an alt attribute.")

    print("\n" + url)
    print(f"  HTTP        : {status}")
    print(f"  Title ({len(title):>3}) : {title or '(missing)'}")
    print(f"  Description : {parser.description or '(missing)'}")
    print(f"  Canonical   : {parser.canonical or '(missing)'}")
    print(f"  Robots      : {parser.robots or '(default)'}")
    print(f"  H1          : {parser.h1s or '(missing)'}")
    print(f"  Images      : {len(parser.images)} total; {len(missing_alt_attr)} missing alt attribute; {len(empty_alt)} empty/decorative alt")
    print("  Result      : " + ("OK" if not issues else "; ".join(issues)))

    page_results.append(
        {
            "url": url,
            "title": title,
            "description": parser.description,
            "links": parser.links,
            "status": status,
        }
    )

    for href in parser.links:
        target = normalize_internal(final, href)
        if target:
            all_internal_links.add(target)

if page_results and all(x["status"] == 200 for x in page_results):
    note("PASS", "All published pages return HTTP 200.")

# --------------------------------------------------------------------
# 4. DUPLICATE SEO METADATA
# --------------------------------------------------------------------
print("\n=== 4. DUPLICATE TITLES / DESCRIPTIONS ===")

title_counts = Counter(x["title"] for x in page_results if x["title"])
desc_counts = Counter(x["description"] for x in page_results if x["description"])

dupe_titles = {k: v for k, v in title_counts.items() if v > 1}
dupe_desc = {k: v for k, v in desc_counts.items() if v > 1}

if dupe_titles:
    print("Duplicate titles:")
    for k, v in dupe_titles.items():
        print(f"  {v}x {k}")
    note("WARN", "Duplicate HTML titles found.")
else:
    print("Duplicate titles: None")
    note("PASS", "All audited page titles are unique.")

if dupe_desc:
    print("Duplicate descriptions:")
    for k, v in dupe_desc.items():
        print(f"  {v}x {k}")
    note("WARN", "Duplicate meta descriptions found.")
else:
    print("Duplicate descriptions: None")
    note("PASS", "All audited meta descriptions are unique.")

# --------------------------------------------------------------------
# 5. INTERNAL LINKS
# --------------------------------------------------------------------
print("\n=== 5. INTERNAL LINK STATUS ===")

broken = []
checked = 0

for url in sorted(all_internal_links):
    status, final, headers, body = fetch(url)
    checked += 1
    if status == 0 or status >= 400:
        broken.append((status, url))

print(f"Checked {checked} unique internal links.")

if broken:
    for status, url in broken:
        print(f"  {status}: {url}")
    note("FAIL", f"{len(broken)} broken internal link(s) found.")
else:
    print("No broken internal links found.")
    note("PASS", "No broken internal links found.")

# --------------------------------------------------------------------
# 6. ROBOTS
# --------------------------------------------------------------------
print("\n=== 6. ROBOTS.TXT ===")

robots_url = BASE + "/robots.txt"
status, final, headers, body = fetch(robots_url)
robots_text = body.decode("utf-8", "replace")
print(f"HTTP {status}")
print(robots_text[:4000])

if status != 200:
    note("WARN", f"robots.txt returned HTTP {status}.")
elif re.search(r"(?im)^\s*Disallow:\s*/\s*$", robots_text):
    note("FAIL", "robots.txt appears to disallow the entire site.")
else:
    note("PASS", "robots.txt does not globally block crawling.")

# --------------------------------------------------------------------
# 7. SITEMAPS - RECURSIVE
# --------------------------------------------------------------------
print("\n=== 7. WORDPRESS SITEMAPS ===")

sitemap_index_url = BASE + "/wp-sitemap.xml"
status, final, headers, body = fetch(sitemap_index_url)
print(f"Index: {sitemap_index_url}")
print(f"HTTP {status}")

all_sitemap_urls = set()

if status == 200:
    note("PASS", "WordPress sitemap index returns HTTP 200.")
    try:
        root = ET.fromstring(body)
        child_sitemaps = [
            el.text.strip()
            for el in root.iter()
            if el.tag.endswith("loc") and el.text
        ]

        print(f"Child sitemaps: {len(child_sitemaps)}")

        for child in child_sitemaps:
            cstatus, cfinal, cheaders, cbody = fetch(child)
            print(f"  {cstatus} {child}")

            if cstatus != 200:
                note("FAIL", f"Child sitemap returned HTTP {cstatus}: {child}")
                continue

            try:
                croot = ET.fromstring(cbody)
                for el in croot.iter():
                    if el.tag.endswith("loc") and el.text:
                        all_sitemap_urls.add(el.text.strip())
            except Exception as e:
                note("FAIL", f"Could not parse child sitemap {child}: {e}")

    except Exception as e:
        print(f"Could not parse sitemap index: {e}")
        note("FAIL", f"Could not parse sitemap index: {e}")
else:
    note("FAIL", f"WordPress sitemap index returned HTTP {status}.")

print("\nPublished page membership:")
for p in published_pages:
    url = p["url"]
    present = url in all_sitemap_urls
    print(f"  {'YES' if present else 'NO '} {url}")
    if not present:
        note("WARN", f"Published page is absent from sitemap: {url}")

print("\nPrivate page exclusion:")
for p in private_pages:
    url = p["url"]
    present = url in all_sitemap_urls
    print(f"  {'BAD' if present else 'OK '} {p['title']}: {url}")
    if present:
        note("FAIL", f"Private page appears in sitemap: {url}")

if private_pages and all(p["url"] not in all_sitemap_urls for p in private_pages):
    note("PASS", "Private pages are absent from the sitemap.")

# --------------------------------------------------------------------
# 8. RESUME PDF - DYNAMIC DISCOVERY
# --------------------------------------------------------------------
print("\n=== 8. PUBLIC RESUME PDF ===")

resume_page = next(
    (
        x for x in page_results
        if urllib.parse.urlsplit(x["url"]).path.rstrip("/") == "/resume"
    ),
    None,
)

pdf_urls = []

if resume_page:
    for href in resume_page["links"]:
        absolute = urllib.parse.urljoin(
            resume_page["url"], html.unescape(href)
        )
        if urllib.parse.urlsplit(absolute).path.lower().endswith(".pdf"):
            if absolute not in pdf_urls:
                pdf_urls.append(absolute)

if not pdf_urls:
    print("No PDF link discovered on the Resume page.")
    note("WARN", "No PDF link was discovered on the Resume page.")
else:
    for pdf in pdf_urls:
        status, final, headers, body = fetch(pdf)
        ctype = headers.get("Content-Type", "") if hasattr(headers, "get") else ""
        print(f"{pdf}")
        print(f"  HTTP         : {status}")
        print(f"  Content-Type : {ctype}")
        print(f"  Bytes        : {len(body)}")

        if status != 200:
            note("FAIL", f"Resume PDF returned HTTP {status}: {pdf}")
        elif "pdf" not in ctype.lower():
            note("WARN", f"Resume PDF has unexpected Content-Type: {ctype}")
        else:
            note("PASS", "Public Resume PDF is reachable as a PDF.")

# --------------------------------------------------------------------
# 9. FINAL SUMMARY
# --------------------------------------------------------------------
print("\n============================================================")
print(" FINAL SUMMARY")
print("============================================================")

print(f"PASS: {len(PASS)}")
for x in PASS:
    print(f"  [PASS] {x}")

print(f"\nWARN: {len(WARN)}")
for x in WARN:
    print(f"  [WARN] {x}")

print(f"\nFAIL: {len(FAIL)}")
for x in FAIL:
    print(f"  [FAIL] {x}")

print()
if FAIL:
    print("OVERALL: ACTION REQUIRED")
    sys.exit(2)
elif WARN:
    print("OVERALL: HEALTHY, WITH ITEMS TO REVIEW")
    sys.exit(0)
else:
    print("OVERALL: CLEAN")
    sys.exit(0)

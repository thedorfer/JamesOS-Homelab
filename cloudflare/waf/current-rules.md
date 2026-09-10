# Current Cloudflare WAF Rules

This document records the public-safe Cloudflare security rules used for the WordPress portfolio site.

Do not commit account IDs, rule IDs, tokens, or screenshots exposing private configuration.

## Rule: Protect wp-login

Purpose: reduce automated login abuse against WordPress.

Expression pattern:

```text
(http.request.uri.path contains "/wp-login.php")
and
(ip.geoip.country ne "US")
```

Action:

```text
Managed Challenge
```

## Rule: Protect wp-admin

Purpose: reduce automated probing of WordPress admin paths.

Expression pattern:

```text
(http.request.uri.path contains "/wp-admin")
and
(ip.geoip.country ne "US")
```

Action:

```text
Managed Challenge
```

## Rule: Block XML-RPC

Purpose: prevent XML-RPC abuse before the request reaches the origin.

Expression pattern:

```text
(http.request.uri.path eq "/xmlrpc.php")
```

Action:

```text
Block
```

## Origin Baseline

The origin also blocks XML-RPC, so the expected public response is:

```text
/xmlrpc.php -> HTTP 403
```

`jamesos-homelab doctor` checks the public XML-RPC response through the WordPress provider.

## Review Notes

- Keep the rules focused and minimal.
- Prefer Managed Challenge for login/admin access instead of broad global blocking.
- Block XML-RPC because it is not needed for the current portfolio site.
- Revisit these rules if legitimate administration is needed from outside the United States.

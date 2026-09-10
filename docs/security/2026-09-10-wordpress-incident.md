# WordPress Recovery

## Summary

A compromised WordPress installation was recovered and rebuilt.

Indicators

- Multiple malicious PHP web shells
- Missing wp-login.php
- Unauthorized files in core directories

Recovery

- Quarantined malicious files
- Rebuilt WordPress core
- Restored wp-login.php
- Removed unauthorized files
- Verified hashes
- Enabled Cloudflare protection
- Disabled XML-RPC
- Disabled theme/plugin editor
- Verified Google indexing
- Created integrity audit

Lessons Learned

Rebuild is safer than repair.

Infrastructure should be version controlled.

Cloudflare should protect the origin.

Every recovery should become documentation.


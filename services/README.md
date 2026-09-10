# Services

The `services/` directory is reserved for service implementation artifacts that should be version-controlled.

Examples may include:

- sanitized compose templates
- service-specific configuration templates
- install helpers
- restore helpers
- `.env.example` files

Service documentation belongs under:

```text
docs/services/
```

Current service documentation:

- `docs/services/wordpress.md`
- `docs/services/nextcloud.md`
- `docs/services/open-webui.md`
- `docs/services/gateway.md`
- `docs/services/storage.md`
- `docs/services/backups.md`

## Public Repository Rule

Do not commit live service configuration containing secrets. Use templates and `.env.example` files instead.

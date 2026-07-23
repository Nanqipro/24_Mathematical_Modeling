# Security policy

This is a research prototype, not a hardened traffic-control service.

- Never commit `Vehicle-tracking-main/settings/db_config.yml`.
- Prefer the `TRAFFIC_DATABASE_URL` environment variable or a machine-local configuration copied from `db_config.example.yml`.
- Do not use production database credentials or identifiable road-user data in tests or examples.
- Treat model files and serialized objects as untrusted unless their source and checksum are known.

If you discover a credential, personal-data exposure, or code-execution risk, use GitHub's private vulnerability reporting for this repository instead of opening a public issue.

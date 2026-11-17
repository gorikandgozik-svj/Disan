# Security policy

This is an experimental local toolchain. Do not expose the stdio server or local queue to untrusted users, put it behind a public unauthenticated tunnel, or run it with administrator privileges.

- All input files are processed with the invoking user's operating-system permissions.
- Browser HTML audit uses an isolated headless context and blocks external fetches; **do not** execute actively malicious HTML under privileged accounts.
- Third-party inputs are untrusted; no arbitrary shell command tool is intentionally provided.
- The tool currently has no authentication, remote API, sandboxing guarantee, file upload service, or multi-user isolation. It is suitable for trusted local development only.
- The queue's inbox is not a security boundary; protect workspace file permissions.
- Use private channels to report security concerns to the maintainer. Do not publish API secrets or sensitive example files.

# DBeaver Community Edition COPR packaging

This repository repackages the official DBeaver Community Edition RPMs for
Fedora COPR. It does not build DBeaver from source. The spec downloads the
exact upstream release assets and verifies their SHA-256 checksums before
extracting their payloads.

## Update procedure

1. Obtain the current x86_64 and aarch64 RPM versions, download URLs, and
   SHA-256 digests from [DBeaver releases](https://github.com/dbeaver/dbeaver/releases).
2. Update `Version`, `Release`, the source URLs and checksums in
   `dbeaver-ce.spec`, and `version` in `.copr/Makefile`.
3. Build from SCM in COPR for the desired Fedora chroots.

## Automated Copr builds

Pushes to `main` that change `.copr/Makefile` or `dbeaver-ce.spec`
automatically submit an SCM build through GitHub Actions. Configure these
repository secrets before the first automated build:

- `COPR_LOGIN`
- `COPR_USERNAME`
- `COPR_TOKEN`

Use the corresponding values from the `[copr-cli]` section of
`~/.config/copr`. The workflow also supports manual runs from the GitHub
Actions page.

Install the resulting package with:

```bash
sudo dnf copr enable ok8219/DBeaver
sudo dnf install dbeaver-ce
```

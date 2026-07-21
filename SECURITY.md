# Security policy

## Reporting

Report suspected vulnerabilities privately via GitHub Security Advisories on this repository,
or by opening a minimal issue that does **not** include sensitive details and asking a
maintainer to open a private channel.

## Scope and design notes

- The skill itself is Markdown plus one self-contained HTML form. It ships no runtime code and
  requires no execution to install.
- `assets/intake-form.html` runs entirely in the browser, uses no browser storage
  (`localStorage`/`sessionStorage`/`indexedDB`), and makes no network requests. This is
  enforced by `tests/test_intake_form.py`.
- Repository tooling (`tools/`) uses only the Python standard library.
- CI runs with top-level `permissions: contents: read`; third-party actions are pinned to full
  commit SHAs; `actions/checkout` runs with `persist-credentials: false`. These invariants are
  enforced by `tools/check_repository.py`.
- Installers should verify the canonical bundle digest before copying files into a trusted
  skills directory; see `install.md`.

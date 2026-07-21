# Contributing

Thanks for your interest in improving the character IP design skill.

## Ground rules

- Keep the skill runtime dependency-free: `SKILL.md`, Markdown references, and self-contained
  assets only. Repository tooling may use the Python standard library (3.10+) but nothing else.
- Do not weld any specific famous IP's symbol combination into the skill's guidance or examples.
  Famous IPs are analysis material only; the skill produces original characters.
- Do not commit local machine paths, large binaries, or generated design outputs.

## Before opening a PR

```bash
python3 -m unittest discover -s tests -v
python3 tools/check_repository.py
python3 -m compileall -q tools tests
```

All three must pass. If you change the skill files, note it in `CHANGELOG.md`.

## Style

- Markdown wrapped to ~95 columns where practical.
- Reference files stay focused; SKILL.md points to them via `references/<name>.md`.

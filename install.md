# Installation plan

Two modes. The quick path suits ordinary local installs. The verified path adds a bundle
digest and an approval receipt for environments that want per-file review.

## Quick install (recommended)

Give your agent the public repository URL, pinned to `main` or (for reproducibility) a release
tag or full 40-character commit SHA, with the skill subtree path:

```text
https://github.com/jacky-0218-lung/character-ip-design/tree/main/skills/character-ip-design
```

Ask the installer to:

1. Prefer direct download; use git only if direct download fails on auth/permission.
2. Install only the `skills/character-ip-design` subtree.
3. Refuse to overwrite an existing destination and report it instead.
4. Not execute any downloaded file merely to install the skill.
5. Report the installed path. The skill is available on the next turn.

## Package identity

- Repository: `jacky-0218-lung/character-ip-design`
- Skill name: `character-ip-design`
- Skill source: `skills/character-ip-design`
- Runtime: none required by the skill itself (Markdown + one self-contained HTML form)
- Repo tooling runtime: Python 3.10+ (standard library only), for tests and packaging
- External dependencies: none
- Network access: the skill *uses* web search during market research when the host provides
  it; the files themselves fetch nothing.

## Destination

Install the verified `skills/character-ip-design` subtree into your agent's trusted skills
directory. Common locations:

- Claude Code / Cowork: `~/.claude/skills/character-ip-design`
- Codex: `$CODEX_HOME/skills/character-ip-design` (or `~/.codex/skills/character-ip-design`)

Restart or open a new session if the skill is not discovered immediately.

## Verified install (optional)

For per-file review and an integrity-bound receipt:

1. Resolve the chosen branch/tag to a full 40-character commit SHA and stage that exact commit
   privately (GitHub archive endpoint or a single clone).
2. Compute the canonical bundle digest of the staged skill directory:

   ```bash
   python3 tools/skill_bundle.py digest skills/character-ip-design
   ```

   The digest covers file contents, names, and layout (`character-ip-design-bundle-v1`). Any
   change — even one that preserves filenames — produces a different digest.
3. Review `SKILL.md`, every file under `references/`, and `assets/intake-form.html`. Show an
   approval receipt (repository, commit SHA, digest, full file list, destination).
4. After approval, copy the staged bytes to the destination and re-verify:

   ```bash
   python3 tools/skill_bundle.py verify <DESTINATION> --expected <APPROVED_DIGEST>
   ```

   Refuse the install on any mismatch.

## First use

Ask the skill to design a character or IP, or open `assets/intake-form.html`, fill it, and
paste the generated brief back. The skill runs its intake → research → design → commercialization
pipeline from there.

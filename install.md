# Installation plan

Three modes. The plugin path is the shortest on Claude Code. The quick path suits any other
agent. The verified path adds a bundle digest and an approval receipt for environments that
want per-file review.

## Plugin install (Claude Code / Cowork — recommended there)

This repository is itself a plugin marketplace (`.claude-plugin/marketplace.json`), with the
plugin sourced at `./` and the skill auto-discovered from `skills/designing-character-ips/`:

```text
/plugin marketplace add jacky-0218-lung/character-ip-design
/plugin install character-ip-design@character-ip-design
```

Notes:

- Pin a branch or tag when adding the marketplace if you need reproducibility; the marketplace
  source supports `ref` but not `sha` (individual plugin sources support both).
- `version` is declared in both `.claude-plugin/plugin.json` and the marketplace entry, and is
  kept in lockstep with the skill's own `metadata.version` by `tools/check_repository.py`. It
  must be bumped for existing users to receive an update — an unchanged version reports
  "already at the latest version".
- Uninstall with `/plugin uninstall character-ip-design`.

## Quick install (any agent)

Give your agent the public repository URL, pinned to `main` or (for reproducibility) a release
tag or full 40-character commit SHA, with the skill subtree path:

```text
https://github.com/jacky-0218-lung/character-ip-design/tree/main/skills/designing-character-ips
```

Ask the installer to:

1. Prefer direct download; use git only if direct download fails on auth/permission.
2. Install only the `skills/designing-character-ips` subtree.
3. Refuse to overwrite an existing destination and report it instead.
4. Not execute any downloaded file merely to install the skill.
5. Report the installed path. The skill is available on the next turn.

## Package identity

- Repository: `jacky-0218-lung/character-ip-design`
- Skill name: `designing-character-ips`
- Skill source: `skills/designing-character-ips`
- Plugin / marketplace name: `character-ip-design` (manifests in `.claude-plugin/`)
- The plugin name and the skill name differ on purpose: the plugin name keeps `/plugin
  install` commands stable across releases, while the skill name follows the Agent Skills
  gerund-form guidance. `tools/check_repository.py` resolves the version-drift anchor by
  falling back to the sole skill in `skills/`, and errors out if that is ever ambiguous.
- Runtime: none required by the skill itself (Markdown + one self-contained HTML form)
- Repo tooling runtime: Python 3.10+ (standard library only), for tests and packaging
- External dependencies: none
- Network access: the skill *uses* web search during market research when the host provides
  it; the files themselves fetch nothing.

## Destination

Install the verified `skills/designing-character-ips` subtree into your agent's trusted skills
directory. Common locations:

- Claude Code / Cowork: `~/.claude/skills/designing-character-ips`
- Codex: `$CODEX_HOME/skills/designing-character-ips` (or `~/.codex/skills/designing-character-ips`)

Restart or open a new session if the skill is not discovered immediately.

## Verified install (optional)

For per-file review and an integrity-bound receipt:

1. Resolve the chosen branch/tag to a full 40-character commit SHA and stage that exact commit
   privately (GitHub archive endpoint or a single clone).
2. Compute the canonical bundle digest of the staged skill directory:

   ```bash
   python3 tools/skill_bundle.py digest skills/designing-character-ips
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

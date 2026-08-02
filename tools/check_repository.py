#!/usr/bin/env python3
"""Repository guard: keep oversized, binary, or insecure-workflow files out of the repo,
hold every skill to the Agent Skills open standard, and keep the plugin marketplace manifests
installable.

Run in CI and locally before tagging a release. Standard library only.

The skill rules implement https://agentskills.io/specification (the cross-agent open standard
Anthropic published the format as), plus one Claude-specific listing-budget warning.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 1_000_000
SKIP_TOP_LEVEL = {"work", "private", "dist", "build"}
ABSOLUTE_USER_PATH = re.compile(rb"[A-Za-z]:\\Users\\[^\\\r\n]+")
HOME_CLAUDE_PATH = re.compile(rb"/home/claude/")
ACTION_USE = re.compile(r"^\s*uses:\s*([^\s]+)\s*$", re.M)
FULL_SHA = re.compile(r"^[^@]+@[0-9a-f]{40}(?:\s+#.*)?$", re.I)

# --- Agent Skills open standard (agentskills.io/specification) -----------------------------
SKILLS_DIR = ROOT / "skills"
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Fields the standard defines. Anything else in the frontmatter is a portability risk:
# strict validators reject unknown keys outright.
ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}
MAX_NAME_CHARS = 64
MAX_DESCRIPTION_CHARS = 1024
MAX_COMPATIBILITY_CHARS = 500
# Claude Code truncates description (+ when_to_use) in the skill listing at this width, so a
# description that is spec-legal can still lose its trailing trigger keywords. Warning only.
LISTING_TRUNCATION_CHARS = 1536
MAX_SKILL_MD_LINES = 500


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]] | tuple[None, None]:
    """Return (flattened top-level scalars, top-level keys) or (None, None) if absent.

    Deliberately minimal: the standard's frontmatter is a flat string mapping, and the repo
    stays standard-library-only (no PyYAML). Nested blocks (e.g. ``metadata:``) are recorded
    as keys with their children folded into one string, which is all the checks below need.
    """
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return None, None
    values: dict[str, str] = {}
    order: list[str] = []
    key = None
    for line in match.group(1).splitlines():
        top = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$", line)
        if top and not line[:1].isspace():
            key = top.group(1)
            if key not in values:
                order.append(key)
            values[key] = top.group(2).strip()
        elif key and line[:1].isspace():
            values[key] = (values[key] + " " + line.strip()).strip()
    return values, order


def check_skills() -> list[str]:
    errors: list[str] = []
    if not SKILLS_DIR.is_dir():
        return errors
    for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        directory = skill_md.parent.name
        where = skill_md.relative_to(ROOT)
        text = skill_md.read_text(encoding="utf-8")
        values, order = parse_frontmatter(text)
        if values is None:
            errors.append(f"{where}: missing YAML frontmatter delimited by ---")
            continue

        name = values.get("name", "")
        if not name:
            errors.append(f"{where}: frontmatter must define a non-empty 'name'")
        else:
            if len(name) > MAX_NAME_CHARS:
                errors.append(f"{where}: name exceeds {MAX_NAME_CHARS} characters")
            if not SKILL_NAME.fullmatch(name):
                errors.append(
                    f"{where}: name {name!r} must be lowercase a-z0-9 with single internal "
                    "hyphens (no leading/trailing '-', no '--')"
                )
            if name != directory:
                errors.append(f"{where}: name {name!r} must match its directory {directory!r}")

        description = values.get("description", "")
        if not description:
            errors.append(f"{where}: frontmatter must define a non-empty 'description'")
        elif len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"{where}: description is {len(description)} characters, over the "
                f"{MAX_DESCRIPTION_CHARS}-character limit"
            )

        compatibility = values.get("compatibility", "")
        if len(compatibility) > MAX_COMPATIBILITY_CHARS:
            errors.append(f"{where}: compatibility exceeds {MAX_COMPATIBILITY_CHARS} characters")

        for extra in [k for k in (order or []) if k not in ALLOWED_FRONTMATTER]:
            errors.append(
                f"{where}: frontmatter key {extra!r} is outside the Agent Skills standard "
                f"({', '.join(sorted(ALLOWED_FRONTMATTER))}); put custom data under 'metadata'"
            )

        line_count = len(text.splitlines())
        if line_count > MAX_SKILL_MD_LINES:
            errors.append(
                f"{where}: {line_count} lines, over the {MAX_SKILL_MD_LINES}-line guidance — "
                "move detail into references/ for progressive disclosure"
            )

        # Reference links must resolve, and must stay one hop deep: an agent that reads only
        # the head of a nested file gets partial instructions.
        for target in sorted(set(re.findall(r"(?<![\w/])references/([A-Za-z0-9._/-]+\.md)", text))):
            if not (skill_md.parent / "references" / target).is_file():
                errors.append(f"{where}: points to missing references/{target}")

        if len(description) > LISTING_TRUNCATION_CHARS:
            print(
                f"warning: {where}: description may be truncated in Claude's skill listing "
                f"(> {LISTING_TRUNCATION_CHARS} chars) — put trigger keywords first",
                file=sys.stderr,
            )
    return errors


# --- Claude Code plugin marketplace (code.claude.com/docs/en/plugin-marketplaces) ----------
PLUGIN_DIR = ROOT / ".claude-plugin"
MARKETPLACE_JSON = PLUGIN_DIR / "marketplace.json"
PLUGIN_JSON = PLUGIN_DIR / "plugin.json"
# Names Anthropic reserves for official marketplaces. A marketplace registered under one of
# these stops loading and is reported as coming from an untrusted source.
RESERVED_MARKETPLACE_NAMES = {
    "claude-code-marketplace",
    "claude-code-plugins",
    "claude-plugins-official",
    "claude-plugins-community",
    "claude-community",
    "anthropic-marketplace",
    "anthropic-plugins",
    "agent-skills",
    "anthropic-agent-skills",
    "knowledge-work-plugins",
    "life-sciences",
    "claude-for-legal",
    "claude-for-financial-services",
    "financial-services-plugins",
    "first-party-plugins",
    "healthcare",
}


def load_json(path: Path, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"{path.relative_to(ROOT)}: missing — the repo is not installable via "
                      "'/plugin marketplace add'")
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
    return None


def check_plugin_manifests() -> list[str]:
    """Validate the marketplace catalog and plugin manifest.

    These two files are what make ``/plugin marketplace add <owner>/<repo>`` work. They are
    easy to get subtly wrong in ways nothing else catches: a plugin.json without a
    marketplace.json installs for nobody, and a version that is set but never bumped leaves
    every existing user pinned to the old commit forever.
    """
    errors: list[str] = []
    if not PLUGIN_DIR.is_dir():
        return errors

    market = load_json(MARKETPLACE_JSON, errors)
    manifest = load_json(PLUGIN_JSON, errors)
    if market is None:
        return errors

    name = market.get("name")
    if not isinstance(name, str) or not name:
        errors.append("marketplace.json: 'name' is required")
    else:
        if not SKILL_NAME.fullmatch(name):
            errors.append(f"marketplace.json: name {name!r} must be kebab-case (a-z0-9, single "
                          "internal hyphens)")
        if name in RESERVED_MARKETPLACE_NAMES:
            errors.append(f"marketplace.json: name {name!r} is reserved for official Anthropic "
                          "marketplaces and will be rejected as untrusted")

    owner = market.get("owner")
    if not isinstance(owner, dict) or not owner.get("name"):
        errors.append("marketplace.json: 'owner' must be an object with a non-empty 'name'")

    plugins = market.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        errors.append("marketplace.json: 'plugins' must be a non-empty array")
        return errors

    for index, entry in enumerate(plugins):
        where = f"marketplace.json plugins[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{where}: must be an object")
            continue
        entry_name = entry.get("name")
        if not isinstance(entry_name, str) or not SKILL_NAME.fullmatch(entry_name or ""):
            errors.append(f"{where}: 'name' is required and must be kebab-case")
        # A string type error (e.g. keywords as a string) is a hard load error, not a warning.
        for field in ("keywords", "tags"):
            if field in entry and not isinstance(entry[field], list):
                errors.append(f"{where}: '{field}' must be an array, not {type(entry[field]).__name__}")

        source = entry.get("source")
        if source is None:
            errors.append(f"{where}: 'source' is required")
            continue
        if isinstance(source, str):
            if not source.startswith("./"):
                errors.append(f"{where}: relative source {source!r} must start with './' "
                              "(it resolves from the repo root, not from .claude-plugin/)")
                continue
            target = (ROOT / source).resolve()
            if not target.is_dir():
                errors.append(f"{where}: source {source!r} does not resolve to a directory")
                continue
            # The plugin must actually expose something loadable: a root SKILL.md, or the
            # auto-discovered skills/ layout.
            has_root_skill = (target / "SKILL.md").is_file()
            has_skills_dir = any((target / "skills").glob("*/SKILL.md"))
            if not (has_root_skill or has_skills_dir or "skills" in entry):
                errors.append(f"{where}: source {source!r} contains no SKILL.md at its root and "
                              "no skills/<name>/SKILL.md — nothing would install")
        elif not isinstance(source, dict):
            errors.append(f"{where}: 'source' must be a string path or an object")

    if manifest is None:
        return errors

    if not isinstance(manifest.get("name"), str) or not manifest.get("name"):
        errors.append("plugin.json: 'name' is required")
    for field in ("keywords",):
        if field in manifest and not isinstance(manifest[field], list):
            errors.append(f"plugin.json: '{field}' must be an array")

    # Self-hosted marketplace: the entry sourced at './' IS this plugin, so the two manifests
    # must agree. Divergence here is silent — the marketplace entry name wins for /plugin,
    # while plugin.json's name is what namespaces components.
    self_entries = [e for e in plugins if isinstance(e, dict) and e.get("source") == "./"]
    for entry in self_entries:
        if entry.get("name") != manifest.get("name"):
            errors.append(
                f"marketplace entry {entry.get('name')!r} and plugin.json {manifest.get('name')!r} "
                "describe the same directory but disagree on 'name'"
            )
        entry_version, manifest_version = entry.get("version"), manifest.get("version")
        if entry_version and manifest_version and entry_version != manifest_version:
            errors.append(
                f"version mismatch: marketplace entry {entry_version!r} vs plugin.json "
                f"{manifest_version!r} — plugin.json wins, so users would see the wrong version"
            )

    # Single-skill repo: keep the published plugin version and the skill's own metadata.version
    # in lockstep, so a skill edit can't ship under a stale plugin version.
    if manifest.get("version"):
        skill_md, anchor_error = resolve_version_anchor(manifest.get("name") or "")
        if anchor_error:
            errors.append(anchor_error)
        elif skill_md is not None:
            values, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            declared = (values or {}).get("metadata", "")
            match = re.search(r"version:\s*[\"']?([^\s\"']+)", declared)
            if match and match.group(1) != manifest["version"]:
                errors.append(
                    f"version drift: plugin.json {manifest['version']!r} vs "
                    f"{skill_md.relative_to(ROOT)} metadata.version {match.group(1)!r} — bump "
                    "both, or existing users never receive the update"
                )
    return errors


def resolve_version_anchor(plugin_name: str) -> tuple[Path | None, str | None]:
    """Find the SKILL.md whose metadata.version must track plugin.json's version.

    The plugin name and the skill name are allowed to differ — the plugin name is what users
    type in ``/plugin install``, while the skill name follows the Agent Skills naming
    guidance (gerund form). So the anchor cannot simply be ``skills/<plugin name>/``: this
    repo's skill is ``designing-character-ips`` while the plugin stays ``character-ip-design``
    for install-command stability.

    Resolution order: exact name match, else the sole skill in ``skills/``. Returns
    ``(path, None)`` when resolved, ``(None, error)`` when the repo has several skills and
    none matches — leaving that unreported would silently disable the version-drift check,
    which is exactly how a stale published version reaches users unnoticed.
    """
    exact = SKILLS_DIR / plugin_name / "SKILL.md"
    if exact.is_file():
        return exact, None
    candidates = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if len(candidates) == 1:
        return candidates[0], None
    if not candidates:
        return None, None
    names = ", ".join(sorted(p.parent.name for p in candidates))
    return None, (
        f"plugin.json name {plugin_name!r} matches no skill directory, and skills/ holds "
        f"{len(candidates)} skills ({names}) — the plugin/skill version-drift check cannot "
        "anchor. Rename the plugin to match one skill, or declare the mapping explicitly."
    )


def relevant_files():
    for path in ROOT.rglob("*"):
        try:
            relative = path.relative_to(ROOT)
        except ValueError:
            continue
        if relative.parts and relative.parts[0] in SKIP_TOP_LEVEL:
            continue
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        yield path


def main() -> int:
    errors: list[str] = []
    for path in relevant_files():
        relative = path.relative_to(ROOT)
        size = path.stat().st_size
        if size > MAX_FILE_BYTES:
            errors.append(f"file exceeds {MAX_FILE_BYTES} bytes: {relative}")
            continue
        data = path.read_bytes()
        # HTML/SVG assets are text; a genuine NUL means an accidental binary commit.
        if b"\x00" in data:
            errors.append(f"binary or NUL-containing file: {relative}")
        if path != Path(__file__):
            if ABSOLUTE_USER_PATH.search(data) or HOME_CLAUDE_PATH.search(data):
                errors.append(f"local machine path leaked into source: {relative}")
        if relative.parts[:2] == (".github", "workflows"):
            text = data.decode("utf-8", errors="replace")
            if "pull_request_target:" in text:
                errors.append(f"pull_request_target is forbidden: {relative}")
            if not re.search(r"^permissions:\s*\n\s+contents:\s+read\s*$", text, re.M):
                errors.append(f"workflow lacks top-level read-only permissions: {relative}")
            for use in ACTION_USE.findall(text):
                if use.startswith("./"):
                    continue
                if not FULL_SHA.fullmatch(use):
                    errors.append(f"action not pinned to a full SHA in {relative}: {use}")
            if "actions/checkout@" in text and "persist-credentials: false" not in text:
                errors.append(f"checkout must disable persisted credentials: {relative}")
    errors.extend(check_skills())
    errors.extend(check_plugin_manifests())
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("repository guard: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

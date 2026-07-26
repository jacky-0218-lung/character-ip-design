#!/usr/bin/env python3
"""Repository guard: keep oversized, binary, or insecure-workflow files out of the repo,
and hold every skill to the Agent Skills open standard.

Run in CI and locally before tagging a release. Standard library only.

The skill rules implement https://agentskills.io/specification (the cross-agent open standard
Anthropic published the format as), plus one Claude-specific listing-budget warning.
"""

from __future__ import annotations

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
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("repository guard: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

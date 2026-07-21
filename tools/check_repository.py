#!/usr/bin/env python3
"""Repository guard: keep oversized, binary, or insecure-workflow files out of the repo.

Run in CI and locally before tagging a release. Standard library only.
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
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("repository guard: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

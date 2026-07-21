#!/usr/bin/env python3
"""Create or verify an integrity receipt for a staged Skill directory.

The canonical bundle digest covers file contents, names, and layout, so any
change to the Skill — even one that preserves filenames — produces a different
approval subject. Standard library only; Python 3.10+.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


ALGORITHM = "character-ip-design-bundle-v1"
FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$", re.I)
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$", re.I)
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


class BundleError(ValueError):
    """Raised when a bundle is unsafe or does not match its receipt."""


def is_reparse_point(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", None)
    return path.is_symlink() or bool(is_junction and is_junction())


def hash_file(path: Path) -> bytes:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.digest()


def bundle_records(root: Path) -> list[tuple[bytes, bytes, str]]:
    root = root.expanduser().absolute()
    if is_reparse_point(root) or not root.is_dir():
        raise BundleError(f"Bundle root must be a regular directory: {root}")
    records: list[tuple[bytes, bytes, str]] = []
    for path in root.rglob("*"):
        if is_reparse_point(path):
            raise BundleError(f"Refusing link or junction: {path.relative_to(root)}")
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise BundleError(f"Refusing non-regular file: {path.relative_to(root)}")
        if "__pycache__" in path.parts:
            continue
        relative = path.relative_to(root).as_posix()
        try:
            relative_bytes = relative.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise BundleError(f"Path is not valid UTF-8: {relative!r}") from exc
        records.append((relative_bytes, hash_file(path), relative))
    return sorted(records, key=lambda record: record[0])


def canonical_bundle_digest(root: Path) -> tuple[str, list[str]]:
    bundle = hashlib.sha256(ALGORITHM.encode("ascii") + b"\0")
    files: list[str] = []
    for relative_bytes, content_digest, relative in bundle_records(root):
        bundle.update(len(relative_bytes).to_bytes(8, "big"))
        bundle.update(relative_bytes)
        bundle.update(content_digest)
        files.append(relative)
    return bundle.hexdigest(), files


def build_receipt(root: Path, *, repository: str, origin: str, commit: str, destination: str) -> dict[str, Any]:
    repository = repository.strip()
    if not REPOSITORY_RE.fullmatch(repository):
        raise BundleError("Repository must be an owner/name identity")
    parsed = urlparse(origin)
    if (
        parsed.scheme.lower() != "https"
        or parsed.hostname is None
        or parsed.hostname.casefold() != "github.com"
    ):
        raise BundleError("Origin must be an https://github.com repository URL")
    if not FULL_SHA_RE.fullmatch(commit):
        raise BundleError("Commit must be a full 40-character SHA")
    if not destination.strip():
        raise BundleError("Destination is required")
    digest, files = canonical_bundle_digest(root)
    return {
        "schema_version": "1.0",
        "algorithm": ALGORITHM,
        "repository": repository,
        "origin": origin,
        "commit": commit.lower(),
        "bundle_digest": digest,
        "files": files,
        "destination": destination,
        "destination_exists": Path(destination).expanduser().exists(),
    }


def verify_digest(root: Path, expected: str) -> str:
    if not DIGEST_RE.fullmatch(expected):
        raise BundleError("Expected digest must contain 64 hexadecimal characters")
    actual, _ = canonical_bundle_digest(root)
    if not hmac.compare_digest(actual, expected.lower()):
        raise BundleError(f"Bundle digest mismatch: expected {expected.lower()}, got {actual}")
    return actual


def atomic_write_json(path: Path, data: dict[str, Any], overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise BundleError(f"Output exists; pass --overwrite to replace it: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = ""
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", delete=False,
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp",
        ) as handle:
            temp_name = handle.name
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if temp_name and os.path.exists(temp_name):
            try:
                os.unlink(temp_name)
            except OSError:
                pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    receipt = sub.add_parser("receipt", help="Create an approval receipt")
    receipt.add_argument("root", type=Path, help="Staged Skill directory")
    receipt.add_argument("--repository", required=True)
    receipt.add_argument("--origin", required=True)
    receipt.add_argument("--commit", required=True)
    receipt.add_argument("--destination", required=True)
    receipt.add_argument("--output", type=Path)
    receipt.add_argument("--overwrite", action="store_true")
    digest = sub.add_parser("digest", help="Print the canonical bundle digest")
    digest.add_argument("root", type=Path)
    verify = sub.add_parser("verify", help="Verify a staged or copied Skill")
    verify.add_argument("root", type=Path)
    verify.add_argument("--expected", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "receipt":
            result = build_receipt(
                args.root, repository=args.repository, origin=args.origin,
                commit=args.commit, destination=args.destination,
            )
            if args.output:
                atomic_write_json(args.output.resolve(), result, args.overwrite)
                result = {**result, "output": str(args.output)}
        elif args.command == "digest":
            digest, files = canonical_bundle_digest(args.root)
            result = {"algorithm": ALGORITHM, "bundle_digest": digest, "files": files}
        else:
            result = {
                "status": "verified",
                "algorithm": ALGORITHM,
                "bundle_digest": verify_digest(args.root, args.expected),
            }
    except (OSError, BundleError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

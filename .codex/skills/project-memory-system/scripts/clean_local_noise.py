#!/usr/bin/env python3
"""Remove ignored local noise from canonical repository lanes."""

from __future__ import annotations

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
CANONICAL_LANES = [
    "ontology",
    "manuscripts",
    "markdown",
    "html",
    "registries",
    "wiki",
]
LATEX_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
}


def should_remove(path: Path) -> bool:
    name = path.name
    return name == ".DS_Store" or name.startswith("._") or path.suffix in LATEX_SUFFIXES


def find_targets() -> list[Path]:
    targets: list[Path] = []
    for lane in CANONICAL_LANES:
        root = REPO_ROOT / lane
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and should_remove(path):
                targets.append(path)
    return sorted(targets)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove .DS_Store, AppleDouble files, and LaTeX byproducts."
    )
    parser.add_argument("--dry-run", action="store_true", help="List targets without deleting.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    targets = find_targets()
    for path in targets:
        relative = path.relative_to(REPO_ROOT).as_posix()
        if args.dry_run:
            print(relative)
        else:
            path.unlink()
            print(f"Deleted {relative}")
    if not targets:
        print("No local noise found.")
    elif args.dry_run:
        print(f"Dry run: {len(targets)} file(s) would be deleted.")
    else:
        print(f"Deleted {len(targets)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

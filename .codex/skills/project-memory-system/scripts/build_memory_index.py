#!/usr/bin/env python3
"""Build the local SQLite FTS memory index."""

from __future__ import annotations

import argparse
from pathlib import Path

from obsidian_wiki_lib import build_memory_index, memory_index_path


REPO_ROOT = Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--index",
        help="SQLite output path. Defaults to .local/memory_index/memory.sqlite.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = memory_index_path(REPO_ROOT, args.index)
    built = build_memory_index(REPO_ROOT, target)
    print(f"Built memory index at {built}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

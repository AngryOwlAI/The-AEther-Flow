#!/usr/bin/env python3
"""Validate the local Obsidian memory vault against registries and sources."""

from __future__ import annotations

import argparse
from pathlib import Path

from obsidian_wiki_lib import lint_vault, vault_root


REPO_ROOT = Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vault",
        help="Vault path. Defaults to .local/obsidian/aether-flow-wiki.",
    )
    parser.add_argument(
        "--require-index",
        action="store_true",
        help="Fail if the local SQLite memory index is missing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    issues = lint_vault(REPO_ROOT, vault_root(REPO_ROOT, args.vault), args.require_index)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}")
        print(f"Obsidian vault validation FAIL: {len(issues)} issue(s)")
        return 1
    print("Obsidian vault validation PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

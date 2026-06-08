#!/usr/bin/env python3
"""Initialize the local generated Obsidian memory vault."""

from __future__ import annotations

import argparse
from pathlib import Path

from obsidian_wiki_lib import ensure_vault, vault_root


REPO_ROOT = Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vault",
        help="Vault path. Defaults to .local/obsidian/aether-flow-wiki.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = vault_root(REPO_ROOT, args.vault)
    ensure_vault(REPO_ROOT, target)
    print(f"Initialized Obsidian memory vault at {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

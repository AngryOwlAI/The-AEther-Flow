#!/usr/bin/env python3
"""Sync registered memory objects into the local Obsidian vault."""

from __future__ import annotations

import argparse
from pathlib import Path

from obsidian_wiki_lib import (
    build_memory_index,
    ensure_vault,
    load_rows_by_registry,
    utc_now,
    vault_root,
    write_generated_registries,
    write_vault,
)


REPO_ROOT = Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vault",
        help="Vault path. Defaults to .local/obsidian/aether-flow-wiki.",
    )
    parser.add_argument(
        "--no-index",
        action="store_true",
        help="Do not rebuild the local SQLite memory index after syncing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = vault_root(REPO_ROOT, args.vault)
    ensure_vault(REPO_ROOT, target)
    rows_by_registry = load_rows_by_registry(REPO_ROOT)
    generated = write_generated_registries(
        REPO_ROOT,
        rows_by_registry,
        utc_now(),
        write_semantic_text=True,
        vault=target,
    )
    rows_by_registry = load_rows_by_registry(REPO_ROOT)
    write_vault(REPO_ROOT, target, rows_by_registry)
    index_path = None if args.no_index else build_memory_index(REPO_ROOT)
    print(f"Synced Obsidian memory vault at {target}")
    print(
        "Generated rows: "
        + ", ".join(f"{name}={len(rows)}" for name, rows in sorted(generated.items()))
    )
    if index_path:
        print(f"Rebuilt memory index at {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

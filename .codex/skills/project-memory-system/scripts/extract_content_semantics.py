#!/usr/bin/env python3
"""Extract deterministic content semantics for registered memory objects."""

from __future__ import annotations

import argparse
from pathlib import Path

from obsidian_wiki_lib import load_rows_by_registry, utc_now, write_generated_registries


REPO_ROOT = Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-write-text",
        action="store_true",
        help="Refresh CSV rows without writing local extracted text files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    generated = write_generated_registries(
        REPO_ROOT,
        load_rows_by_registry(REPO_ROOT),
        utc_now(),
        write_semantic_text=not args.no_write_text,
    )
    print(
        "Generated semantic registries: "
        + ", ".join(f"{name}={len(rows)}" for name, rows in sorted(generated.items()))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

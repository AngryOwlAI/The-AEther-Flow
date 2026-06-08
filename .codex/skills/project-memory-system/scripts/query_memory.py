#!/usr/bin/env python3
"""Query the combined CSV, Obsidian, relationship, and content-semantic memory system."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from obsidian_wiki_lib import (
    lookup_object,
    memory_index_path,
    related_objects,
    search_index,
    status,
    vault_root,
)


REPO_ROOT = Path(__file__).resolve().parents[4]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    lookup = subparsers.add_parser("lookup", help="Look up an object ID or path.")
    lookup.add_argument("identifier")
    lookup.add_argument("--json", action="store_true", help=argparse.SUPPRESS)

    search = subparsers.add_parser("search", help="Search extracted content and registry metadata.")
    search.add_argument("query")
    search.add_argument("--formats", help="Comma-separated format filter.")
    search.add_argument("--limit", type=int, default=20)
    search.add_argument("--index", help="SQLite index path override.")
    search.add_argument("--json", action="store_true", help=argparse.SUPPRESS)

    related = subparsers.add_parser("related", help="Traverse relationship edges.")
    related.add_argument("object_id")
    related.add_argument("--depth", type=int, default=1)
    related.add_argument("--json", action="store_true", help=argparse.SUPPRESS)

    current_status = subparsers.add_parser("status", help="Report memory-system status.")
    current_status.add_argument("--vault", help="Vault path override.")
    current_status.add_argument("--index", help="SQLite index path override.")
    current_status.add_argument("--json", action="store_true", help=argparse.SUPPRESS)

    return parser.parse_args()


def emit(payload: object, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


def main() -> int:
    args = parse_args()
    if args.command == "lookup":
        payload = lookup_object(REPO_ROOT, args.identifier)
    elif args.command == "search":
        formats = {item.strip() for item in args.formats.split(",")} if args.formats else None
        payload = search_index(
            REPO_ROOT,
            args.query,
            formats,
            args.limit,
            memory_index_path(REPO_ROOT, args.index) if args.index else None,
        )
    elif args.command == "related":
        payload = related_objects(REPO_ROOT, args.object_id, args.depth)
    elif args.command == "status":
        payload = status(
            REPO_ROOT,
            vault_root(REPO_ROOT, args.vault) if args.vault else None,
            memory_index_path(REPO_ROOT, args.index) if args.index else None,
        )
    else:
        raise AssertionError(args.command)
    emit(payload, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

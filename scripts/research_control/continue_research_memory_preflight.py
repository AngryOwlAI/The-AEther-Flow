#!/usr/bin/env python3
"""Refresh local retrieval surfaces before continue-research routing when needed."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
MEMORY_SCRIPT_DIR = REPO_ROOT / ".codex" / "skills" / "project-memory-system" / "scripts"
if str(MEMORY_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(MEMORY_SCRIPT_DIR))

from obsidian_wiki_lib import (  # noqa: E402
    build_memory_index,
    ensure_vault,
    load_rows_by_registry,
    memory_index_path,
    status as memory_status,
    utc_now,
    vault_root,
    write_generated_registries,
    write_vault,
)


STATUS_COMMAND = (
    ".venv/bin/python "
    ".codex/skills/project-memory-system/scripts/query_memory.py status --json"
)
REFRESH_COMMAND = (
    ".venv/bin/python "
    ".codex/skills/project-memory-system/scripts/sync_obsidian_vault.py"
)
AUTHORITY_NOTE = (
    "Obsidian wiki notes semantic extracts SQLite memory index and .local files "
    "are retrieval layers only and not authority."
)


def warning_count(payload: dict[str, Any], category: str) -> int:
    categories = payload.get("freshness_categories", {})
    if not isinstance(categories, dict):
        return 0
    values = categories.get(category, [])
    return len(values) if isinstance(values, list) else 0


def summarize_status(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "core_validation_status": payload.get("core_validation_status", ""),
        "freshness_status": payload.get("freshness_status", ""),
        "local_retrieval_status": payload.get("local_retrieval_status", ""),
        "vault_exists": bool(payload.get("vault_exists", False)),
        "memory_index_exists": bool(payload.get("memory_index_exists", False)),
        "source_object_count": int(payload.get("source_object_count", 0) or 0),
        "vault_row_count": int(payload.get("vault_row_count", 0) or 0),
        "semantic_row_count": int(payload.get("semantic_row_count", 0) or 0),
        "relationship_row_count": int(payload.get("relationship_row_count", 0) or 0),
        "local_cache_only_warning_count": warning_count(payload, "local_cache_only"),
        "blocking_warning_count": warning_count(payload, "blocking"),
        "non_blocking_warning_count": warning_count(payload, "non_blocking"),
    }


def local_retrieval_refresh_needed(payload: dict[str, Any]) -> bool:
    return warning_count(payload, "local_cache_only") > 0


def sync_local_retrieval(
    repo_root: Path,
    *,
    vault: Path | None = None,
    index_path: Path | None = None,
) -> dict[str, Any]:
    target_vault = vault or vault_root(repo_root)
    ensure_vault(repo_root, target_vault)
    generated = write_generated_registries(
        repo_root,
        load_rows_by_registry(repo_root),
        utc_now(),
        write_semantic_text=True,
        vault=target_vault,
    )
    write_vault(repo_root, target_vault, load_rows_by_registry(repo_root))
    target_index = build_memory_index(repo_root, index_path)
    return {
        "command": REFRESH_COMMAND,
        "vault_path": target_vault.as_posix(),
        "memory_index_path": target_index.as_posix(),
        "generated_rows": {name: len(rows) for name, rows in sorted(generated.items())},
    }


def run_preflight(
    repo_root: Path,
    *,
    refresh: bool = True,
    vault: Path | None = None,
    index_path: Path | None = None,
) -> dict[str, Any]:
    before = memory_status(repo_root, vault, index_path)
    refresh_needed = local_retrieval_refresh_needed(before)
    refresh_result: dict[str, Any] = {}
    if refresh and refresh_needed:
        refresh_result = sync_local_retrieval(
            repo_root,
            vault=vault,
            index_path=index_path,
        )
        after = memory_status(repo_root, vault, index_path)
    else:
        after = before
    return {
        "status_command": STATUS_COMMAND,
        "refresh_command": REFRESH_COMMAND,
        "refresh_needed": refresh_needed,
        "refresh_performed": bool(refresh_result),
        "before_status_summary": summarize_status(before),
        "status_summary": summarize_status(after),
        "after_status_summary": summarize_status(after),
        "refresh_result": refresh_result,
        "remaining_freshness_warnings": after.get("freshness_warnings", []),
        "authority_note": AUTHORITY_NOTE,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON output. This is the default.")
    parser.add_argument(
        "--no-refresh",
        action="store_true",
        help="Only report memory status; do not refresh stale local retrieval surfaces.",
    )
    parser.add_argument("--vault", help="Vault path override.")
    parser.add_argument("--index", help="SQLite index path override.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    vault = vault_root(REPO_ROOT, args.vault) if args.vault else None
    index = memory_index_path(REPO_ROOT, args.index) if args.index else None
    payload = run_preflight(
        REPO_ROOT,
        refresh=not args.no_refresh,
        vault=vault,
        index_path=index,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    if args.no_refresh:
        return 0
    return 0 if payload["status_summary"]["local_retrieval_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

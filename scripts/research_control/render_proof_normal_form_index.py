#!/usr/bin/env python3
"""Render a deterministic proof-normal-form reader index.

This renderer creates derivative reader surfaces from
registries/PROOF_NORMAL_FORM_REGISTRY.csv. The output is navigational support
only; it does not replace source artifacts, gate decisions, TeX authority, or
proof authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_proof_normal_form_registry import (  # noqa: E402
    DEFAULT_REGISTRY_PATH,
    ProofNormalFormRegistryError,
    is_high_risk,
    load_rows,
    split_semicolon_list,
    validate_registry,
)


SCHEMA_ID = "proof_normal_form_index_v1"
DEFAULT_JSON_PATH = "output/proof_normal_form_index.json"
DEFAULT_MARKDOWN_PATH = "wiki/indexes/proof_normal_form_index.md"
AUTHORITY_NOTICE = (
    "This generated proof-normal-form index is reader and retrieval support "
    "only. It is not proof authority, TeX authority, Gate Chair authority, "
    "claim-promotion authority, or a substitute for registered source "
    "artifacts and control records."
)


class ProofNormalFormIndexError(RuntimeError):
    """Raised when the proof-normal-form index cannot be rendered."""


def repo_path(path_text: str | Path) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def rel_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix() if path.is_relative_to(REPO_ROOT) else path.as_posix()


def file_hash(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def bool_text(value: str) -> bool:
    return value.strip().lower() == "true"


def count_by(rows: list[dict[str, Any]], field_name: str) -> dict[str, int]:
    return dict(sorted(Counter(str(row.get(field_name, "")) for row in rows).items()))


def row_summary(row: dict[str, str]) -> dict[str, Any]:
    return {
        "proof_normal_form_row_id": row["proof_normal_form_row_id"],
        "object_id": row["object_id"],
        "source_artifact_path": row["source_artifact_path"],
        "claim_type": row["claim_type"],
        "authority_status": row["authority_status"],
        "status": row["status"],
        "premises": row["premises"],
        "forbidden_premises": split_semicolon_list(row["forbidden_premises"]),
        "conclusion": row["conclusion"],
        "scope": row["scope"],
        "allowed_uses": row["allowed_uses"],
        "non_conclusions": split_semicolon_list(row["non_conclusions"]),
        "depends_on": split_semicolon_list(row["depends_on"]),
        "eligible_next_routes": split_semicolon_list(row["eligible_next_routes"]),
        "machine_checkable_fragment": bool_text(row["machine_checkable_fragment"]),
        "high_risk": is_high_risk(row),
        "created_at": row["created_at"],
        "notes": row["notes"],
    }


def latest_row_timestamp(rows: list[dict[str, str]]) -> str:
    timestamps = sorted(row.get("created_at", "") for row in rows if row.get("created_at", ""))
    return timestamps[-1] if timestamps else ""


def blocked_overread_terms(rows: list[dict[str, Any]]) -> list[str]:
    terms: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for term in row["non_conclusions"]:
            if term not in seen:
                terms.append(term)
                seen.add(term)
    return terms


def build_snapshot(registry_path: str | Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    registry = repo_path(registry_path)
    if not registry.exists():
        raise ProofNormalFormIndexError(f"missing registry: {rel_path(registry)}")

    try:
        validation_receipt = validate_registry(registry)
    except ProofNormalFormRegistryError as exc:
        raise ProofNormalFormIndexError(
            "proof-normal-form registry validation failed; refusing to render index"
        ) from exc

    _, raw_rows = load_rows(registry)
    rows = [row_summary(row) for row in raw_rows]
    high_risk_rows = [row for row in rows if row["high_risk"]]
    source_paths = [row["source_artifact_path"] for row in rows]
    source_missing_count = sum(1 for path in source_paths if not repo_path(path).exists())
    registry_hash = file_hash(registry)

    snapshot = {
        "schema_id": SCHEMA_ID,
        "generated_from": rel_path(registry),
        "generated_at": latest_row_timestamp(raw_rows),
        "source_fingerprint": registry_hash,
        "registry_hash": registry_hash,
        "source_basis": [
            rel_path(registry),
            "research_control/formalization/proof_normal_form_schema_v1.md",
            "scripts/research_control/validate_proof_normal_form_registry.py",
        ],
        "authority_notice": AUTHORITY_NOTICE,
        "authority_boundary": {
            "support_only": True,
            "proof_authority": False,
            "physics_promotion_authorized": False,
            "scientific_claims_changed": False,
            "replaces_source_artifacts": False,
            "source_artifacts_remain_authority": True,
        },
        "summary": {
            "row_count": len(rows),
            "high_risk_row_count": len(high_risk_rows),
            "scientific_gate_row_count": sum(
                1 for row in rows if row["authority_status"] == "scientific_gate"
            ),
            "support_only_row_count": sum(
                1 for row in rows if row["authority_status"] == "support_only"
            ),
            "machine_checkable_fragment_count": sum(
                1 for row in rows if row["machine_checkable_fragment"]
            ),
            "source_missing_count": source_missing_count,
            "claim_type_counts": count_by(rows, "claim_type"),
            "authority_status_counts": count_by(rows, "authority_status"),
            "status_counts": count_by(rows, "status"),
        },
        "blocked_overread_terms": blocked_overread_terms(rows),
        "rows": rows,
        "validation": validation_receipt,
    }
    snapshot["snapshot_hash"] = sha256_text(json.dumps(snapshot, sort_keys=True, ensure_ascii=False))
    return snapshot


def json_text(snapshot: dict[str, Any]) -> str:
    return json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def markdown_list(items: list[str]) -> str:
    if not items:
        return ""
    return "<br>".join(items)


def markdown_text(snapshot: dict[str, Any]) -> str:
    summary = snapshot["summary"]
    lines = [
        "<!-- generated: true; authority: derivative -->",
        "",
        "# Proof Normal Form Index",
        "",
        snapshot["authority_notice"],
        "",
        "If this index conflicts with registered source artifacts, control registries, task completions, handoffs, or Gate Chair decisions, those tracked authority surfaces govern.",
        "",
        "## Summary",
        "",
        "| Field | Value |",
        "| --- | --- |",
        f"| Schema | `{snapshot['schema_id']}` |",
        f"| Generated from | `{snapshot['generated_from']}` |",
        f"| Registry hash | `{snapshot['registry_hash']}` |",
        f"| Row count | {summary['row_count']} |",
        f"| High-risk row count | {summary['high_risk_row_count']} |",
        f"| Scientific-gate row count | {summary['scientific_gate_row_count']} |",
        f"| Machine-checkable fragment count | {summary['machine_checkable_fragment_count']} |",
        f"| Source missing count | {summary['source_missing_count']} |",
        f"| Proof authority | {str(snapshot['authority_boundary']['proof_authority']).lower()} |",
        f"| Physics promotion authorized | {str(snapshot['authority_boundary']['physics_promotion_authorized']).lower()} |",
        "",
        "## Counts",
        "",
        "### Claim Types",
        "",
        "| Claim type | Count |",
        "| --- | --- |",
    ]
    for key, value in summary["claim_type_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "### Authority Statuses", "", "| Authority status | Count |", "| --- | --- |"])
    for key, value in summary["authority_status_counts"].items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(["", "### Proof-State Statuses", "", "| Status | Count |", "| --- | --- |"])
    for key, value in summary["status_counts"].items():
        lines.append(f"| `{key}` | {value} |")

    lines.extend(
        [
            "",
            "## Rows",
            "",
            "| Row | Object | Status | Source | Conclusion | Non-conclusions |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in snapshot["rows"]:
        status = f"{row['claim_type']} / {row['authority_status']} / {row['status']}"
        lines.append(
            "| `{row_id}` | `{object_id}` | {status} | `{source}` | {conclusion} | {non_conclusions} |".format(
                row_id=row["proof_normal_form_row_id"],
                object_id=row["object_id"],
                status=status,
                source=row["source_artifact_path"],
                conclusion=row["conclusion"],
                non_conclusions=markdown_list(row["non_conclusions"]),
            )
        )

    lines.extend(
        [
            "",
            "## Blocked Overreads",
            "",
        ]
    )
    for term in snapshot["blocked_overread_terms"]:
        lines.append(f"- {term}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(snapshot: dict[str, Any], json_path: Path, markdown_path: Path) -> dict[str, Any]:
    json_output = json_text(snapshot)
    markdown_output = markdown_text(snapshot)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json_output, encoding="utf-8")
    markdown_path.write_text(markdown_output, encoding="utf-8")
    return {
        "json_path": rel_path(json_path),
        "json_hash": sha256_text(json_output),
        "markdown_path": rel_path(markdown_path),
        "markdown_hash": sha256_text(markdown_output),
    }


def check_outputs(snapshot: dict[str, Any], json_path: Path, markdown_path: Path) -> dict[str, Any]:
    expected_json = json_text(snapshot)
    expected_markdown = markdown_text(snapshot)
    checks: list[dict[str, Any]] = []
    for path, expected_text, label in [
        (json_path, expected_json, "json"),
        (markdown_path, expected_markdown, "markdown"),
    ]:
        actual_text = path.read_text(encoding="utf-8") if path.exists() else ""
        checks.append(
            {
                "label": label,
                "path": rel_path(path),
                "fresh": actual_text == expected_text,
                "actual_hash": sha256_text(actual_text) if actual_text else "",
                "expected_hash": sha256_text(expected_text),
            }
        )
    status = "PASS" if all(item["fresh"] for item in checks) else "FAIL"
    return {"status": status, "checks": checks}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render proof-normal-form reader index surfaces.")
    parser.add_argument("--registry", default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--json", default=DEFAULT_JSON_PATH, help="JSON output path.")
    parser.add_argument("--markdown", default=DEFAULT_MARKDOWN_PATH, help="Markdown output path.")
    parser.add_argument("--check", action="store_true", help="Check existing outputs without writing.")
    parser.add_argument("--stdout-json", action="store_true", help="Print the rendered JSON snapshot.")
    args = parser.parse_args(argv)

    try:
        snapshot = build_snapshot(args.registry)
        json_path = repo_path(args.json)
        markdown_path = repo_path(args.markdown)
        if args.check:
            report = check_outputs(snapshot, json_path, markdown_path)
            print(json.dumps(report, indent=2, sort_keys=True) + "\n", end="")
            return 0 if report["status"] == "PASS" else 1
        output_report = write_outputs(snapshot, json_path, markdown_path)
        report = {"status": "PASS", **output_report}
        if args.stdout_json:
            print(json_text(snapshot), end="")
        else:
            print(json.dumps(report, indent=2, sort_keys=True) + "\n", end="")
        return 0
    except ProofNormalFormIndexError as exc:
        report = {"status": "FAIL", "error": str(exc)}
        print(json.dumps(report, indent=2, sort_keys=True) + "\n", end="", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the P15-T02 compact current-frontier renderer outputs."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = ROOT / "scripts" / "research_control"
YAML_PATH = ROOT / "output/compact_current_frontier_v16.yaml"
JSON_PATH = ROOT / "output/compact_current_frontier_v16.json"
MARKDOWN_PATH = ROOT / "wiki/indexes/compact_current_frontier_v16.md"
REQUIRED_HIGH_RISK_ROWS = {
    "m_src",
    "g_eff",
    "matter_coupling",
    "einstein_equations",
    "benchmark_promotion",
}
REQUIRED_BLOCKED_CLAIMS = {
    "source-law adoption",
    "matter-coupling derivation or adoption",
    "Einstein equations",
    "benchmark promotion",
    "completed derivation",
}


def load_module(module_name: str, path: Path):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_report() -> dict[str, object]:
    strict_yaml = load_module("strict_yaml", SCRIPT_DIR / "strict_yaml.py")
    renderer = load_module(
        "render_compact_current_frontier_v16",
        SCRIPT_DIR / "render_compact_current_frontier_v16.py",
    )
    missing_paths = [
        str(path.relative_to(ROOT))
        for path in [YAML_PATH, JSON_PATH, MARKDOWN_PATH]
        if not path.exists()
    ]
    if missing_paths:
        return {"status": "FAIL", "missing_paths": missing_paths}

    yaml_data = strict_yaml.load(YAML_PATH)
    json_data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rendered = renderer.build_snapshot(ROOT)
    validation_errors = renderer.validate_snapshot(json_data)
    high_risk_rows = {
        row.get("burden_id")
        for row in json_data.get("distance_to_gr", {}).get("high_risk_rows", [])
        if isinstance(row, dict)
    }
    blocked_claims = set(json_data.get("claim_boundary", {}).get("blocked_claims", []))
    bare_accepted_rows = [
        row.get("burden_id")
        for row in json_data.get("distance_to_gr", {}).get("high_risk_rows", [])
        if isinstance(row, dict)
        and row.get("burden_id") in REQUIRED_HIGH_RISK_ROWS
        and row.get("reader_facing_status") == "accepted"
    ]
    failures = []
    if yaml_data != json_data:
        failures.append("yaml_json_mismatch")
    if rendered != json_data:
        failures.append("json_not_equal_to_live_render")
    for burden_id in sorted(REQUIRED_HIGH_RISK_ROWS - high_risk_rows):
        failures.append(f"missing_high_risk_row:{burden_id}")
    for claim in sorted(REQUIRED_BLOCKED_CLAIMS - blocked_claims):
        failures.append(f"missing_blocked_claim:{claim}")
    if bare_accepted_rows:
        failures.append("bare_accepted_high_risk_rows:" + ",".join(sorted(bare_accepted_rows)))
    if json_data.get("authority_warning", {}).get("snapshot_only_not_authority") is not True:
        failures.append("snapshot_only_warning_missing_or_false")
    if json_data.get("claim_boundary", {}).get("physics_claim_authority") is not False:
        failures.append("physics_claim_authority_not_false")
    if json_data.get("claim_boundary", {}).get("proof_authority") is not False:
        failures.append("proof_authority_not_false")

    return {
        "status": "PASS" if not failures and not validation_errors else "FAIL",
        "schema_id": json_data.get("schema_id"),
        "active_task_id": json_data.get("active_state", {}).get("active_task_id"),
        "latest_handoff_id": json_data.get("active_state", {}).get("latest_handoff_id"),
        "next_route_id": json_data.get("next_route", {}).get("route_id"),
        "yaml_path": str(YAML_PATH.relative_to(ROOT)),
        "json_path": str(JSON_PATH.relative_to(ROOT)),
        "markdown_path": str(MARKDOWN_PATH.relative_to(ROOT)),
        "yaml_sha256": sha256_path(YAML_PATH),
        "json_sha256": sha256_path(JSON_PATH),
        "markdown_sha256": sha256_path(MARKDOWN_PATH),
        "high_risk_rows": sorted(high_risk_rows),
        "blocked_claim_count": len(blocked_claims),
        "validation_errors": validation_errors,
        "failures": failures,
        "snapshot_only_not_authority": json_data.get("authority_warning", {}).get("snapshot_only_not_authority"),
        "physics_claim_authority": json_data.get("claim_boundary", {}).get("physics_claim_authority"),
        "proof_authority": json_data.get("claim_boundary", {}).get("proof_authority"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.output:
        args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json or not args.output:
        print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

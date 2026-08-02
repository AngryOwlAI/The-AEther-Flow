#!/usr/bin/env python3
"""Validate the P13-T07 live-report freshness packet and negative fixtures."""

from __future__ import annotations

import argparse
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts/research_control"
for import_path in (REPO_ROOT, SCRIPT_DIR):
    if str(import_path) not in sys.path:
        sys.path.insert(0, str(import_path))

import generated_report_provenance as provenance  # noqa: E402
import validate_generated_report_freshness as live_validator  # noqa: E402


SCHEMA_ID = "p13_t07_generated_report_freshness_validation_receipt_v1"
RECEIPT_PATH = (
    "research_control/tasks/RT-20260801-011/artifacts/"
    "p13_t07_generated_report_freshness_receipt.json"
)
FIXTURE_PATH = (
    "research_control/tasks/RT-20260801-011/artifacts/"
    "stale_generated_report_fixture_v1.json"
)
SOURCE_PATHS = [
    "research_control/tasks/RT-20260801-011/artifacts/generated_report_freshness_metadata_schema_v1.yaml",
    FIXTURE_PATH,
    "scripts/research_control/generated_report_provenance.py",
    "scripts/research_control/validate_generated_report_freshness.py",
    "scripts/research_control/render_current_frontier.py",
    "scripts/research_control/render_compact_current_frontier_v16.py",
    "scripts/research_control/render_task_index.py",
    "scripts/research_control/render_dependency_graph.py",
    "scripts/research_control/validate_compact_current_frontier_v16.py",
    "scripts/research_control/validate_task_index.py",
    "research_control/tasks/RT-20260801-011/artifacts/validate_p13_t07_generated_report_freshness.py",
]


def _git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _mutated_hash_fixture(live_report: dict[str, Any]) -> dict[str, Any]:
    expected = copy.deepcopy(live_report["report_provenance"])
    observed = copy.deepcopy(expected)
    observed["source_hashes"][0]["sha256"] = "0" * 64
    validation = provenance.validate_metadata(
        repo_root=REPO_ROOT,
        observed=observed,
        expected=expected,
        strict=True,
    )
    finding_ids = [item["finding_id"] for item in validation["findings"]]
    return {
        "fixture_id": "mutated_primary_source_hash",
        "status": validation["status"],
        "finding_ids": finding_ids,
        "expected_finding_observed": "generated_report_source_metadata_stale" in finding_ids,
    }


def _second_commit_fixture() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="p13-t07-lag-") as directory:
        repo_root = Path(directory)
        _git(repo_root, "init", "-q")
        _git(repo_root, "config", "user.name", "P13-T07 Fixture")
        _git(repo_root, "config", "user.email", "fixture@example.invalid")
        source = repo_root / "source.txt"
        source.write_text("source\n", encoding="utf-8")
        _git(repo_root, "add", "source.txt")
        _git(repo_root, "commit", "-q", "-m", "source")
        source_commit = _git(repo_root, "rev-parse", "HEAD")
        source_hash = provenance.sha256_bytes(source.read_bytes())
        metadata = provenance.build_metadata(
            report_class="current_frontier",
            source_commit=source_commit,
            source_hashes={"source.txt": source_hash},
            primary_source_paths=["source.txt"],
            generation_time="1970-01-01T00:00:00Z",
            task_count=1,
            renderer_path=provenance.HELPER_PATH,
            renderer_sha256=provenance.HELPER_SHA256,
            strict=False,
        )
        for index in (1, 2):
            marker = repo_root / f"unrelated-{index}.txt"
            marker.write_text(f"{index}\n", encoding="utf-8")
            _git(repo_root, "add", marker.name)
            _git(repo_root, "commit", "-q", "-m", f"unrelated {index}")
        validation = provenance.validate_metadata(
            repo_root=repo_root,
            observed=metadata,
            expected=metadata,
            strict=False,
        )
        finding_ids = [item["finding_id"] for item in validation["findings"]]
        return {
            "fixture_id": "second_unrefreshed_commit",
            "status": validation["status"],
            "finding_ids": finding_ids,
            "observed_commit_lag": validation["observed_commit_lag"],
            "maximum_commit_lag": validation["maximum_commit_lag"],
            "expected_finding_observed": "generated_report_commit_lag_exceeded" in finding_ids,
        }


def _stable_live_summary(live: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": live["status"],
        "report_count": live["report_count"],
        "failure_count": live["failure_count"],
        "reports": [
            {
                "report_class": report["report_class"],
                "status": report["status"],
                "output_count": report.get("output_count", 0),
                "source_commit": report.get("report_provenance", {}).get("source_commit", ""),
                "source_manifest_sha256": report.get("report_provenance", {}).get(
                    "source_manifest_sha256", ""
                ),
                "source_path_count": report.get("report_provenance", {}).get(
                    "source_path_count", ""
                ),
                "task_count": report.get("report_provenance", {}).get("task_count", ""),
                "generation_time": report.get("report_provenance", {}).get(
                    "generation_time", ""
                ),
                "maximum_commit_lag": report.get("report_provenance", {}).get(
                    "maximum_commit_lag", ""
                ),
                "artifact_sha256": {
                    name: details["actual_sha256"]
                    for name, details in report.get("artifacts", {}).items()
                },
            }
            for report in live["reports"]
        ],
    }


def build_receipt() -> dict[str, Any]:
    live = live_validator.validate_live_reports(REPO_ROOT)
    usable_report = next(
        (report for report in live["reports"] if "report_provenance" in report),
        None,
    )
    if usable_report is None:
        mutated = {
            "fixture_id": "mutated_primary_source_hash",
            "status": "BLOCKED",
            "finding_ids": [],
            "expected_finding_observed": False,
        }
    else:
        mutated = _mutated_hash_fixture(usable_report)
    lagged = _second_commit_fixture()
    fixtures = [mutated, lagged]
    status = "PASS" if (
        live["status"] == "PASS"
        and all(
            fixture["status"] == "FAIL" and fixture["expected_finding_observed"]
            for fixture in fixtures
        )
    ) else "FAIL"
    fixture_spec = json.loads((REPO_ROOT / FIXTURE_PATH).read_text(encoding="utf-8"))
    return {
        "schema_id": SCHEMA_ID,
        "status": status,
        "task_id": "RT-20260801-011",
        "job_id": "AJ-RT-20260801-011-001",
        "plan_task_id": "P13-T07",
        "goal_receipt": {
            "goal_id": "crg-20260720T161354Z-96bc2664ce31bfe0",
            "generation": 210,
            "pass_index": 188,
            "idempotency_key": "crg-20260720T161354Z-96bc2664ce31bfe0:210",
            "claim_token": "3c35003390b47fd650edd94e68cbb5ca8cb2e43ff0d5ded7",
        },
        "policy_id": str(provenance.POLICY["policy_id"]),
        "live_validation": _stable_live_summary(live),
        "negative_fixtures": fixtures,
        "fixture_spec_schema_id": fixture_spec["schema_id"],
        "source_hashes": {
            path: provenance.sha256_file(REPO_ROOT, path) for path in SOURCE_PATHS
        },
        "claim_boundary_id": "CB-PS-P13-T07-GENERATED-REPORT-FRESHNESS-001",
        "scientific_claims_changed": False,
        "distance_to_gr_changed": False,
        "physics_promotion_authorized": False,
        "proof_authority": False,
        "checkpoint_or_validator_pass_is_scientific_proof": False,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    receipt = build_receipt()
    receipt_text = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    receipt_path = REPO_ROOT / RECEIPT_PATH
    if args.write:
        receipt_path.write_text(receipt_text, encoding="utf-8")
    elif args.check:
        if not receipt_path.is_file() or receipt_path.read_text(encoding="utf-8") != receipt_text:
            receipt["status"] = "FAIL"
            receipt["receipt_fresh"] = False
        else:
            receipt["receipt_fresh"] = True
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(
            f"{receipt['status']} reports={receipt['live_validation']['report_count']} "
            f"negative_fixtures={len(receipt['negative_fixtures'])}"
        )
    return 0 if receipt["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

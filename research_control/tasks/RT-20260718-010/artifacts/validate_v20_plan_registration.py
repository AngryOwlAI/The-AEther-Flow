#!/usr/bin/env python3
"""Validate the bounded v20 P0-T01 plan-registration transaction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260718-010"
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v20.md"
REGISTRY = ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"
REPORT = TASK_DIR / "artifacts/v20_plan_registration_report.json"
HASH_RECEIPT = TASK_DIR / "artifacts/v20_plan_source_hash_receipt.json"
VALIDATION_RECEIPT = TASK_DIR / "artifacts/v20_plan_registration_validation_receipt.json"
OBJECT_ID = "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V20"
EXPECTED_RECOMMENDATIONS = [f"V20-R{number:02d}" for number in range(1, 22)]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def require(condition: bool, finding_id: str, message: str, findings: list[dict[str, str]]) -> None:
    if not condition:
        findings.append({"finding_id": finding_id, "message": message})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings: list[dict[str, str]] = []
    plan_bytes = PLAN.read_bytes()
    plan_text = plan_bytes.decode("utf-8")
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    hash_receipt = json.loads(HASH_RECEIPT.read_text(encoding="utf-8"))

    require(plan_text.startswith("<!-- authority: control -->\n"), "V20-REG-001", "control authority marker missing", findings)
    require('plan_id: "recommendations_implementation_plan_continue_task-v20"' in plan_text, "V20-REG-002", "plan ID missing", findings)
    require('plan_version: "v20"' in plan_text, "V20-REG-003", "plan version missing", findings)
    require('plan_filename: "recommendations_implementation_plan_continue_task-v20.md"' in plan_text, "V20-REG-004", "plan filename missing", findings)
    require('plan_is_runtime_authority: false' in plan_text, "V20-REG-005", "runtime non-authority declaration missing", findings)
    require('goal_files_are_tracked_authority: false' in plan_text, "V20-REG-006", "goal-file non-authority declaration missing", findings)

    phases = re.findall(r"^## P(\d+)\.", plan_text, flags=re.MULTILINE)
    task_cards = re.findall(r"^### (P\d+-T\d+):", plan_text, flags=re.MULTILINE)
    require(len(phases) == 17 and len(set(phases)) == 17, "V20-REG-007", "expected exactly 17 unique phases", findings)
    require(len(task_cards) == 104 and len(set(task_cards)) == 104, "V20-REG-008", "expected exactly 104 unique task cards", findings)

    inventory_text = plan_text.split("## 3. Complete v20 recommendation inventory", 1)[1].split("## 4.", 1)[0]
    coverage_text = plan_text.split("## Appendix A: Recommendation-to-task coverage matrix", 1)[1].split("## Appendix B:", 1)[0]
    inventory_ids = sorted(set(re.findall(r"V20-R\d{2}", inventory_text)))
    coverage_ids = sorted(set(re.findall(r"V20-R\d{2}", coverage_text)))
    require(inventory_ids == EXPECTED_RECOMMENDATIONS, "V20-REG-009", "recommendation inventory is not V20-R01 through V20-R21", findings)
    require(coverage_ids == EXPECTED_RECOMMENDATIONS, "V20-REG-010", "coverage matrix is not V20-R01 through V20-R21", findings)

    with REGISTRY.open(newline="", encoding="utf-8") as stream:
        rows = [row for row in csv.DictReader(stream) if row["object_id"] == OBJECT_ID]
    require(len(rows) == 1, "V20-REG-011", "expected exactly one v20 source registry row", findings)
    if len(rows) == 1:
        row = rows[0]
        require(row["path"] == str(PLAN.relative_to(ROOT)), "V20-REG-012", "registry path mismatch", findings)
        require(row["source_hash"] == sha256(plan_bytes), "V20-REG-013", "registry source hash mismatch", findings)
        require(row["authority_status"] == "project_control", "V20-REG-014", "registry authority status mismatch", findings)
        require("not scientific authority" in row["notes"], "V20-REG-015", "registry non-authority note missing", findings)

    require(report["plan_sha256"] == sha256(plan_bytes), "V20-REG-016", "registration report SHA-256 mismatch", findings)
    require(report["plan_git_blob_sha1"] == git_blob_sha1(plan_bytes), "V20-REG-017", "registration report Git blob mismatch", findings)
    require(report["observed_counts"]["phase_count"] == len(phases), "V20-REG-018", "reported phase count mismatch", findings)
    require(report["observed_counts"]["task_card_count"] == len(task_cards), "V20-REG-019", "reported task-card count mismatch", findings)
    require(report["recommendation_inventory"] == EXPECTED_RECOMMENDATIONS, "V20-REG-020", "reported inventory mismatch", findings)
    require(report["coverage_matrix_recommendations"] == EXPECTED_RECOMMENDATIONS, "V20-REG-021", "reported coverage mismatch", findings)
    require(all(value is False for value in report["non_authority_checks"].values()), "V20-REG-022", "non-authority report contains an authorized protected action", findings)

    for source in hash_receipt["sources"]:
        path = ROOT / source["path"]
        require(path.is_file(), "V20-REG-023", f"hash source missing: {source['path']}", findings)
        if path.is_file():
            data = path.read_bytes()
            require(source["current_sha256"] == sha256(data), "V20-REG-024", f"SHA-256 mismatch: {source['path']}", findings)
            require(source["current_git_blob_sha1"] == git_blob_sha1(data), "V20-REG-025", f"Git blob mismatch: {source['path']}", findings)

    status = "PASS" if not findings else "FAIL"
    receipt = {
        "schema_version": "v20_plan_registration_validation_receipt.v1",
        "task_id": "RT-20260718-010",
        "plan_task_id": "P0-T01",
        "status": status,
        "finding_count": len(findings),
        "findings": findings,
        "observed": {
            "plan_sha256": sha256(plan_bytes),
            "plan_git_blob_sha1": git_blob_sha1(plan_bytes),
            "phase_count": len(phases),
            "task_card_count": len(task_cards),
            "inventory_recommendation_count": len(inventory_ids),
            "coverage_recommendation_count": len(coverage_ids),
            "source_registry_row_count": len(rows),
        },
        "authority_note": "Validation confirms project-control registration only and is not scientific evidence.",
    }
    if args.write_report:
        VALIDATION_RECEIPT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the bounded post-repair v21 P0-T01 registration transaction."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
TASK_DIR = ROOT / "research_control/tasks/RT-20260720-003"
PLAN = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
REGISTRY = ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv"
PROGRAM_STATE = ROOT / "research_control/program_state.yaml"
GITIGNORE = ROOT / ".gitignore"
REPORT = TASK_DIR / "artifacts/v21_plan_registration_report.json"
HASH_RECEIPT = TASK_DIR / "artifacts/v21_plan_source_hash_receipt.json"
VALIDATION_RECEIPT = TASK_DIR / "artifacts/v21_plan_registration_validation_receipt.json"
OBJECT_ID = "MD-RECOMMENDATIONS-IMPLEMENTATION-PLAN-CONTINUE-TASK-V21"
EXPECTED_RECOMMENDATIONS = [f"V21-R{number:02d}" for number in range(1, 73)]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def require(
    condition: bool,
    finding_id: str,
    message: str,
    findings: list[dict[str, str]],
) -> None:
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
    program_state = PROGRAM_STATE.read_text(encoding="utf-8")
    gitignore = GITIGNORE.read_text(encoding="utf-8")
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    hash_receipt = json.loads(HASH_RECEIPT.read_text(encoding="utf-8"))

    require(plan_text.startswith("<!-- authority: control -->\n"), "V21-REG-001", "control authority marker missing", findings)
    require('plan_id: "recommendations_implementation_plan_continue_task-v21"' in plan_text, "V21-REG-002", "plan ID missing", findings)
    require('plan_version: "v21"' in plan_text, "V21-REG-003", "plan version missing", findings)
    require('plan_filename: "recommendations_implementation_plan_continue_task-v21.md"' in plan_text, "V21-REG-004", "plan filename missing", findings)
    require("physics_promotion_authorized_by_plan: false" in plan_text, "V21-REG-005", "physics non-authority declaration missing", findings)
    require("canonical_ontology_edit_authorized_by_plan: false" in plan_text, "V21-REG-006", "ontology non-authority declaration missing", findings)
    require("source_law_adoption_authorized_by_plan: false" in plan_text, "V21-REG-007", "source-law non-authority declaration missing", findings)
    require("completed_derivation_authorized_by_plan: false" in plan_text, "V21-REG-008", "completed-derivation non-authority declaration missing", findings)

    phases = re.findall(r"^## P(\d+)\.", plan_text, flags=re.MULTILINE)
    task_cards = re.findall(r"^### (P\d+-T\d+):", plan_text, flags=re.MULTILINE)
    require(len(phases) == 17 and len(set(phases)) == 17, "V21-REG-009", "expected exactly 17 unique phases", findings)
    require(len(task_cards) == 122 and len(set(task_cards)) == 122, "V21-REG-010", "expected exactly 122 unique work-item cards", findings)

    inventory_text = plan_text.split("## 9. Recommendation inventory", 1)[1].split("## 10.", 1)[0]
    coverage_text = plan_text.split("## 16. Recommendation coverage matrix", 1)[1]
    inventory_ids = sorted(set(re.findall(r"V21-R\d{2}", inventory_text)))
    coverage_ids = sorted(set(re.findall(r"V21-R\d{2}", coverage_text)))
    require(inventory_ids == EXPECTED_RECOMMENDATIONS, "V21-REG-011", "recommendation inventory is not V21-R01 through V21-R72", findings)
    require(coverage_ids == EXPECTED_RECOMMENDATIONS, "V21-REG-012", "coverage matrix is not V21-R01 through V21-R72", findings)

    with REGISTRY.open(newline="", encoding="utf-8") as stream:
        rows = [row for row in csv.DictReader(stream) if row["object_id"] == OBJECT_ID]
    require(len(rows) == 1, "V21-REG-013", "expected exactly one v21 source registry row", findings)
    if len(rows) == 1:
        row = rows[0]
        require(row["path"] == str(PLAN.relative_to(ROOT)), "V21-REG-014", "registry path mismatch", findings)
        require(row["source_hash"] == sha256(plan_bytes), "V21-REG-015", "registry source hash mismatch", findings)
        require(row["authority_status"] == "project_control", "V21-REG-016", "registry authority status mismatch", findings)
        require("not scientific authority" in row["notes"], "V21-REG-017", "registry non-authority note missing", findings)

    exception = "!implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
    require(exception in gitignore.splitlines(), "V21-REG-018", "v21 ignore exception missing", findings)
    require(report["registration_status"] == "COMPLETED", "V21-REG-019", "registration report is not complete", findings)
    require(report["plan_sha256"] == sha256(plan_bytes), "V21-REG-020", "registration report SHA-256 mismatch", findings)
    require(report["plan_git_blob_sha1"] == git_blob_sha1(plan_bytes), "V21-REG-021", "registration report Git blob mismatch", findings)
    require(report["observed_counts"]["phase_count"] == len(phases), "V21-REG-022", "reported phase count mismatch", findings)
    require(report["observed_counts"]["task_card_count"] == len(task_cards), "V21-REG-023", "reported work-item count mismatch", findings)
    require(report["observed_counts"]["inventory_recommendation_count"] == len(inventory_ids), "V21-REG-024", "reported inventory count mismatch", findings)
    require(report["observed_counts"]["coverage_matrix_recommendation_count"] == len(coverage_ids), "V21-REG-025", "reported coverage count mismatch", findings)
    require(all(value is False for value in report["non_authority_checks"].values()), "V21-REG-026", "report contains an authorized protected action", findings)

    require('active_task_id: "RT-20260720-003"' in program_state, "V21-REG-027", "program state active task mismatch", findings)
    require('latest_handoff_id: "handoff-0773"' in program_state, "V21-REG-028", "program state control handoff mismatch", findings)
    require('preserved_scientific_handoff_id: "handoff-0772"' in program_state, "V21-REG-029", "scientific handoff preservation missing", findings)
    require('route_id: "v21_p0_t02_backlog_materialization"' in program_state, "V21-REG-030", "P0-T02 route missing", findings)

    for source in hash_receipt["sources"]:
        path = ROOT / source["path"]
        require(path.is_file(), "V21-REG-031", f"hash source missing: {source['path']}", findings)
        if path.is_file():
            data = path.read_bytes()
            require(source["current_sha256"] == sha256(data), "V21-REG-032", f"SHA-256 mismatch: {source['path']}", findings)
            require(source["current_git_blob_sha1"] == git_blob_sha1(data), "V21-REG-033", f"Git blob mismatch: {source['path']}", findings)

    status = "PASS" if not findings else "FAIL"
    receipt = {
        "schema_version": "v21_plan_registration_validation_receipt.v1",
        "task_id": "RT-20260720-003",
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
            "preserved_scientific_handoff": "handoff-0772",
            "next_plan_work_item": "P0-T02",
        },
        "authority_note": "Validation confirms project-control registration only and is not scientific evidence.",
    }
    if args.write_report:
        VALIDATION_RECEIPT.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    else:
        print(status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the v14 P9-T01 external red-team role-contract packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]

ROLE_PATH = ROOT / ".agents/roles/physics/external-red-team-reviewer.v0.1.0.md"
DESIGN_PATH = ROOT / "research_control/design/external_red_team_reviewer_role_design.md"
APPROVAL_PATH = ROOT / "research_control/approvals/approval-20260702-001.yaml"
ROLE_REGISTRY_PATH = ROOT / "registries/AGENT_ROLE_REGISTRY.csv"
PLAN_PATH = ROOT / "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"


ROLE_REQUIRED_PHRASES = [
    "circularity",
    "hidden target imports",
    "process-authority laundering",
    "evidence-as-adoption laundering",
    "no-target certificate overread",
    "`RR_E` separation collapse",
    "Literature comparison is allowed only when the owning",
    "challenge definitions, assumptions, theorem scope",
    "repair, obstruction, freeze, literature review, selector, or continuation",
    "may not adopt or reject physics objects",
    "Gate Chair verdict",
    "override canonical sources",
    "It may not claim a global no-go theorem unless a separate routed",
    "It may not create permanent role authority",
    "may_promote_claims: false",
]

DESIGN_REQUIRED_PHRASES = [
    "reconciled by v14 P9-T01",
    "approval-20260702-001",
    "process-authority laundering",
    "evidence-as-adoption laundering",
    "no-target certificate overread",
    "`RR_E` separation collapse",
    "V14 P9-T02 should update the review template",
]

PLAN_REQUIRED_PHRASES = [
    "## P9-T01: External red-team role contract",
    "test process-authority laundering",
    "test evidence-as-adoption laundering",
    "test no-target certificate overread",
    "test `RR_E` separation collapse",
    "create permanent role authority without proper project-system process",
]

APPROVAL_REQUIRED_PHRASES = [
    'approval_id: "approval-20260702-001"',
    'decision_id: "DDR-20260702-024"',
    'consumed_by: "AJ-RT-20260702-024-001"',
    "non-promotional permanent role-contract update only",
    "Gate Chair authority",
    "claim promotion",
    "source-law adoption",
    "benchmark promotion",
    "completed derivation",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def phrase_check(label: str, text: str, phrases: list[str]) -> dict:
    normalized_text = re.sub(r"\s+", " ", text)
    missing = [
        phrase
        for phrase in phrases
        if phrase not in text and re.sub(r"\s+", " ", phrase) not in normalized_text
    ]
    return {
        "label": label,
        "status": "PASS" if not missing else "FAIL",
        "missing": missing,
        "required_count": len(phrases),
    }


def load_role_registry_row() -> dict:
    with ROLE_REGISTRY_PATH.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("role_id") == "external-red-team-reviewer" and row.get("version") == "0.1.0":
                return row
    return {}


def registry_check() -> dict:
    row = load_role_registry_row()
    failures = []
    expected = {
        "role_contract_path": ".agents/roles/physics/external-red-team-reviewer.v0.1.0.md",
        "authority_level": "science_draft",
        "status": "active",
        "may_modify_sources": "false",
        "may_promote_claims": "false",
        "requires_human_gate": "false",
        "updated_at": "2026-07-02T08:04:00Z",
    }
    if not row:
        failures.append("missing external-red-team-reviewer@0.1.0 row")
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{key} expected {value!r} got {row.get(key)!r}")
    notes = row.get("notes", "")
    for phrase in [
        "v14 P9",
        "process authority laundering",
        "evidence as adoption",
        "no target overread",
        "RR_E collapse",
        "without source modification or claim promotion",
    ]:
        if phrase not in notes:
            failures.append(f"notes missing {phrase!r}")
    return {
        "label": "agent_role_registry",
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "row": row,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Optional JSON report output path.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    args = parser.parse_args()

    role_text = read(ROLE_PATH)
    design_text = read(DESIGN_PATH)
    plan_text = read(PLAN_PATH)
    approval_text = read(APPROVAL_PATH)

    checks = [
        phrase_check("role_contract", role_text, ROLE_REQUIRED_PHRASES),
        phrase_check("role_design", design_text, DESIGN_REQUIRED_PHRASES),
        phrase_check("v14_plan_source", plan_text, PLAN_REQUIRED_PHRASES),
        phrase_check("approval", approval_text, APPROVAL_REQUIRED_PHRASES),
        registry_check(),
    ]
    status = "PASS" if all(check["status"] == "PASS" for check in checks) else "FAIL"
    report = {
        "schema_id": "p9_t01_external_red_team_role_contract_validation_v1",
        "task_id": "RT-20260702-024",
        "job_id": "AJ-RT-20260702-024-001",
        "status": status,
        "checks": checks,
        "hashes": {
            "role_contract": sha256(ROLE_PATH),
            "role_design": sha256(DESIGN_PATH),
            "approval": sha256(APPROVAL_PATH),
            "agent_role_registry": sha256(ROLE_REGISTRY_PATH),
            "v14_plan": sha256(PLAN_PATH),
        },
        "claim_boundary": {
            "may_promote_claims": False,
            "gate_chair_authority_created": False,
            "physics_object_adoption_or_rejection_authorized": False,
            "benchmark_promotion_authorized": False,
            "completed_derivation_authorized": False,
        },
    }

    if args.output:
        output_path = ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if args.json or not args.output:
        print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

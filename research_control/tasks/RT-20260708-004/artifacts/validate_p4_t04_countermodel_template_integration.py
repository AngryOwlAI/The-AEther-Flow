#!/usr/bin/env python3
"""Validate v18 P4-T04 countermodel-obligation template integration."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
REPORT = ROOT / "research_control/tasks/RT-20260708-004/artifacts/p4_t04_countermodel_template_integration_report.json"

TARGETS = {
    "tasks_readme": ROOT / "research_control/tasks/README.md",
    "completion_template": ROOT / "research_control/templates/COMPLETION_TEMPLATE.yaml",
}

REQUIRED_SNIPPETS = {
    "tasks_readme": [
        "Theorem-Candidate Task Template Requirement",
        "countermodel_obligations:",
        "Director Decision Record waiver",
        "template rule",
    ],
    "completion_template": [
        "countermodel_obligations:",
        "policy_id: \"minimal_countermodel_obligation_policy_v1\"",
        "waiver_decision_id:",
        "countermodel_slot:",
        "forbidden_overread:",
    ],
}

FORBIDDEN_PROMOTION_SNIPPETS = [
    "authorizes source-law adoption",
    "authorizes matter-coupling derivation",
    "authorizes Einstein-equation derivation",
    "authorizes benchmark promotion",
    "authorizes completed derivation",
    "program-wide no-go is established",
]


def check_file(label: str, path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    missing = [snippet for snippet in REQUIRED_SNIPPETS[label] if snippet not in text]
    forbidden_hits = [snippet for snippet in FORBIDDEN_PROMOTION_SNIPPETS if snippet in text]
    return {
        "path": str(path.relative_to(ROOT)),
        "required_snippets_present": not missing,
        "missing_required_snippets": missing,
        "forbidden_promotion_snippets_absent": not forbidden_hits,
        "forbidden_promotion_hits": forbidden_hits,
    }


def main() -> int:
    checks = {label: check_file(label, path) for label, path in TARGETS.items()}
    status = "PASS"
    if any(not item["required_snippets_present"] for item in checks.values()):
        status = "FAIL"
    if any(not item["forbidden_promotion_snippets_absent"] for item in checks.values()):
        status = "FAIL"

    report = {
        "task_id": "RT-20260708-004",
        "plan_task_id": "P4-T04",
        "validator_id": "validate_p4_t04_countermodel_template_integration",
        "status": status,
        "template_requirement": "theorem candidates require countermodel_obligations or explicit DDR waiver",
        "physics_claims_changed": False,
        "physics_promotion_authorized": False,
        "next_route": "P4-T05",
        "checks": checks,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Task-local validator for v18 P7-T07 support formalization traceability."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
REPORT_PATH = (
    REPO_ROOT
    / "research_control"
    / "tasks"
    / "RT-20260708-025"
    / "artifacts"
    / "p7_t07_support_formalization_traceability_report.json"
)
INDEX_PATH = REPO_ROOT / "wiki" / "indexes" / "support_formalization_v18.md"
REGISTRY_PATH = (
    REPO_ROOT
    / "research_control"
    / "design"
    / "support_formalization_traceability_registry_v18.yaml"
)
PNF_REGISTRY_PATH = REPO_ROOT / "registries" / "PROOF_NORMAL_FORM_REGISTRY.csv"


def run_json(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(completed.stdout)


def validate() -> dict[str, object]:
    traceability = run_json(
        [
            sys.executable,
            "scripts/research_control/support_formalization/validate_traceability_registry_v18.py",
            "--json",
        ]
    )
    proof_normal_form = run_json(
        [
            sys.executable,
            "scripts/research_control/validate_proof_normal_form_registry.py",
            "--json",
        ]
    )
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    checks = {
        "registry_exists": REGISTRY_PATH.exists(),
        "pnf_registry_exists": PNF_REGISTRY_PATH.exists(),
        "traceability_pass": traceability.get("status") == "PASS",
        "traceability_entry_count_is_5": traceability.get("entry_count") == 5,
        "proof_normal_form_pass": proof_normal_form.get("status") == "PASS",
        "proof_normal_form_support_rows_present": proof_normal_form.get("support_only_row_count") == 5,
        "index_exists": INDEX_PATH.exists(),
        "index_declares_no_proof_authority": "Proof authority | false" in index_text,
        "index_routes_all_tools": all(
            tool_id in index_text
            for tool_id in [
                "typed_eqsrc_orbit_checker",
                "closure_countermodel_generator",
                "no_target_import_mutation_tester",
                "metric_use_tex_reference_validator",
                "detector_placeholder_collapse_checker",
            ]
        ),
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "traceability": traceability,
        "proof_normal_form": proof_normal_form,
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
        "next_route": "P7-T08 support_formalization_refuter_review",
    }


def main() -> int:
    result = validate()
    if "--write-report" in sys.argv:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

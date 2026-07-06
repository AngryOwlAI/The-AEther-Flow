#!/usr/bin/env python3
"""Validate v17 P7-T02 proof-normal-form initial extraction rows."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
REGISTRY = ROOT / "registries" / "PROOF_NORMAL_FORM_REGISTRY.csv"
REPORT = (
    ROOT
    / "research_control"
    / "tasks"
    / "RT-20260706-014"
    / "artifacts"
    / "p7_t02_proof_normal_form_initial_extraction_report.json"
)

REQUIRED_OBJECTS = {
    "TEX-RESEARCH-CONTROL-M-SRC-GSC-INTEGRATED-SOURCE-ONLY-ADOPTION-THEOREM-GATE-CHAIR-REVIEW",
    "TEX-RESEARCH-CONTROL-NONBOTTOM-METRICDATA-WITNESS-SRC-GSC-POST-GATE-GEFF-CANDIDATE-SCOPED-SOURCE-EXTENSION-ADOPTION-GATE-CHAIR-REVIEW",
    "TEX-V15-P3-T02-SOURCE-CERTIFICATE-OPERATION-LAWS",
    "TEX-V16-P3-SOURCE-SIDE-COUPLING-LAW-TARGET-SPECIFICATION",
    "TEX-V17-P1-T02-SOURCE-SIDE-COUPLING-LAW-CANDIDATE",
    "TEX-RESEARCH-CONTROL-RESP-LC-FINITE-TOY-METRIC-RESPONSE-MODEL-REFUTER-STRESS-TEST",
    "TEX-RESEARCH-CONTROL-RESP-LC-SOURCE-EXTENSION-HUMAN-GATE-ADOPTION-DECISION",
}

ALLOWED_CLAIM_TYPES = {
    "definition",
    "lemma",
    "theorem",
    "proposition",
    "obstruction",
    "decision",
    "boundary",
    "nonconclusion",
}
ALLOWED_AUTHORITY = {"science_draft", "scientific_gate", "control", "support_only"}
ALLOWED_STATUS = {
    "draft_control",
    "scoped_evidence",
    "scoped_adopted",
    "blocked",
    "frozen_negative",
    "not_started",
}
PROMOTION_TERMS = {
    "matter coupling is derived",
    "Einstein equations are derived",
    "benchmark is promoted",
    "completed derivation",
    "adopted as source law",
}


def main() -> int:
    errors: list[str] = []
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    p7_rows = [row for row in rows if row["proof_normal_form_row_id"].startswith("PNF-RT-20260706-014-")]
    row_ids = [row["proof_normal_form_row_id"] for row in p7_rows]
    if len(p7_rows) != 7:
        errors.append(f"expected 7 P7-T02 rows found {len(p7_rows)}")
    if len(row_ids) != len(set(row_ids)):
        errors.append("duplicate P7-T02 row ids found")

    objects = {row["object_id"] for row in p7_rows}
    missing = sorted(REQUIRED_OBJECTS - objects)
    if missing:
        errors.append(f"missing required objects: {missing}")

    for row in p7_rows:
        row_id = row["proof_normal_form_row_id"]
        if row["claim_type"] not in ALLOWED_CLAIM_TYPES:
            errors.append(f"{row_id} invalid claim_type {row['claim_type']}")
        if row["authority_status"] not in ALLOWED_AUTHORITY:
            errors.append(f"{row_id} invalid authority_status {row['authority_status']}")
        if row["status"] not in ALLOWED_STATUS:
            errors.append(f"{row_id} invalid status {row['status']}")
        if not row["source_artifact_path"]:
            errors.append(f"{row_id} missing source_artifact_path")
        if not row["forbidden_premises"]:
            errors.append(f"{row_id} missing forbidden_premises")
        if not row["non_conclusions"]:
            errors.append(f"{row_id} missing non_conclusions")
        if row["authority_status"] == "scientific_gate" and row["status"] != "scoped_adopted":
            errors.append(f"{row_id} scientific_gate row is not scoped_adopted")
        if row["authority_status"] != "scientific_gate" and row["status"] == "scoped_adopted":
            errors.append(f"{row_id} non-gate row claims scoped_adopted")
        if row["claim_type"] == "obstruction" and "global theory rejection" not in row["non_conclusions"]:
            errors.append(f"{row_id} obstruction row lacks global theory rejection guard")
        conclusion_lower = row["conclusion"].lower()
        for term in PROMOTION_TERMS:
            if term.lower() in conclusion_lower:
                errors.append(f"{row_id} conclusion contains promotion term {term}")

    report = {
        "status": "PASS" if not errors else "FAIL",
        "row_count": len(p7_rows),
        "required_object_count": len(REQUIRED_OBJECTS),
        "missing_required_objects": missing if "missing" in locals() else [],
        "errors": errors,
        "support_only": True,
        "proof_authority": False,
        "physics_promotion_authorized": False,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

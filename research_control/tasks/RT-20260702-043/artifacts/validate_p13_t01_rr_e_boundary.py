#!/usr/bin/env python3
"""Validate the bounded P13-T01 RR_E separation boundary packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DOC_PATH = "research_control/design/rr_e_separation_boundary_control_note.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
HANDOFF_PATH = "research_control/handoffs/handoff-0496.yaml"

REQUIRED_RULE = (
    "`RR_E` records may be identified only under explicit source transport, "
    "source invariance, or source factorization certificates for a declared "
    "object. Otherwise separation or obstruction is preserved."
)

REQUIRED_BOUNDARIES = [
    "Future agents must not identify `RR_E` records merely because doing so",
    "simplifies matter semantics",
    "coupling-law arguments",
    "Missing certificate data fails closed",
    "separation or obstruction",
]

NON_CONCLUSION_TERMS = [
    "unrestricted `RR_E` irrelevance theorem status",
    "`RR_E` collapse by detector semantics",
    "`RR_E` collapse by `g_eff`",
    "`RR_E` collapse by benchmark behavior",
    "`RR_ETransportCompletenessOrInvarianceLaw_v1` adoption",
    "source-law adoption",
    "matter-semantics adoption",
    "detector-semantics adoption",
    "coupling-law adoption",
    "matter-coupling derivation or adoption",
    "Einstein equations",
    "benchmark promotion",
    "completed derivation",
]

MACHINE_FLAGS = [
    "rr_e_identification_requires_declared_object: true",
    "rr_e_identification_requires_source_transport_certificate: true",
    "rr_e_identification_requires_source_invariance_certificate: true",
    "rr_e_identification_requires_source_factorization_certificate: true",
    "missing_certificate_preserves_separation_or_obstruction: true",
    "convenience_for_matter_semantics_is_not_identification_evidence: true",
    "convenience_for_coupling_is_not_identification_evidence: true",
    "detector_semantics_cannot_collapse_rr_e: true",
    "g_eff_cannot_collapse_rr_e: true",
    "benchmark_behavior_cannot_collapse_rr_e: true",
    "rr_e_transport_law_adopted: false",
    "unrestricted_rr_e_irrelevance_theorem_proved: false",
    "no_physics_promotion_authorized: true",
    'next_required_packet: "P13-T02 RR_E allowed-identification checklist"',
]


def digest(rel: str) -> str:
    return hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()


def normalize(text: str) -> str:
    return " ".join(text.split())


def load_handoff_task_type() -> str:
    text = (REPO_ROOT / HANDOFF_PATH).read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("task_type:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def validate() -> dict[str, object]:
    errors: list[str] = []
    doc = (REPO_ROOT / DOC_PATH).read_text(encoding="utf-8")
    normalized_doc = normalize(doc)

    if normalize(REQUIRED_RULE) not in normalized_doc:
        errors.append("missing required RR_E identification rule")

    missing_boundaries = [item for item in REQUIRED_BOUNDARIES if item not in doc]
    if missing_boundaries:
        errors.append(f"missing boundary phrases: {missing_boundaries}")

    missing_non_conclusions = [item for item in NON_CONCLUSION_TERMS if item not in doc]
    if missing_non_conclusions:
        errors.append(f"missing non-conclusion terms: {missing_non_conclusions}")

    missing_flags = [item for item in MACHINE_FLAGS if item not in doc]
    if missing_flags:
        errors.append(f"missing machine flags: {missing_flags}")

    if load_handoff_task_type() != "v14_p13_t02_rr_e_allowed_identification_checklist":
        errors.append("handoff-0496 must route to P13-T02 RR_E allowed-identification checklist")

    return {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260702-043",
        "validator_id": "validate_p13_t01_rr_e_boundary",
        "doc_path": DOC_PATH,
        "doc_hash": digest(DOC_PATH),
        "plan_path": PLAN_PATH,
        "plan_hash": digest(PLAN_PATH),
        "required_rule_present": normalize(REQUIRED_RULE) in normalized_doc,
        "non_conclusion_count": len(NON_CONCLUSION_TERMS),
        "machine_flag_count": len(MACHINE_FLAGS),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

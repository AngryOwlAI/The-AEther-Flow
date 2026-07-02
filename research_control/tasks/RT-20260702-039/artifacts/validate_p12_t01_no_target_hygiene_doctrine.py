#!/usr/bin/env python3
"""Validate the bounded P12-T01 no-target certificate hygiene doctrine packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
DOC_PATH = "research_control/design/no_target_certificate_hygiene_doctrine.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
HANDOFF_PATH = "research_control/handoffs/handoff-0492.yaml"

REQUIRED_DOCTRINE = "Negative certificates prevent illegal imports. Positive source-side objects must still construct semantics."

CERTIFICATE_CLASSES = [
    "no-target-topology certificate",
    "no-target-atlas certificate",
    "no-target-metric certificate",
    "no-proper-time certificate",
    "no-detector-import certificate",
    "no-empirical-calibration certificate",
    "no-stress-energy-import certificate",
    "no-matter-action-import certificate",
    "no-GR-benchmark-import certificate",
    "no-process-authority certificate",
]

FORBIDDEN_OVERREADS = [
    "no-target certificate supplies matter semantics",
    "no-detector certificate supplies detector semantics",
    "no-stress-energy certificate supplies stress-energy semantics",
    "no-action certificate supplies matter action",
    "no-benchmark certificate supplies benchmark recovery",
    "no-process-authority certificate supplies mathematical proof",
]

PROMOTION_BLOCKS = [
    "does not adopt `PositiveMSProfile_v1`",
    "`RR_ETransportCompletenessOrInvarianceLaw_v1`",
    "source-side matter semantics",
    "detector semantics",
    "a coupling law",
    "matter coupling",
    "stress-energy semantics",
    "matter action",
    "Einstein equations",
    "benchmark recovery",
    "completed derivation",
]

MACHINE_FLAGS = [
    "negative_certificates_prevent_illegal_imports: true",
    "positive_source_side_objects_must_construct_semantics: true",
    "no_physics_promotion_authorized: true",
    "no_source_law_adoption_authorized: true",
    "no_benchmark_promotion_authorized: true",
    "no_completed_derivation_authorized: true",
    'next_required_packet: "P12-T02 positive semantics requirement note"',
]


def digest(rel: str) -> str:
    return hashlib.sha256((REPO_ROOT / rel).read_bytes()).hexdigest()


def load_handoff_task_type() -> str:
    text = (REPO_ROOT / HANDOFF_PATH).read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("task_type:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def validate() -> dict[str, object]:
    errors: list[str] = []
    doc = (REPO_ROOT / DOC_PATH).read_text(encoding="utf-8")

    if REQUIRED_DOCTRINE not in " ".join(doc.split()):
        errors.append("missing exact required doctrine sentence")

    missing_classes = [item for item in CERTIFICATE_CLASSES if item not in doc]
    if missing_classes:
        errors.append(f"missing certificate classes: {missing_classes}")

    missing_overreads = [item for item in FORBIDDEN_OVERREADS if item not in doc]
    if missing_overreads:
        errors.append(f"missing forbidden overreads: {missing_overreads}")

    missing_blocks = [item for item in PROMOTION_BLOCKS if item not in doc]
    if missing_blocks:
        errors.append(f"missing promotion boundaries: {missing_blocks}")

    missing_flags = [item for item in MACHINE_FLAGS if item not in doc]
    if missing_flags:
        errors.append(f"missing machine flags: {missing_flags}")

    if load_handoff_task_type() != "v14_p12_t02_positive_semantics_requirement_note":
        errors.append("handoff-0492 must route to P12-T02 positive semantics requirement note")

    return {
        "status": "PASS" if not errors else "FAIL",
        "task_id": "RT-20260702-039",
        "validator_id": "validate_p12_t01_no_target_hygiene_doctrine",
        "doc_path": DOC_PATH,
        "doc_hash": digest(DOC_PATH),
        "plan_path": PLAN_PATH,
        "plan_hash": digest(PLAN_PATH),
        "certificate_class_count": len(CERTIFICATE_CLASSES),
        "forbidden_overread_count": len(FORBIDDEN_OVERREADS),
        "promotion_boundary_count": len(PROMOTION_BLOCKS),
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

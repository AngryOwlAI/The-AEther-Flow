#!/usr/bin/env python3
"""Validate the v15 P10-T01 route signature schema control document."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
GENERATED_AT = "2026-07-03T14:42:00Z"
DOC_PATH = "research_control/design/route_signature_schema_v1.md"
LEGACY_DOC_PATH = "research_control/design/route_signature_definition.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v15.md"
RECEIPT_PATH = (
    "research_control/tasks/RT-20260703-017/artifacts/"
    "p10_t01_route_signature_schema_receipt.md"
)

REQUIRED_FIELDS = [
    "target_derivation_milestone",
    "milestone_burden",
    "object_or_claim_name",
    "route_family",
    "role_family",
    "mathematical_payload_class",
    "distance_to_gr_delta",
    "source_extension_classification",
    "obstruction_id",
    "freeze_criteria_status",
    "next_route_selected",
]

REQUIRED_PHRASES = [
    "<!-- authority: control -->",
    "route_signature_schema_v1",
    "Route-Cycle Detection Support",
    "New Mathematics Versus Process Refresh",
    "new_mathematics_signature",
    "process_refresh_signature",
    "route_signature_key",
    "This schema is operational control metadata only.",
    "not a physics source",
    "not a Gate Chair verdict",
    "not authority to promote ontology",
    "Compatibility Projection From v14",
    "source_evidence",
    "Done Criteria",
]

REQUIRED_TUPLE_ITEMS = [
    "`target_derivation_milestone`",
    "`milestone_burden`",
    "`object_or_claim_name`",
    "`route_family`",
    "`role_family`",
    "`mathematical_payload_class`",
    "`distance_to_gr_delta.effect`",
    "`source_extension_classification`",
    "`obstruction_id`",
    "`freeze_criteria_status.decision`",
    "`next_route_selected`",
]

PROHIBITED_PHRASES = [
    "this schema proves",
    "this schema derives",
    "route repetition proves impossibility",
    "therefore future source extensions are impossible",
    "therefore the program is rejected",
]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_receipt(doc_hash: str, legacy_doc_hash: str, plan_hash: str) -> str:
    fields = "\n".join(f"- `{field}`" for field in REQUIRED_FIELDS)
    tuple_items = "\n".join(f"- {item}" for item in REQUIRED_TUPLE_ITEMS)
    receipt = f"""<!-- authority: control -->

# P10-T01 Route Signature Schema Receipt

Generated at: `{GENERATED_AT}`

## Verdict

PASS. The v15 route signature schema defines the required comparison fields,
distinguishes new mathematical payload from process refresh, and supplies a
deterministic tuple for later route-cycle detection. It preserves the
operational-only authority boundary and does not promote any physics claim.

## Hashes

| Source | SHA-256 |
| --- | --- |
| `{DOC_PATH}` | `{doc_hash}` |
| `{LEGACY_DOC_PATH}` | `{legacy_doc_hash}` |
| `{PLAN_PATH}` | `{plan_hash}` |

## Required Fields Confirmed

{fields}

## Comparison Tuple Confirmed

{tuple_items}

## Boundary

The schema is project-control metadata only. It is not a physics source, not
a derivation, not a Gate Chair verdict, not a freeze verdict, and not
authority for ontology promotion, source-law adoption, matter coupling,
stress-energy semantics, Einstein equations, benchmark promotion, completed
derivation, global no-go status, or future source-extension impossibility.

## Next Route

P10-T02 should implement or specify a route signature extractor and run it on
recent matter-coupling tasks.
"""
    receipt_path = REPO_ROOT / RECEIPT_PATH
    receipt_path.write_text(receipt, encoding="utf-8")
    return sha256_text(receipt)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    doc_text = read_text(DOC_PATH)
    legacy_doc_text = read_text(LEGACY_DOC_PATH)
    plan_text = read_text(PLAN_PATH)
    lower_doc = doc_text.lower()

    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if f"`{field}`" not in doc_text and f"{field}:" not in doc_text:
            errors.append(f"{DOC_PATH} missing required field: {field}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in doc_text:
            errors.append(f"{DOC_PATH} missing required phrase: {phrase}")
    for item in REQUIRED_TUPLE_ITEMS:
        if item not in doc_text:
            errors.append(f"{DOC_PATH} missing comparison tuple item: {item}")
    for phrase in PROHIBITED_PHRASES:
        if phrase in lower_doc:
            errors.append(f"{DOC_PATH} contains prohibited phrase: {phrase}")
    if "route_signature_definition_v1" not in legacy_doc_text:
        errors.append(f"{LEGACY_DOC_PATH} no longer contains route_signature_definition_v1")
    if "P10-T01" not in plan_text or "route_signature_schema_v15" not in plan_text:
        errors.append(f"{PLAN_PATH} no longer contains the P10-T01 route signature task")

    doc_hash = sha256_text(doc_text)
    legacy_doc_hash = sha256_text(legacy_doc_text)
    plan_hash = sha256_text(plan_text)
    receipt_hash = ""
    if not errors:
        receipt_hash = write_receipt(
            doc_hash=doc_hash,
            legacy_doc_hash=legacy_doc_hash,
            plan_hash=plan_hash,
        )

    result = {
        "status": "PASS" if not errors else "FAIL",
        "generated_at": GENERATED_AT,
        "doc_path": DOC_PATH,
        "doc_hash": doc_hash,
        "legacy_doc_path": LEGACY_DOC_PATH,
        "legacy_doc_hash": legacy_doc_hash,
        "plan_path": PLAN_PATH,
        "plan_hash": plan_hash,
        "required_field_count": len(REQUIRED_FIELDS),
        "required_phrase_count": len(REQUIRED_PHRASES),
        "comparison_tuple_item_count": len(REQUIRED_TUPLE_ITEMS),
        "receipt_path": RECEIPT_PATH if not errors else "",
        "receipt_hash": receipt_hash,
        "errors": errors,
    }
    output_path = REPO_ROOT / args.output
    output_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

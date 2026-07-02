#!/usr/bin/env python3
"""Validate the v14 P8-T01 route signature definition artifact."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
GENERATED_AT = "2026-07-02T06:08:34Z"
DOC_PATH = "research_control/design/route_signature_definition.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
CURRENT_FRONTIER_PATH = "research_control/current_frontier.md"
RECEIPT_PATH = (
    "research_control/tasks/RT-20260702-018/artifacts/"
    "p8_t01_route_signature_definition_receipt.md"
)
EXPECTED_DOC_HASH = "cd7431c0c4986533a530e6a913a34ef6f6e09a77670f070ea85833951a871f79"

REQUIRED_FIELDS = [
    "signature_schema_id",
    "signature_id",
    "source_task_id",
    "source_job_id",
    "source_completion_path",
    "implementation_plan_id",
    "plan_task_id",
    "target_derivation_milestone",
    "milestone_burden",
    "object_family",
    "object_name",
    "task_type",
    "role_id",
    "execution_role_ref",
    "source_extension_category",
    "selected_route",
    "missing_primitive",
    "payload_type",
    "obstruction_label",
    "freeze_candidate",
    "boundary_synchronization_state",
    "gate_chair_state",
    "previous_task_ids",
    "new_mathematical_payload_exists",
    "exact_repair_attempted",
    "freeze_criteria_evaluated",
    "new_source_evidence_exists",
    "signature_hash",
]

REQUIRED_PHRASES = [
    "route_signature_definition_v1",
    "operational diagnostics",
    "not a physics source",
    "hard orbit candidate",
    "boundary_synchronization_state",
    "scoped_evidence_or_precondition_accepted",
    "evidence-as-adoption laundering",
    "P8-T02 extractor",
]


def read_text(path: str) -> str:
    return (REPO_ROOT / path).read_text(encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_receipt(doc_hash: str, plan_hash: str, current_frontier_hash: str) -> str:
    rows = "\n".join(f"- `{field}`" for field in REQUIRED_FIELDS)
    receipt = f"""<!-- authority: control -->

# P8-T01 Route Signature Definition Receipt

Generated at: `{GENERATED_AT}`

## Verdict

PASS. `route_signature_definition_v1` is defined as a project-control schema
for later route-history extraction and route-orbit validation. The definition
does not implement the extractor or validator and does not create physics
claim authority.

## Hashes

| Source | SHA-256 |
| --- | --- |
| `{DOC_PATH}` | `{doc_hash}` |
| `{PLAN_PATH}` | `{plan_hash}` |
| `{CURRENT_FRONTIER_PATH}` | `{current_frontier_hash}` |

## Required Fields Confirmed

{rows}

## Boundary

The definition is operational control metadata only. It does not authorize
canonical ontology edits, source-law adoption, matter coupling, Einstein
equations, benchmark promotion, completed derivation, or route freezing by
itself.

## Next Route

P8-T02 should implement route-history extraction against this schema before a
route-orbit validator or matter-coupling pilot is attempted.
"""
    receipt_path = REPO_ROOT / RECEIPT_PATH
    receipt_path.write_text(receipt, encoding="utf-8")
    return sha256_text(receipt)


def main() -> int:
    doc_text = read_text(DOC_PATH)
    plan_text = read_text(PLAN_PATH)
    current_frontier_text = read_text(CURRENT_FRONTIER_PATH)

    errors: list[str] = []
    doc_hash = sha256_text(doc_text)
    if doc_hash != EXPECTED_DOC_HASH:
        errors.append(f"{DOC_PATH} hash mismatch: {doc_hash} != {EXPECTED_DOC_HASH}")
    for field in REQUIRED_FIELDS:
        if f"`{field}`" not in doc_text:
            errors.append(f"{DOC_PATH} missing field {field}")
    for phrase in REQUIRED_PHRASES:
        if phrase not in doc_text:
            errors.append(f"{DOC_PATH} missing phrase {phrase}")

    receipt_hash = ""
    if not errors:
        receipt_hash = write_receipt(
            doc_hash=doc_hash,
            plan_hash=sha256_text(plan_text),
            current_frontier_hash=sha256_text(current_frontier_text),
        )

    result = {
        "status": "PASS" if not errors else "FAIL",
        "generated_at": GENERATED_AT,
        "doc_path": DOC_PATH,
        "doc_hash": doc_hash,
        "expected_doc_hash": EXPECTED_DOC_HASH,
        "field_count": len(REQUIRED_FIELDS),
        "receipt_path": RECEIPT_PATH if not errors else "",
        "receipt_hash": receipt_hash,
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

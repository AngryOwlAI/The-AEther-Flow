#!/usr/bin/env python3
"""Validate the v14 P8-T02 route-history extractor packet."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = "scripts/research_control/extract_route_history.py"
TEST_PATH = "tests/test_route_history_extractor.py"
SAMPLE_PATH = "research_control/tasks/RT-20260702-019/artifacts/p8_t02_route_history_sample.json"
RECEIPT_PATH = "research_control/tasks/RT-20260702-019/artifacts/p8_t02_route_history_extractor_receipt.md"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v14.md"
SIGNATURE_DEFINITION_PATH = "research_control/design/route_signature_definition.md"
CURRENT_FRONTIER_PATH = "research_control/current_frontier.md"
GENERATED_AT = "2026-07-02T06:29:55Z"


def load_extractor() -> Any:
    script_file = REPO_ROOT / SCRIPT_PATH
    spec = importlib.util.spec_from_file_location("extract_route_history", script_file)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def sha256_file(path: str) -> str:
    return hashlib.sha256((REPO_ROOT / path).read_bytes()).hexdigest()


def read_sample() -> dict[str, Any]:
    return json.loads((REPO_ROOT / SAMPLE_PATH).read_text(encoding="utf-8"))


def write_receipt(hashes: dict[str, str], sample: dict[str, Any], p8_signature_hash: str) -> str:
    receipt = f"""<!-- authority: control -->

# P8-T02 Route-History Extractor Receipt

Generated at: `{GENERATED_AT}`

## Verdict

PASS. `extract_route_history.py` emits `route_signature_definition_v1`
signatures from tracked task, AgentJob, completion, and registry records. The
extractor is project-control tooling only. It does not add route-orbit hard
gates, freeze routes, or change physics claim authority.

## Hashes

| Source | SHA-256 |
| --- | --- |
| `{SCRIPT_PATH}` | `{hashes[SCRIPT_PATH]}` |
| `{TEST_PATH}` | `{hashes[TEST_PATH]}` |
| `{SAMPLE_PATH}` | `{hashes[SAMPLE_PATH]}` |
| `{PLAN_PATH}` | `{hashes[PLAN_PATH]}` |
| `{SIGNATURE_DEFINITION_PATH}` | `{hashes[SIGNATURE_DEFINITION_PATH]}` |
| `{CURRENT_FRONTIER_PATH}` | `{hashes[CURRENT_FRONTIER_PATH]}` |

## Sample Coverage

- Sample mode: `{sample["sample"]}`
- Signature count: `{sample["signature_count"]}`
- `RT-20260701-030` Gate Chair state:
  `scoped_evidence_or_precondition_accepted`
- `RT-20260701-031` boundary synchronization state: `synchronized`
- P8-T01 extracted signature hash: `{p8_signature_hash}`

## Boundary

The extractor preserves raw source-evidence paths for non-default fields and
emits `unknown`, `none`, or `not_applicable` when tracked evidence does not
support a stronger normalized value. It is not a physics source, not a Gate
Chair verdict, not route-freeze authority, and not proof authority.

## Next Route

P8-T03 may implement route-orbit validator warnings or hard-fail conditions
against these extracted signatures. That validator remains a separate bounded
packet.
"""
    receipt_path = REPO_ROOT / RECEIPT_PATH
    receipt_path.write_text(receipt, encoding="utf-8")
    return hashlib.sha256(receipt.encode("utf-8")).hexdigest()


def main() -> int:
    extractor = load_extractor()
    sample = read_sample()
    errors: list[str] = []

    if sample.get("schema_id") != "route_history_extractor_v1":
        errors.append("sample schema_id mismatch")
    if sample.get("signature_schema_id") != "route_signature_definition_v1":
        errors.append("sample signature_schema_id mismatch")
    if sample.get("sample") != "recent-matter-rr-e":
        errors.append("sample mode mismatch")
    if sample.get("signature_count", 0) < 20:
        errors.append("sample does not cover enough recent route signatures")
    if sample.get("extraction_errors") != []:
        errors.append("sample contains extraction errors")

    signatures = sample.get("signatures", [])
    if not isinstance(signatures, list):
        errors.append("sample.signatures is not a list")
        signatures = []
    signatures_by_task = {
        signature.get("source_task_id"): signature
        for signature in signatures
        if isinstance(signature, dict)
    }

    for signature in signatures:
        if not isinstance(signature, dict):
            errors.append("sample contains a non-map signature")
            continue
        for field in extractor.SIGNATURE_FIELDS:
            if field not in signature:
                errors.append(f"{signature.get('source_task_id', 'unknown')} missing {field}")
        if "signature_hash" in signature and signature.get("signature_hash") != extractor.compute_signature_hash(signature):
            errors.append(f"{signature.get('source_task_id', 'unknown')} signature_hash mismatch")
        if not isinstance(signature.get("source_evidence", {}), dict):
            errors.append(f"{signature.get('source_task_id', 'unknown')} source_evidence is not a map")

    gate_signature = signatures_by_task.get("RT-20260701-030", {})
    if gate_signature.get("gate_chair_state") != "scoped_evidence_or_precondition_accepted":
        errors.append("RT-20260701-030 Gate Chair scoped evidence/precondition state was not extracted")
    sync_signature = signatures_by_task.get("RT-20260701-031", {})
    if sync_signature.get("boundary_synchronization_state") != "synchronized":
        errors.append("RT-20260701-031 boundary synchronization state was not extracted")
    if "RT-20260701-030" not in sync_signature.get("previous_task_ids", []):
        errors.append("RT-20260701-031 did not preserve RT-20260701-030 predecessor link")

    p8_report = extractor.build_route_history(REPO_ROOT, task_ids=["RT-20260702-018"])
    if p8_report.get("extraction_errors") != [] or p8_report.get("signature_count") != 1:
        errors.append("P8-T01 single-task extraction failed")
    p8_signature = p8_report["signatures"][0] if p8_report.get("signatures") else {}
    if p8_signature.get("plan_task_id") != "P8-T01":
        errors.append("P8-T01 plan_task_id not extracted")
    if p8_signature.get("object_name") != "route_signature_definition_v1":
        errors.append("P8-T01 route_signature_definition_v1 object not extracted")

    hashes = {
        path: sha256_file(path)
        for path in (
            SCRIPT_PATH,
            TEST_PATH,
            SAMPLE_PATH,
            PLAN_PATH,
            SIGNATURE_DEFINITION_PATH,
            CURRENT_FRONTIER_PATH,
        )
    }
    receipt_hash = ""
    if not errors:
        receipt_hash = write_receipt(
            hashes=hashes,
            sample=sample,
            p8_signature_hash=str(p8_signature.get("signature_hash", "")),
        )

    result = {
        "status": "PASS" if not errors else "FAIL",
        "generated_at": GENERATED_AT,
        "script_path": SCRIPT_PATH,
        "test_path": TEST_PATH,
        "sample_path": SAMPLE_PATH,
        "receipt_path": RECEIPT_PATH if not errors else "",
        "script_hash": hashes[SCRIPT_PATH],
        "test_hash": hashes[TEST_PATH],
        "sample_hash": hashes[SAMPLE_PATH],
        "p8_signature_hash": p8_signature.get("signature_hash", ""),
        "signature_count": sample.get("signature_count", 0),
        "receipt_hash": receipt_hash,
        "errors": errors,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

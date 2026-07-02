#!/usr/bin/env python3
"""Run the P8-T04 matter-coupling route-orbit pilot."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from extract_route_history import build_route_history, compute_signature_hash  # noqa: E402
from validate_route_orbits import validate_route_history  # noqa: E402


CHAINS = {
    "SourceMatterSemanticsAdoptionReadinessLaw_v1": {
        "task_ids": [
            "RT-20260701-001",
            "RT-20260701-002",
            "RT-20260701-007",
            "RT-20260701-008",
            "RT-20260701-009",
            "RT-20260701-010",
        ],
        "required_steps": ["formalization", "audit", "stress", "selector", "Gate Chair", "boundary"],
        "gate_task_id": "RT-20260701-009",
        "boundary_task_id": "RT-20260701-010",
    },
    "PositiveMSProfile_v1": {
        "task_ids": [
            "RT-20260701-015",
            "RT-20260701-016",
            "RT-20260701-017",
            "RT-20260701-018",
            "RT-20260701-019",
            "RT-20260701-020",
            "RT-20260701-021",
        ],
        "required_steps": ["target", "candidate", "audit", "stress", "selector", "Gate Chair", "boundary"],
        "gate_task_id": "RT-20260701-020",
        "boundary_task_id": "RT-20260701-021",
    },
    "RR_E": {
        "task_ids": [
            "RT-20260701-022",
            "RT-20260701-023",
            "RT-20260701-024",
            "RT-20260701-025",
            "RT-20260701-026",
        ],
        "required_steps": ["theorem target", "theorem-or-obstruction", "audit", "stress", "selector"],
        "gate_task_id": "",
        "boundary_task_id": "",
    },
    "RR_ETransportCompletenessOrInvarianceLaw_v1": {
        "task_ids": [
            "RT-20260701-027",
            "RT-20260701-028",
            "RT-20260701-029",
            "RT-20260701-030",
            "RT-20260701-031",
        ],
        "required_steps": ["formalization", "audit", "stress", "Gate Chair", "P5-T06 sync"],
        "gate_task_id": "RT-20260701-030",
        "boundary_task_id": "RT-20260701-031",
    },
}


def signature_by_task(route_history: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {signature["source_task_id"]: signature for signature in route_history["signatures"]}


def evidence_summary(signature: dict[str, Any]) -> dict[str, Any]:
    return {
        "task_id": signature["source_task_id"],
        "completion_path": signature["source_completion_path"],
        "object_name": signature["object_name"],
        "task_type": signature["task_type"],
        "role_id": signature["role_id"],
        "boundary_synchronization_state": signature["boundary_synchronization_state"],
        "gate_chair_state": signature["gate_chair_state"],
        "new_mathematical_payload_exists": signature["new_mathematical_payload_exists"],
        "route_cycle_control_present": signature.get("route_cycle_control_present", False),
        "source_evidence_keys": sorted(signature.get("source_evidence", {}).keys()),
    }


def classify_chain(name: str, config: dict[str, Any]) -> dict[str, Any]:
    route_history = build_route_history(REPO_ROOT, task_ids=config["task_ids"])
    validation = validate_route_history(route_history)
    signatures = signature_by_task(route_history)
    evidence = [evidence_summary(signatures[task_id]) for task_id in config["task_ids"]]
    warning_codes = {warning["code"] for warning in validation["warnings"]}
    gate_task_id = config.get("gate_task_id", "")
    boundary_task_id = config.get("boundary_task_id", "")
    boundary_sync_recognized = True
    if gate_task_id and boundary_task_id:
        boundary_sync_recognized = (
            signatures[gate_task_id]["gate_chair_state"] == "scoped_evidence_or_precondition_accepted"
            and signatures[boundary_task_id]["boundary_synchronization_state"] == "synchronized"
            and "scoped_gate_followed_by_construction_before_boundary_sync" not in warning_codes
        )
    return {
        "chain_id": name,
        "required_steps": config["required_steps"],
        "task_ids": config["task_ids"],
        "signature_count": route_history["signature_count"],
        "validator_status": validation["status"],
        "hard_failure_count": validation["hard_failure_count"],
        "warning_count": validation["warning_count"],
        "warning_codes": sorted(warning_codes),
        "boundary_sync_recognized": boundary_sync_recognized,
        "source_evidence_complete": all(
            bool(signature.get("source_completion_path")) and bool(signature.get("source_evidence"))
            for signature in route_history["signatures"]
        ),
        "source_evidence": evidence,
    }


def replay_signature(base: dict[str, Any], task_id: str, role_id: str, task_type: str, created_at: str) -> dict[str, Any]:
    signature = dict(base)
    signature.update(
        {
            "signature_id": f"route-sig-{task_id}",
            "source_task_id": task_id,
            "source_job_id": f"AJ-{task_id}-001",
            "source_completion_path": "synthetic/p8_t04_no_payload_replay_control.yaml",
            "role_id": role_id,
            "task_type": task_type,
            "selected_route": "ontology-law-research-packet",
            "new_mathematical_payload_exists": False,
            "exact_repair_attempted": False,
            "obstruction_label": "none",
            "freeze_candidate": "none",
            "freeze_criteria_evaluated": False,
            "boundary_synchronization_state": "pending",
            "gate_chair_state": "not_requested" if role_id != "gate-chair" else "pending",
            "new_source_evidence_exists": False,
            "route_cycle_control_present": False,
            "source_created_at": created_at,
            "source_evidence": {
                "pilot_control_basis": [
                    "research_control/tasks/RT-20260702-021/artifacts/audit_p8_t04_route_orbit_pilot.py"
                ]
            },
        }
    )
    signature["signature_hash"] = compute_signature_hash(signature)
    return signature


def build_no_payload_replay_control() -> dict[str, Any]:
    base_history = build_route_history(REPO_ROOT, task_ids=["RT-20260701-027"])
    base = base_history["signatures"][0]
    control_signatures = [
        replay_signature(base, "RT-P8T04-REPLAY-FORMALIZE", "ontology-formalizer", "replay_formalization", "2026-07-02T07:08:00Z"),
        replay_signature(base, "RT-P8T04-REPLAY-AUDIT", "smuggling-auditor", "replay_audit", "2026-07-02T07:08:01Z"),
        replay_signature(base, "RT-P8T04-REPLAY-STRESS", "refuter", "replay_stress", "2026-07-02T07:08:02Z"),
        replay_signature(base, "RT-P8T04-REPLAY-GATE", "gate-chair", "replay_gate", "2026-07-02T07:08:03Z"),
    ]
    control_history = {
        "schema_id": "route_history_extractor_v1",
        "sample": "p8_t04_no_payload_replay_control",
        "task_count": len(control_signatures),
        "signature_count": len(control_signatures),
        "signatures": control_signatures,
        "extraction_errors": [],
    }
    validation = validate_route_history(control_history)
    return {
        "control_id": "REPEATED_FORMALIZE_AUDIT_STRESS_GATE_NO_NEW_PAYLOAD",
        "basis_task_id": "RT-20260701-027",
        "synthetic_control": True,
        "validator_status": validation["status"],
        "hard_failure_count": validation["hard_failure_count"],
        "warning_count": validation["warning_count"],
        "hard_failures": validation["hard_failures"],
        "warning_codes": sorted({warning["code"] for warning in validation["warnings"]}),
        "flagged": validation["hard_failure_count"] > 0,
    }


def build_report() -> dict[str, Any]:
    chain_reports = [classify_chain(name, config) for name, config in CHAINS.items()]
    all_task_ids: list[str] = []
    for config in CHAINS.values():
        all_task_ids.extend(config["task_ids"])
    combined_history = build_route_history(REPO_ROOT, task_ids=all_task_ids)
    combined_validation = validate_route_history(combined_history)
    replay_control = build_no_payload_replay_control()
    acceptance = {
        "p5_t06_boundary_sync_recognized_not_orbiting": next(
            report for report in chain_reports if report["chain_id"] == "RR_ETransportCompletenessOrInvarianceLaw_v1"
        )["boundary_sync_recognized"],
        "repeated_no_payload_loop_flagged": replay_control["flagged"],
        "recent_chains_classified_with_source_evidence": all(report["source_evidence_complete"] for report in chain_reports),
        "combined_recent_chains_no_hard_failures": combined_validation["hard_failure_count"] == 0,
    }
    return {
        "schema_id": "p8_t04_route_orbit_pilot_report_v1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "source_history_schema_id": combined_history["schema_id"],
        "validator_schema_id": combined_validation["schema_id"],
        "chain_reports": chain_reports,
        "combined_recent_chain_validation": {
            "task_count": combined_history["task_count"],
            "signature_count": combined_history["signature_count"],
            "status": combined_validation["status"],
            "hard_failure_count": combined_validation["hard_failure_count"],
            "warning_count": combined_validation["warning_count"],
            "hard_failures": combined_validation["hard_failures"],
            "warnings": combined_validation["warnings"],
        },
        "no_payload_replay_control": replay_control,
        "acceptance": acceptance,
        "status": "PASS" if all(acceptance.values()) else "FAIL",
        "claim_boundary": {
            "operational_diagnostic_only": True,
            "route_freeze_authorized": False,
            "physics_promotion_authorized": False,
            "source_law_adoption_authorized": False,
            "completed_derivation_authorized": False,
        },
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(list(argv or sys.argv[1:]))
    report = build_report()
    payload = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output is not None:
        output_path = args.output if args.output.is_absolute() else REPO_ROOT / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload, encoding="utf-8")
    if args.json or args.output is None:
        print(payload, end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

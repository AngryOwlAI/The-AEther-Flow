#!/usr/bin/env python3
"""Focused validator for the RT005 signed-cubic Refuter transaction."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260811-005"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_validation.json"
COMPACT = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_compact_receipt.json"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{relative}: top level must be a mapping")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, evidence: Any) -> None:
        checks.append({"check_id": check_id, "passed": bool(condition), "evidence": evidence})
        if not condition:
            errors.append(f"{check_id}: {evidence}")

    yaml_paths = [
        "research_control/tasks/RT-20260811-005/00_TASK.yaml",
        "research_control/tasks/RT-20260811-005/jobs/AJ-RT-20260811-005-001.yaml",
        "research_control/tasks/RT-20260811-005/roles/refuter@0.2.0--RT-20260811-005.yaml",
        "research_control/tasks/RT-20260811-005/artifacts/v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_matrix_v1.yaml",
        "research_control/tasks/RT-20260811-005/artifacts/v22_p4_t02_b2_signed_cubic_viability_selector_refuter_obstruction_v1.yaml",
        "research_control/tasks/RT-20260811-005/artifacts/child_phys_math_p4_t02_b2_signed_cubic_viability_selector_refuter_stress.yaml",
        "research_control/tasks/RT-20260811-005/artifacts/child_phys_phil_p4_t02_b2_signed_cubic_viability_selector_refuter_stress.yaml",
        "research_control/tasks/RT-20260811-005/artifacts/parent_conflict_review_p4_t02_b2_signed_cubic_viability_selector_refuter_stress.yaml",
        "research_control/tasks/RT-20260811-005/artifacts/v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_provenance_manifest_v1.yaml",
        "research_control/tasks/RT-20260811-005/jobs/completions/AJC-AJ-RT-20260811-005-001.yaml",
        "research_control/handoffs/handoff-1019.yaml",
    ]
    loaded: dict[str, dict[str, Any]] = {}
    for relative in yaml_paths:
        try:
            loaded[relative] = load_yaml(relative)
        except Exception as exc:  # noqa: BLE001 - validation boundary
            errors.append(f"strict_yaml:{relative}:{exc}")
    check("strict_unique_yaml", len(loaded) == len(yaml_paths), {"loaded": len(loaded), "required": len(yaml_paths)})

    matrix_path = yaml_paths[3]
    matrix = loaded.get(matrix_path, {})
    check("one_refuter_class", matrix.get("decisive_result_class") == "scoped_obstruction", matrix.get("decisive_result_class"))
    branches = matrix.get("stress_branches", [])
    check("ten_stress_branches", isinstance(branches, list) and len(branches) == 10, len(branches) if isinstance(branches, list) else "not_list")
    payloads = matrix.get("new_mathematical_payload", [])
    check("five_new_payloads", isinstance(payloads, list) and len(payloads) == 5, len(payloads) if isinstance(payloads, list) else "not_list")
    freezes = matrix.get("preserved_freezes", [])
    freeze_ids = [item.get("freeze_id") for item in freezes if isinstance(item, dict)] if isinstance(freezes, list) else []
    check(
        "five_freezes",
        len(freeze_ids) == 5 and "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS" in freeze_ids,
        freeze_ids,
    )
    distance = matrix.get("distance_to_gr_status", [])
    no_delta = [item for item in distance if isinstance(item, dict) and item.get("task_delta") == "no_delta"] if isinstance(distance, list) else []
    check("distance_to_gr_14_no_delta", len(distance) == 14 and len(no_delta) == 14, {"rows": len(distance), "no_delta": len(no_delta)})
    successor = matrix.get("selected_successor", {})
    check(
        "successor_selected_not_executed",
        isinstance(successor, dict)
        and successor.get("packet_id") == "PKT-V22-P4T02-B2-POST-SIGNED-CUBIC-VIABILITY-REFUTER-THEORETICAL-CONTINUATION-SELECTION-V1"
        and successor.get("execution_status") == "selected_not_executed",
        successor,
    )

    obstruction_path = yaml_paths[4]
    obstruction = loaded.get(obstruction_path, {}).get("refuter_obstruction_record", {})
    required_obstruction_fields = {
        "obstruction_id",
        "target_claim",
        "target_milestone",
        "failed_premise",
        "minimal_countermodel_available",
        "countermodel_path",
        "countermodel_scope",
        "certificate_gap",
        "source_extension_repair_possible",
        "global_no_go_claim_authorized",
        "future_source_extension_impossibility_authorized",
        "freeze_criteria_status",
        "route_cycle_control",
        "forbidden_conclusions",
    }
    check(
        "obstruction_schema_complete",
        isinstance(obstruction, dict) and required_obstruction_fields.issubset(obstruction),
        sorted(required_obstruction_fields - set(obstruction)) if isinstance(obstruction, dict) else "not_mapping",
    )
    check(
        "obstruction_protected_claims_false",
        obstruction.get("global_no_go_claim_authorized") is False
        and obstruction.get("future_source_extension_impossibility_authorized") is False,
        {
            "global": obstruction.get("global_no_go_claim_authorized"),
            "future_extension": obstruction.get("future_source_extension_impossibility_authorized"),
        },
    )

    model_path = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_model.py"
    model_run = subprocess.run(
        [sys.executable, str(model_path), "--json"],
        cwd=ROOT,
        check=False,
        text=True,
        capture_output=True,
    )
    try:
        model = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model = {"status": "UNREADABLE", "stderr": model_run.stderr[-500:]}
    check(
        "exact_model_9_of_9",
        model_run.returncode == 0 and model.get("status") == "PASS" and model.get("passed_check_count") == 9,
        {"returncode": model_run.returncode, "status": model.get("status"), "passed": model.get("passed_check_count")},
    )

    for child_path in yaml_paths[5:7]:
        child_text = str(loaded.get(child_path, {}))
        check(
            f"child_contract_{Path(child_path).stem}",
            "scoped_obstruction" in child_text
            and "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS" in child_text
            and "PKT-V22-P4T02-B2-POST-SIGNED-CUBIC-VIABILITY-REFUTER-THEORETICAL-CONTINUATION-SELECTION-V1" in child_text,
            "verdict/freeze/successor parity",
        )

    conflict = loaded.get(yaml_paths[7], {})
    check(
        "parent_conflict_zero",
        conflict.get("unresolved_blocking_conflict_count") == 0,
        conflict.get("unresolved_blocking_conflict_count"),
    )

    tex_path = ART / "v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.exists() else ""
    tex_tokens = [
        "scoped\\_obstruction",
        "F_{\\sigma,\\mu}(a)=-\\gamma a^3+\\mu\\sigma",
        "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
        "No delta",
        "THEORETICAL-CONTINUATION-SELECTION-V1",
    ]
    check("fused_tex_contract", all(token in tex for token in tex_tokens), [token for token in tex_tokens if token not in tex])

    manifest = loaded.get(yaml_paths[8], {})
    source_rows = manifest.get("sources", [])
    hash_failures = []
    if isinstance(source_rows, list):
        for row in source_rows:
            if not isinstance(row, dict):
                hash_failures.append("non_mapping")
                continue
            relative = str(row.get("path", ""))
            expected = str(row.get("sha256", ""))
            source_path = ROOT / relative
            if not source_path.exists() or sha256(source_path) != expected:
                hash_failures.append(relative)
    else:
        hash_failures.append("sources_not_list")
    check("provenance_hashes", isinstance(source_rows, list) and len(source_rows) >= 12 and not hash_failures, {"rows": len(source_rows) if isinstance(source_rows, list) else 0, "failures": hash_failures})

    completion = loaded.get(yaml_paths[9], {})
    loop_risk = completion.get("loop_risk_decision", {})
    check(
        "completion_parent_child_synthesis",
        isinstance(completion.get("parent_child_synthesis"), dict)
        and isinstance(loop_risk, dict)
        and loop_risk.get("category") == "scoped_obstruction",
        {"loop_risk_decision": loop_risk},
    )
    handoff = loaded.get(yaml_paths[10], {})
    check(
        "handoff_successor_unexecuted",
        handoff.get("required_next_packet", {}).get("packet_id")
        == "PKT-V22-P4T02-B2-POST-SIGNED-CUBIC-VIABILITY-REFUTER-THEORETICAL-CONTINUATION-SELECTION-V1"
        and handoff.get("required_next_packet", {}).get("executed") is False,
        handoff.get("required_next_packet", {}),
    )

    status = "PASS" if not errors else "FAIL"
    report = {
        "schema_id": "v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_validation_v1",
        "status": status,
        "check_count": len(checks),
        "passed_check_count": sum(1 for item in checks if item["passed"]),
        "failed_check_count": sum(1 for item in checks if not item["passed"]),
        "errors": errors,
        "checks": checks,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_signed_cubic_viability_selector_refuter_stress_compact_receipt_v1",
            "status": status,
            "check_count": report["check_count"],
            "passed_check_count": report["passed_check_count"],
            "failed_check_count": report["failed_check_count"],
            "report_path": REPORT.relative_to(ROOT).as_posix(),
            "report_sha256": sha256(REPORT),
            "relevant_finding_ids": errors,
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    summary = {
        "status": status,
        "check_count": report["check_count"],
        "passed_check_count": report["passed_check_count"],
        "failed_check_count": report["failed_check_count"],
        "report_path": REPORT.relative_to(ROOT).as_posix(),
        "compact_receipt_path": COMPACT.relative_to(ROOT).as_posix(),
        "errors": errors,
    }
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"{status}: {summary['passed_check_count']}/{summary['check_count']} checks")
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

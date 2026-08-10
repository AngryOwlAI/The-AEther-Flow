#!/usr/bin/env python3
"""Focused validator for the RT-20260810-009 post-Refuter selector.

Passing this validator is operational evidence only.  It is not source-law
construction, ontology adoption, proof promotion, or physics authority.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260810-009"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_post_refuter_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_post_refuter_selector_compact_receipt.json"

PACKET_ID = (
    "PKT-V22-P4T02-B2-COMMON-CHARACTER-DESCENT-"
    "INDEPENDENT-VARIATION-FORMALIZATION-V1"
)
ROUTE_B = "B_COMMON_CHARACTER_DESCENT_AND_INDEPENDENT_SOURCE_VARIATION_PRIMITIVE"
NEXT_ROLE = "ontology-formalizer@0.2.0"
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
}

EXPECTED_HASHES = {
    "child_phys_math_p4_t02_b2_post_refuter_selector.yaml": "c3d387c824d94256d986181b0d5a5c1e1ea02dab74cf15c39ea275da584b7b6f",
    "child_phys_phil_p4_t02_b2_post_refuter_selector.yaml": "dbebbdef1c3f67e73609d0a83998e2c8fb76573a0f7447083d2dba0fd5af4559",
    "parent_conflict_review_p4_t02_b2_post_refuter_selector.yaml": "1368f2951c6ea9a2531d88605a04f4f536d14fa46f172559976272b14cfa0cdf",
    "parent_fusion_notes_p4_t02_b2_post_refuter_selector.md": "bb1d12008fa1dda67540b7355d1f5cfed7e328ebc1236a5fe8efb4a4f5cad797",
    "v22_p4_t02_b2_post_refuter_route_comparison_v1.yaml": "f3a5241652a0ba38d802e65a9366f2de7e93fd4fdbf96ce7823df3001c614d78",
    "v22_p4_t02_b2_post_refuter_route_selection_v1.tex": "f65be2c4890d3595a4e60dc9515cf244faa7c77c2cc52998285d1d0d6c0292da",
    "v22_p4_t02_b2_post_refuter_selector_decision_v1.yaml": "683df4dceec4e3830a55bba859af9c18eb72c7ad1af7cc647a2967f03dc67a6c",
    "v22_p4_t02_b2_post_refuter_selector_latex_compile_receipt.json": "e658d8d8b5140e1d9c935a924751b6f677b665e86429694bcac4b4d3f8f09afb",
    "v22_p4_t02_b2_post_refuter_selector_model.py": "4addddb1535bf63c00670b73b72f5244b12348241d32699dc99d6692bf7d4c93",
    "v22_p4_t02_b2_post_refuter_source_provenance_manifest_v1.yaml": "707472a2c11f7344264117c2d148b862e7e74d190e6db5a58d0455a8467cc064",
    "v22_p4_t02_b2_selected_future_packet_v1.yaml": "18518be4ca42afb94954d362c75117f3bd27bc24dfadbb96a532644b00828941",
}

PREDECESSOR_HASHES = {
    "research_control/handoffs/handoff-1005.yaml": "2f6e77e701381d59b76ffa04c89aa5166e93bdcf9c3400d21d7616c0ea188771",
    "research_control/tasks/RT-20260810-008/artifacts/v22_p4_t02_b2_common_envelope_refuter_stress_v1.tex": "7f860d25cdb6e0578acaf59e70cc745388a2777dbcd2749d3736d6c6e017dea2",
    "research_control/tasks/RT-20260810-008/artifacts/v22_p4_t02_b2_common_envelope_refuter_stress_verdict_v1.yaml": "02cdfa7d5c5e4a0198c88b8c3b76a2770e483947dcce49fd4c4beea38052370c",
    "research_control/tasks/RT-20260810-008/artifacts/v22_p4_t02_b2_common_envelope_refuter_obstruction_v1.yaml": "3128720ae129546a42d40c05221ccef12ee2232daf9459f0ed18fd0ffcb188e9",
}

BURDENS = {
    "Source ontology primitives",
    "Source equivalence EqSrc",
    "RetainH",
    "GenH",
    "ObsLoc_lc",
    "Resp_lc",
    "M_src",
    "g_eff",
    "matter coupling",
    "Einstein equations",
    "finite-variation robustness",
    "benchmark promotion",
    "Gate Chair status",
    "current route freeze or hard-fail status",
}


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.Node, deep: bool = False
) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(
                f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}"
            )
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=UniqueKeyLoader)


def csv_row(path: Path, key: str, value: str) -> dict[str, str] | None:
    with path.open(newline="", encoding="utf-8") as handle:
        return next((row for row in csv.DictReader(handle) if row.get(key) == value), None)


def find_p4_t02(value: Any) -> dict[str, Any] | None:
    if isinstance(value, list):
        return next(
            (
                row
                for row in value
                if isinstance(row, dict) and row.get("plan_task_id") == "P4-T02"
            ),
            None,
        )
    if isinstance(value, dict):
        for child in value.values():
            found = find_p4_t02(child)
            if found is not None:
                return found
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    required = [ART / name for name in EXPECTED_HASHES]
    required.extend(
        [
            TASK / "00_TASK.yaml",
            TASK / "DDR-20260810-009.md",
            TASK / "documentation_impact.yaml",
            TASK / "jobs/AJ-RT-20260810-009-001.yaml",
            TASK / "jobs/completions/AJC-AJ-RT-20260810-009-001.yaml",
            TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260810-009.yaml",
            ROOT / "research_control/handoffs/handoff-1006.yaml",
            ROOT / "research_control/handoffs/handoff-1006.md",
            ROOT / "research_control/program_state.yaml",
            ROOT / "research_control/design/v22_recommendation_backlog.yaml",
        ]
    )
    for path in required:
        check(
            f"exists:{path.relative_to(ROOT)}",
            path.is_file(),
            "required transaction artifact exists",
        )

    for name, expected in EXPECTED_HASHES.items():
        path = ART / name
        check(
            f"hash:{name}",
            path.is_file() and sha256(path) == expected,
            f"expected SHA-256 {expected}",
        )
    for relative, expected in PREDECESSOR_HASHES.items():
        path = ROOT / relative
        check(
            f"immutable:{relative}",
            path.is_file() and sha256(path) == expected,
            "closed predecessor bytes are unchanged",
        )

    yaml_paths = list(TASK.rglob("*.yaml")) + [
        ROOT / "research_control/handoffs/handoff-1006.yaml",
        ROOT / "research_control/design/v22_recommendation_backlog.yaml",
    ]
    parsed: dict[Path, Any] = {}
    for path in yaml_paths:
        try:
            parsed[path] = load_yaml(path)
            check(
                f"yaml_unique:{path.relative_to(ROOT)}",
                True,
                "YAML parses with unique keys",
            )
        except Exception as exc:  # pragma: no cover - diagnostic branch
            check(f"yaml_unique:{path.relative_to(ROOT)}", False, str(exc))
    program_path = ROOT / "research_control/program_state.yaml"
    try:
        parsed[program_path] = yaml.safe_load(program_path.read_text(encoding="utf-8"))
        check("yaml_parse:research_control/program_state.yaml", True, "program state parses")
    except Exception as exc:  # pragma: no cover - diagnostic branch
        check("yaml_parse:research_control/program_state.yaml", False, str(exc))

    model_run = subprocess.run(
        [
            sys.executable,
            str(ART / "v22_p4_t02_b2_post_refuter_selector_model.py"),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        model = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model = {}
    model_checks = model.get("checks", [])
    check("model_exit", model_run.returncode == 0, model_run.stderr or "model exits zero")
    check("model_status", model.get("status") == "PASS", "model status is PASS")
    check(
        "model_checks",
        model.get("check_count") == 9
        and len(model_checks) == 9
        and all(row.get("passed") is True for row in model_checks),
        "all nine exact model checks pass",
    )
    check(
        "model_selection",
        model.get("selected_route")
        == "common_response_line_descent_and_independent_admissible_variation_primitive"
        and model.get("selected_packet_executed") is False,
        "model selects Route B without execution",
    )
    freeze_check = next(
        (row for row in model_checks if row.get("check_id") == "both_local_freezes_preserved"),
        {},
    )
    check(
        "model_freezes",
        set(freeze_check.get("details", [])) == FREEZES,
        "model preserves both local freezes",
    )

    decision_path = ART / "v22_p4_t02_b2_post_refuter_selector_decision_v1.yaml"
    decision = parsed.get(decision_path, {})
    output = decision.get("theoretical_decision_output", {})
    comparison = decision.get("route_comparison_result", {})
    check(
        "decision_exact",
        decision.get("decisive_result")
        == "ontology_law_research_packet_selected_formalization_pending"
        and decision.get("no_fog_check") is True
        and output.get("selected_packet_id") == PACKET_ID
        and output.get("selected_next_role_family") == NEXT_ROLE
        and output.get("selected_packet_executed") is False,
        "decision selects one exact unexecuted Route-B packet",
    )
    check(
        "decision_routes",
        comparison.get("route_count") == 3
        and comparison.get("selected_route") == ROUTE_B
        and len(comparison.get("rejected_routes", [])) == 2
        and comparison.get("route_c_retained_status")
        == "open_later_alternative_after_precise_route_b_obstruction_and_fresh_admission",
        "exactly three routes are compared and Route C is retained only as a later option",
    )
    check(
        "decision_payloads",
        len(decision.get("selector_level_mathematics", [])) == 5,
        "five selector-level mathematical payloads are recorded",
    )

    packet_path = ART / "v22_p4_t02_b2_selected_future_packet_v1.yaml"
    packet = parsed.get(packet_path, {})
    classification = packet.get("source_extension_classification", {})
    authority = packet.get("authority_limits", {})
    check(
        "packet_identity",
        packet.get("packet_id") == PACKET_ID
        and packet.get("selected_next_packet_type") == "ontology_law_research_packet"
        and packet.get("packet_subtype") == "source_side_selector_primitive"
        and packet.get("next_role_family") == NEXT_ROLE
        and packet.get("status") == "selected_not_executed"
        and packet.get("selected_packet_executed") is False,
        "future packet identity, route, role, and execution boundary are exact",
    )
    check(
        "packet_obligations",
        len(packet.get("proof_obligations", [])) == 14
        and len(packet.get("failure_branches", [])) == 11,
        "future packet has fourteen proof obligations and eleven fail-closed branches",
    )
    check(
        "packet_classification",
        classification.get("category") == "source_extension_candidate"
        and classification.get("classification")
        == "new_ontology_primitive_proposal_only_pending_source_purity_audit"
        and classification.get("canonical_ontology_candidate") is False
        and classification.get("adopted") is False
        and classification.get("target_import_detected_at_selection") is False,
        "packet remains proposal-only source-extension data pending source-purity audit",
    )
    boolean_authority = [value for value in authority.values() if isinstance(value, bool)]
    check(
        "packet_authority",
        boolean_authority and all(value is False for value in boolean_authority),
        "future packet grants no construction, adoption, physical, protected, or outward authority",
    )

    route_path = ART / "v22_p4_t02_b2_post_refuter_route_comparison_v1.yaml"
    route = parsed.get(route_path, {})
    selection = route.get("selection", {})
    check(
        "route_comparison",
        len(route.get("routes", [])) == 3
        and selection.get("selected_route_id") == ROUTE_B
        and selection.get("packet_id") == PACKET_ID
        and selection.get("selected_packet_executed") is False
        and route.get("conflict_resolution", {}).get("resolution_round_count") == 2
        and route.get("conflict_resolution", {}).get("route_c_value_preserved") is True,
        "route comparison binds three routes, two rounds, Route B, and retained Route C",
    )

    conflict_path = ART / "parent_conflict_review_p4_t02_b2_post_refuter_selector.yaml"
    conflict = parsed.get(conflict_path, {})
    child_rows = conflict.get("reviewed_child_outputs", [])
    check(
        "conflict_resolved",
        conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_count") == 0
        and conflict.get("unresolved_conflicts") == []
        and conflict.get("resolution_round_count") == 2,
        "two-round parent conflict review is resolved",
    )
    check(
        "children_converged",
        len(child_rows) == 2
        and all(row.get("final_selection") == ROUTE_B for row in child_rows)
        and {row.get("final_sha256") for row in child_rows}
        == {
            EXPECTED_HASHES["child_phys_math_p4_t02_b2_post_refuter_selector.yaml"],
            EXPECTED_HASHES["child_phys_phil_p4_t02_b2_post_refuter_selector.yaml"],
        },
        "both independent children converge on Route B and are hash-bound",
    )

    completion_path = TASK / "jobs/completions/AJC-AJ-RT-20260810-009-001.yaml"
    completion = parsed.get(completion_path, {})
    theory = completion.get("theoretical_decision_output", {})
    ontology = completion.get("ontology_law_research_packet", {})
    check(
        "completion_status",
        completion.get("status") == "completed"
        and theory.get("selected_packet_id") == PACKET_ID
        and theory.get("selected_next_role_family") == NEXT_ROLE
        and theory.get("selected_packet_executed") is False,
        "completion is terminal and binds the exact unexecuted packet",
    )
    check(
        "completion_contract",
        completion.get("physics_progress_status", {}).get("status")
        == "selector_only_no_distance_delta"
        and completion.get("distance_to_gr_delta", {}).get("changed") is False
        and len(completion.get("mathematical_payload_manifest", [])) == 5,
        "selector-only no-distance-delta contract and five payloads are complete",
    )
    burden_rows = completion.get("distance_to_gr_status", [])
    check(
        "completion_burdens",
        len(burden_rows) == 14
        and {row.get("burden") for row in burden_rows} == BURDENS,
        "all fourteen Distance-to-GR burdens occur exactly once",
    )
    receipt_payload = ontology.get("candidate_law_payload", {})
    check(
        "ontology_law_receipt",
        ontology.get("route") == "ontology-law-research-packet"
        and ontology.get("trigger_classification")
        == "derivation_critical_missing_source_law"
        and ontology.get("no_go_theorem_status") == "not_proved"
        and receipt_payload.get("candidate_status") == "proposal-only"
        and isinstance(receipt_payload.get("maps"), list)
        and isinstance(receipt_payload.get("proof_obligations"), list),
        "completion contains a validator-shaped ontology-law receipt",
    )
    completion_freeze = completion.get("freeze_criteria_status", {})
    check(
        "completion_freezes",
        set(completion_freeze.get("preserved_freeze_labels", [])) == FREEZES
        and completion_freeze.get("freeze_decision") == "not_frozen"
        and completion_freeze.get("global_theory_rejection") is False,
        "both old freezes remain while the distinct Route-B packet is not pre-frozen",
    )

    handoff = parsed.get(ROOT / "research_control/handoffs/handoff-1006.yaml", {})
    check(
        "handoff_binding",
        handoff.get("task_id") == "RT-20260810-009"
        and handoff.get("completion_sha256") == sha256(completion_path)
        and handoff.get("claim_boundary", {}).get("selected_packet_id") == PACKET_ID
        and handoff.get("claim_boundary", {}).get("selected_packet_executed") is False
        and handoff.get("selected_next_route", {}).get("role_family") == NEXT_ROLE
        and handoff.get("selected_next_route", {}).get("executed") is False,
        "handoff binds completion and one unexecuted Ontology Formalizer route",
    )

    program = parsed.get(ROOT / "research_control/program_state.yaml", {})
    current = program.get("v22_p4_t02_b2_post_refuter_theoretical_selection", {})
    check(
        "program_state",
        program.get("active_task_id") == "RT-20260810-009"
        and program.get("latest_handoff_id") == "handoff-1006"
        and current.get("selected_packet_id") == PACKET_ID
        and current.get("theoretical_continuation_selector_executed") is True
        and current.get("ontology_formalizer_packet_executed") is False,
        "program state reflects the exact post-selector frontier",
    )

    backlog = parsed.get(ROOT / "research_control/design/v22_recommendation_backlog.yaml", {})
    p4_t02 = find_p4_t02(backlog) or {}
    check(
        "backlog_state",
        p4_t02.get("implementation_status")
        == "b2_post_refuter_route_b_ontology_law_packet_selected_unexecuted_checkpoint_pending"
        and p4_t02.get("runtime_post_refuter_theoretical_continuation_selector_executed") is True
        and p4_t02.get("runtime_post_refuter_selected_route") == ROUTE_B
        and p4_t02.get("runtime_post_refuter_selected_packet_id") == PACKET_ID
        and p4_t02.get("runtime_post_refuter_selected_packet_executed") is False
        and p4_t02.get("runtime_post_refuter_route_c_retained_later_alternative") is True,
        "V22 backlog records the selector outcome and unexecuted packet boundary",
    )

    registry_expectations = [
        ("RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260810-009", "status", "completed"),
        ("DIRECTOR_DECISION_REGISTRY.csv", "decision_id", "DDR-20260810-009", "status", "completed"),
        ("AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260810-009-001", "status", "completed"),
        ("ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref", "theoretical-continuation-selector@0.1.0--RT-20260810-009", "validation_status", "PASS_PRECHECKPOINT_STAGING_REQUIRED"),
        ("CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id", "CB-V22-P4-T02-B2-POST-REFUTER-THEORETICAL-SELECTION-001", "status", "completed"),
        ("TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V22-P4-T02-B2-POST-REFUTER-ROUTE-SELECTION-V1", "source_hash", EXPECTED_HASHES["v22_p4_t02_b2_post_refuter_route_selection_v1.tex"]),
        ("MARKDOWN_SOURCE_REGISTRY.csv", "object_id", "MD-V22-P4-T02-B2-PARENT-FUSION-POST-REFUTER-SELECTION-V1", "source_hash", EXPECTED_HASHES["parent_fusion_notes_p4_t02_b2_post_refuter_selector.md"]),
    ]
    for filename, key, value, field, expected in registry_expectations:
        row = csv_row(ROOT / "registries" / filename, key, value)
        check(
            f"registry:{filename}:{value}",
            row is not None and row.get(field) == expected,
            f"registry field {field} equals {expected}",
        )

    result_status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    report = {
        "schema_id": "v22_p4_t02_b2_post_refuter_selector_validation_v1",
        "task_id": "RT-20260810-009",
        "job_id": "AJ-RT-20260810-009-001",
        "status": result_status,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "failure_count": sum(row["status"] == "FAIL" for row in checks),
        "checks": checks,
        "authority": "operational_validation_only_not_source_law_adoption_or_physics_promotion",
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_post_refuter_selector_compact_receipt_v1",
        "task_id": "RT-20260810-009",
        "job_id": "AJ-RT-20260810-009-001",
        "status": result_status,
        "decisive_result": "ontology_law_research_packet_selected_formalization_pending",
        "selected_route": ROUTE_B,
        "selected_packet_id": PACKET_ID,
        "selected_packet_executed": False,
        "next_role": NEXT_ROLE,
        "preserved_freeze_labels": sorted(FREEZES),
        "route_c_retained_later_alternative": True,
        "distance_to_gr_changed": False,
        "physics_promotion_authorized": False,
        "check_count": len(checks),
        "failure_count": report["failure_count"],
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(result_status)
        if result_status == "FAIL":
            for row in checks:
                if row["status"] == "FAIL":
                    print(f"FAIL {row['check_id']}: {row['detail']}")
    return 0 if result_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

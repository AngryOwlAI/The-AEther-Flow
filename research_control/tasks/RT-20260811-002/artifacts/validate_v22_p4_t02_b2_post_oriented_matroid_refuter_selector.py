#!/usr/bin/env python3
"""Focused validator for the RT-20260811-002 selector transaction.

This validator checks conformance, traceability, and exact finite controls.  It
does not prove a source law, physical interpretation, or Distance-to-GR delta.
"""

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
TASK = ROOT / "research_control/tasks/RT-20260811-002"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_compact_receipt.json"

SELECTED_ROUTE = "A_SOURCE_DYNAMICAL_VIABILITY_ADMISSIBILITY_THEOREM"
SELECTED_PACKET = (
    "PKT-V22-P4T02-B2-SOURCE-DYNAMICAL-VIABILITY-ADMISSIBILITY-"
    "SELECTOR-FORMALIZATION-V1"
)
SELECTED_ROLE = "ontology-formalizer@0.2.0"
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
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


class UniqueLoader(yaml.SafeLoader):
    """YAML loader that rejects duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(
                f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}"
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.load(handle, Loader=UniqueLoader)
    if not isinstance(data, dict):
        raise ValueError(f"{rel(path)} must contain one YAML mapping")
    return data


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{rel(path)} must contain one JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: dict[str, bool] = {}
    failures: list[str] = []
    observations: dict[str, Any] = {}

    def check(name: str, condition: bool, detail: str = "") -> None:
        ok = bool(condition)
        checks[name] = ok
        if not ok:
            failures.append(f"{name}: {detail or 'condition was false'}")

    required = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260811-002-001.yaml",
        "role": TASK
        / "roles/theoretical-continuation-selector@0.1.0--RT-20260811-002.yaml",
        "model": ART
        / "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_model.py",
        "future": ART
        / "v22_p4_t02_b2_post_oriented_matroid_refuter_selected_future_packet_v1.yaml",
        "comparison": ART
        / "v22_p4_t02_b2_post_oriented_matroid_refuter_route_comparison_v1.yaml",
        "decision": ART
        / "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_decision_v1.yaml",
        "tex": ART
        / "v22_p4_t02_b2_post_oriented_matroid_refuter_route_selection_v1.tex",
        "child_math": ART
        / "child_phys_math_p4_t02_b2_post_oriented_matroid_refuter_selector.yaml",
        "child_phil": ART
        / "child_phys_phil_p4_t02_b2_post_oriented_matroid_refuter_selector.yaml",
        "conflict": ART
        / "parent_conflict_review_p4_t02_b2_post_oriented_matroid_refuter_selector.yaml",
        "fusion": ART
        / "parent_fusion_notes_p4_t02_b2_post_oriented_matroid_refuter_selector.md",
        "manifest": ART
        / "v22_p4_t02_b2_post_oriented_matroid_refuter_source_provenance_manifest_v1.yaml",
        "latex": ART
        / "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_latex_compile_receipt.json",
        "completion": TASK
        / "jobs/completions/AJC-AJ-RT-20260811-002-001.yaml",
        "handoff_yaml": ROOT / "research_control/handoffs/handoff-1016.yaml",
        "handoff_md": ROOT / "research_control/handoffs/handoff-1016.md",
        "documentation": TASK / "documentation_impact.yaml",
    }
    for name, path in required.items():
        check(f"required_path_{name}", path.is_file(), rel(path))

    if failures:
        report = {
            "schema_id": "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_validation_v1",
            "status": "FAIL",
            "checks": checks,
            "failures": failures,
        }
        if args.write_report:
            REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        print(json.dumps(report, indent=2, sort_keys=True) if args.json else "FAIL")
        return 1

    try:
        task = load_yaml(required["task"])
        job = load_yaml(required["job"])
        role = load_yaml(required["role"])
        future = load_yaml(required["future"])
        comparison = load_yaml(required["comparison"])
        decision = load_yaml(required["decision"])
        child_math = load_yaml(required["child_math"])
        child_phil = load_yaml(required["child_phil"])
        conflict = load_yaml(required["conflict"])
        manifest = load_yaml(required["manifest"])
        completion = load_yaml(required["completion"])
        handoff = load_yaml(required["handoff_yaml"])
        documentation = load_yaml(required["documentation"])
        latex = load_json(required["latex"])
        checks["strict_unique_key_yaml"] = True
    except Exception as exc:  # exact diagnostic belongs in receipt
        failures.append(f"strict_unique_key_yaml: {exc}")
        checks["strict_unique_key_yaml"] = False
        task = job = role = future = comparison = decision = {}
        child_math = child_phil = conflict = manifest = completion = handoff = {}
        documentation = latex = {}

    model_run = subprocess.run(
        [sys.executable, str(required["model"]), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        model = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model = {}
    check("exact_model_exit_zero", model_run.returncode == 0, model_run.stderr[-500:])
    check("exact_model_pass", model.get("status") == "PASS")
    check("exact_model_selected_route", model.get("selected_route_id") == SELECTED_ROUTE)
    check(
        "exact_model_selected_packet",
        model.get("selected_future_packet_id") == SELECTED_PACKET,
    )
    check(
        "exact_model_checks_all_true",
        bool(model.get("checks")) and all(model.get("checks", {}).values()),
    )
    observations["exact_model_payload_sha256"] = model.get("payload_sha256", "")

    if not failures or task:
        check("task_identity", task.get("task_id") == "RT-20260811-002")
        check("task_completed", task.get("status") == "completed")
        check(
            "task_validation_pass",
            str(task.get("validation_status", "")).startswith("PASS"),
        )
        check("job_identity", job.get("job_id") == "AJ-RT-20260811-002-001")
        check("job_completed", job.get("status") == "completed")
        check(
            "job_validation_pass",
            str(job.get("validation_status", "")).startswith("PASS"),
        )
        check("role_expired", role.get("status") == "expired")
        check(
            "role_validation_pass",
            str(role.get("validation_status", "")).startswith("PASS"),
        )

        task_freezes = set(task.get("completion_contract", {}).get("preserved_freeze_labels", []))
        check("task_exact_four_freezes", task_freezes == FREEZES, str(task_freezes))

        routes = comparison.get("routes", [])
        selected_routes = [r for r in routes if r.get("disposition") == "selected_not_executed"]
        check("comparison_exact_four_routes", len(routes) == 4, str(len(routes)))
        check("comparison_unique_route_ids", len({r.get('route_id') for r in routes}) == 4)
        check("comparison_one_selected", len(selected_routes) == 1, str(selected_routes))
        check(
            "comparison_selected_route",
            bool(selected_routes) and selected_routes[0].get("route_id") == SELECTED_ROUTE,
        )
        check(
            "comparison_three_rejected",
            len([r for r in routes if r.get("disposition") == "not_selected"]) == 3,
        )

        td = decision.get("theoretical_decision_output", {})
        check("decision_selected_packet_type", td.get("selected_next_packet_type") == "ontology_law_research_packet")
        check("decision_selected_packet", td.get("selected_packet_id") == SELECTED_PACKET)
        check("decision_selected_role", td.get("selected_next_role_family") == SELECTED_ROLE)
        check("decision_preserves_claim_blocks", td.get("preserves_claim_blocks") is True)
        check("decision_no_human_gate_now", td.get("requires_human_gate") is False)
        check("decision_packet_unexecuted", td.get("selected_packet_executed") is False)
        check(
            "decision_route_trigger",
            td.get("trigger_classification") == "derivation_critical_missing_source_law",
        )
        check(
            "decision_blocked_adoption_open_continuation",
            td.get("adoption_status") == "blocked_adoption_open_continuation",
        )

        check("future_packet_identity", future.get("packet_id") == SELECTED_PACKET)
        check("future_packet_unexecuted", future.get("selected_packet_executed") is False)
        check("future_packet_role", future.get("next_role_family") == SELECTED_ROLE)
        check("future_packet_type", future.get("selected_next_packet_type") == "ontology_law_research_packet")
        check("future_formal_domain_count", len(future.get("formal_domains", {})) == 9)
        check("future_formal_object_count", len(future.get("formal_objects", [])) == 7)
        check("future_formal_map_count", len(future.get("formal_maps", [])) == 6)
        check("future_theorem_target_count", len(future.get("theorem_targets", [])) == 3)
        check("future_proof_obligation_count", len(future.get("proof_obligations", [])) == 14)
        check("future_failure_branch_count", len(future.get("failure_branches", [])) == 11)
        check(
            "future_no_fog",
            future.get("formalization_attempt_status_contract", {}).get("no_fog_check_required") is True
            and future.get("formalization_attempt_status_contract", {}).get(
                "obligations_only_completion_allowed"
            )
            is False,
        )

        for label, child in (("math", child_math), ("phil", child_phil)):
            selection = child.get("decisive_selection", {})
            if label == "math":
                route_id = selection.get("selected_route_id")
                packet_id = selection.get("selected_future_packet_id")
                role_id = selection.get("selected_next_role_family")
                unexecuted = selection.get("selected_packet_executed") is False
                rows = child.get("distance_to_gr_status", {}).get("rows", [])
                child_freezes = {
                    r.get("freeze_label")
                    for r in child.get("freeze_evaluation", {}).get("evaluations", [])
                }
            else:
                route_id = selection.get("selected_route_id")
                packet_id = selection.get("selected_future_packet_id")
                role_id = selection.get("selected_next_role")
                unexecuted = selection.get("selected_packet_executed") is False
                rows = child.get("distance_to_gr_status", {}).get("rows", [])
                child_freezes = {
                    r.get("freeze_label")
                    for r in child.get("freeze_preservation", {}).get("freezes", [])
                }
            check(f"child_{label}_route", route_id == SELECTED_ROUTE)
            check(f"child_{label}_packet", packet_id == SELECTED_PACKET)
            check(f"child_{label}_role", role_id == SELECTED_ROLE)
            check(f"child_{label}_unexecuted", unexecuted)
            check(f"child_{label}_four_freezes", child_freezes == FREEZES, str(child_freezes))
            check(f"child_{label}_fourteen_distance_rows", len(rows) == 14)
            check(
                f"child_{label}_all_no_delta",
                all((r.get("status") == "no_delta") for r in rows),
            )

        synthesis = decision.get("parent_child_synthesis", {})
        child_records = synthesis.get("child_outputs", [])
        check("synthesis_two_children", len(child_records) == 2)
        check(
            "synthesis_child_hashes_match",
            {r.get("sha256") for r in child_records}
            == {digest(required["child_math"]), digest(required["child_phil"])},
        )
        check("conflict_zero_blocking", conflict.get("blocking_conflict_count") == 0)
        check("conflict_no_unresolved", conflict.get("unresolved_conflicts") == [])
        check("conflict_zero_rounds", conflict.get("resolution_round_count") == 0)

        decision_rows = decision.get("distance_to_gr_status", [])
        check("decision_fourteen_distance_rows", len(decision_rows) == 14)
        check(
            "decision_exact_burden_set",
            {r.get("burden") for r in decision_rows} == BURDENS,
        )
        check("decision_all_no_delta", all(r.get("task_delta") == "none" for r in decision_rows))
        check("distance_delta_false", decision.get("distance_to_gr_delta", {}).get("changed") is False)

        active_freezes = set(
            decision.get("freeze_criteria_status", {}).get("active_freeze_labels", [])
        )
        check("decision_exact_four_freezes", active_freezes == FREEZES, str(active_freezes))

        tex_text = required["tex"].read_text(encoding="utf-8")
        fusion_text = required["fusion"].read_text(encoding="utf-8")
        handoff_md = required["handoff_md"].read_text(encoding="utf-8")
        for phrase in (
            "Representation--occurrence separation",
            "Reachability-component branch robustness",
            "Finite source-barrier propagation",
            SELECTED_PACKET,
            "fourteen literal no-delta rows",
        ):
            check(f"tex_phrase_{hashlib.sha1(phrase.encode()).hexdigest()[:8]}", phrase in tex_text, phrase)
        check("fusion_selected_packet", SELECTED_PACKET in fusion_text)
        check("fusion_fourteen_no_delta", "fourteen Distance-to-GR rows" in fusion_text)
        check("handoff_markdown_selected_packet", SELECTED_PACKET in handoff_md)

        check("latex_pass", latex.get("status") == "PASS")
        check("latex_five_pages", latex.get("page_count") == 5)
        check("latex_visual_pass", latex.get("visual_inspection", {}).get("status") == "PASS")
        check("latex_source_hash", latex.get("source_sha256") == digest(required["tex"]))

        manifest_rows = manifest.get("governing_sources", []) + manifest.get(
            "science_and_synthesis_artifacts", []
        )
        manifest_mismatches: list[str] = []
        for row in manifest_rows:
            path = ROOT / str(row.get("path", ""))
            expected = row.get("sha256", "")
            if not path.is_file() or digest(path) != expected:
                manifest_mismatches.append(str(row.get("path", "")))
        check("manifest_hash_closure", not manifest_mismatches, str(manifest_mismatches))
        check(
            "manifest_declared_counts",
            len(manifest.get("governing_sources", [])) == 16
            and len(manifest.get("science_and_synthesis_artifacts", [])) == 10,
        )

        check("completion_identity", completion.get("completion_id") == "AJC-AJ-RT-20260811-002-001")
        check(
            "completion_pass",
            str(completion.get("validation_status", "")).startswith("PASS"),
        )
        check("completion_selector_only", completion.get("physics_progress_status", {}).get("status") == "selector_only_no_distance_delta")
        check("completion_no_distance_delta", completion.get("distance_to_gr_delta", {}).get("changed") is False)
        check("completion_project_signals_empty", completion.get("project_improvement_signals") == [])
        check("handoff_identity", handoff.get("handoff_id") == "handoff-1016")
        check("handoff_pass", str(handoff.get("validation_status", "")).startswith("PASS"))
        check("handoff_selected_packet", handoff.get("claim_boundary", {}).get("selected_packet_id") == SELECTED_PACKET)
        check("handoff_packet_unexecuted", handoff.get("claim_boundary", {}).get("selected_packet_executed") is False)
        check("documentation_update_recorded", documentation.get("docs_update_required") is True)

    report = {
        "schema_id": "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_validation_v1",
        "task_id": "RT-20260811-002",
        "job_id": "AJ-RT-20260811-002-001",
        "status": "PASS" if all(checks.values()) and not failures else "FAIL",
        "selected_route_id": SELECTED_ROUTE,
        "selected_packet_id": SELECTED_PACKET,
        "selected_role": SELECTED_ROLE,
        "selected_packet_executed": False,
        "check_count": len(checks),
        "pass_count": sum(1 for value in checks.values() if value),
        "fail_count": sum(1 for value in checks.values() if not value),
        "checks": checks,
        "failures": failures,
        "observations": observations,
        "authority_note": "PASS establishes transaction conformance, not source-law truth, physical meaning, adoption, or Distance-to-GR progress.",
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    compact = {
        "schema_id": "v22_p4_t02_b2_post_oriented_matroid_refuter_selector_compact_receipt_v1",
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "status": report["status"],
        "check_count": report["check_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "selected_route_id": SELECTED_ROUTE,
        "selected_packet_id": SELECTED_PACKET,
        "selected_packet_executed": False,
        "full_report_path": rel(REPORT),
        "full_report_payload_sha256": report["payload_sha256"],
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output: dict[str, Any] = report if args.json else compact
    print(json.dumps(output, indent=2, sort_keys=True) if args.json else output["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

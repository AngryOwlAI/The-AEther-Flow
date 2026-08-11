#!/usr/bin/env python3
"""Focused conformance validator for the bounded RT-20260811-006 selector."""

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
TASK = ROOT / "research_control/tasks/RT-20260811-006"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_compact_receipt.json"

ROUTE = "A_SOURCE_LAW_SPACE_ROBUST_INVARIANCE_PROTECTION"
MATH_ROUTE_ALIAS = "A_SOURCE_LAW_SPACE_ROBUST_INVARIANCE_PROTECTION_LAW"
PACKET = "PKT-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-FORMALIZATION-V1"
ROLE = "ontology-formalizer@0.2.0"
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
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
    """Reject duplicate mapping keys."""


def _unique(loader: UniqueLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = yaml.load(handle, Loader=UniqueLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{rel(path)} is not one YAML mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{rel(path)} is not one JSON object")
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: dict[str, bool] = {}
    failures: list[str] = []
    observations: dict[str, Any] = {}

    def check(name: str, condition: bool, detail: str = "") -> None:
        checks[name] = bool(condition)
        if not condition:
            failures.append(f"{name}: {detail or 'condition was false'}")

    required = {
        "task": TASK / "00_TASK.yaml",
        "job": TASK / "jobs/AJ-RT-20260811-006-001.yaml",
        "role": TASK / "roles/theoretical-continuation-selector@0.1.0--RT-20260811-006.yaml",
        "model": ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_model.py",
        "future": ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selected_future_packet_v1.yaml",
        "comparison": ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_route_comparison_v1.yaml",
        "decision": ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_decision_v1.yaml",
        "tex": ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_route_selection_v1.tex",
        "child_math": ART / "child_phys_math_p4_t02_b2_post_signed_cubic_viability_refuter_selector.yaml",
        "child_phil": ART / "child_phys_phil_p4_t02_b2_post_signed_cubic_viability_refuter_selector.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_post_signed_cubic_viability_refuter_selector.yaml",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_post_signed_cubic_viability_refuter_selector.md",
        "manifest": ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_source_provenance_manifest_v1.yaml",
        "latex": ART / "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_latex_compile_receipt.json",
        "completion": TASK / "jobs/completions/AJC-AJ-RT-20260811-006-001.yaml",
        "handoff_yaml": ROOT / "research_control/handoffs/handoff-1020.yaml",
        "handoff_md": ROOT / "research_control/handoffs/handoff-1020.md",
        "documentation": TASK / "documentation_impact.yaml",
    }
    for name, path in required.items():
        check(f"required_path_{name}", path.is_file(), rel(path))

    if failures:
        report = {
            "schema_id": "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_validation_v1",
            "task_id": "RT-20260811-006",
            "job_id": "AJ-RT-20260811-006-001",
            "status": "FAIL",
            "checks": checks,
            "failures": failures,
        }
        if args.write_report:
            REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2, sort_keys=True) if args.json else "FAIL")
        return 1

    try:
        records = {name: load_yaml(path) for name, path in required.items() if path.suffix == ".yaml"}
        latex = load_json(required["latex"])
        checks["strict_unique_key_yaml"] = True
    except Exception as exc:
        records = {}
        latex = {}
        checks["strict_unique_key_yaml"] = False
        failures.append(f"strict_unique_key_yaml: {exc}")

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
    check("exact_model_route", model.get("selected_route_id") == ROUTE)
    check("exact_model_packet", model.get("selected_packet_id") == PACKET)
    check("exact_model_unexecuted", model.get("selected_packet_executed") is False)
    check("exact_model_twelve_checks", len(model.get("checks", {})) == 12)
    check("exact_model_all_checks", bool(model.get("checks")) and all(model.get("checks", {}).values()))
    observations["model_stdout_sha256"] = hashlib.sha256(model_run.stdout.encode()).hexdigest()

    if records:
        task = records["task"]
        job = records["job"]
        role = records["role"]
        future = records["future"]
        comparison = records["comparison"]
        decision = records["decision"]
        child_math = records["child_math"]
        child_phil = records["child_phil"]
        conflict = records["conflict"]
        manifest = records["manifest"]
        completion = records["completion"]
        handoff = records["handoff_yaml"]
        documentation = records["documentation"]

        check("task_completed", task.get("task_id") == "RT-20260811-006" and task.get("status") == "completed")
        check("task_validation_pass", str(task.get("validation_status", "")).startswith("PASS"))
        check("job_completed", job.get("job_id") == "AJ-RT-20260811-006-001" and job.get("status") == "completed")
        check("job_validation_pass", str(job.get("validation_status", "")).startswith("PASS"))
        check("role_expired", role.get("status") == "expired")
        check("role_validation_pass", str(role.get("validation_status", "")).startswith("PASS"))

        routes = comparison.get("routes", [])
        selected = [row for row in routes if row.get("disposition") == "selected"]
        check("comparison_exact_four_routes", len(routes) == 4, str(len(routes)))
        check("comparison_unique_route_ids", len({row.get("route_id") for row in routes}) == 4)
        check("comparison_one_selected", len(selected) == 1, str(selected))
        check("comparison_selected_route", bool(selected) and selected[0].get("route_id") == ROUTE)
        check("comparison_selected_packet", comparison.get("selected_route", {}).get("packet_id") == PACKET)
        check("comparison_packet_unexecuted", comparison.get("selected_route", {}).get("selected_packet_executed") is False)
        check("comparison_five_freezes", set(comparison.get("preserved_freeze_labels", [])) == FREEZES)
        comparison_rows = comparison.get("distance_to_gr_status", [])
        check("comparison_fourteen_rows", len(comparison_rows) == 14)
        check("comparison_burdens", {row.get("burden") for row in comparison_rows} == BURDENS)
        check("comparison_all_no_delta", all(row.get("status") == "no_delta" for row in comparison_rows))

        selected_path = decision.get("selected_path", {})
        theoretical = decision.get("theoretical_decision_output", {})
        check("decision_route", selected_path.get("route_id") == ROUTE)
        check("decision_packet", selected_path.get("packet_id") == PACKET)
        check("decision_role", selected_path.get("next_role_family") == ROLE)
        check("decision_type", theoretical.get("selected_next_packet_type") == "ontology_law_research_packet")
        check("decision_preserves_blocks", theoretical.get("preserves_claim_blocks") is True)
        check("decision_no_gate_now", theoretical.get("requires_human_gate") is False)
        check("decision_unexecuted", selected_path.get("selected_packet_executed") is False)
        decision_rows = decision.get("distance_to_gr_status", [])
        check("decision_fourteen_rows", len(decision_rows) == 14)
        check("decision_all_no_delta", all(row.get("status") == "no_delta" for row in decision_rows))

        check("future_packet", future.get("packet_id") == PACKET)
        check("future_role", future.get("selected_next_role_family") == ROLE)
        check("future_status", future.get("packet_status") == "selected_not_executed")
        check("future_unexecuted", future.get("result_contract", {}).get("selected_packet_executed") is False)
        check("future_objects", len(future.get("formal_objects", [])) == 8)
        check("future_domains", len(future.get("domains", [])) == 5)
        check("future_maps", len(future.get("maps", [])) == 6)
        check("future_theorems", len(future.get("theorem_targets", [])) == 5)
        check("future_obligations", len(future.get("proof_obligations", [])) == 14)
        check("future_failures", len(future.get("failure_branches", [])) == 11)
        check("future_five_freezes", set(future.get("preserved_freeze_labels", [])) == FREEZES)

        math_sel = child_math.get("decisive_selection", {})
        phil_sel = child_phil.get("decisive_selection", {})
        check("child_math_route_alias_resolved", math_sel.get("selected_route_id") == MATH_ROUTE_ALIAS)
        check("child_math_packet", math_sel.get("selected_future_packet_id") == PACKET)
        check("child_math_role", math_sel.get("selected_next_role_family") == ROLE)
        check("child_math_unexecuted", math_sel.get("selected_packet_executed") is False)
        check("child_phil_route", phil_sel.get("selected_route_id") == ROUTE)
        check("child_phil_packet", phil_sel.get("selected_future_packet_id") == PACKET)
        check("child_phil_role", phil_sel.get("selected_next_role") == ROLE)
        check("child_phil_unexecuted", phil_sel.get("selected_packet_executed") is False)
        for label, child in (("math", child_math), ("phil", child_phil)):
            rows = child.get("distance_to_gr_status", {}).get("rows", [])
            check(f"child_{label}_fourteen_rows", len(rows) == 14)
            check(f"child_{label}_all_no_delta", all(row.get("status") == "no_delta" for row in rows))
        math_freezes = {row.get("freeze_label") for row in child_math.get("freeze_evaluation", {}).get("evaluations", [])}
        phil_freezes = {row.get("freeze_label") for row in child_phil.get("freeze_preservation", {}).get("freezes", [])}
        check("child_math_five_freezes", math_freezes == FREEZES, str(math_freezes))
        check("child_phil_five_freezes", phil_freezes == FREEZES, str(phil_freezes))

        check("conflict_resolved", conflict.get("status") == "resolved")
        check("conflict_round_one", conflict.get("resolution_rounds") == 1)
        check("conflict_two_resolutions", conflict.get("resolved_conflict_count") == 2)
        check("conflict_no_unresolved", conflict.get("unresolved_conflicts") == [])
        check("conflict_canonical_route", conflict.get("fusion_result", {}).get("selected_route_id") == ROUTE)
        check("conflict_child_hashes", {row.get("sha256") for row in conflict.get("child_inputs", [])} == {digest(required["child_math"]), digest(required["child_phil"])})

        tex_text = required["tex"].read_text(encoding="utf-8")
        tex_semantic_text = tex_text.replace("\\\\\n", "")
        fusion_text = required["fusion"].read_text(encoding="utf-8")
        handoff_text = required["handoff_md"].read_text(encoding="utf-8")
        for token in (PACKET, "RobInv", "Balanced-normal-variation obstruction", "fourteen"):
            check(f"tex_token_{hashlib.sha1(token.encode()).hexdigest()[:8]}", token in tex_semantic_text, token)
        check("fusion_packet", PACKET in fusion_text)
        check("fusion_no_unresolved", "no unresolved blocking conflicts" in fusion_text)
        check("handoff_markdown_packet", PACKET in handoff_text)

        check("latex_pass", latex.get("status") == "PASS")
        check("latex_five_pages", latex.get("page_count") == 5)
        check("latex_source_hash", latex.get("source_sha256") == digest(required["tex"]))
        check("latex_visual_pass", latex.get("visual_inspection", {}).get("status") == "PASS")
        check("latex_all_pages_inspected", latex.get("visual_inspection", {}).get("pages_inspected") == [1, 2, 3, 4, 5])

        manifest_mismatches: list[str] = []
        for row in manifest.get("sources", []):
            item = ROOT / str(row.get("path", ""))
            if not item.is_file() or digest(item) != row.get("sha256"):
                manifest_mismatches.append(str(row.get("path", "")))
        check("manifest_eighteen_sources", len(manifest.get("sources", [])) == 18)
        check("manifest_hash_closure", not manifest_mismatches, str(manifest_mismatches))

        check("completion_identity", completion.get("completion_id") == "AJC-AJ-RT-20260811-006-001")
        check("completion_pass", str(completion.get("validation_status", "")).startswith("PASS"))
        check("completion_selector_only", completion.get("physics_progress_status", {}).get("status") == "selector_only_no_distance_delta")
        check("completion_packet", completion.get("theoretical_decision_output", {}).get("selected_packet_id") == PACKET)
        check("completion_unexecuted", completion.get("theoretical_decision_output", {}).get("selected_packet_executed") is False)
        completion_rows = completion.get("distance_to_gr_status", [])
        check("completion_fourteen_rows", len(completion_rows) == 14)
        check("completion_no_delta", all(row.get("task_delta") == "none" for row in completion_rows))
        check("completion_project_signals_empty", completion.get("project_improvement_signals") == [])

        check("handoff_identity", handoff.get("handoff_id") == "handoff-1020")
        check("handoff_pass", str(handoff.get("validation_status", "")).startswith("PASS"))
        check("handoff_packet", handoff.get("claim_boundary", {}).get("selected_packet_id") == PACKET)
        check("handoff_unexecuted", handoff.get("claim_boundary", {}).get("selected_packet_executed") is False)
        check("documentation_completed", documentation.get("status") == "completed")
        check("documentation_update_recorded", documentation.get("docs_update_required") is True)

    report = {
        "schema_id": "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_validation_v1",
        "task_id": "RT-20260811-006",
        "job_id": "AJ-RT-20260811-006-001",
        "status": "PASS" if all(checks.values()) and not failures else "FAIL",
        "selected_route_id": ROUTE,
        "selected_packet_id": PACKET,
        "selected_role": ROLE,
        "selected_packet_executed": False,
        "check_count": len(checks),
        "pass_count": sum(checks.values()),
        "fail_count": sum(not value for value in checks.values()),
        "checks": checks,
        "failures": failures,
        "observations": observations,
        "authority_note": "PASS establishes selector-transaction conformance only; it does not establish source-law truth, physical interpretation, adoption, proof authority, or Distance-to-GR progress.",
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    report["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    compact = {
        "schema_id": "v22_p4_t02_b2_post_signed_cubic_viability_refuter_selector_compact_receipt_v1",
        "task_id": report["task_id"],
        "job_id": report["job_id"],
        "status": report["status"],
        "check_count": report["check_count"],
        "pass_count": report["pass_count"],
        "fail_count": report["fail_count"],
        "selected_route_id": ROUTE,
        "selected_packet_id": PACKET,
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

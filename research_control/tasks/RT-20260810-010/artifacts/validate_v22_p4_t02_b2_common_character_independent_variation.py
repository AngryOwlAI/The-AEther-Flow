#!/usr/bin/env python3
"""Focused validator for the RT-20260810-010 proposal-only source law.

Passing this validator is operational evidence only. It is not a source-purity
verdict, ontology adoption, physical interpretation, or proof promotion.
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
TASK = ROOT / "research_control/tasks/RT-20260810-010"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_common_character_validation.json"
COMPACT = ART / "v22_p4_t02_b2_common_character_compact_receipt.json"

CANDIDATE = "CAND-V22-B2-COMMON-CHARACTER-DESCENT-INDEPENDENT-VARIATION-LAW-V1"
PACKET = "PKT-V22-P4T02-B2-COMMON-CHARACTER-DESCENT-INDEPENDENT-VARIATION-FORMALIZATION-V1"
RESULT = "constructed_candidate_pending_smuggling_audit"
NEXT_ROLE = "smuggling-auditor@0.2.0"
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
}

EXPECTED_HASHES = {
    "child_phys_math_p4_t02_b2_common_character_independent_variation.yaml": "369c17b6204997b01301e5b43fde17ea8d2795bd5c74c096d73b7785d603f669",
    "child_phys_phil_p4_t02_b2_common_character_independent_variation.yaml": "e158ed1cdc95d21924693c9631ee844f4d33c5f1388ea850821a80e6c3590ece",
    "parent_conflict_review_p4_t02_b2_common_character_independent_variation.yaml": "fd4463b1323c256641df56b7338f87b891f67fb87827216362d5725b0af89e7a",
    "parent_fusion_notes_p4_t02_b2_common_character_independent_variation.md": "966fba0889677cc1d8ad2c6aa49af42eba793a0a9f94455b3b58170f7857f862",
    "v22_p4_t02_b2_common_character_candidate_disposition_v1.yaml": "1fa1e74be8c983aae376278df79c71748d97aa2e8713e0df3052b3235f7a73e0",
    "v22_p4_t02_b2_common_character_descent_spec_v1.yaml": "70f25b557642d9bc4d71b92b9b05cdca045c670df775089058f4b444bfa1a4a2",
    "v22_p4_t02_b2_independent_variation_law_v1.yaml": "bb30f36984d97f084a914b07253e872935f8f05190779a5c76a095d03235c774",
    "v22_p4_t02_b2_source_provenance_separation_v1.yaml": "8692478fa808e39bbc580ff395d34c9162786a1e67000d7bbddba54fe72e04f0",
    "v22_p4_t02_b2_common_character_model.py": "ff5a0d9e1973e8f5bc9a0db48e9b11afb25e17a8bc35b0d01a19097c9b8c67c8",
    "v22_p4_t02_b2_common_character_independent_variation_law_v1.tex": "6c81af99ff98b315b3867deed2658ec8123386b7d2f9fbc9517ed80b0c1f695f",
    "v22_p4_t02_b2_common_character_latex_compile_receipt.json": "9ccfff794ddad00b6d356280e41925446e2d5d2c340195e25eb51fc31d42dafb",
}

PREDECESSOR_HASHES = {
    "research_control/handoffs/handoff-1006.yaml": "16bc80b7fa359cd88913de6c9828a5681917e66cdaa2316a6c2690827493a347",
    "research_control/tasks/RT-20260810-009/artifacts/v22_p4_t02_b2_selected_future_packet_v1.yaml": "18518be4ca42afb94954d362c75117f3bd27bc24dfadbb96a532644b00828941",
    "research_control/tasks/RT-20260810-009/artifacts/v22_p4_t02_b2_post_refuter_route_selection_v1.tex": "f65be2c4890d3595a4e60dc9515cf244faa7c77c2cc52998285d1d0d6c0292da",
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
        for item in value:
            if isinstance(item, dict) and item.get("plan_task_id") == "P4-T02":
                return item
            found = find_p4_t02(item)
            if found is not None:
                return found
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
            TASK / "DDR-20260810-010.md",
            TASK / "documentation_impact.yaml",
            TASK / "jobs/AJ-RT-20260810-010-001.yaml",
            TASK / "jobs/completions/AJC-AJ-RT-20260810-010-001.yaml",
            TASK / "roles/ontology-formalizer@0.2.0--RT-20260810-010.yaml",
            ROOT / "research_control/handoffs/handoff-1007.yaml",
            ROOT / "research_control/handoffs/handoff-1007.md",
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
        ROOT / "research_control/handoffs/handoff-1007.yaml",
        ROOT / "research_control/design/v22_recommendation_backlog.yaml",
    ]
    parsed: dict[Path, Any] = {}
    for path in yaml_paths:
        if not path.is_file():
            continue
        try:
            parsed[path] = load_yaml(path)
            check(
                f"yaml_unique:{path.relative_to(ROOT)}",
                True,
                "YAML parses with unique keys",
            )
        except Exception as exc:
            check(f"yaml_unique:{path.relative_to(ROOT)}", False, str(exc))

    program_path = ROOT / "research_control/program_state.yaml"
    try:
        program = yaml.safe_load(program_path.read_text(encoding="utf-8"))
        check("yaml_parse:program_state", isinstance(program, dict), "program state parses")
    except Exception as exc:
        program = {}
        check("yaml_parse:program_state", False, str(exc))

    model_run = subprocess.run(
        [sys.executable, str(ART / "v22_p4_t02_b2_common_character_model.py"), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        model = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model = {}
    model_checks = model.get("checks", {})
    check("model_exit", model_run.returncode == 0, model_run.stderr or "model exits zero")
    check("model_status", model.get("status") == "PASS", "model reports PASS")
    check(
        "model_exact_checks",
        len(model_checks) == 19 and all(model_checks.values()),
        "all nineteen exact finite-model checks pass",
    )
    check(
        "model_anchors",
        all(values[0] == 0 for values in model.get("cochain_exponents", {}).values())
        and model_checks.get("sector_intertwiner_anchors_fixed") is True,
        "all declared sector cochains satisfy a_s(0)=1",
    )
    check(
        "model_variation",
        model.get("balance_rank") == 2
        and model.get("kernel_dimension") == 2
        and model.get("variation_quotient_dimension") == 1
        and model.get("cycle_character_log_variation_rate") == 6
        and model.get("e01_sector_rate_vector") == [4, -2, 8],
        "rank, quotient, holonomy, and non-diagonal rates match the exact witness",
    )
    check(
        "model_claim_blocks",
        model.get("claim_blocks")
        and not any(model["claim_blocks"].values()),
        "all model-level promotion claims remain false",
    )

    descent = parsed.get(ART / "v22_p4_t02_b2_common_character_descent_spec_v1.yaml", {})
    variation = parsed.get(ART / "v22_p4_t02_b2_independent_variation_law_v1.yaml", {})
    provenance = parsed.get(ART / "v22_p4_t02_b2_source_provenance_separation_v1.yaml", {})
    disposition = parsed.get(ART / "v22_p4_t02_b2_common_character_candidate_disposition_v1.yaml", {})
    conflict = parsed.get(ART / "parent_conflict_review_p4_t02_b2_common_character_independent_variation.yaml", {})
    child_math = parsed.get(ART / "child_phys_math_p4_t02_b2_common_character_independent_variation.yaml", {})
    child_phil = parsed.get(ART / "child_phys_phil_p4_t02_b2_common_character_independent_variation.yaml", {})

    check(
        "candidate_identity",
        descent.get("candidate_id") == CANDIDATE
        and descent.get("packet_id") == PACKET
        and disposition.get("candidate_id") == CANDIDATE
        and disposition.get("packet_id") == PACKET,
        "candidate and packet identities are exact",
    )
    check(
        "decisive_result",
        descent.get("status") == RESULT and disposition.get("decisive_result") == RESULT,
        "the allowed constructed-candidate result is exact",
    )
    check(
        "obligation_cardinality",
        len(disposition.get("proof_obligation_results", [])) == 14
        and {row.get("obligation_id") for row in disposition.get("proof_obligation_results", [])}
        == {f"PO-{number:02d}-{suffix}" for number, suffix in [
            (1, "EXACT-TYPING"), (2, "COMMON-COCYCLE"), (3, "REDUCTION-CRITERION"),
            (4, "NO-SHARED-TAU-REPLAY"), (5, "INDEPENDENT-VARIATION-PROVENANCE"),
            (6, "NONVACUITY"), (7, "DESCENT-VARIATION-INDEPENDENCE"),
            (8, "SOURCE-NATURALITY"), (9, "FINITE-VARIATION-INTEGRABILITY"),
            (10, "TOTAL-FAIL-CLOSED-OUTPUT"), (11, "SOURCE-PURITY"),
            (12, "MATERIAL-DISTINCTNESS"), (13, "FINITE-SECTOR-SCOPE"),
            (14, "CLAIM-BLOCKS"),
        ]},
        "all fourteen exact packet obligations are present",
    )
    check(
        "failure_branch_cardinality",
        len(disposition.get("failure_branch_results", [])) == 11
        and {row.get("branch_id", "")[:5] for row in disposition.get("failure_branch_results", [])}
        == {f"FB-{number:02d}" for number in range(1, 12)},
        "all eleven failure branches are present",
    )
    check(
        "anchor_torsor_resolution",
        "sector_intertwiner_torsor_theorem" in descent.get("cochain_reduction_and_gauge_classification", {})
        and descent.get("failure_branch_status", {}).get("FB-04-NONUNIQUENESS", "").startswith("NOT_TRIGGERED")
        and next(
            (row.get("status", "") for row in disposition.get("failure_branch_results", []) if row.get("branch_id") == "FB-08-PROVENANCE-DEPENDENCE"),
            "",
        ) == "NOT_CLEARED_PENDING_SMUGGLING_AUDIT",
        "FB-04 is resolved only for fixed anchors and FB-08 remains uncleared",
    )
    check(
        "variation_contract",
        variation.get("status") == RESULT
        and variation.get("admissible_variation_quotient", {}).get("dimension") == 1
        and variation.get("finite_admissible_flow", {}).get("base_positive_interval") == "-2<t<1"
        and variation.get("exact_model_receipt", {}).get("exact_check_count") == 19,
        "the independent nonzero quotient and finite positive interval are exact",
    )
    check(
        "provenance_boundary",
        provenance.get("status") == "internal_source_provenance_pass_pending_separate_smuggling_audit"
        and provenance.get("preload_neutrality_audit", {}).get("preload_cost")
        == "high_but_explicit_including_normalization_anchor"
        and provenance.get("authority_limits", {}).get("internal_provenance_scan_is_independent_smuggling_audit") is False,
        "internal provenance is explicit but not mislabelled as the independent audit",
    )

    for source in provenance.get("source_hashes", []):
        path = ROOT / source.get("path", "")
        check(
            f"source_hash:{source.get('path', '')}",
            path.is_file() and sha256(path) == source.get("sha256"),
            "provenance source hash matches",
        )

    check(
        "children_consensus",
        child_math.get("decisive_result") == RESULT
        and child_phil.get("decisive_disposition", {}).get("decisive_result") == RESULT
        and child_math.get("conflict_resolution_revision", {}).get("final_disposition", {}).get("conflict_resolved") is True
        and child_phil.get("conflict_resolution_revision", {}).get("blocking_conflict_remains") is False,
        "both children converge after one conflict round",
    )
    check(
        "conflict_resolution",
        conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_count") == 0
        and conflict.get("resolution_round_count") == 1
        and conflict.get("unresolved_conflicts") == [],
        "no unresolved blocking parent-child conflict remains",
    )
    check(
        "distance_matrix",
        len(disposition.get("distance_to_gr_status", [])) == 14
        and {row.get("burden") for row in disposition.get("distance_to_gr_status", [])} == BURDENS
        and all(row.get("task_delta") == "none" for row in disposition.get("distance_to_gr_status", []))
        and disposition.get("distance_to_gr_delta", {}).get("changed") is False,
        "expanded fourteen-row Distance-to-GR matrix records no delta",
    )
    check(
        "freezes",
        set(disposition.get("freeze_criteria_status", {}).get("preserved_freeze_labels", [])) == FREEZES
        and disposition.get("freeze_criteria_status", {}).get("global_freeze_applied") is False,
        "both inherited freezes are preserved without global freeze",
    )
    next_route = disposition.get("selected_next_route", {})
    check(
        "next_packet_unexecuted",
        next_route.get("packet_type") == "source_extension_smuggling_audit"
        and next_route.get("role_family") == NEXT_ROLE
        and next_route.get("selected") is True
        and next_route.get("admitted_or_executed_in_rt010") is False,
        "exactly one later smuggling audit is selected but not executed",
    )

    tex = (ART / "v22_p4_t02_b2_common_character_independent_variation_law_v1.tex").read_text(encoding="utf-8")
    check(
        "tex_claims",
        "Anchored intertwiner torsor resolution" in tex
        and "constructed candidate pending separate smuggling audit" in tex
        and "a_s(0;x)=1" in tex
        and "Distance-to-GR" in tex,
        "manuscript contains the anchor theorem, disposition, and burden boundary",
    )
    receipt = json.loads((ART / "v22_p4_t02_b2_common_character_latex_compile_receipt.json").read_text(encoding="utf-8"))
    check(
        "latex_receipt",
        receipt.get("status") == "PASS"
        and receipt.get("source_sha256") == sha256(ART / "v22_p4_t02_b2_common_character_independent_variation_law_v1.tex")
        and receipt.get("undefined_references") == 0
        and receipt.get("overfull_boxes") == 0
        and receipt.get("underfull_boxes") == 0
        and receipt.get("visual_review", {}).get("result") == "PASS",
        "two-pass compile and all-page visual review pass",
    )
    check("no_task_pdf", not list(TASK.rglob("*.pdf")), "no PDF derivative is tracked in the task")

    task_record = parsed.get(TASK / "00_TASK.yaml", {})
    job_record = parsed.get(TASK / "jobs/AJ-RT-20260810-010-001.yaml", {})
    completion = parsed.get(TASK / "jobs/completions/AJC-AJ-RT-20260810-010-001.yaml", {})
    role = parsed.get(TASK / "roles/ontology-formalizer@0.2.0--RT-20260810-010.yaml", {})
    handoff = parsed.get(ROOT / "research_control/handoffs/handoff-1007.yaml", {})
    check(
        "control_completion",
        task_record.get("status") == "completed"
        and job_record.get("status") == "completed"
        and role.get("status") == "completed"
        and completion.get("status") == "completed"
        and completion.get("objective_result") == RESULT,
        "task, job, role, and completion records are terminalized",
    )
    check(
        "handoff",
        handoff.get("handoff_id") == "handoff-1007"
        and handoff.get("claim_boundary", {}).get("decisive_result") == RESULT
        and handoff.get("selected_next_route", {}).get("role_family") == NEXT_ROLE
        and handoff.get("selected_next_route", {}).get("executed") is False,
        "handoff selects the audit without executing it",
    )
    check(
        "program_state",
        program.get("active_task_id") == "RT-20260810-010"
        and program.get("active_job_id") == "AJ-RT-20260810-010-001"
        and program.get("active_handoff_id") == "handoff-1007",
        "program state points to the completed RT010 frontier",
    )

    backlog = parsed.get(ROOT / "research_control/design/v22_recommendation_backlog.yaml", {})
    p4_t02 = find_p4_t02(backlog) or {}
    check(
        "backlog",
        p4_t02.get("runtime_common_character_descent_independent_variation_formalization_executed") is True
        and p4_t02.get("runtime_common_character_descent_independent_variation_formalization_result") == RESULT
        and p4_t02.get("runtime_selected_next_role_family") == NEXT_ROLE,
        "P4-T02 runtime state records construction and the pending audit",
    )

    tex_row = csv_row(
        ROOT / "registries/TEX_SOURCE_REGISTRY.csv",
        "object_id",
        "TEX-V22-P4-T02-B2-COMMON-CHARACTER-INDEPENDENT-VARIATION-LAW-V1",
    )
    md_row = csv_row(
        ROOT / "registries/MARKDOWN_SOURCE_REGISTRY.csv",
        "object_id",
        "MD-V22-P4-T02-B2-PARENT-FUSION-COMMON-CHARACTER-INDEPENDENT-VARIATION-V1",
    )
    check("tex_registry", tex_row is not None, "canonical task-local TeX is registered")
    check("markdown_registry", md_row is not None, "parent fusion Markdown is registered")

    failed = [row for row in checks if row["status"] == "FAIL"]
    report = {
        "schema_id": "v22_p4_t02_b2_common_character_validation_v1",
        "task_id": "RT-20260810-010",
        "job_id": "AJ-RT-20260810-010-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "pass_count": len(checks) - len(failed),
        "fail_count": len(failed),
        "checks": checks,
        "authority": "operational_validation_only_not_source_purity_adoption_physical_truth_or_proof_promotion",
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_common_character_compact_receipt_v1",
        "task_id": "RT-20260810-010",
        "job_id": "AJ-RT-20260810-010-001",
        "status": report["status"],
        "decisive_result": RESULT,
        "candidate_id": CANDIDATE,
        "model_check_count": len(model_checks),
        "proof_obligation_count": len(disposition.get("proof_obligation_results", [])),
        "failure_branch_count": len(disposition.get("failure_branch_results", [])),
        "distance_to_gr_row_count": len(disposition.get("distance_to_gr_status", [])),
        "child_conflict_resolved": conflict.get("blocking_conflict_count") == 0,
        "source_purity_audit_completed": False,
        "distance_to_gr_changed": False,
        "next_role": NEXT_ROLE,
        "next_packet_executed": False,
        "authority": "compact_control_receipt_only",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

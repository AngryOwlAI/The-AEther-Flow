#!/usr/bin/env python3
"""Focused validator for the RT-20260810-008 repaired-quotient stress.

Passing this validator is operational evidence only.  It is not theorem,
adoption, Gate, benchmark, proof, or physics-promotion authority.
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
TASK = ROOT / "research_control/tasks/RT-20260810-008"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_common_envelope_refuter_stress_validation.json"
COMPACT = ART / "v22_p4_t02_b2_common_envelope_refuter_stress_compact_receipt.json"

EXPECTED_HASHES = {
    "child_phys_math_p4_t02_b2_common_envelope_refuter_stress.yaml": "6a86c331a523b7120678a5e78ec99d1507c407716007c7450c93e614af4c8666",
    "child_phys_phil_p4_t02_b2_common_envelope_refuter_stress.yaml": "7dab016e65166f15398333b7b715f90bc081ebcb043b5387daf066878517e122",
    "parent_conflict_review_p4_t02_b2_common_envelope_refuter_stress.yaml": "ac3eca8803026d697cbb44dcf26725ce8fbb30e23b8d15f96d4e8d703a623606",
    "parent_fusion_notes_p4_t02_b2_common_envelope_refuter_stress.md": "efebdd847b917ceb09f4b32332506abb7a15c577c6e93a3412baa40193146d74",
    "v22_p4_t02_b2_common_envelope_refuter_obstruction_v1.yaml": "3128720ae129546a42d40c05221ccef12ee2232daf9459f0ed18fd0ffcb188e9",
    "v22_p4_t02_b2_common_envelope_refuter_stress_control_matrix_v1.yaml": "442f767c2ad41e049210a143bd9f3881b0ef7c19c84f289a7ab315adb9dc54e2",
    "v22_p4_t02_b2_common_envelope_refuter_stress_latex_compile_receipt.json": "37c2bbf2dd8dd50e11165fa98ced092b3a59cc2f4820954704b9e309774fbe42",
    "v22_p4_t02_b2_common_envelope_refuter_stress_model.py": "71239f92ae5847c3c1d9b021e866f4db7095102b3dbaa40b028effb0f621a26e",
    "v22_p4_t02_b2_common_envelope_refuter_stress_v1.tex": "7f860d25cdb6e0578acaf59e70cc745388a2777dbcd2749d3736d6c6e017dea2",
    "v22_p4_t02_b2_common_envelope_refuter_stress_verdict_v1.yaml": "02cdfa7d5c5e4a0198c88b8c3b76a2770e483947dcce49fd4c4beea38052370c",
}

PREDECESSOR_HASHES = {
    "research_control/handoffs/handoff-1004.yaml": "5d357cb6254d91c0437c1988f80de215580c8f4e2b0b8979548a86d550049539",
    "research_control/tasks/RT-20260810-007/artifacts/v22_p4_t02_b2_common_envelope_quotient_rank_repair_v1.tex": "2882fea5872b730d403855ca7b6f06d16526739d1c4ac6a7fb62e3816ce4c052",
    "research_control/tasks/RT-20260810-007/artifacts/v22_p4_t02_b2_common_envelope_quotient_rank_repair_record_v1.yaml": "fc7446f179fa348cd9cd077b79996f04e91ad872fd74d91fd9062d3680b21aa0",
    "research_control/tasks/RT-20260810-007/artifacts/v22_p4_t02_b2_typed_response_image_repair_v1.yaml": "191dedc37210e2d7533b1adbe6f52b07378e4694dc509817c18bd6bc02de1538",
    "research_control/tasks/RT-20260810-007/artifacts/v22_p4_t02_b2_common_envelope_quotient_rank_repair_control_matrix_v1.yaml": "adf7bc2a6170899f4fe359e8dc4fae043662697069620efd90c964f6b9f1353b",
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
            TASK / "DDR-20260810-008.md",
            TASK / "documentation_impact.yaml",
            TASK / "jobs/AJ-RT-20260810-008-001.yaml",
            TASK / "jobs/completions/AJC-AJ-RT-20260810-008-001.yaml",
            TASK / "roles/refuter@0.2.0--RT-20260810-008.yaml",
            ROOT / "research_control/handoffs/handoff-1005.yaml",
            ROOT / "research_control/handoffs/handoff-1005.md",
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
        ROOT / "research_control/handoffs/handoff-1005.yaml",
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
        check(
            "yaml_parse:research_control/program_state.yaml",
            True,
            "legacy program state parses",
        )
    except Exception as exc:  # pragma: no cover - diagnostic branch
        check("yaml_parse:research_control/program_state.yaml", False, str(exc))

    model_run = subprocess.run(
        [
            sys.executable,
            str(ART / "v22_p4_t02_b2_common_envelope_refuter_stress_model.py"),
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
    check("model_exit", model_run.returncode == 0, model_run.stderr or "model exits zero")
    check("model_status", model.get("status") == "PASS", "model status is PASS")
    model_checks = model.get("checks", {})
    check(
        "model_checks",
        len(model_checks) == 11 and all(model_checks.values()),
        "all eleven exact model checks pass",
    )
    check(
        "model_result",
        model.get("decisive_result_supported") == "scoped_obstruction",
        "model supports exactly scoped_obstruction",
    )
    fixed = model.get("fixed_candidate", {})
    finite = model.get("finite_variation", {})
    descent = model.get("transition_descent", {})
    check(
        "model_fixed_candidate",
        fixed.get("rank") == 2
        and fixed.get("kernel_dimension") == 2
        and fixed.get("sign_orbit_count") == 6,
        "fixed candidate retains rank two kernel dimension two and six sign cells",
    )
    check(
        "model_countermodel",
        finite.get("perturbed_rank") == 3
        and finite.get("perturbed_sign_orbit_count") == 8
        and finite.get("common_positivity_survives") is True
        and finite.get("midpoint_family_codimension") == 4
        and finite.get("h0_normalized_midpoint_codimension") == 3,
        "arbitrarily small countermodel and both codimensions are exact",
    )
    check(
        "model_descent",
        descent.get("independent_positive_factors_preserve_Q_sign") is True
        and descent.get("independent_positive_factors_preserve_Q_ray") is False
        and descent.get("common_transition_cocycle_required") is True,
        "sign invariance is separated from positive-ray descent",
    )
    check(
        "model_authority",
        all(value is False for value in model.get("authority_limits", {}).values()),
        "model grants no physical or protected authority",
    )

    verdict = parsed.get(ART / "v22_p4_t02_b2_common_envelope_refuter_stress_verdict_v1.yaml", {})
    check(
        "verdict_decisive",
        verdict.get("decisive_result") == "scoped_obstruction"
        and verdict.get("no_fog_check") is True,
        "verdict is exactly decisive and non-fog",
    )
    check(
        "verdict_fixed",
        verdict.get("fixed_candidate_results_preserved", {}).get("response_rank") == 2
        and verdict.get("fixed_candidate_results_preserved", {}).get("realized_nonzero_sign_orbits") == 6,
        "verdict preserves fixed-candidate scope",
    )
    check(
        "verdict_payload",
        len(verdict.get("new_mathematical_payload", [])) == 5,
        "five new mathematical payloads are recorded",
    )
    check(
        "verdict_distance",
        verdict.get("distance_to_gr_delta", {}).get("changed") is False
        and len(verdict.get("distance_to_gr_status", [])) == 14,
        "Distance-to-GR remains unchanged with all fourteen burdens",
    )

    obstruction = parsed.get(ART / "v22_p4_t02_b2_common_envelope_refuter_obstruction_v1.yaml", {})
    record = obstruction.get("refuter_obstruction_record", {})
    check(
        "obstruction_schema",
        obstruction.get("schema_id") == "refuter_obstruction_schema_v1"
        and obstruction.get("result_classification") == "scoped_obstruction",
        "obstruction uses the required schema and scope",
    )
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
        "obstruction_fields",
        required_obstruction_fields.issubset(record),
        "all required Refuter obstruction fields are present",
    )
    check(
        "obstruction_limits",
        record.get("minimal_countermodel_available") is True
        and record.get("countermodel_scope") == "source_extension_candidate"
        and record.get("global_no_go_claim_authorized") is False
        and record.get("future_source_extension_impossibility_authorized") is False,
        "countermodel scope and protected limits are exact",
    )

    matrix = parsed.get(ART / "v22_p4_t02_b2_common_envelope_refuter_stress_control_matrix_v1.yaml", {})
    branches = matrix.get("stress_branches", [])
    check(
        "matrix_branches",
        [row.get("branch_id") for row in branches]
        == ["collapse", "nonuniqueness", "inverse_defect", "cocycle_defect", "finite_variation_fragility"],
        "all five required stress branches occur exactly once",
    )
    check(
        "matrix_result",
        matrix.get("decisive_classification") == "scoped_obstruction"
        and matrix.get("next_unexecuted_role") == "theoretical-continuation-selector@0.1.0",
        "matrix selects one unexecuted theoretical selector",
    )

    conflict = parsed.get(ART / "parent_conflict_review_p4_t02_b2_common_envelope_refuter_stress.yaml", {})
    check(
        "conflict_resolved",
        conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_detected") is False
        and conflict.get("unresolved_conflicts") == [],
        "parent conflict review is resolved",
    )
    check(
        "children_agree",
        len(conflict.get("child_inputs", [])) == 2
        and all(row.get("result_classification") == "scoped_obstruction" for row in conflict.get("child_inputs", [])),
        "both independent children return scoped_obstruction",
    )

    completion_path = TASK / "jobs/completions/AJC-AJ-RT-20260810-008-001.yaml"
    completion = parsed.get(completion_path, {})
    check(
        "completion_status",
        completion.get("status") == "completed"
        and completion.get("refuter_result", {}).get("decisive_classification") == "scoped_obstruction",
        "completion is terminal and decisive",
    )
    check(
        "completion_contract",
        completion.get("physics_progress_status", {}).get("status") == "precise_obstruction_found"
        and completion.get("distance_to_gr_delta", {}).get("changed") is False
        and len(completion.get("mathematical_payload_manifest", [])) == 5
        and completion.get("obstruction_record", {}).get("present") is True,
        "mathematical decisiveness contract is complete",
    )
    burden_rows = completion.get("distance_to_gr_status", [])
    check(
        "completion_burdens",
        len(burden_rows) == 14
        and {row.get("burden") for row in burden_rows} == BURDENS,
        "all fourteen Distance-to-GR burdens occur exactly once",
    )
    freeze = completion.get("freeze_criteria_status", {})
    check(
        "completion_freeze",
        freeze.get("freeze_decision") == "not_frozen"
        and freeze.get("active_freeze_label")
        == "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS"
        and freeze.get("global_theory_rejection") is False,
        "candidate-scope local freeze is exact",
    )
    authority = completion.get("authorization_layers", {})
    boolean_authority = [value for value in authority.values() if isinstance(value, bool)]
    check(
        "completion_authority",
        boolean_authority
        and all(value is False for value in boolean_authority)
        and authority.get("protected_scoped_gate_review_authority_source_path") == ""
        and authority.get("downstream_physics_promotion_authority_source_path") == ""
        and authority.get("benchmark_promotion_authority_source_path") == ""
        and authority.get("completed_derivation_authority_source_path") == "",
        "completion grants no protected authority",
    )

    handoff = parsed.get(ROOT / "research_control/handoffs/handoff-1005.yaml", {})
    check(
        "handoff_binding",
        handoff.get("task_id") == "RT-20260810-008"
        and handoff.get("completion_sha256") == sha256(completion_path)
        and handoff.get("selected_next_route", {}).get("role_family")
        == "theoretical-continuation-selector@0.1.0"
        and handoff.get("selected_next_route", {}).get("executed") is False,
        "handoff binds completion and one unexecuted selector",
    )

    program = parsed.get(ROOT / "research_control/program_state.yaml", {})
    current = program.get("v22_p4_t02_b2_common_envelope_refuter_stress", {})
    check(
        "program_state",
        program.get("active_task_id") == "RT-20260810-008"
        and program.get("latest_handoff_id") == "handoff-1005"
        and current.get("decisive_result") == "scoped_obstruction"
        and current.get("refuter_stress_executed") is True
        and current.get("theoretical_continuation_selector_executed") is False,
        "program state reflects the exact post-stress frontier",
    )

    backlog = parsed.get(ROOT / "research_control/design/v22_recommendation_backlog.yaml", {})
    p4_t02 = find_p4_t02(backlog) or {}
    check(
        "backlog_state",
        p4_t02.get("implementation_status")
        == "b2_common_envelope_refuter_stress_scoped_obstruction_selector_selected_checkpoint_pending"
        and p4_t02.get("runtime_refuter_stress_executed") is True
        and p4_t02.get("runtime_refuter_stress_result") == "scoped_obstruction"
        and p4_t02.get("runtime_post_refuter_theoretical_continuation_selector_executed") is False,
        "V22 backlog records stress completion freeze and selector boundary",
    )

    registry_expectations = [
        ("RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260810-008", "status", "completed"),
        ("DIRECTOR_DECISION_REGISTRY.csv", "decision_id", "DDR-20260810-008", "status", "completed"),
        ("AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260810-008-001", "status", "completed"),
        ("ROLE_EXECUTION_REGISTRY.csv", "execution_role_ref", "refuter@0.2.0--RT-20260810-008", "validation_status", "PASS_PRECHECKPOINT_STAGING_REQUIRED"),
        ("CLAIM_BOUNDARY_REGISTRY.csv", "claim_boundary_id", "CB-V22-P4-T02-B2-COMMON-ENVELOPE-REFUTER-STRESS-001", "status", "completed"),
        ("TEX_SOURCE_REGISTRY.csv", "object_id", "TEX-V22-P4-T02-B2-COMMON-ENVELOPE-REFUTER-STRESS-V1", "source_hash", EXPECTED_HASHES["v22_p4_t02_b2_common_envelope_refuter_stress_v1.tex"]),
        ("MARKDOWN_SOURCE_REGISTRY.csv", "object_id", "MD-V22-P4-T02-B2-PARENT-FUSION-COMMON-ENVELOPE-REFUTER-STRESS-V1", "source_hash", EXPECTED_HASHES["parent_fusion_notes_p4_t02_b2_common_envelope_refuter_stress.md"]),
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
        "schema_id": "v22_p4_t02_b2_common_envelope_refuter_stress_validation_v1",
        "task_id": "RT-20260810-008",
        "job_id": "AJ-RT-20260810-008-001",
        "status": result_status,
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "failure_count": sum(row["status"] == "FAIL" for row in checks),
        "checks": checks,
        "authority": "operational_validation_only_not_proof_or_physics_promotion",
    }
    compact = {
        "schema_id": "v22_p4_t02_b2_common_envelope_refuter_stress_compact_receipt_v1",
        "task_id": "RT-20260810-008",
        "job_id": "AJ-RT-20260810-008-001",
        "status": result_status,
        "decisive_result": "scoped_obstruction",
        "obstruction_id": "OB-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS-001",
        "freeze_label": "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
        "next_role": "theoretical-continuation-selector@0.1.0",
        "next_role_executed": False,
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

#!/usr/bin/env python3
"""Focused validator for the RT-20260810-007 quotient-rank repair.

This validator checks exact task-local mathematics, parent-child fusion,
control bindings, registrations, and authority limits.  Passing it is
operational evidence only; it is not proof or physics-promotion authority.
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
TASK = ROOT / "research_control/tasks/RT-20260810-007"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_common_envelope_quotient_rank_repair_validation.json"
COMPACT = ART / "v22_p4_t02_b2_common_envelope_quotient_rank_repair_compact_receipt.json"

EXPECTED_HASHES = {
    "child_phys_math_p4_t02_b2_common_envelope_quotient_rank_repair.yaml": "bce3507a651a4d7c4cb0964f095cb7703223b5ec5d04204d4b0eef504556cc1e",
    "child_phys_phil_p4_t02_b2_common_envelope_quotient_rank_repair.yaml": "18d2df8cef30564d2c5dd3316dec2790a76a1f86208864f773c6ef52aa677844",
    "parent_conflict_review_p4_t02_b2_common_envelope_quotient_rank_repair.yaml": "6e683b33edd91a085a2f9d80d797100035d3a87ed3f08e13e0b9f6aeadc3dce2",
    "parent_fusion_notes_p4_t02_b2_common_envelope_quotient_rank_repair.md": "7235d7837882917a383d298ba6f1fd0d197db8477eb0d5f2b854376ce0cf7c96",
    "v22_p4_t02_b2_common_envelope_quotient_rank_repair_control_matrix_v1.yaml": "adf7bc2a6170899f4fe359e8dc4fae043662697069620efd90c964f6b9f1353b",
    "v22_p4_t02_b2_common_envelope_quotient_rank_repair_latex_compile_receipt.json": "561d9808e23478c94cd503d3726ffa01d8aba14fff32992492275937e21d2f83",
    "v22_p4_t02_b2_common_envelope_quotient_rank_repair_model.py": "4d957bd3aa531255435f26c9bcd478b86ff37a81bc9d409fe54c215a04e45cbc",
    "v22_p4_t02_b2_common_envelope_quotient_rank_repair_record_v1.yaml": "fc7446f179fa348cd9cd077b79996f04e91ad872fd74d91fd9062d3680b21aa0",
    "v22_p4_t02_b2_common_envelope_quotient_rank_repair_v1.tex": "2882fea5872b730d403855ca7b6f06d16526739d1c4ac6a7fb62e3816ce4c052",
    "v22_p4_t02_b2_typed_response_image_repair_v1.yaml": "191dedc37210e2d7533b1adbe6f52b07378e4694dc509817c18bd6bc02de1538",
}

EXPECTED_CONTROL_HASHES = {
    "00_TASK.yaml": "e3b3ad950c8b569fdaf75db6a3640adc25834b3652b086ac2816d6018f1d9e0b",
    "DDR-20260810-007.md": "6221c3f3745cb6d0d2c012cc04887bc53b275fed06b3b9ec1c2d5794a8744181",
    "documentation_impact.yaml": "88dbecbdc6a4a8e1f399baf5028555154bc87f14c6ad56247fc805162361077e",
    "jobs/AJ-RT-20260810-007-001.yaml": "53e13cac278bd7a261098a5198af5f101bb6acceb0a5fcaf02ed3c212eaba9d3",
    "jobs/completions/AJC-AJ-RT-20260810-007-001.yaml": "19353a63e703b40c01d2171852371f0c36ca922169a27910f722e432419d4396",
    "roles/candidate-constructor@0.2.0--RT-20260810-007.yaml": "22433cd5c366fe18f4110ee56dadb0d1785a8e778d7acc8d72d6fb5120950c7e",
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


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def find_p4_t02(backlog: Any) -> dict[str, Any] | None:
    if isinstance(backlog, list):
        return next(
            (row for row in backlog if isinstance(row, dict) and row.get("plan_task_id") == "P4-T02"),
            None,
        )
    if isinstance(backlog, dict):
        for value in backlog.values():
            found = find_p4_t02(value)
            if found:
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
    required.extend(TASK / name for name in EXPECTED_CONTROL_HASHES)
    required.extend(
        [
            ROOT / "research_control/handoffs/handoff-1004.yaml",
            ROOT / "research_control/handoffs/handoff-1004.md",
            ROOT / "research_control/program_state.yaml",
            ROOT / "research_control/design/v22_recommendation_backlog.yaml",
        ]
    )
    for path in required:
        check(
            f"exists:{path.relative_to(ROOT)}",
            path.is_file(),
            "required tracked artifact exists",
        )
    for name, expected in EXPECTED_HASHES.items():
        path = ART / name
        check(
            f"hash:{name}",
            path.is_file() and sha256(path) == expected,
            f"expected SHA-256 {expected}",
        )
    for name, expected in EXPECTED_CONTROL_HASHES.items():
        path = TASK / name
        check(
            f"control_hash:{name}",
            path.is_file() and sha256(path) == expected,
            f"expected SHA-256 {expected}",
        )

    yaml_paths = list(TASK.rglob("*.yaml")) + [
        ROOT / "research_control/handoffs/handoff-1004.yaml",
        ROOT / "research_control/design/v22_recommendation_backlog.yaml",
    ]
    parsed: dict[Path, Any] = {}
    for path in yaml_paths:
        try:
            parsed[path] = load_yaml(path)
            check(
                f"yaml_unique:{path.relative_to(ROOT)}",
                True,
                "YAML parses with unique mapping keys",
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
            str(ART / "v22_p4_t02_b2_common_envelope_quotient_rank_repair_model.py"),
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
    check(
        "model_checks",
        len(model.get("checks", {})) == 13 and all(model.get("checks", {}).values()),
        "all thirteen exact model checks pass",
    )
    check(
        "model_result",
        model.get("decisive_result_supported") == "constructed_candidate",
        "model supports constructed_candidate",
    )
    check(
        "model_image",
        model.get("response_image_equation") == "r_R+r_D=2*r_S",
        "exact image-plane relation",
    )
    check("model_rank", model.get("response_rank") == 2, "response rank is two")
    check(
        "model_kernel",
        model.get("response_kernel") == "ann(span{u,z})"
        and model.get("response_kernel_dimension") == 2,
        "kernel and dimension are exact",
    )
    check(
        "model_projective",
        model.get("positive_projective_image_dimension") == 1
        and "sigma" in model.get("projective_coordinate", ""),
        "one continuous coordinate plus the discrete sheet",
    )
    check(
        "model_sign_cells",
        len(model.get("realized_nonzero_sign_orbits", [])) == 6
        and len(model.get("excluded_nonzero_sign_orbits", [])) == 2,
        "six sign cells realized and two alternating cells excluded",
    )
    counter = model.get("rank_three_unstructured_countercontrol", {})
    check(
        "model_rank_three_control",
        counter.get("rank") == 3
        and counter.get("realized_nonzero_sign_orbit_count") == 8,
        "unstructured countercontrol has rank three and eight sign cells",
    )
    check(
        "model_authority_false",
        all(value is False for value in model.get("authority_limits", {}).values()),
        "model grants no protected or physical authority",
    )

    repair = parsed.get(
        ART / "v22_p4_t02_b2_common_envelope_quotient_rank_repair_record_v1.yaml", {}
    )
    image = parsed.get(ART / "v22_p4_t02_b2_typed_response_image_repair_v1.yaml", {})
    matrix = parsed.get(
        ART / "v22_p4_t02_b2_common_envelope_quotient_rank_repair_control_matrix_v1.yaml", {}
    )
    check(
        "repair_decisive",
        repair.get("decisive_result") == "constructed_candidate"
        and repair.get("no_fog_check") is True,
        "repair record is decisive",
    )
    theorem = repair.get("response_image_theorem", {})
    check(
        "repair_theorem",
        theorem.get("rank") == 2
        and theorem.get("kernel_dimension") == 2
        and "r_R+r_D=2r_S" in theorem.get("image", ""),
        "repair theorem binds image rank and kernel",
    )
    projective = repair.get("positive_projective_image", {})
    check(
        "repair_projective",
        projective.get("continuous_dimension") == 1
        and projective.get("sheet_count") == 2
        and "sigma" in projective.get("normalized_ray", ""),
        "repair record binds the two-sheet atlas",
    )
    signs = repair.get("nonzero_sign_image", {})
    check(
        "repair_signs",
        signs.get("realized_orbit_count") == 6
        and signs.get("excluded_ordered_orbits") == ["-+-", "+-+"],
        "repair record binds all sign cells",
    )
    retained = repair.get("retained_conditional_results", {})
    check(
        "repair_preimages",
        len(retained.get("positive_preimage_identities", [])) == 2,
        "both positive-preimage identities survive",
    )
    check(
        "repair_next",
        repair.get("candidate_constructor_result", {}).get("next_required_packet")
        == "source_extension_refuter_stress"
        and repair.get("candidate_constructor_result", {}).get("full_refuter_stress_executed")
        is False,
        "fresh Refuter stress is selected but unexecuted",
    )

    exact_map = image.get("exact_map", {})
    ray = image.get("positive_ray_layer", {})
    check(
        "typed_map",
        exact_map.get("map_rank") == 2
        and exact_map.get("kernel_dimension") == 2
        and exact_map.get("image_equation") == "r_R+r_D=2r_S",
        "typed map is exact",
    )
    check(
        "typed_ray",
        ray.get("continuous_dimension") == 1
        and ray.get("sheet_count") == 2
        and ray.get("discrete_sheet") == "sigma=sgn(a)",
        "typed ray layer retains sigma and t",
    )
    check(
        "typed_closure",
        "outside D" in image.get("sign_orbit_layer", {}).get("closure_chart_note", ""),
        "a=0 closure rays are outside D",
    )
    check(
        "typed_robustness_scope",
        "rank three" in image.get("robustness_rank_identity_separation", {}).get("countercontrol", ""),
        "typed record separates common positivity from rank identity",
    )

    matrix_text = json.dumps(matrix, sort_keys=True)
    for token in [
        "r_R+r_D=2r_S",
        "ann(span{u,z})",
        "source_extension_refuter_stress",
        "physical",
        "six_of_eight_nonzero_ordered_orbits",
    ]:
        check(f"matrix_token:{token}", token in matrix_text, f"control matrix contains {token}")

    conflict = parsed.get(
        ART / "parent_conflict_review_p4_t02_b2_common_envelope_quotient_rank_repair.yaml", {}
    )
    check(
        "conflict_resolved",
        conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_count") == 0
        and conflict.get("unresolved_conflicts") == [],
        "parent conflict review is resolved",
    )
    check(
        "conflict_children",
        len(conflict.get("child_inputs", [])) == 2
        and all(row.get("execution_status") == "completed" for row in conflict.get("child_inputs", [])),
        "both child artifacts completed",
    )
    check(
        "conflict_sheet_resolution",
        conflict.get("pre_fusion_precision_resolution", {}).get("both_final_children_agree")
        is True,
        "both children agree on the retained positive-ray sheet",
    )
    decisions = conflict.get("parent_fusion_decisions", {})
    check(
        "conflict_result",
        decisions.get("result_type") == "constructed_candidate"
        and decisions.get("next_packet_type") == "source_extension_refuter_stress"
        and decisions.get("next_role_execution_authorized") is False,
        "parent selects one unexecuted stress packet",
    )

    tex_path = ART / "v22_p4_t02_b2_common_envelope_quotient_rank_repair_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.is_file() else ""
    for token in [
        "r_R+r_D=2r_S",
        "\\sigma=\\sgn(a)",
        "\\ann(\\operatorname{span}\\{u,z\\})",
        "six",
        "response rank can become three",
        "Non-conclusion.",
    ]:
        check(f"tex_token:{token}", token in tex, f"TeX contains {token}")

    compile_receipt = json.loads(
        (ART / "v22_p4_t02_b2_common_envelope_quotient_rank_repair_latex_compile_receipt.json").read_text(
            encoding="utf-8"
        )
    )
    check("compile_pass", compile_receipt.get("status") == "PASS", "Tectonic compile passed")
    check(
        "compile_source",
        compile_receipt.get("source_sha256")
        == EXPECTED_HASHES["v22_p4_t02_b2_common_envelope_quotient_rank_repair_v1.tex"],
        "compile receipt binds final TeX",
    )
    check(
        "compile_pages",
        compile_receipt.get("page_count") == 5
        and compile_receipt.get("rendered_page_count") == 5,
        "five pages compiled and rendered",
    )
    check(
        "visual_all_pages",
        compile_receipt.get("visually_inspected_pages") == [1, 2, 3, 4, 5]
        and compile_receipt.get("visual_inspection_status") == "PASS"
        and not any(compile_receipt.get("visual_findings", {}).values()),
        "all five pages pass visual inspection",
    )
    check(
        "pdf_non_authority",
        compile_receipt.get("tracked_pdf_created") is False
        and compile_receipt.get("proof_authority") is False,
        "temporary PDF is non-authoritative",
    )

    task = parsed.get(TASK / "00_TASK.yaml", {})
    job = parsed.get(TASK / "jobs/AJ-RT-20260810-007-001.yaml", {})
    role = parsed.get(
        TASK / "roles/candidate-constructor@0.2.0--RT-20260810-007.yaml", {}
    )
    completion = parsed.get(
        TASK / "jobs/completions/AJC-AJ-RT-20260810-007-001.yaml", {}
    )
    check(
        "task_closed",
        task.get("status") == "completed"
        and task.get("claim_boundary", {}).get("boundary_status") == "completed_closed",
        "task and claim boundary are closed",
    )
    check(
        "job_completed",
        job.get("status") == "completed"
        and job.get("role_decomposition", {}).get("subagent_count") == 2
        and all(row.get("status") == "completed" for row in job.get("role_decomposition", {}).get("children", [])),
        "one outer job and two child units completed",
    )
    check("role_expired", role.get("status") == "expired_completed", "role overlay expired")
    check(
        "completion_result",
        completion.get("objective_result")
        == "constructed_candidate_repaired_typed_response_image_two_sheet_projective_atlas",
        "completion records exact result",
    )
    check(
        "completion_payload",
        len(completion.get("new_mathematical_payload", [])) >= 6
        and len(completion.get("mathematical_payload_manifest", [])) >= 5,
        "completion carries substantive mathematical payload",
    )
    check(
        "completion_distance",
        completion.get("distance_to_gr_delta", {}).get("changed") is False
        and len(completion.get("distance_to_gr_status", [])) == 14,
        "Distance-to-GR is unchanged and fourteen burdens are reported",
    )
    check(
        "completion_candidate",
        completion.get("candidate_constructor_result", {}).get("result_type")
        == "constructed_candidate"
        and completion.get("candidate_constructor_result", {}).get("next_required_role")
        == "refuter",
        "Candidate Constructor returns the exact next role",
    )
    check(
        "completion_next",
        completion.get("selected_next_route", {}).get("selected_next_packet_type")
        == "source_extension_refuter_stress"
        and completion.get("selected_next_route", {}).get("executed") is False,
        "completion selects an unexecuted Refuter stress",
    )
    check(
        "completion_freeze",
        completion.get("freeze_criteria_status", {}).get("freeze_decision") == "not_frozen"
        and completion.get("freeze_criteria_status", {}).get("next_allowed_route") == "refuter",
        "repaired branch is not frozen",
    )
    check(
        "completion_authority",
        completion.get("authorization_layers", {}).get("downstream_physics_promotion_authorized")
        is False
        and completion.get("project_improvement_signals") == [],
        "completion grants no promotion and emits no system signal",
    )

    handoff_path = ROOT / "research_control/handoffs/handoff-1004.yaml"
    handoff = parsed.get(handoff_path, {})
    check(
        "handoff_hash",
        sha256(handoff_path) == "5d357cb6254d91c0437c1988f80de215580c8f4e2b0b8979548a86d550049539",
        "handoff hash is exact",
    )
    check(
        "handoff_completion",
        handoff.get("completion_sha256")
        == EXPECTED_CONTROL_HASHES["jobs/completions/AJC-AJ-RT-20260810-007-001.yaml"],
        "handoff binds completion",
    )
    check(
        "handoff_result",
        handoff.get("claim_boundary", {}).get("decisive_result") == "constructed_candidate"
        and handoff.get("claim_boundary", {}).get("positive_projective_sheet_count") == 2,
        "handoff binds the repaired result",
    )
    check(
        "handoff_next",
        handoff.get("required_next_packet", {}).get("executed") is False
        and handoff.get("selected_next_route", {}).get("role_family") == "refuter@0.2.0",
        "handoff selects a checkpoint-gated Refuter stress",
    )

    program = parsed.get(ROOT / "research_control/program_state.yaml", {})
    block = program.get("v22_p4_t02_b2_common_envelope_quotient_rank_repair", {})
    check(
        "program_active",
        program.get("active_task_id") == "RT-20260810-007"
        and program.get("latest_handoff_id") == "handoff-1004",
        "program state points to RT007 and handoff-1004",
    )
    check(
        "program_result",
        block.get("decisive_result") == "constructed_candidate"
        and block.get("positive_projective_sheet_count") == 2
        and block.get("selected_next_packet_type") == "source_extension_refuter_stress",
        "program state binds the result and next route",
    )

    backlog = parsed.get(ROOT / "research_control/design/v22_recommendation_backlog.yaml", {})
    p4_t02 = find_p4_t02(backlog)
    check("backlog_row", isinstance(p4_t02, dict), "P4-T02 backlog row exists")
    if isinstance(p4_t02, dict):
        check(
            "backlog_repair",
            p4_t02.get("runtime_common_envelope_quotient_rank_repair_executed") is True
            and p4_t02.get("runtime_common_envelope_quotient_rank_repair_result")
            == "constructed_candidate",
            "backlog records executed repair",
        )
        check(
            "backlog_atlas",
            p4_t02.get("runtime_positive_projective_image_dimension") == 1
            and p4_t02.get("runtime_positive_projective_sheet_count") == 2,
            "backlog records one continuous dimension and two sheets",
        )
        check(
            "backlog_next",
            p4_t02.get("runtime_refuter_stress_selected") is True
            and p4_t02.get("runtime_refuter_stress_executed") is False
            and p4_t02.get("runtime_selected_next_role_family") == "refuter@0.2.0",
            "backlog selects but does not execute Refuter stress",
        )

    registry_expectations = [
        ("AGENT_JOB_REGISTRY.csv", "job_id", "AJ-RT-20260810-007-001"),
        (
            "CLAIM_BOUNDARY_REGISTRY.csv",
            "claim_boundary_id",
            "CB-V22-P4-T02-B2-COMMON-ENVELOPE-QUOTIENT-RANK-REPAIR-001",
        ),
        ("DIRECTOR_DECISION_REGISTRY.csv", "decision_id", "DDR-20260810-007"),
        ("RESEARCH_TASK_REGISTRY.csv", "task_id", "RT-20260810-007"),
        (
            "ROLE_EXECUTION_REGISTRY.csv",
            "execution_role_ref",
            "candidate-constructor@0.2.0--RT-20260810-007",
        ),
        (
            "TEX_SOURCE_REGISTRY.csv",
            "object_id",
            "TEX-V22-P4-T02-B2-COMMON-ENVELOPE-QUOTIENT-RANK-REPAIR-V1",
        ),
        (
            "MARKDOWN_SOURCE_REGISTRY.csv",
            "object_id",
            "MD-V22-P4-T02-B2-PARENT-FUSION-COMMON-ENVELOPE-QUOTIENT-RANK-REPAIR-V1",
        ),
    ]
    for name, key, value in registry_expectations:
        matches = [row for row in csv_rows(ROOT / "registries" / name) if row.get(key) == value]
        check(f"registry:{name}", len(matches) == 1, f"{value} occurs exactly once")

    for path in list(TASK.rglob("*")) + [
        ROOT / "research_control/handoffs/handoff-1004.yaml",
        ROOT / "research_control/handoffs/handoff-1004.md",
    ]:
        if path.is_file() and path.suffix in {".yaml", ".md", ".tex", ".py", ".json"}:
            data = path.read_bytes()
            check(
                f"newline:{path.relative_to(ROOT)}",
                data.endswith(b"\n"),
                "file has a terminal newline",
            )

    failures = [item for item in checks if item["status"] != "PASS"]
    report = {
        "schema_id": "v22_p4_t02_b2_common_envelope_quotient_rank_repair_validation_v1",
        "task_id": "RT-20260810-007",
        "job_id": "AJ-RT-20260810-007-001",
        "status": "PASS" if not failures else "FAIL",
        "decisive_result": "constructed_candidate",
        "response_image_relation": "r_R+r_D=2*r_S",
        "response_rank": 2,
        "response_kernel_dimension": 2,
        "positive_projective_continuous_dimension": 1,
        "positive_projective_sheet_count": 2,
        "realized_nonzero_sign_orbit_count": 6,
        "check_count": len(checks),
        "failure_count": len(failures),
        "checks": checks,
        "authority": "operational_validation_only_not_proof_or_physics_promotion",
        "authority_limits": {
            "refuter_stress_executed": False,
            "adequacy_reevaluated": False,
            "b2_activated": False,
            "p4_t03_unlocked": False,
            "effective_metric_constructed": False,
            "distance_to_gr_changed": False,
            "proof_authority": False,
            "physics_promotion_authorized": False,
        },
    }
    if args.write_report:
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        compact = {
            "schema_id": "v22_p4_t02_b2_common_envelope_quotient_rank_repair_compact_receipt_v1",
            "task_id": "RT-20260810-007",
            "job_id": "AJ-RT-20260810-007-001",
            "status": report["status"],
            "decisive_result": "constructed_candidate",
            "response_rank": 2,
            "response_kernel_dimension": 2,
            "positive_projective_continuous_dimension": 1,
            "positive_projective_sheet_count": 2,
            "realized_nonzero_sign_orbit_count": 6,
            "check_count": len(checks),
            "failure_count": len(failures),
            "full_report_path": str(REPORT.relative_to(ROOT)),
            "full_report_sha256": sha256(REPORT),
            "refuter_stress_executed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        }
        COMPACT.write_text(
            json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    output = report if args.json else {
        "status": report["status"],
        "check_count": report["check_count"],
        "failure_count": report["failure_count"],
    }
    print(json.dumps(output, indent=2, sort_keys=True) if args.json else output)
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())

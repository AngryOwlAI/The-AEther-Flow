#!/usr/bin/env python3
"""Deterministic task-local validator for RT-20260727-007.

Operational validation only. PASS does not adopt ontology, establish physical
matter, or create proof or promotion authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[4]
TASK = REPO / "research_control/tasks/RT-20260727-007"
ART = TASK / "artifacts"
REPORT = ART / "source_matter_ontology_validation_v1.json"

EXPECTED_SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/tasks/RT-20260614-257/artifacts/"
    "286_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_"
    "MATTER_COUPLING_BRIDGE_TARGET_V1_FORMALIZATION.tex":
        "3d1c6dfb2ea543c8ea455ee2f3553e3cac76e3072902213ed07aff0db514605e",
    "research_control/tasks/RT-20260702-064/artifacts/"
    "source_certificate_operation_laws_v1.tex":
        "2ebc781bd82b4d39ab394255e5d3836d992625bdece8b8f912a8ab809669b986",
    "research_control/design/frontier_theorem_inventory.md":
        "fa7d97207315b49517e6e05bc3ae5b6bfcd0e335b669ba6a98371e55b4721600",
    "registries/METRIC_USE_LEDGER.csv":
        "108b1b56d9ef2d2d6cd30d7caa77461c813d8729890afd537206c6f94a1f24cb",
    "research_control/tasks/RT-20260629-055/artifacts/"
    "matter_semantics_candidate_law_payload_v1.tex":
        "0adf7d4b034f26cd478603ba6d9cb526dd7743dcb3a9a9f01d2e981efb2d81bf",
    "research_control/tasks/RT-20260629-057/artifacts/"
    "matter_semantics_candidate_law_refuter_stress_v1.tex":
        "78825184f37ad01071be86f0b190b12762539cdcb80093c55543fdf542676ca6",
    "research_control/tasks/RT-20260630-022/artifacts/"
    "matter_semantics_target_formalization_v1.tex":
        "4af3609b3a79e2870cbc9bb6d6c632adc7f381806cf1e63630319589572e1d16",
    "research_control/tasks/RT-20260630-023/artifacts/"
    "matter_semantics_candidate_v1.tex":
        "8dd53571106b37329152142b73fe2bbee5066b898e15c096f689842235a7f03a",
    "research_control/tasks/RT-20260727-004/jobs/completions/"
    "AJC-AJ-RT-20260727-004-001.yaml":
        "86c5122fd324c59406bf4992f326a533f563c4b23d0bdf83513b0282e9be7760",
}

REQUIRED_ARTIFACTS = [
    "source_matter_ontology_and_sector_taxonomy_v1.tex",
    "source_matter_ontology_spec_v1.yaml",
    "source_matter_sector_charge_taxonomy_v1.yaml",
    "source_matter_assumption_dependency_table_v1.yaml",
    "child_phys_math_p7_t01_source_matter_ontology.yaml",
    "child_phys_phil_p7_t01_source_matter_ontology.yaml",
    "parent_conflict_review_p7_t01_source_matter_ontology.yaml",
    "parent_fusion_notes_p7_t01_source_matter_ontology.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    value = yaml.safe_load((ART / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{name} must contain a YAML mapping")
    return value


def get_path(obj: Any, path: str) -> Any:
    current = obj
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, condition: bool, detail: str) -> None:
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if condition else "FAIL",
                "detail": detail,
            }
        )

    for name in REQUIRED_ARTIFACTS:
        check(
            f"artifact_exists::{name}",
            (ART / name).is_file(),
            f"required task-local artifact {name}",
        )

    spec = load_yaml("source_matter_ontology_spec_v1.yaml")
    taxonomy = load_yaml("source_matter_sector_charge_taxonomy_v1.yaml")
    assumptions = load_yaml("source_matter_assumption_dependency_table_v1.yaml")
    tex = (ART / "source_matter_ontology_and_sector_taxonomy_v1.tex").read_text(
        encoding="utf-8"
    )

    expected_spec_values = {
        "schema_id": "source_matter_ontology_spec_v1",
        "candidate_status": "proposal-only",
        "candidate_id": "SourceMatterIncidenceCandidate_v1",
        "adoption_status": "blocked_adoption_open_continuation",
        "source_data.incidence_complex.axiom": "partial_1 partial_2 = 0",
        "source_data.incidence_complex.augmentation_axiom":
            "epsilon partial_1 = 0",
        "source_data.internal_symmetry.charge_label_map":
            "chi: Ghat_decl union {0_R} -> A_int with chi(0_R)=0",
        "configuration.primitive_tuple": "(m, z)",
        "transition.id": "SourceMatterTransition_v1",
        "theorem.theorem_id":
            "P7T01-THM-SOURCE-RELABELING-SECTOR-NATURALITY-001",
        "witnesses.nontrivial.continuity_residual": "0",
        "witnesses.nontrivial.defect_residual": "0",
        "witnesses.nontrivial.charge_label_map": "chi(rho)=1",
        "witnesses.malformed.failed_condition": "T1_CONTINUITY",
        "witnesses.malformed.result": "bottom_mat",
        "witnesses.nontrivial_neutral.distinct_from_null": True,
        "witnesses.underdetermined.result": "undetermined_mat",
        "ontology_position.canonical_fundamental_or_emergent_decision": "open",
    }
    for path, expected in expected_spec_values.items():
        actual = get_path(spec, path)
        check(
            f"spec::{path}",
            actual == expected,
            f"expected {expected!r}; observed {actual!r}",
        )

    config_fields = {
        item.get("field")
        for item in spec.get("configuration", {}).get("tuple", [])
        if isinstance(item, dict)
    }
    check(
        "spec::configuration_fields",
        config_fields == {"m", "z"},
        f"observed {sorted(config_fields)}",
    )

    derived_fields = {
        item.get("field")
        for item in spec.get("configuration", {}).get("derived_fields", [])
        if isinstance(item, dict)
    }
    check(
        "spec::derived_configuration_fields",
        derived_fields == {"nu", "q_v", "q", "M"},
        f"observed {sorted(derived_fields)}",
    )

    conditions = {
        item.get("condition_id")
        for item in spec.get("configuration", {}).get(
            "admissibility_conditions", []
        )
        if isinstance(item, dict)
    }
    check(
        "spec::configuration_conditions",
        conditions
        == {
            "C1_DECLARED_DOMAINS",
            "C2_DERIVED_FIELDS",
            "C3_DEFECT_CYCLE",
            "C4_NO_TARGET_IMPORT",
        },
        f"observed {sorted(conditions)}",
    )

    transition_conditions = {
        item.get("condition_id")
        for item in spec.get("transition", {}).get("kinematic_conditions", [])
        if isinstance(item, dict)
    }
    check(
        "spec::transition_conditions",
        transition_conditions
        == {"T1_CONTINUITY", "T2_DEFECT_RELATION", "T3_SOURCE_ONLY_UPDATE"},
        f"observed {sorted(transition_conditions)}",
    )

    theorem_conclusions = spec.get("theorem", {}).get("conclusions", [])
    check(
        "spec::theorem_conclusions",
        len(theorem_conclusions) == 5,
        f"observed {len(theorem_conclusions)} conclusions",
    )

    legacy_mapping = spec.get("legacy_mapping", [])
    check(
        "spec::legacy_mapping_count",
        len(legacy_mapping) == 10,
        f"observed {len(legacy_mapping)} mappings",
    )
    check(
        "spec::legacy_no_upgrade",
        all(item.get("status_upgraded") is False for item in legacy_mapping),
        "all retained legacy mappings must preserve status",
    )

    false_authority_flags = [
        "canonical_ontology_modified",
        "source_law_adopted",
        "matter_ontology_adopted",
        "physical_charge_established",
        "physical_conservation_established",
        "detector_semantics_established",
        "target_metric_imported",
        "effective_geometry_assumed",
        "stress_energy_established",
        "matter_action_established",
        "coupling_law_adopted",
        "matter_coupling_derived",
        "einstein_equations_derived",
        "benchmark_promoted",
        "completed_derivation_claimed",
        "global_no_go_claimed",
        "future_source_extension_impossibility_claimed",
        "proof_authority",
    ]
    auth = spec.get("authority_limits", {})
    check(
        "spec::authority_flags_false",
        all(auth.get(name) is False for name in false_authority_flags),
        "all protected authority flags must remain false",
    )

    taxonomy_rows = taxonomy.get("taxonomy", [])
    taxonomy_ids = {
        row.get("class_id") for row in taxonomy_rows if isinstance(row, dict)
    }
    check(
        "taxonomy::class_ids",
        taxonomy_ids
        == {
            "SM-NULL",
            "SM-CHARGE",
            "SM-DEFECT",
            "SM-REP",
            "SM-INVARIANT",
            "SM-CURRENT",
            "SM-MALFORMED",
            "SM-UNDERDETERMINED",
        },
        f"observed {sorted(taxonomy_ids)}",
    )
    check(
        "taxonomy::class_count_receipt",
        get_path(taxonomy, "finding_counts.taxonomy_class_count") == 8,
        "taxonomy count receipt must equal eight",
    )
    check(
        "taxonomy::no_adopted_physical_sector",
        get_path(taxonomy, "finding_counts.adopted_physical_sector_count") == 0,
        "no physical sector may be adopted",
    )

    assumption_rows = assumptions.get("assumptions", [])
    dependency_rows = assumptions.get("dependencies", [])
    check(
        "assumptions::count",
        len(assumption_rows) == 8
        and get_path(assumptions, "assumption_counts.total") == 8,
        f"observed {len(assumption_rows)} assumptions",
    )
    check(
        "dependencies::count",
        len(dependency_rows) == 9
        and get_path(assumptions, "dependency_counts.total") == 9,
        f"observed {len(dependency_rows)} dependencies",
    )
    check(
        "assumptions::no_target_geometry",
        get_path(assumptions, "assumption_counts.target_geometry_assumptions")
        == 0,
        "target-geometry assumption count must be zero",
    )

    required_tex_markers = [
        "SourceMatterIncidenceCandidate",
        "P7T01-THM-SOURCE-RELABELING-SECTOR-NATURALITY-001",
        r"q^+-q^- &= \partial_1J",
        r"z^+-z^- &= \partial_2w",
        r"\epsilon_{\Aint}\partial_1=0",
        r"\chi:\Rdecl\cup\{0_R\}\longrightarrow\Aint",
        r"\chi'(\gamma\rho)=\alpha(\chi(\rho))",
        r"L_i^A=F_i\otimes\alpha",
        r"\mathrm{SourceMatterSector}_{v1}",
        r"\mathrm{MatSrcDiscLaw}_{v1}",
        r"\mathrm{PositiveMSProfile}_{v1}",
        "blocked\\_adoption\\_open\\_continuation",
        "not a physical vacuum",
        "not a particle trajectory",
        "Nontrivial neutral configuration",
        "Underdetermined request",
        "not the general",
        "P7-T02",
    ]
    for marker in required_tex_markers:
        check(
            f"tex::marker::{marker}",
            marker in tex,
            f"required TeX marker {marker!r}",
        )

    source_hashes: dict[str, str] = {}
    for relative, expected_hash in EXPECTED_SOURCE_HASHES.items():
        path = REPO / relative
        actual_hash = sha256(path) if path.is_file() else ""
        source_hashes[relative] = actual_hash
        check(
            f"source_hash::{relative}",
            actual_hash == expected_hash,
            f"expected {expected_hash}; observed {actual_hash}",
        )

    artifact_hashes = {
        name: sha256(ART / name)
        for name in REQUIRED_ARTIFACTS
        if (ART / name).is_file()
    }
    failed = [item for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "source_matter_ontology_validation_v1",
        "authority": "operational_validation_only",
        "task_id": "RT-20260727-007",
        "job_id": "AJ-RT-20260727-007-001",
        "candidate_id": "SourceMatterIncidenceCandidate_v1",
        "theorem_id":
            "P7T01-THM-SOURCE-RELABELING-SECTOR-NATURALITY-001",
        "validated_at": "2026-07-28T00:10:00Z",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failed),
        "finding_counts": {
            "configuration_field_count": len(config_fields),
            "derived_configuration_field_count": len(derived_fields),
            "configuration_condition_count": len(conditions),
            "transition_condition_count": len(transition_conditions),
            "taxonomy_class_count": len(taxonomy_ids),
            "assumption_count": len(assumption_rows),
            "dependency_count": len(dependency_rows),
            "legacy_mapping_count": len(legacy_mapping),
            "nontrivial_witness_count": 1,
            "null_witness_count": 1,
            "nontrivial_neutral_witness_count": 1,
            "malformed_branch_count": 1,
            "underdetermined_branch_count": 1,
            "theorem_count": 1,
            "adopted_physical_sector_count": 0,
        },
        "source_hashes": source_hashes,
        "artifact_hashes": artifact_hashes,
        "checks": checks,
        "authority_limits": {
            "validator_pass_counts_as_physics": False,
            "theorem_truth_inferred": False,
            "canonical_ontology_modified": False,
            "source_law_adopted": False,
            "matter_ontology_adopted": False,
            "physical_interpretation_established": False,
            "distance_to_gr_changed": True,
            "physics_promotion_authorized": False,
            "proof_authority": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    if args.write_report:
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        if not REPORT.is_file():
            report["status"] = "FAIL"
            report["failure_count"] = int(report["failure_count"]) + 1
            report["checks"].append(
                {
                    "check_id": "validation_report_exists",
                    "status": "FAIL",
                    "detail": str(REPORT.relative_to(REPO)),
                }
            )
        else:
            recorded = json.loads(REPORT.read_text(encoding="utf-8"))
            if recorded != report:
                report["status"] = "FAIL"
                report["failure_count"] = int(report["failure_count"]) + 1
                report["checks"].append(
                    {
                        "check_id": "validation_report_current",
                        "status": "FAIL",
                        "detail": "recorded validation report differs from recomputed report",
                    }
                )

    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        print(
            f"{report['status']}: {report['check_count']} checks; "
            f"{report['failure_count']} failures"
        )
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

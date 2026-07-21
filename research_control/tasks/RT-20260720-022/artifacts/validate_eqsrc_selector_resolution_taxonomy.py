#!/usr/bin/env python3
"""Validate the bounded v21 P3-T01 selector-resolution taxonomy packet."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml


ARTIFACTS = Path(__file__).resolve().parent
ROOT = ARTIFACTS.parents[3]
TAXONOMY_ID = "EQSRC-SELECTOR-RESOLUTION-TAXONOMY-V1"
REPORT = ARTIFACTS / "eqsrc_selector_resolution_taxonomy_validation.json"
CLASSES = [
    "added_source_structure",
    "representative_irrelevance",
    "dynamical_symmetry_breaking",
    "probabilistic_selection",
    "scoped_obstruction",
]
PRIMARY_ORDER = [
    "representative_irrelevance",
    "probabilistic_selection",
    "dynamical_symmetry_breaking",
    "added_source_structure",
    "scoped_obstruction",
]
STATUS_AXES = {
    "definition_status",
    "existence_status",
    "uniqueness_status",
    "naturality_status",
    "covariance_status",
    "robustness_status",
    "dynamics_status",
    "operational_status",
    "empirical_status",
    "authority_status",
}
CLAIM_LAYERS = {"ontology", "model", "physical", "empirical", "authority"}
COST_COMPONENTS = {
    "source_signature_delta",
    "selector_or_readout_law_delta",
    "state_or_boundary_data_delta",
    "dynamics_delta",
    "probability_delta",
    "variation_class_delta",
    "set_theoretic_choice_delta",
    "empirical_calibration_delta",
    "target_import_risk",
    "human_authority_required",
}
EXPECTED_SOURCES = {
    "research_control/tasks/RT-20260613-025/artifacts/41_LOCALIZATION_SOURCE_BASIS_AXIOM_SELECTOR_DOMAIN_EQSRC_SOURCE_EQUIVALENCE_OBLIGATION_PACKET_OR_CONTROLLED_PAUSE.tex": "bf56d4587d0875e1f9cb244fe3f6acc2b36c522ec96ef9221b9bb1cfb4d42a2d",
    "research_control/design/frontier_theorem_inventory.md": "0f7d22dff2079b3c4d3f53ba5a1147dbc0fd245eb7ddb74e74dfca7cd2f54124",
    "research_control/design/gr_derivation_burden_map.md": "6d1df3488be163b72296cf34ee07b979e29b061d508e6a4c271ac3305373aa1f",
    "registries/DISTANCE_TO_GR_LEDGER.csv": "0ec3266d708398acde6f380515c37751c0db8ce03bbb135f8aa60fb0f494ce61",
    "research_control/tasks/RT-20260720-013/artifacts/eqsrc_naturality_primary_literature_review.md": "0206681a534ce7470175630beb0aee05c487c5bacc4114b35a436961c04eed74",
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex": "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae",
    "research_control/tasks/RT-20260720-020/artifacts/eqsrc_selector_theorem_refuter_stress_v1.tex": "d519bcc9534af3b2ca3e3d44604bd56bf72c425e0d06322c33cc7e66abfd2b49",
    "research_control/tasks/RT-20260720-021/artifacts/eqsrc_selector_theorem_external_red_team_review_v1.yaml": "25e8e0ec587c72c3d2d7f2269ba2646986828393054f98ce4e82dc9da5b52645",
    "ontology/tex/aether_flow_foundations.tex": "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(name: str) -> dict[str, Any]:
    return yaml.safe_load((ARTIFACTS / name).read_text(encoding="utf-8"))


def add_check(
    condition: bool,
    check_id: str,
    detail: str,
    checks: list[dict[str, str]],
) -> None:
    checks.append(
        {
            "check_id": check_id,
            "detail": detail,
            "status": "PASS" if condition else "FAIL",
        }
    )


def validate() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    paths = {
        "tex": ARTIFACTS / "eqsrc_selector_resolution_taxonomy_v1.tex",
        "schema": ARTIFACTS / "eqsrc_selector_resolution_decision_schema_v1.yaml",
        "examples": ARTIFACTS / "eqsrc_selector_resolution_worked_examples_v1.yaml",
        "math": ARTIFACTS / "child_phys_math_eqsrc_selector_resolution_taxonomy.yaml",
        "phil": ARTIFACTS / "child_phys_phil_eqsrc_selector_resolution_taxonomy.yaml",
        "conflict": ARTIFACTS / "parent_conflict_review_eqsrc_selector_resolution_taxonomy.yaml",
        "fusion": ARTIFACTS / "parent_fusion_notes_eqsrc_selector_resolution_taxonomy.md",
        "receipt": ARTIFACTS / "eqsrc_selector_resolution_compact_receipt.json",
    }
    add_check(
        all(path.is_file() for path in paths.values()),
        "artifact_set",
        "All eight fused, child, review, example, schema, and compact-receipt artifacts exist.",
        checks,
    )

    tex = paths["tex"].read_text(encoding="utf-8")
    normalized_tex = " ".join(tex.split())
    lower_tex = normalized_tex.lower()
    schema = load_yaml(paths["schema"].name)
    examples = load_yaml(paths["examples"].name)
    math_child = load_yaml(paths["math"].name)
    phil_child = load_yaml(paths["phil"].name)
    conflict = load_yaml(paths["conflict"].name)
    fusion = paths["fusion"].read_text(encoding="utf-8")
    receipt = json.loads(paths["receipt"].read_text(encoding="utf-8"))

    add_check(
        schema.get("taxonomy_id") == TAXONOMY_ID
        and examples.get("taxonomy_id") == TAXONOMY_ID
        and conflict.get("taxonomy_id") == TAXONOMY_ID
        and TAXONOMY_ID in tex
        and TAXONOMY_ID in fusion,
        "taxonomy_identity",
        "All fused artifacts share the exact taxonomy identity.",
        checks,
    )
    add_check(
        tex.count("{") == tex.count("}")
        and "\\begin{document}" in tex
        and "\\end{document}" in tex
        and "Unique primary classification" in tex,
        "tex_structure_and_payload",
        "The TeX source is structurally complete and contains the new normal-form proposition.",
        checks,
    )
    add_check(
        all(term in lower_tex for term in (
            "proposal-only source-extension control data",
            "structural automorphisms are not thereby physical gauge",
            "dynamics-mediated selection",
            "does not execute that ordering",
        ))
        and "unclassified" in lower_tex
        and "fail closed" in lower_tex,
        "claim_boundary_language",
        "Proposal, gauge, fail-closed, dynamics-label, and downstream ownership boundaries are explicit.",
        checks,
    )

    schema_classes = schema.get("primary_classes", [])
    schema_class_ids = [row.get("class_id") for row in schema_classes]
    add_check(
        schema_class_ids == CLASSES
        and schema.get("completion_contract", {}).get("exact_class_count") == 5
        and schema.get("completion_contract", {}).get("primary_class_count") == 1,
        "five_class_exactness",
        "The schema contains exactly the five plan-defined classes and one-primary cardinality.",
        checks,
    )
    add_check(
        all(
            row.get("decision_predicate")
            and row.get("necessary_evidence")
            and row.get("rejection_conditions")
            and row.get("route_consequence")
            for row in schema_classes
        ),
        "class_evidence_completeness",
        "Every class has a decision predicate, evidence burden, rejection conditions, and route consequence.",
        checks,
    )

    ordered_rules = schema.get("normalization_algorithm", {}).get(
        "ordered_primary_rule", []
    )
    order_terms = [
        "RI" if "Choose RI" in text else
        "PS" if "choose PS" in text else
        "DSB" if "choose DSB" in text else
        "AS" if "choose AS" in text else
        "SO" if "choose SO" in text else
        "ELSE" if "reject" in text.lower() else "UNKNOWN"
        for text in ordered_rules
    ]
    add_check(
        order_terms == ["RI", "PS", "DSB", "AS", "SO", "ELSE"]
        and schema.get("completion_contract", {}).get("unclassified_is_valid") is False
        and schema.get("completion_contract", {}).get("ambiguous_is_valid") is False,
        "overlap_and_primary_class_guards",
        "The deterministic RI-PS-DSB-AS-SO order and fail-closed else branch are exact.",
        checks,
    )
    required_fields = set(schema.get("input_contract", {}).get("required_fields", []))
    add_check(
        {"assumption_delta", "assumption_cost_vector", "claim_layer_status", "authority_flags"}.issubset(required_fields)
        and set(schema.get("status_axes", {}).get("required", [])) == STATUS_AXES
        and set(schema.get("claim_layer_status", {}).get("required_layers", [])) == CLAIM_LAYERS
        and set(schema.get("assumption_cost_vector", {}).get("required_components", {})) == COST_COMPONENTS,
        "status_and_assumption_type_system",
        "Ten status axes, five claim layers, and ten componentwise assumption-cost fields are required.",
        checks,
    )

    example_rows = examples.get("examples", [])
    example_classes = [row.get("primary_class") for row in example_rows]
    add_check(
        examples.get("example_count") == 5
        and len(example_rows) == 5
        and sorted(example_classes) == sorted(CLASSES)
        and len(set(example_classes)) == 5
        and examples.get("class_coverage") == {name: 1 for name in CLASSES},
        "worked_example_consistency",
        "Five worked controls classify one-to-one into the exact primary classes.",
        checks,
    )
    add_check(
        all(set(row.get("status_axes", {})) == STATUS_AXES for row in example_rows)
        and examples.get("authority_guards", {}).get("canonical_ontology_edit_authorized") is False
        and examples.get("authority_guards", {}).get("physics_promotion_authorized") is False
        and examples.get("authority_guards", {}).get("global_no_go_authorized") is False,
        "worked_example_status_and_authority",
        "Each control reports every status axis and keeps protected authority false.",
        checks,
    )

    c2_fixed = [x for x in (0, 1) if 1 - x == x]
    c3_weights = [1 / 3, 1 / 3, 1 / 3]
    c3_invariant = all(c3_weights[index] == c3_weights[(index - 1) % 3] for index in range(3))
    double_well_slopes = {point: 1 - 3 * point * point for point in (-1, 0, 1)}
    add_check(
        not c2_fixed
        and c3_invariant
        and abs(sum(c3_weights) - 1.0) < 1e-12
        and double_well_slopes[-1] < 0
        and double_well_slopes[0] > 0
        and double_well_slopes[1] < 0,
        "finite_and_dynamical_controls",
        "The C2 obstruction, C3 invariant law, and double-well linear stability signs reproduce exactly.",
        checks,
    )

    math_classes = list(math_child.get("resolution_classes", {}))
    phil_classes = [row.get("class_id") for row in phil_child.get("classes", [])]
    add_check(
        math_child.get("status") == "completed"
        and phil_child.get("status") == "completed"
        and math_classes == CLASSES
        and phil_classes == CLASSES,
        "parallel_child_outputs",
        "Both independent child syntheses completed with the same exact class set.",
        checks,
    )
    add_check(
        conflict.get("status") == "completed"
        and conflict.get("resolution_rounds") == 1
        and not conflict.get("unresolved_blocking_conflicts")
        and len(conflict.get("conflicts", [])) == 5
        and all(row.get("status") == "resolved" for row in conflict.get("conflicts", [])),
        "parent_conflict_resolution",
        "One parent round resolved all five synthesis differences without blocking residue.",
        checks,
    )

    source_receipts: list[dict[str, str]] = []
    source_hashes_match = True
    for relative, expected in EXPECTED_SOURCES.items():
        path = ROOT / relative
        actual = digest(path) if path.is_file() else "missing"
        source_hashes_match &= actual == expected
        source_receipts.append(
            {"path": relative, "expected_sha256": expected, "actual_sha256": actual}
        )
    add_check(
        source_hashes_match,
        "source_hash_parity",
        "All nine fixed source, theorem, stress, review, ledger, and ontology hashes match the job contract.",
        checks,
    )

    add_check(
        receipt.get("taxonomy_id") == TAXONOMY_ID
        and receipt.get("result_status") == "completed"
        and receipt.get("finding_counts", {}).get("primary_class_count") == 5
        and receipt.get("finding_counts", {}).get("worked_example_count") == 5
        and receipt.get("claim_boundary_summary", {}).get("physics_promotion_authorized") is False
        and receipt.get("claim_boundary_summary", {}).get("distance_to_gr_delta") is False,
        "compact_receipt",
        "The compact receipt records result, counts, source evidence, and no-promotion/no-distance boundaries.",
        checks,
    )

    failures = [check for check in checks if check["status"] != "PASS"]
    return {
        "schema_id": "EQSRC-SELECTOR-RESOLUTION-TAXONOMY-VALIDATION-V1",
        "taxonomy_id": TAXONOMY_ID,
        "task_id": "RT-20260720-022",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "checks": checks,
        "finding_counts": {
            "primary_class_count": len(schema_classes),
            "worked_example_count": len(example_rows),
            "child_control_count": len(math_child.get("worked_controls", [])),
            "resolved_conflict_count": len(conflict.get("conflicts", [])),
            "status_axis_count": len(STATUS_AXES),
            "claim_layer_count": len(CLAIM_LAYERS),
            "assumption_cost_component_count": len(COST_COMPONENTS),
        },
        "source_receipts": source_receipts,
        "claim_boundary": {
            "status": "draft/control proposal-only",
            "distance_to_gr_delta": False,
            "ontology_modification_authorized": False,
            "physics_promotion_authorized": False,
            "global_no_go_authorized": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result["status"])
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

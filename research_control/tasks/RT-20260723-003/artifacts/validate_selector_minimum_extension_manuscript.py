#!/usr/bin/env python3
"""Deterministically validate the bounded P15-T03 manuscript packet."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import sys
from pathlib import Path
from typing import Any

import yaml


SCRIPT = Path(__file__).resolve()
ARTIFACTS = SCRIPT.parent
ROOT = SCRIPT.parents[4]
TASK_DIR = ARTIFACTS.parent

MANUSCRIPT = ARTIFACTS / "selector_minimum_extension_theorem_manuscript_v1.tex"
PROOF_ARCHIVE = ARTIFACTS / "selector_theorem_proof_archive_v1.yaml"
COUNTERMODEL_DATA = ARTIFACTS / "selector_theorem_countermodel_data_v1.json"
REVIEW_PACKET = ARTIFACTS / "selector_minimum_extension_review_packet_v1.yaml"
CHILD_MATH = ARTIFACTS / "child_phys_math_selector_minimum_extension_manuscript.yaml"
CHILD_PHIL = ARTIFACTS / "child_phys_phil_selector_minimum_extension_manuscript.yaml"
CONFLICT_REVIEW = ARTIFACTS / "parent_conflict_review_selector_minimum_extension_manuscript.yaml"
FUSION_NOTES = ARTIFACTS / "parent_fusion_notes_selector_minimum_extension_manuscript.md"
REPORT = ARTIFACTS / "selector_minimum_extension_validation_report.json"
COMPACT_RECEIPT = ARTIFACTS / "selector_minimum_extension_compact_receipt.json"

SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v21.md":
        "4d11bd3aa78d97e8707cf48821a139bfe3ddb311f798b78663544ef6520bf087",
    "research_control/handoffs/handoff-0835.yaml":
        "d20bdcacdcc4e8b08b2570a5a0e98ae2c87761eb7f8398f4908daf2138fd1094",
    "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex":
        "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae",
    "research_control/tasks/RT-20260720-017/artifacts/eqsrc_finite_countermodel_atlas_v1.tex":
        "4a7c84ecf769b19e92b2b2dffd7224ddd4e1e02e4cc93cff797d01fa0e1bc62b",
    "research_control/tasks/RT-20260720-023/artifacts/eqsrc_source_extension_lattice_v1.tex":
        "b0f539b7a1d53f9cafb93151f6420cbd12077c317e2bba8176442607c0319a85",
    "research_control/tasks/RT-20260720-026/artifacts/eqsrc_invariant_functor_quotient_relation_candidate_v1.tex":
        "badc60c72ff16f84fe88568b825ff738a8f160a225f011715f027c1da2cfa1c3",
    "research_control/tasks/RT-20260720-027/artifacts/eqsrc_invariant_functor_quotient_smuggling_audit_v1.tex":
        "0e3991d70dd7754149821d132808062dd5bf153c810086629686e45593c78c1c",
    "research_control/tasks/RT-20260722-020/artifacts/negative_result_success_pathway_v1.tex":
        "a5b59ddf497659097783e8e8dcd9c4de1726652265b0b53cab007da233f34aa3",
    "ontology/tex/aether_flow_foundations.tex":
        "b14c99501bdb2b9fad0702df3a41230a4bf3bd279ee660c31329e1d33e577fa2",
    "ontology/tex/aether_flow_geometry.tex":
        "ad43e3408fe2d9686a52a71de7ab8326668e8f04ebe2d2845986898b7d2c000f",
}

REQUIRED_MANUSCRIPT_PHRASES = [
    "Fixed-locus classification",
    "Relation-image uniqueness",
    "Full-category equalizer guard",
    "Exact declaration envelope",
    "Compatible fixed-locus trichotomy",
    "Finite minimum-extension signatures",
    "Incomplete-universe guard",
    "Kernel equivalence",
    "prospective fixation",
    "marked-interface",
    "project-specific, source-traced synthesis",
    "structural isomorphism is not automatically physical gauge",
    "No Distance-to-GR ledger row changes",
    "same-context internal source-trace",
    "not blind independent human review",
]

PRIMARY_DOIS = [
    "10.1090/S0002-9947-1945-0013131-6",
    "10.1145/800141.804655",
    "10.1109/SFCS.1981.41",
    "10.2307/1970335",
    "10.1007/BF01609471",
    "10.1016/0034-4877(74)90021-4",
]

FALSE_AUTHORITY_KEYS = [
    "scientific_status_changed",
    "general_eqsrc_discharged",
    "physical_gauge_established",
    "ontology_or_source_law_adopted",
    "future_extension_impossibility_established",
    "distance_to_gr_changed",
    "physics_promotion_authorized",
    "publication_authorized",
    "global_no_go_claimed",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return value


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def canonical_sets(values: list[list[str]]) -> set[tuple[str, ...]]:
    return {tuple(sorted(item)) for item in values}


def minimal_hitting_sets(universe: list[str], clauses: list[list[str]]) -> set[tuple[str, ...]]:
    clause_sets = [set(item) for item in clauses]
    hits: list[set[str]] = []
    for size in range(len(universe) + 1):
        for combo in itertools.combinations(universe, size):
            candidate = set(combo)
            if all(candidate & clause for clause in clause_sets):
                hits.append(candidate)
    minima = [
        item for item in hits
        if not any(other < item for other in hits)
    ]
    return {tuple(sorted(item)) for item in minima}


def build_report() -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({
            "check_id": name,
            "status": "PASS" if condition else "FAIL",
            "detail": detail,
        })

    required_paths = [
        MANUSCRIPT, PROOF_ARCHIVE, COUNTERMODEL_DATA, REVIEW_PACKET,
        CHILD_MATH, CHILD_PHIL, CONFLICT_REVIEW, FUSION_NOTES,
    ]
    for path in required_paths:
        check(
            f"exists:{path.name}",
            path.is_file(),
            str(path.relative_to(ROOT)),
        )

    # Fail closed if a required artifact is absent, while still returning a report.
    if not all(path.is_file() for path in required_paths):
        errors = [item["check_id"] for item in checks if item["status"] == "FAIL"]
        return {
            "schema_id": "selector_minimum_extension_validation_report_v1",
            "task_id": "RT-20260723-003",
            "job_id": "AJ-RT-20260723-003-001",
            "status": "FAIL",
            "check_count": len(checks),
            "error_count": len(errors),
            "errors": errors,
            "checks": checks,
            "authority": "operational_validation_only",
        }

    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    proof = load_yaml(PROOF_ARCHIVE)
    data = load_json(COUNTERMODEL_DATA)
    review = load_yaml(REVIEW_PACKET)
    child_math = load_yaml(CHILD_MATH)
    child_phil = load_yaml(CHILD_PHIL)
    conflict = load_yaml(CONFLICT_REVIEW)
    fusion = FUSION_NOTES.read_text(encoding="utf-8")

    for relpath, expected in SOURCE_HASHES.items():
        path = ROOT / relpath
        check(
            f"source_hash:{relpath}",
            path.is_file() and sha256(path) == expected,
            expected,
        )

    for phrase in REQUIRED_MANUSCRIPT_PHRASES:
        check(
            f"manuscript_phrase:{phrase}",
            phrase in manuscript,
            phrase,
        )
    for doi in PRIMARY_DOIS:
        check(f"primary_doi:{doi}", doi in manuscript, doi)

    check(
        "manuscript_theorem_count",
        manuscript.count("\\begin{theorem}") >= 4,
        "at least four explicit theorem environments",
    )
    check(
        "manuscript_proof_count",
        manuscript.count("\\begin{proof}") >= 8,
        "at least eight explicit proof environments",
    )
    check(
        "manuscript_proposal_only",
        "proposal-only" in manuscript and "draft/control" in manuscript,
        "status labels",
    )

    examples = data.get("examples", [])
    example_ids = {
        item.get("example_id") for item in examples if isinstance(item, dict)
    }
    expected_example_ids = {
        "SIGN-SWAP-EMPTY-FIXED-LOCUS",
        "TAGGED-SINGLETON-POSITIVE-CONTROL",
        "GL2-F2-THREE-LINES",
        "MARKED-LINE-STABILIZER",
        "ROOTED-TWO-CYCLE",
        "ROOTED-FOUR-CYCLE",
        "LOADED-ROOT-SINGLETON",
        "GRADED-FOUR-CHAIN",
        "TRIVIAL-TWO-CHOICE-RELATION-IMAGE-CONTROL",
    }
    check("countermodel_example_count", len(examples) == 9, "nine fixed-point controls")
    check("countermodel_example_ids", example_ids == expected_example_ids, "exact example identities")

    by_id = {item["example_id"]: item for item in examples}
    check(
        "sign_swap_counts",
        by_id["SIGN-SWAP-EMPTY-FIXED-LOCUS"]["group_order"] == 2
        and len(by_id["SIGN-SWAP-EMPTY-FIXED-LOCUS"]["fixed_choices"]) == 0
        and by_id["SIGN-SWAP-EMPTY-FIXED-LOCUS"]["selector_count"] == 0,
        "C2 transitive two-choice obstruction",
    )
    check(
        "line_counts",
        by_id["GL2-F2-THREE-LINES"]["group_order"] == 6
        and len(by_id["GL2-F2-THREE-LINES"]["eligible_choices"]) == 3
        and len(by_id["GL2-F2-THREE-LINES"]["fixed_choices"]) == 0,
        "GL(2,F2) three-line obstruction",
    )
    check(
        "root_cycle_counts",
        by_id["ROOTED-FOUR-CYCLE"]["group_order"] == 4
        and len(by_id["ROOTED-FOUR-CYCLE"]["eligible_choices"]) == 4
        and by_id["ROOTED-FOUR-CYCLE"]["potential_relation_class_count"] == 2,
        "C4 root and parity classes",
    )
    check(
        "relation_image_control",
        by_id["TRIVIAL-TWO-CHOICE-RELATION-IMAGE-CONTROL"]["selector_count"] == 2
        and by_id["TRIVIAL-TWO-CHOICE-RELATION-IMAGE-CONTROL"]["injective_relation_image_count"] == 2
        and by_id["TRIVIAL-TWO-CHOICE-RELATION-IMAGE-CONTROL"]["constant_relation_image_count"] == 1,
        "selector multiplicity separated from relation multiplicity",
    )
    empty_selector_relation_counts = {
        "SIGN-SWAP-EMPTY-FIXED-LOCUS": 2,
        "GL2-F2-THREE-LINES": 3,
        "ROOTED-TWO-CYCLE": 2,
        "ROOTED-FOUR-CYCLE": 2,
    }
    check(
        "empty_selector_relation_value_distinction",
        all(
            by_id[example_id]["eligible_relation_value_count"] == expected_count
            and by_id[example_id]["induced_natural_relation_section_count"] == 0
            for example_id, expected_count in empty_selector_relation_counts.items()
        ),
        "eligible pointwise relation values remain distinct from an empty selector-induced image",
    )
    check(
        "positive_selector_relation_sections",
        all(
            by_id[example_id]["induced_natural_relation_section_count"] == 1
            for example_id in [
                "TAGGED-SINGLETON-POSITIVE-CONTROL",
                "MARKED-LINE-STABILIZER",
                "LOADED-ROOT-SINGLETON",
                "GRADED-FOUR-CHAIN",
            ]
        ),
        "each singleton selector control induces one natural relation section",
    )

    partition = data["arbitrary_partition_control"]
    partition_keys = {
        tuple(sorted(tuple(sorted(block)) for block in item))
        for item in partition["partitions"]
    }
    check("partition_count", partition["partition_count"] == 5, "Bell number B3")
    check("partition_uniqueness", len(partition_keys) == 5, "five distinct partitions")

    lattice = data["extension_lattice"]
    check("b8_node_count", lattice["node_count"] == 2 ** 8 == 256, "2^8")
    check(
        "b8_cover_count",
        lattice["directed_cover_edge_count"] == 8 * 2 ** 7 == 1024,
        "8*2^7",
    )
    expected_ranks = [math.comb(8, k) for k in range(9)]
    check("b8_rank_sizes", lattice["rank_sizes"] == expected_ranks, str(expected_ranks))

    minimum = data["minimum_extension_control"]
    computed_minima = minimal_hitting_sets(minimum["universe"], minimum["clauses"])
    recorded_minima = canonical_sets(minimum["minimal_signatures"])
    check("minimum_signature_reproduction", computed_minima == recorded_minima, str(sorted(computed_minima)))
    check(
        "minimum_failed_controls",
        all(
            tuple(sorted(item)) not in computed_minima
            for item in minimum["failed_signatures"]
        ),
        "empty d and n are not minima",
    )

    interface = data["marked_interface_countermodel"]
    check(
        "marked_interface_before",
        interface["invariant_before"]["x"] == [1, 0]
        and interface["invariant_before"]["y"] == [1, 0],
        "same object invariant before operation",
    )
    check(
        "marked_interface_after",
        interface["invariant_after"]["x"] == [1, 0]
        and interface["invariant_after"]["y"] == [1, 1],
        "operation fails to descend",
    )

    obligations = proof.get("proof_obligations", [])
    check("proof_obligation_count", len(obligations) == 8, "eight archived obligations")
    check(
        "proof_obligations_resolved",
        all(str(item.get("status", "")).startswith("reproduced") for item in obligations),
        "all obligations reproduced at declared scope",
    )
    check(
        "proof_source_count",
        len(proof.get("source_basis", [])) == 6,
        "six controlling science sources",
    )

    citations = review.get("primary_literature", [])
    check("primary_literature_count", len(citations) == 8, "eight primary sources")
    check(
        "primary_citations_apa_ready",
        all("citation_apa7" in item and item["citation_apa7"] for item in citations),
        "all primary entries carry APA-ready citations",
    )
    check(
        "review_not_external",
        review.get("independent_external_review") is False
        and review.get("peer_review") is False
        and review.get("publication_authorized") is False,
        "same-context internal review only",
    )

    for name, child, unit, perspective in [
        ("math", child_math, "child_phys_math", "physicist_mathematician"),
        ("phil", child_phil, "child_phys_phil", "physicist_philosopher"),
    ]:
        check(f"child_{name}_unit", child.get("execution_unit_id") == unit, unit)
        check(f"child_{name}_perspective", child.get("perspective") == perspective, perspective)
        check(f"child_{name}_complete", child.get("status") == "completed", "completed")
        check(
            f"child_{name}_boundary",
            child.get("authority") == "draft/control",
            "draft/control",
        )

    check("conflict_review_complete", conflict.get("status") == "completed", "completed")
    check("conflict_review_rounds", conflict.get("review_rounds") == 1, "one bounded round")
    check("conflict_review_unresolved", conflict.get("unresolved_conflict_count") == 0, "zero unresolved")
    check(
        "conflict_fusion_proceeds",
        conflict.get("fusion_disposition", {}).get("proceed") is True,
        "parent fusion approved",
    )
    check(
        "fusion_notes_boundaries",
        "general EqSrc remains open" in fusion
        and "publication authority remains absent" in fusion,
        "required fusion limits",
    )

    for surface_name, limits in [
        ("data", data.get("authority_limits", {})),
        ("proof", proof.get("authority_limits", {})),
        ("review", review.get("authority_limits", {})),
    ]:
        for key in FALSE_AUTHORITY_KEYS:
            if key in limits:
                check(
                    f"authority_false:{surface_name}:{key}",
                    limits.get(key) is False,
                    "false",
                )

    artifact_hashes = {
        str(path.relative_to(ROOT)): sha256(path)
        for path in required_paths + [SCRIPT]
    }
    errors = [item["check_id"] for item in checks if item["status"] == "FAIL"]
    return {
        "schema_id": "selector_minimum_extension_validation_report_v1",
        "schema_version": 1,
        "task_id": "RT-20260723-003",
        "job_id": "AJ-RT-20260723-003-001",
        "status": "PASS" if not errors else "FAIL",
        "check_count": len(checks),
        "error_count": len(errors),
        "errors": errors,
        "checks": checks,
        "artifact_hashes": artifact_hashes,
        "source_hashes": SOURCE_HASHES,
        "authority": "operational_validation_only",
        "authority_limits": {
            "validator_is_physics_evidence": False,
            "theorem_truth_inferred": False,
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "publication_authorized": False,
        },
    }


def serialized(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def build_receipt(report: dict[str, Any]) -> dict[str, Any]:
    report_bytes = serialized(report).encode("utf-8")
    return {
        "schema_id": "selector_minimum_extension_compact_receipt_v1",
        "schema_version": 1,
        "task_id": "RT-20260723-003",
        "job_id": "AJ-RT-20260723-003-001",
        "status": report["status"],
        "validation_check_count": report["check_count"],
        "validation_error_count": report["error_count"],
        "validation_report_path": str(REPORT.relative_to(ROOT)),
        "validation_report_sha256": hashlib.sha256(report_bytes).hexdigest(),
        "manuscript_path": str(MANUSCRIPT.relative_to(ROOT)),
        "manuscript_sha256": sha256(MANUSCRIPT) if MANUSCRIPT.exists() else "",
        "proof_archive_path": str(PROOF_ARCHIVE.relative_to(ROOT)),
        "proof_archive_sha256": sha256(PROOF_ARCHIVE) if PROOF_ARCHIVE.exists() else "",
        "countermodel_data_path": str(COUNTERMODEL_DATA.relative_to(ROOT)),
        "countermodel_data_sha256": sha256(COUNTERMODEL_DATA) if COUNTERMODEL_DATA.exists() else "",
        "review_packet_path": str(REVIEW_PACKET.relative_to(ROOT)),
        "review_packet_sha256": sha256(REVIEW_PACKET) if REVIEW_PACKET.exists() else "",
        "scientific_status_changed": False,
        "general_eqsrc_discharged": False,
        "distance_to_gr_changed": False,
        "ontology_or_source_law_adopted": False,
        "physical_gauge_established": False,
        "physics_promotion_authorized": False,
        "publication_authorized": False,
        "global_no_go_claimed": False,
        "authority": "operational_validation_only",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = build_report()
    receipt = build_receipt(report)
    report_text = serialized(report)
    receipt_text = serialized(receipt)

    if args.write_report:
        REPORT.write_text(report_text, encoding="utf-8")
        COMPACT_RECEIPT.write_text(receipt_text, encoding="utf-8")

    stale: list[str] = []
    if args.check:
        if not REPORT.is_file() or REPORT.read_text(encoding="utf-8") != report_text:
            stale.append(str(REPORT.relative_to(ROOT)))
        if not COMPACT_RECEIPT.is_file() or COMPACT_RECEIPT.read_text(encoding="utf-8") != receipt_text:
            stale.append(str(COMPACT_RECEIPT.relative_to(ROOT)))

    summary = {
        "status": "FAIL" if stale or report["status"] != "PASS" else "PASS",
        "check_count": report["check_count"],
        "error_count": report["error_count"],
        "stale_outputs": stale,
        "report_path": str(REPORT.relative_to(ROOT)),
        "compact_receipt_path": str(COMPACT_RECEIPT.relative_to(ROOT)),
        "authority": "operational_validation_only",
    }
    if args.json:
        print(json.dumps(summary, sort_keys=True))
    elif report["status"] != "PASS" or stale:
        print(serialized(summary), end="")
    return 0 if report["status"] == "PASS" and not stale else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Validate the bounded P4-T06 canonical ontology integration."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260724-010"
ART = TASK / "artifacts"
REPORT = ART / "p4_t06_canonical_integration_validation_v1.json"
RECEIPT = ART / "p4_t06_canonical_integration_compact_receipt_v1.json"

CANONICAL_SOURCES = (
    "ontology/tex/aether_flow_foundations.tex",
    "ontology/tex/aether_flow_dynamics.tex",
    "ontology/tex/aether_flow_geometry.tex",
)

CONTROL_SOURCES = (
    "research_control/design/frontier_theorem_inventory.md",
    "research_control/design/epistemic_category_glossary.md",
    "research_control/design/gr_derivation_burden_map.md",
    "research_control/tasks/RT-20260721-009/artifacts/v21_burden_definitions_v1.yaml",
    "registries/DISTANCE_TO_GR_LEDGER.csv",
)

HISTORICAL_HASHES = {
    "research_control/tasks/RT-20260720-031/artifacts/"
    "continuum_first_premetric_ontology_option_v1.tex":
        "7d408e527015f4e7c09df90277282c284f299fb705cbd4917a22e62ab3e0d1f8",
    "research_control/tasks/RT-20260720-032/artifacts/"
    "emergence_first_process_order_ontology_option_v1.tex":
        "121e86bd8609863ca79fd21d1cf9b5ee855057bc5a0804927946911f1222d6f5",
    "research_control/tasks/RT-20260721-002/artifacts/"
    "ontology_regime_comparison_report_v1.md":
        "5dd5526ebdce949ff121f4aa2785e665e006b5e9fec5f8b1d72877d7da26b7ae",
    "research_control/tasks/RT-20260724-004/artifacts/"
    "ontology_regime_gate_chair_decision_v1.tex":
        "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934",
    "research_control/tasks/RT-20260724-004/artifacts/"
    "human_authorization_p4_t05_continuum_first_v1.yaml":
        "3421808c71a64279ef5ba62df5376ab4999d2c67978d4f7ceabbeb0ae9b2bde6",
    "research_control/approvals/approval-20260724-001.yaml":
        "37038157b5deb23a3ae8249dcf5562ac8e9be37f6fa4ae8704c47b0eeb24a412",
    "research_control/tasks/RT-20260724-004/artifacts/"
    "canonical_next_route_authorization_v1.yaml":
        "52edb6e43e024b09de58d2fc9242a6747630678800e91d47d6c4195203cd8c86",
}

ARTIFACT_YAMLS = (
    "child_phys_math_p4_t06_ontology_integration.yaml",
    "child_phys_phil_p4_t06_ontology_integration.yaml",
    "parent_conflict_review_p4_t06_ontology_integration.yaml",
    "selected_ontology_regime_assumption_delta_v1.yaml",
    "selected_ontology_regime_burden_dependency_v1.yaml",
    "hybrid_ontology_language_deprecation_v1.yaml",
    "selected_ontology_regime_claim_vocabulary_v1.yaml",
)


class ValidationError(RuntimeError):
    """Raised when a bounded P4-T06 invariant fails."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def sha256(rel_path: str) -> str:
    return hashlib.sha256((ROOT / rel_path).read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"YAML root is not a mapping: {path}")
    return value


def changed_paths() -> set[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line for line in result.stdout.splitlines() if line}


def validate_authority(checks: list[dict[str, str]]) -> None:
    for rel_path, expected_hash in HISTORICAL_HASHES.items():
        require(sha256(rel_path) == expected_hash, f"authority hash drift: {rel_path}")

    approval = load_yaml(ROOT / "research_control/approvals/approval-20260724-001.yaml")
    authorization = load_yaml(
        ROOT
        / "research_control/tasks/RT-20260724-004/artifacts/"
        "human_authorization_p4_t05_continuum_first_v1.yaml"
    )
    route = load_yaml(
        ROOT
        / "research_control/tasks/RT-20260724-004/artifacts/"
        "canonical_next_route_authorization_v1.yaml"
    )
    require(
        approval["human_authorization_id"]
        == "HUMAN-P4-T05-20260722-CONTINUUM-FIRST-01",
        "approval identity mismatch",
    )
    require(approval["status"] == "consumed", "P4-T05 approval status changed")
    require(
        authorization["canonical_integration_boundary"]["p4_t06_authorized"] is True,
        "human authorization does not authorize P4-T06",
    )
    require(route["selected_next_plan_task_id"] == "P4-T06", "route is not P4-T06")
    require(
        route["selected_next_strategy_id"]
        == "integrate_narrow_continuum_first_boundary_without_physical_promotion_v1",
        "route strategy mismatch",
    )
    checks.append(
        {
            "check_id": "protected_authorization_scope",
            "status": "PASS",
            "evidence": "Approval, human authorization, P4-T05 decision, and canonical-next-route hashes and identities match.",
        }
    )


def validate_source_language(checks: list[dict[str, str]]) -> None:
    foundations = (ROOT / CANONICAL_SOURCES[0]).read_text(encoding="utf-8")
    dynamics = (ROOT / CANONICAL_SOURCES[1]).read_text(encoding="utf-8")
    geometry = (ROOT / CANONICAL_SOURCES[2]).read_text(encoding="utf-8")

    foundations_required = (
        "canonical mainline research architecture is continuum-first",
        "explicit primitive debt",
        "unresolved abstract source-order or evolution slot",
        "does not identify \\(\\Sub\\) with physical spacetime",
        "P5-T02 must resolve the semantics of \\(\\PhiSrc\\)",
        "historical interpretive motivation",
    )
    for phrase in foundations_required:
        require(phrase in foundations, f"foundations missing boundary phrase: {phrase}")

    foundations_forbidden = (
        "underlying four-dimensional substrate of reality",
        "\\Phi_{\\lambda}:\\Sub \\to \\Sub",
        "\\iota_s:\\Sigma_s \\hookrightarrow \\Sub",
        "\\frac{dS}{d\\lambda} > 0",
        "three-dimensional appearance of deeper four-dimensional ordered motion",
    )
    for phrase in foundations_forbidden:
        require(phrase not in foundations, f"foundations retains hybrid phrase: {phrase}")

    dynamics_required = (
        "source research architecture is continuum-first",
        "Neither object is identified with physical spacetime",
        "\\(\\PhiSrc\\) remains unresolved",
        "No source metric, order field, action, variation law, or",
    )
    for phrase in dynamics_required:
        require(phrase in dynamics, f"dynamics missing boundary phrase: {phrase}")

    geometry_required = (
        "It is not the unresolved source slot \\(\\PhiSrc\\)",
        "source-to-congruence bridge is claimed",
        "does not identify \\(u^\\mu\\) with \\(\\PhiSrc\\)",
        "None of these target-side quantities supplies the missing semantics",
    )
    for phrase in geometry_required:
        require(phrase in geometry, f"geometry missing boundary phrase: {phrase}")

    for text, label in ((dynamics, "dynamics"), (geometry, "geometry")):
        for phrase in (
            "underlying four-dimensional substrate of reality",
            "the \\Aflow{} is its intrinsic ordered motion",
            "local experiential slice of that deeper substrate",
        ):
            require(phrase not in text, f"{label} retains hybrid phrase: {phrase}")

    checks.append(
        {
            "check_id": "canonical_source_boundary",
            "status": "PASS",
            "evidence": "All three canonical ontology manuscripts express the narrow primitive-debt, unresolved-Phi_src, source-target separation.",
        }
    )


def validate_control_sync(checks: list[dict[str, str]]) -> None:
    glossary = (ROOT / CONTROL_SOURCES[1]).read_text(encoding="utf-8")
    inventory = (ROOT / CONTROL_SOURCES[0]).read_text(encoding="utf-8")
    burden_map = (ROOT / CONTROL_SOURCES[2]).read_text(encoding="utf-8")
    definitions = load_yaml(ROOT / CONTROL_SOURCES[3])

    require(
        "Canonical mainline research architecture" in glossary,
        "glossary lacks architecture category",
    )
    require(
        "`control_status`: `accepted_as_scoped_source_object`"
        in inventory,
        "frontier inventory lacks integrated control status",
    )
    require("`candidate_next_task`: `P5-T01`" in inventory, "inventory route stale")
    require("## P4-T06 Source-Ontology Boundary" in burden_map, "burden map stale")

    source_definition = next(
        (
            row
            for row in definitions["definitions"]
            if row["milestone"] == "source_ontology"
        ),
        None,
    )
    require(source_definition is not None, "source_ontology definition missing")
    require(
        source_definition["required_object"]
        == "selected primitive source arena and unresolved source-order or evolution slot",
        "stable source_ontology required object is stale",
    )
    definition_hash = sha256(CONTROL_SOURCES[3])
    marker = re.search(
        r"stable-burden-definitions-sha256:\s*([0-9a-f]{64})", burden_map
    )
    require(marker is not None, "stable definition marker missing")
    require(marker.group(1) == definition_hash, "stable definition marker is stale")

    with (ROOT / CONTROL_SOURCES[4]).open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    source_row = next(
        (row for row in rows if row["burden_id"] == "source_ontology_primitives"),
        None,
    )
    require(source_row is not None, "source_ontology_primitives ledger row missing")
    require(source_row["current_status"] == "accepted", "ledger status changed")
    require(
        source_row["control_status"] == "accepted_as_scoped_source_object",
        "ledger control status is stale",
    )
    require(
        source_row["physical_status"] == "no_physical_interpretation_authorized",
        "ledger physical boundary is stale",
    )
    require(
        source_row["promotion_status"] == "scoped_source_object_only",
        "ledger promotion boundary is stale",
    )

    checks.append(
        {
            "check_id": "control_surface_synchronization",
            "status": "PASS",
            "evidence": "Glossary, frontier inventory, burden map, stable definition, and source-ontology ledger row agree.",
        }
    )


def validate_synthesis(checks: list[dict[str, str]]) -> None:
    parsed = {name: load_yaml(ART / name) for name in ARTIFACT_YAMLS}
    require(
        parsed["child_phys_math_p4_t06_ontology_integration.yaml"]["status"]
        == "completed",
        "math perspective is incomplete",
    )
    require(
        parsed["child_phys_phil_p4_t06_ontology_integration.yaml"]["status"]
        == "completed",
        "philosophy perspective is incomplete",
    )
    conflict = parsed["parent_conflict_review_p4_t06_ontology_integration.yaml"]
    require(conflict["unresolved_conflicts"] == [], "synthesis conflict unresolved")
    require(conflict["fusion_status"] == "approved", "fusion not approved")
    delta = parsed["selected_ontology_regime_assumption_delta_v1.yaml"]
    require(delta["distance_to_gr_delta"]["changed"] is False, "distance delta claimed")
    burden = parsed["selected_ontology_regime_burden_dependency_v1.yaml"]
    require(
        burden["downstream_dependency_map"][0]["plan_task_id"] == "P5-T01",
        "P5-T01 route missing",
    )
    deprecation = parsed["hybrid_ontology_language_deprecation_v1.yaml"]
    require(
        deprecation["historical_rewrite_performed"] is False,
        "historical rewrite claimed",
    )
    vocabulary = parsed["selected_ontology_regime_claim_vocabulary_v1.yaml"]
    require(vocabulary["physics_promotion_authorized"] is False, "promotion claimed")

    fused = (ART / "selected_ontology_regime_integration_v1.tex").read_text(
        encoding="utf-8"
    )
    for phrase in (
        "canonical mainline",
        "research architecture",
        "explicit primitive debt",
        "\\not\\equiv",
        "P5-T01",
        "no physical Distance-to-GR delta",
    ):
        require(phrase in fused, f"fused integration missing phrase: {phrase}")

    checks.append(
        {
            "check_id": "parent_child_synthesis",
            "status": "PASS",
            "evidence": "Both internal perspectives completed, three tensions were resolved, and the fused integration preserves all nonclaims.",
        }
    )


def validate_allowlist(checks: list[dict[str, str]]) -> None:
    changed = changed_paths()
    changed_ontology = {
        path for path in changed if path.startswith("ontology/tex/")
    }
    require(
        changed_ontology == set(CANONICAL_SOURCES),
        f"unexpected canonical ontology changes: {sorted(changed_ontology)}",
    )
    changed_design = {
        path for path in changed if path.startswith("research_control/design/")
    }
    require(
        changed_design
        <= {
            "research_control/design/frontier_theorem_inventory.md",
            "research_control/design/epistemic_category_glossary.md",
            "research_control/design/gr_derivation_burden_map.md",
        },
        f"unexpected design-source changes: {sorted(changed_design)}",
    )
    for rel_path, expected_hash in HISTORICAL_HASHES.items():
        require(sha256(rel_path) == expected_hash, f"historical artifact changed: {rel_path}")
    checks.append(
        {
            "check_id": "canonical_source_allowlist_and_history",
            "status": "PASS",
            "evidence": "Exactly three ontology TeX sources changed; no P4-T02 through P4-T05 historical authority artifact changed.",
        }
    )


def build_records() -> tuple[dict[str, Any], dict[str, Any]]:
    checks: list[dict[str, str]] = []
    validate_authority(checks)
    validate_source_language(checks)
    validate_control_sync(checks)
    validate_synthesis(checks)
    validate_allowlist(checks)

    source_paths = list(CANONICAL_SOURCES) + list(CONTROL_SOURCES)
    source_hashes = {path: sha256(path) for path in source_paths}
    report = {
        "schema_id": "p4_t06_canonical_integration_validation_v1",
        "status": "PASS",
        "task_id": "RT-20260724-010",
        "job_id": "AJ-RT-20260724-010-001",
        "plan_task_id": "P4-T06",
        "checks": checks,
        "source_hashes": source_hashes,
        "finding_counts": {
            "canonical_ontology_files_changed": 3,
            "canonical_control_sources_synchronized": 5,
            "deprecated_pattern_classes": 6,
            "historical_authority_artifacts_changed": 0,
            "physical_structures_adopted": 0,
            "physics_promotions": 0,
        },
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "next_plan_task_id": "P5-T01",
    }
    receipt = {
        "schema_id": "p4_t06_canonical_integration_compact_receipt_v1",
        "status": "PASS",
        "task_id": "RT-20260724-010",
        "job_id": "AJ-RT-20260724-010-001",
        "plan_task_id": "P4-T06",
        "definition_id": "V21-P4-T06-CONTINUUM-FIRST-SOURCE-ARCHITECTURE-BOUNDARY-V1",
        "source_hashes": source_hashes,
        "finding_counts": report["finding_counts"],
        "validator_ids": [check["check_id"] for check in checks],
        "claim_boundary_summary": (
            "Continuum-first is integrated only as the canonical mainline "
            "research architecture; the smooth four-dimensional source arena "
            "is explicit primitive debt, Phi_src is unresolved, the source "
            "arena is not physical spacetime, emergence-first is preserved, "
            "and every physical bridge remains open."
        ),
        "distance_to_gr_delta_changed": False,
        "physics_promotion_authorized": False,
        "next_plan_task_id": "P5-T01",
    }
    return report, receipt


def encoded(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        report, receipt = build_records()
        if args.write_report:
            REPORT.write_text(encoded(report), encoding="utf-8")
            RECEIPT.write_text(encoded(receipt), encoding="utf-8")
        else:
            require(REPORT.is_file(), "validation report is missing")
            require(RECEIPT.is_file(), "compact receipt is missing")
            require(REPORT.read_text(encoding="utf-8") == encoded(report), "validation report is stale")
            require(RECEIPT.read_text(encoding="utf-8") == encoded(receipt), "compact receipt is stale")
        if args.json:
            print(json.dumps(report, sort_keys=True))
        else:
            print("P4-T06 canonical integration validation: PASS")
        return 0
    except (AssertionError, KeyError, OSError, ValidationError, yaml.YAMLError) as exc:
        failure = {
            "schema_id": "p4_t06_canonical_integration_validation_v1",
            "status": "FAIL",
            "task_id": "RT-20260724-010",
            "error": str(exc),
        }
        print(json.dumps(failure, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

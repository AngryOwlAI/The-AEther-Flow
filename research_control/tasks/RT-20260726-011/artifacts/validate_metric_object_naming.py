#!/usr/bin/env python3
"""Validate the bounded P6-T07 metric-object naming integration."""

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
TASK = ROOT / "research_control/tasks/RT-20260726-011"
ART = TASK / "artifacts"

HISTORICAL_HASHES = {
    "research_control/tasks/RT-20260614-216/artifacts/"
    "245_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_METRICFORMASSIGN_"
    "GEFF_CANDIDATE_OR_OBSTRUCTION.tex": (
        "dd30573519ed1df66b3800d29ee0adc9fcc94d9c8d3b9b5a7fcffde503d5f0ef"
    ),
    "research_control/tasks/RT-20260614-222/artifacts/"
    "251_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_GEFF_CANDIDATE_"
    "SCOPED_SOURCE_EXTENSION_ADOPTION_GATE_CHAIR_REVIEW.tex": (
        "3ce8cbc6cd79c6852d78f81045633beea44c4dfc6e2912c604b08e3c8bdb0257"
    ),
    "ontology/tex/aether_flow_geometry.tex": (
        "f60a81b63f814b03cca7190b3ac6285842a55317f4aed058cc6e75154cc0b4d7"
    ),
}

CONTROL_SURFACES = {
    "research_control/design/distance_to_gr_status_aliases.yaml",
    "research_control/design/accepted_status_calibration_v1.yaml",
    "research_control/design/accepted_status_calibration_v2.yaml",
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "registries/METRIC_USE_LEDGER.csv",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} did not contain a mapping")
    return value


def add_check(checks: list[dict[str, Any]], check_id: str, ok: bool, detail: str) -> None:
    checks.append(
        {
            "check_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
        }
    )


def classify_reference(path: str) -> str:
    if path.startswith("wiki/") or path.startswith("output/"):
        return "generated_derivative"
    if path.startswith("research_control/tasks/RT-20260614-"):
        return "immutable_historical_task_evidence"
    if path.startswith("research_control/tasks/RT-20260726-011/"):
        return "current_task"
    if path in CONTROL_SURFACES or path == "research_control/current_frontier.md":
        return "current_control_surface"
    if path.startswith("implementations_plans/") or path.startswith(".agents/"):
        return "plan_role_or_schema"
    if path.startswith("research_control/tasks/"):
        return "tracked_task_evidence"
    return "tracked_source_or_control"


def reference_audit() -> dict[str, Any]:
    tracked = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8").split("\0")
    candidates = {item for item in tracked if item}
    for path in TASK.rglob("*"):
        if path.is_file():
            candidates.add(path.relative_to(ROOT).as_posix())

    rows: list[dict[str, Any]] = []
    token_count = 0
    for relative in sorted(candidates):
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size > 5_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        count = text.count("g_eff") + text.count("\\geff") + text.count("ScopedMetricStructureRecord")
        if count:
            rows.append(
                {
                    "path": relative,
                    "classification": classify_reference(relative),
                    "reference_count": count,
                    "current_mutation": relative in CONTROL_SURFACES
                    or relative.startswith("research_control/tasks/RT-20260726-011/"),
                }
            )
            token_count += count
    return {
        "schema_id": "p6_t07_g_eff_reference_audit_v1",
        "task_id": "RT-20260726-011",
        "status": "PASS",
        "scope": "all tracked text files plus current task files; path-level bounded classification",
        "path_count": len(rows),
        "reference_count": token_count,
        "class_counts": {
            classification: sum(
                1 for row in rows if row["classification"] == classification
            )
            for classification in sorted({row["classification"] for row in rows})
        },
        "rows": rows,
        "authority_note": (
            "Historical wording is preserved as provenance. Only current claim-bearing "
            "surfaces are migrated; generated derivatives are non-authoritative."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        default=str(ART / "metric_object_naming_validation_receipt_v1.json"),
    )
    parser.add_argument(
        "--audit-output",
        default=str(ART / "g_eff_reference_audit_v1.json"),
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []
    decision = load_yaml(ART / "metric_object_naming_decision_v1.yaml")
    migration = load_yaml(ART / "metric_object_alias_migration_plan_v1.yaml")
    gate_b = load_yaml(ART / "gate_b_readiness_verdict_v1.yaml")
    aliases = load_yaml(ROOT / "research_control/design/distance_to_gr_status_aliases.yaml")
    calibration_v1 = load_yaml(
        ROOT / "research_control/design/accepted_status_calibration_v1.yaml"
    )
    calibration_v2 = load_yaml(
        ROOT / "research_control/design/accepted_status_calibration_v2.yaml"
    )

    primary = decision.get("primary_object", {})
    legacy = decision.get("legacy_alias", {})
    add_check(
        checks,
        "primary_type",
        primary.get("type_name") == "ScopedMetricStructureRecord_src",
        "Primary type is ScopedMetricStructureRecord_src.",
    )
    add_check(
        checks,
        "exact_field_order",
        primary.get("field_order")
        == ["D_E", "Q_E", "S_E", "Theta_E", "N_E", "B_E", "F_E", "C_E", "O_E", "L_E"],
        "Historical ten-slot field order is exact.",
    )
    add_check(
        checks,
        "legacy_alias",
        legacy.get("resolution") == "exact_alias_to_primary_object"
        and legacy.get("scope_expansion_allowed") is False,
        "Historical g_eff^{GSC-cand} is an exact no-expansion alias.",
    )
    add_check(
        checks,
        "bare_geff_unresolved",
        decision.get("reserved_burden_name", {}).get(
            "extant_unscoped_physical_metric_instance"
        )
        is False,
        "Bare g_eff names an unresolved burden, not an extant physical metric.",
    )
    add_check(
        checks,
        "comparison_forms_distinct",
        decision.get("comparison_controls", {}).get("alias_instances") is False
        and decision.get("comparison_controls", {}).get("physical_geometry_adopted")
        is False,
        "Gate-B comparison forms are neither alias instances nor adopted geometry.",
    )
    add_check(
        checks,
        "target_metric_distinct",
        decision.get("target_object", {}).get("alias_of_primary_object") is False,
        "The exact-GR target metric remains distinct.",
    )
    add_check(
        checks,
        "gate_b_zero_of_eight",
        gate_b.get("criterion_count") == 8
        and gate_b.get("met_count") == 0
        and gate_b.get("unmet_count") == 8
        and gate_b.get("verdict") == "not_ready"
        and all(row.get("status") == "not_met" for row in gate_b.get("criteria", [])),
        "All eight Gate B criteria remain unmet.",
    )
    add_check(
        checks,
        "next_packet",
        decision.get("selected_next_packet", {}).get("selected_next_packet_type")
        == "source_extension_smuggling_audit"
        and decision.get("selected_next_packet", {}).get("selected_next_plan_task_id")
        == "P6-T08",
        "P6-T08 independent source-extension smuggling audit is selected.",
    )
    add_check(
        checks,
        "migration_additive",
        migration.get("migration_mode") == "additive_compatibility_retype"
        and migration.get("historical_resolution", {}).get(
            "rename_historical_artifacts_in_place"
        )
        is False,
        "Migration is additive and preserves historical artifacts.",
    )

    alias_g = aliases["row_aliases"]["g_eff"]
    v1_g = calibration_v1["accepted_status_calibration_v1"]["high_risk_objects"][
        "g_eff"
    ]
    v2_g = calibration_v2["accepted_status_calibration_v2"]["high_risk_objects"][
        "g_eff"
    ]["status_card_v2"]
    add_check(
        checks,
        "alias_v1_parity",
        alias_g.get("acceptance_calibration") == v1_g,
        "Alias-map acceptance calibration exactly mirrors v1.",
    )
    add_check(
        checks,
        "alias_v2_parity",
        alias_g.get("status_card_v2") == v2_g,
        "Alias-map status card exactly mirrors v2.",
    )
    add_check(
        checks,
        "alias_primary_name",
        alias_g.get("primary_object_type") == "ScopedMetricStructureRecord_src"
        and alias_g.get("legacy_alias", {}).get("resolution")
        == "exact_alias_to_primary_object",
        "Alias map records the primary type and exact legacy resolver.",
    )

    expected_phrase = (
        "ScopedMetricStructureRecord_src is the primary name for the adopted "
        "scoped source-extension record"
    )
    for relative in sorted(CONTROL_SURFACES):
        text = (ROOT / relative).read_text(encoding="utf-8")
        add_check(
            checks,
            f"surface_primary_name:{relative}",
            expected_phrase in text or "ScopedMetricStructureRecord_src" in text,
            f"{relative} names the primary scoped record.",
        )

    for relative, expected_hash in HISTORICAL_HASHES.items():
        add_check(
            checks,
            f"historical_hash:{relative}",
            digest(ROOT / relative) == expected_hash,
            f"{relative} bytes remain unchanged.",
        )

    with (ROOT / "registries/DISTANCE_TO_GR_LEDGER.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        ledger_rows = list(csv.DictReader(handle))
    g_row = next(row for row in ledger_rows if row["burden_id"] == "g_eff")
    add_check(
        checks,
        "distance_ledger_status",
        g_row["mathematical_status"] == "scoped_source_extension_geff_object"
        and "ScopedMetricStructureRecord_src" in g_row["required_object"]
        and g_row["physical_status"]
        == "not_unscoped_lorentzian_metric_not_matter_coupling_not_einstein_equations",
        "Distance-to-GR preserves the registered layer vocabulary and physical block while recording the primary resolver.",
    )

    audit = reference_audit()
    audit_path = Path(args.audit_output)
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    add_check(
        checks,
        "reference_audit_nonempty",
        audit["path_count"] > 0 and audit["reference_count"] > 0,
        f"Classified {audit['path_count']} paths containing metric-object references.",
    )

    failures = [item for item in checks if item["status"] != "PASS"]
    receipt = {
        "schema_id": "v21_p6_t07_metric_object_naming_validation_receipt_v1",
        "task_id": "RT-20260726-011",
        "status": "PASS" if not failures else "FAIL",
        "check_count": len(checks),
        "failure_count": len(failures),
        "finding_counts": {
            "primary_object_count": 1,
            "legacy_alias_count": 1,
            "unresolved_bare_geff_count": 1,
            "gate_b_criterion_count": 8,
            "gate_b_met_count": 0,
            "reference_path_count": audit["path_count"],
        },
        "validator_ids": [
            "p6_t07_metric_object_naming_v1",
            "p6_t07_alias_parity_v1",
            "p6_t07_historical_hash_guard_v1",
            "p6_t07_reference_audit_v1",
        ],
        "claim_boundary_summary": (
            "Primary control naming and exact legacy resolution only; no historical "
            "rewrite, ontology or source-law change, physical metric, Gate B passage, "
            "matter coupling, Einstein equations, benchmark promotion, proof, or "
            "completed derivation."
        ),
        "audit_path": audit_path.relative_to(ROOT).as_posix(),
        "checks": checks,
    }
    output_path = Path(args.output)
    output_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    compact = {
        "status": receipt["status"],
        "check_count": receipt["check_count"],
        "failure_count": receipt["failure_count"],
        "receipt_path": output_path.relative_to(ROOT).as_posix(),
        "audit_path": audit_path.relative_to(ROOT).as_posix(),
    }
    if args.json:
        print(json.dumps(compact, sort_keys=True))
    else:
        print(
            f"{compact['status']}: {compact['check_count']} checks, "
            f"{compact['failure_count']} failures"
        )
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Focused deterministic validator for RT-20260810-012."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = Path(__file__).resolve().parent
REPORT = ART / "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_validation.json"

IMMUTABLE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1008.yaml":
        "589603e620e819bd184ce860d5bec20067bc29712a6d491eb6227a353e979a99",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_independent_variation_law_v1.tex":
        "6c81af99ff98b315b3867deed2658ec8123386b7d2f9fbc9517ed80b0c1f695f",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_descent_spec_v1.yaml":
        "70f25b557642d9bc4d71b92b9b05cdca045c670df775089058f4b444bfa1a4a2",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_independent_variation_law_v1.yaml":
        "bb30f36984d97f084a914b07253e872935f8f05190779a5c76a095d03235c774",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_candidate_disposition_v1.yaml":
        "1fa1e74be8c983aae376278df79c71748d97aa2e8713e0df3052b3235f7a73e0",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_model.py":
        "ff5a0d9e1973e8f5bc9a0db48e9b11afb25e17a8bc35b0d01a19097c9b8c67c8",
    "research_control/tasks/RT-20260810-010/artifacts/parent_fusion_notes_p4_t02_b2_common_character_independent_variation.md":
        "966fba0889677cc1d8ad2c6aa49af42eba793a0a9f94455b3b58170f7857f862",
    "research_control/tasks/RT-20260810-011/artifacts/v22_p4_t02_b2_common_character_independent_variation_smuggling_audit_v1.tex":
        "73285bd22fbe5c13314ef7a4d00ddabde08da4a34b8fb0596890e2867d6871f3",
    "research_control/tasks/RT-20260810-011/artifacts/v22_p4_t02_b2_common_character_independent_variation_smuggling_matrix_v1.yaml":
        "d2744f81e039fa9bd584f59e1115c6c5c462350bc3a5dcaed26e5ea2a2eb4d87",
    "research_control/tasks/RT-20260810-011/artifacts/v22_p4_t02_b2_common_character_independent_variation_smuggling_disposition_v1.yaml":
        "49db802d9c27b1f608dc2663fe29a4a25d676dde1a1230315650dd2bf9c7e272",
    "research_control/tasks/RT-20260810-011/artifacts/v22_p4_t02_b2_common_character_independent_variation_smuggling_model.py":
        "602240668c871958fde5eadb88c52fa65a8b3c1acbe457c18dcb8fecef7f2938",
    "research_control/tasks/RT-20260810-011/artifacts/parent_fusion_notes_p4_t02_b2_common_character_independent_variation_smuggling_audit.md":
        "1889d527fbf61a1da0a0cce4d86a9b30e4e5059663effbaef0297b19dda1cfa9",
    ".agents/roles/physics/refuter.v0.2.0.md":
        "01b7897ecf5861d952d7349e3eb743feed6f178112264de73f5226d3c88946fc",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}

REQUIRED_ARTIFACTS = [
    "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_v1.tex",
    "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_matrix_v1.yaml",
    "v22_p4_t02_b2_common_character_independent_variation_refuter_obstruction_v1.yaml",
    "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_model.py",
    "child_phys_math_p4_t02_b2_common_character_independent_variation_refuter_stress.yaml",
    "child_phys_phil_p4_t02_b2_common_character_independent_variation_refuter_stress.yaml",
    "parent_conflict_review_p4_t02_b2_common_character_independent_variation_refuter_stress.yaml",
    "parent_fusion_notes_p4_t02_b2_common_character_independent_variation_refuter_stress.md",
    "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_latex_compile_receipt.json",
    "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_compact_receipt.json",
]

REQUIRED_BRANCHES = {
    "STRESS-H1-INDEPENDENT-SECTOR-HOLONOMY",
    "STRESS-INTERNAL-T-MINUS-HALF-COLLAPSE",
    "STRESS-ANCHOR-ERASURE-AND-REANCHORING",
    "STRESS-SOURCE-PRESENTATION-ENLARGEMENT",
    "STRESS-POINT-AND-FRAME-NONSELECTION",
    "STRESS-ALTERNATIVE-COVECTOR",
    "STRESS-RANK-PRESERVING-BALANCE-FAMILY",
    "STRESS-INVERSE-AND-COCYCLE",
    "STRESS-FROZEN-ROUTE-CONTROLS",
}

INHERITED_FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
}
ACTIVE_FREEZE = "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION"
NEXT_PACKET = "PKT-V22-P4T02-B2-POST-COMMON-CHARACTER-REFUTER-THEORETICAL-CONTINUATION-SELECTION-V1"
NEXT_ROLE = "theoretical-continuation-selector@0.1.0"


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe loader that rejects duplicate mapping keys."""


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_mapping,
)


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contains_scalar(value: object, expected: object) -> bool:
    if value == expected:
        return True
    if isinstance(value, dict):
        return any(contains_scalar(item, expected) for item in value.values())
    if isinstance(value, list):
        return any(contains_scalar(item, expected) for item in value)
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    checks: list[dict[str, object]] = []

    def check(check_id: str, passed: bool, evidence: object) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "evidence": evidence})

    missing = [name for name in REQUIRED_ARTIFACTS if not (ART / name).is_file()]
    check("REQUIRED-ARTIFACTS", not missing, {"missing": missing})

    hash_evidence = {}
    for rel, expected in IMMUTABLE_HASHES.items():
        actual = digest(ROOT / rel)
        hash_evidence[rel] = {"expected": expected, "actual": actual, "match": expected == actual}
    check("IMMUTABLE-SOURCE-HASHES", all(row["match"] for row in hash_evidence.values()), hash_evidence)

    yaml_names = [name for name in REQUIRED_ARTIFACTS if name.endswith(".yaml")]
    parsed = {}
    yaml_errors = {}
    for name in yaml_names:
        try:
            parsed[name] = load_yaml(ART / name)
        except Exception as exc:  # deterministic error capture
            yaml_errors[name] = str(exc)
    check("UNIQUE-KEY-YAML", not yaml_errors, yaml_errors)

    matrix_name = "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_matrix_v1.yaml"
    matrix = parsed.get(matrix_name, {})
    branches = matrix.get("stress_branches", [])
    branch_ids = [row.get("branch_id") for row in branches]
    check(
        "NINE-RECORDED-BRANCHES-COVER-EIGHT-HANDOFF-FAMILIES",
        len(branches) == 9 and set(branch_ids) == REQUIRED_BRANCHES,
        branch_ids,
    )
    check(
        "EXACT-REFUTER-CLASS",
        matrix.get("decisive_refuter_class") == "scoped_obstruction"
        and matrix.get("refuter_result", {}).get("classification") == "scoped_obstruction"
        and matrix.get("no_fog_check") is True,
        {
            "decisive_refuter_class": matrix.get("decisive_refuter_class"),
            "refuter_result": matrix.get("refuter_result", {}),
            "no_fog_check": matrix.get("no_fog_check"),
        },
    )
    check(
        "FIXED-CANDIDATE-BOUNDARY-PRESERVED",
        matrix.get("candidate_held_fixed") is True
        and matrix.get("predecessor_source_purity_verdict_preserved") is True
        and matrix.get("refuter_result", {}).get("fixed_candidate_invalidated") is False,
        matrix.get("fixed_candidate_invariants", {}),
    )
    payloads = matrix.get("new_mathematical_payload", [])
    check(
        "NEW-MATHEMATICAL-PAYLOAD",
        len(payloads) >= 5 and len({row.get("payload_id") for row in payloads}) == len(payloads),
        [row.get("payload_id") for row in payloads],
    )
    dgr = matrix.get("distance_to_gr_status", [])
    check(
        "FOURTEEN-DISTANCE-ROWS-NO-DELTA",
        len(dgr) == 14 and all(row.get("task_delta") == "none" for row in dgr),
        {"count": len(dgr), "deltas": [row.get("task_delta") for row in dgr]},
    )

    declared_hashes = {}
    for row in matrix.get("source_hashes", []):
        rel = row.get("path", "")
        declared = row.get("sha256", "")
        actual = digest(ROOT / rel) if rel and (ROOT / rel).is_file() else "MISSING"
        declared_hashes[rel] = {"declared": declared, "actual": actual, "match": declared == actual}
    check(
        "MATRIX-DECLARED-SOURCE-HASHES",
        len(declared_hashes) >= 7 and all(row["match"] for row in declared_hashes.values()),
        declared_hashes,
    )

    obstruction_name = "v22_p4_t02_b2_common_character_independent_variation_refuter_obstruction_v1.yaml"
    obstruction = parsed.get(obstruction_name, {})
    record = obstruction.get("refuter_obstruction_record", {})
    compact_record = obstruction.get("obstruction_record", {})
    check(
        "PRECISE-OBSTRUCTION-RECORD",
        obstruction.get("decisive_result") == "scoped_obstruction"
        and obstruction.get("no_fog_check") is True
        and record.get("minimal_countermodel_available") is True
        and record.get("source_extension_repair_possible") is True
        and compact_record.get("present") is True
        and compact_record.get("scope") == "source_extension_candidate",
        {"record": record, "compact_record": compact_record},
    )
    counters = obstruction.get("exact_countermodels", {})
    check(
        "EXACT-COUNTERMODEL-CERTIFICATES",
        counters.get("h1_family", {}).get("arbitrarily_small") is True
        and counters.get("h1_family", {}).get("representation_syntax_preserved") is True
        and counters.get("internal_flow_collapse", {}).get("mu") == 0
        and counters.get("internal_flow_collapse", {}).get("all_transition_factors") == 1
        and counters.get("internal_flow_collapse", {}).get("formal_descent_survives") is True
        and counters.get("balance_family", {}).get("rank_preserved") == 2
        and counters.get("balance_family", {}).get("quotient_dimension_preserved") == 1,
        counters,
    )
    freeze = obstruction.get("freeze_criteria_status", {})
    check(
        "THREE-LOCAL-FREEZES",
        freeze.get("freeze_decision") == "locally_frozen"
        and freeze.get("active_freeze_label") == ACTIVE_FREEZE
        and set(freeze.get("preserved_freeze_labels", [])) == INHERITED_FREEZES,
        freeze,
    )
    route = obstruction.get("selected_next_route", {})
    check(
        "ONE-UNEXECUTED-THEORETICAL-SELECTOR",
        route.get("packet_id") == NEXT_PACKET
        and route.get("role_family") == NEXT_ROLE
        and route.get("selected") is True
        and route.get("admitted") is False
        and route.get("executed") is False,
        route,
    )
    limits = obstruction.get("authority_limits", {})
    required_false = [
        "global_no_go_claim_authorized",
        "future_source_extension_impossibility_authorized",
        "source_purity_verdict_reversed",
        "fixed_candidate_conditional_algebra_refuted",
        "source_law_adopted_or_rejected",
        "canonical_ontology_modified",
        "d7_adequacy_reevaluated",
        "b2_activated_or_disposed",
        "p4_t03_unlocked",
        "physical_or_empirical_meaning_assigned",
        "effective_metric_constructed",
        "distance_to_gr_changed",
        "proof_authority",
        "publication_authorized",
        "push_authorized",
        "external_action_authorized",
        "completed_derivation_claimed",
        "successor_executed",
    ]
    check(
        "AUTHORITY-BLOCKS",
        all(limits.get(key) is False for key in required_false),
        {key: limits.get(key) for key in required_false},
    )

    child_names = [
        "child_phys_math_p4_t02_b2_common_character_independent_variation_refuter_stress.yaml",
        "child_phys_phil_p4_t02_b2_common_character_independent_variation_refuter_stress.yaml",
    ]
    child_results = {name: contains_scalar(parsed.get(name, {}), "scoped_obstruction") for name in child_names}
    child_next_roles = {name: contains_scalar(parsed.get(name, {}), NEXT_ROLE) for name in child_names}
    check("CHILD-REFUTER-RESULTS", all(child_results.values()), child_results)
    check("CHILD-NEXT-ROUTE-RECORDED", all(child_next_roles.values()), child_next_roles)

    conflict_name = "parent_conflict_review_p4_t02_b2_common_character_independent_variation_refuter_stress.yaml"
    conflict = parsed.get(conflict_name, {})
    conflict_policy = conflict.get("conflict_policy_result", {})
    child_hash_checks = {}
    for row in conflict.get("child_inputs", []):
        rel = row.get("path", "")
        declared = row.get("sha256", "")
        actual = digest(ROOT / rel) if rel and (ROOT / rel).is_file() else "MISSING"
        child_hash_checks[rel] = {"declared": declared, "actual": actual, "match": declared == actual}
    check(
        "PARENT-CONFLICT-RESOLVED",
        conflict_policy.get("unresolved_blocking_conflict") is False
        and conflict.get("final_parent_verdict") == "scoped_obstruction"
        and len(child_hash_checks) == 2
        and all(row["match"] for row in child_hash_checks.values()),
        {"policy": conflict_policy, "child_hashes": child_hash_checks},
    )

    model_run = subprocess.run(
        [
            str(ROOT / ".venv/bin/python"),
            str(ART / "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_model.py"),
            "--json",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        model_report = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model_report = {"status": "UNPARSEABLE", "stdout": model_run.stdout, "stderr": model_run.stderr}
    check(
        "EXACT-REFUTER-MODEL",
        model_run.returncode == 0
        and model_report.get("status") == "PASS"
        and model_report.get("check_count") == 34,
        model_report,
    )

    tex_path = ART / "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.exists() else ""
    required_tex_tokens = [
        "scoped obstruction",
        "source pure as written",
        "Transverse $H^1$ instability",
        "Admitted transition-collapse point",
        "Rank-preserving balance-law family",
        "Eight-branch disposition",
        "Distance-to-GR matrix",
        ACTIVE_FREEZE,
        "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
        "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
        NEXT_PACKET,
    ]
    check(
        "TEX-SEMANTIC-TOKENS",
        all(token in tex for token in required_tex_tokens),
        {token: token in tex for token in required_tex_tokens},
    )

    receipt_path = ART / "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_latex_compile_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.exists() else {}
    check(
        "LATEX-RENDER-RECEIPT",
        receipt.get("status") == "PASS"
        and receipt.get("source_sha256") == (digest(tex_path) if tex_path.exists() else "")
        and receipt.get("page_count", 0) > 0
        and receipt.get("overfull_boxes") == 0
        and receipt.get("visual_review", {}).get("all_pages_inspected") is True
        and receipt.get("visual_review", {}).get("result") == "PASS",
        receipt,
    )

    task = load_yaml(ROOT / "research_control/tasks/RT-20260810-012/00_TASK.yaml")
    job = load_yaml(ROOT / "research_control/tasks/RT-20260810-012/jobs/AJ-RT-20260810-012-001.yaml")
    role = load_yaml(ROOT / "research_control/tasks/RT-20260810-012/roles/refuter@0.2.0--RT-20260810-012.yaml")
    completion_path = ROOT / "research_control/tasks/RT-20260810-012/jobs/completions/AJC-AJ-RT-20260810-012-001.yaml"
    completion = load_yaml(completion_path) if completion_path.exists() else {}
    handoff_path = ROOT / "research_control/handoffs/handoff-1009.yaml"
    handoff = load_yaml(handoff_path) if handoff_path.exists() else {}
    check(
        "CONTROL-TERMINAL-STATE",
        task.get("status") == "completed"
        and job.get("status") == "completed"
        and role.get("status") == "completed"
        and completion.get("completion_status") == "PASS"
        and handoff.get("handoff_id") == "handoff-1009",
        {
            "task_status": task.get("status"),
            "job_status": job.get("status"),
            "role_status": role.get("status"),
            "completion_status": completion.get("completion_status"),
            "handoff_id": handoff.get("handoff_id"),
        },
    )

    report = {
        "schema_id": "v22_p4_t02_b2_common_character_independent_variation_refuter_stress_validation_v1",
        "task_id": "RT-20260810-012",
        "job_id": "AJ-RT-20260810-012-001",
        "status": "PASS" if all(item["passed"] for item in checks) else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "authority": "validation evidence only; not theorem proof, ontology adoption, physics promotion, or Distance-to-GR credit",
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rendered = json.dumps(report, indent=2, sort_keys=True)
    print(rendered if args.json else rendered)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Focused deterministic validator for RT-20260810-011."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = Path(__file__).resolve().parent
REPORT = ART / "v22_p4_t02_b2_common_character_independent_variation_smuggling_validation.json"

IMMUTABLE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1007.yaml":
        "5e7cab444d0db4b373a619f59e4d9228a4e5add26ab9245c8d717905cc396a3c",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_independent_variation_law_v1.tex":
        "6c81af99ff98b315b3867deed2658ec8123386b7d2f9fbc9517ed80b0c1f695f",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_descent_spec_v1.yaml":
        "70f25b557642d9bc4d71b92b9b05cdca045c670df775089058f4b444bfa1a4a2",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_independent_variation_law_v1.yaml":
        "bb30f36984d97f084a914b07253e872935f8f05190779a5c76a095d03235c774",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_source_provenance_separation_v1.yaml":
        "8692478fa808e39bbc580ff395d34c9162786a1e67000d7bbddba54fe72e04f0",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_candidate_disposition_v1.yaml":
        "1fa1e74be8c983aae376278df79c71748d97aa2e8713e0df3052b3235f7a73e0",
    "research_control/tasks/RT-20260810-010/artifacts/v22_p4_t02_b2_common_character_model.py":
        "ff5a0d9e1973e8f5bc9a0db48e9b11afb25e17a8bc35b0d01a19097c9b8c67c8",
    "research_control/tasks/RT-20260810-010/artifacts/parent_fusion_notes_p4_t02_b2_common_character_independent_variation.md":
        "966fba0889677cc1d8ad2c6aa49af42eba793a0a9f94455b3b58170f7857f862",
    ".agents/roles/physics/smuggling-auditor.v0.2.0.md":
        "2ec5a542caffa90a54d11f0c03630fde839e92f4917d5dbd55b80b724a46c882",
    "research_control/design/gr_derivation_burden_map.md":
        "8e9d44e3a18ecc8a2430a9c42497da3eb9911c2cf6cd714c1525c5d91551835e",
    "registries/DISTANCE_TO_GR_LEDGER.csv":
        "8b3aca0b7c5cd8aca4c0e4456ca423e2b0d0d63b1fe2f2a092a604554beff642",
}

REQUIRED_ARTIFACTS = [
    "v22_p4_t02_b2_common_character_independent_variation_smuggling_audit_v1.tex",
    "v22_p4_t02_b2_common_character_independent_variation_smuggling_matrix_v1.yaml",
    "v22_p4_t02_b2_common_character_independent_variation_smuggling_disposition_v1.yaml",
    "v22_p4_t02_b2_common_character_independent_variation_smuggling_model.py",
    "child_phys_math_p4_t02_b2_common_character_independent_variation_smuggling_audit.yaml",
    "child_phys_phil_p4_t02_b2_common_character_independent_variation_smuggling_audit.yaml",
    "parent_conflict_review_p4_t02_b2_common_character_independent_variation_smuggling_audit.yaml",
    "parent_fusion_notes_p4_t02_b2_common_character_independent_variation_smuggling_audit.md",
    "v22_p4_t02_b2_common_character_independent_variation_smuggling_latex_compile_receipt.json",
]

FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


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
    check("IMMUTABLE-SOURCE-HASHES", all(x["match"] for x in hash_evidence.values()), hash_evidence)

    yaml_names = [name for name in REQUIRED_ARTIFACTS if name.endswith(".yaml")]
    parsed = {}
    yaml_errors = {}
    for name in yaml_names:
        try:
            parsed[name] = load_yaml(ART / name)
        except Exception as exc:  # deterministic error capture
            yaml_errors[name] = str(exc)
    check("UNIQUE-KEY-YAML", not yaml_errors, yaml_errors)

    matrix = parsed.get("v22_p4_t02_b2_common_character_independent_variation_smuggling_matrix_v1.yaml", {})
    dimensions = matrix.get("audit_dimensions", [])
    dimension_ids = [row.get("dimension_id") for row in dimensions]
    check("TWELVE-AUDIT-DIMENSIONS", len(dimensions) == 12 and len(set(dimension_ids)) == 12, dimension_ids)
    check("MATRIX-VERDICT", matrix.get("decisive_verdict") == "source_pure_as_written", matrix.get("decisive_verdict"))
    check(
        "MATRIX-SOURCE-CLASSIFICATION",
        matrix.get("source_extension_classification", {}).get("classification") == "new_ontology_primitive_candidate",
        matrix.get("source_extension_classification", {}),
    )
    check("NEW-MATHEMATICAL-PAYLOAD", len(matrix.get("new_mathematical_audit_payload", [])) >= 1, matrix.get("new_mathematical_audit_payload", []))

    disposition = parsed.get("v22_p4_t02_b2_common_character_independent_variation_smuggling_disposition_v1.yaml", {})
    check("DISPOSITION-VERDICT", disposition.get("decisive_result") == "source_pure_as_written", disposition.get("decisive_result"))
    dgr = disposition.get("distance_to_gr_status", [])
    check(
        "FOURTEEN-DISTANCE-ROWS",
        len(dgr) == 14 and all(row.get("task_delta") == "none" for row in dgr),
        {"count": len(dgr), "deltas": [row.get("task_delta") for row in dgr]},
    )
    freeze_block = disposition.get("freeze_criteria_status", {})
    check("BOTH-FREEZES-PRESERVED", set(freeze_block.get("preserved_freeze_labels", [])) == FREEZES, freeze_block)
    route = disposition.get("selected_next_route", {})
    check(
        "ONE-UNEXECUTED-REFUTER-PACKET",
        route.get("packet_id") == "PKT-V22-P4T02-B2-COMMON-CHARACTER-INDEPENDENT-VARIATION-REFUTER-STRESS-V1"
        and route.get("role_family") == "refuter@0.2.0"
        and route.get("selected") is True
        and route.get("executed_in_rt011") is False,
        route,
    )
    limits = disposition.get("authority_limits", {})
    required_false = [
        "current_ontology_derivation_claimed",
        "source_law_adopted",
        "physical_or_empirical_meaning_assigned",
        "all_p7_sector_universality_established",
        "d7_adequacy_reevaluated",
        "b2_activated_or_disposed",
        "p4_t03_unlocked",
        "effective_metric_constructed",
        "distance_to_gr_changed",
        "proof_authority",
        "global_no_go_claimed",
    ]
    check("AUTHORITY-BLOCKS", all(limits.get(key) is False for key in required_false), {key: limits.get(key) for key in required_false})

    child_verdicts = {}
    for key, name in (
        ("math", "child_phys_math_p4_t02_b2_common_character_independent_variation_smuggling_audit.yaml"),
        ("phil", "child_phys_phil_p4_t02_b2_common_character_independent_variation_smuggling_audit.yaml"),
    ):
        data = parsed.get(name, {})
        child_verdicts[key] = (
            data.get("audit_verdict")
            or data.get("decisive_result")
            or data.get("decisive_verdict")
            or data.get("verdict")
            or data.get("decisive_audit", {}).get("audit_verdict")
        )
    check("CHILD-VERDICTS-RECORDED", all(value in {"source_pure_as_written", "repair_required", "forbidden_target_import", "precise_obstruction"} for value in child_verdicts.values()), child_verdicts)

    conflict = parsed.get("parent_conflict_review_p4_t02_b2_common_character_independent_variation_smuggling_audit.yaml", {})
    conflict_policy = conflict.get("conflict_policy_result", {})
    check(
        "PARENT-CONFLICT-RESOLVED",
        conflict_policy.get("unresolved_blocking_conflict") is False
        and conflict.get("final_parent_verdict") == "source_pure_as_written",
        conflict,
    )

    model_run = subprocess.run(
        [str(ROOT / ".venv/bin/python"), str(ART / "v22_p4_t02_b2_common_character_independent_variation_smuggling_model.py"), "--json"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        model_report = json.loads(model_run.stdout)
    except json.JSONDecodeError:
        model_report = {"status": "UNPARSEABLE", "stdout": model_run.stdout, "stderr": model_run.stderr}
    check("EXACT-AUDIT-MODEL", model_run.returncode == 0 and model_report.get("status") == "PASS", model_report)

    tex_path = ART / "v22_p4_t02_b2_common_character_independent_variation_smuggling_audit_v1.tex"
    tex = tex_path.read_text(encoding="utf-8") if tex_path.exists() else ""
    required_tex_tokens = [
        "source pure as written",
        "codimension two",
        "epistemic independence",
        "Distance-to-GR matrix",
        "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
        "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
        "PKT-V22-P4T02-B2-COMMON-CHARACTER-INDEPENDENT-VARIATION-REFUTER-STRESS-V1",
    ]
    check("TEX-SEMANTIC-TOKENS", all(token in tex for token in required_tex_tokens), {token: token in tex for token in required_tex_tokens})

    receipt_path = ART / "v22_p4_t02_b2_common_character_independent_variation_smuggling_latex_compile_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.exists() else {}
    check(
        "LATEX-RENDER-RECEIPT",
        receipt.get("status") == "PASS"
        and receipt.get("source_sha256") == (digest(tex_path) if tex_path.exists() else "")
        and receipt.get("page_count", 0) > 0
        and receipt.get("visual_review", {}).get("result") == "PASS",
        receipt,
    )

    task = load_yaml(ROOT / "research_control/tasks/RT-20260810-011/00_TASK.yaml")
    job = load_yaml(ROOT / "research_control/tasks/RT-20260810-011/jobs/AJ-RT-20260810-011-001.yaml")
    completion_path = ROOT / "research_control/tasks/RT-20260810-011/jobs/completions/AJC-AJ-RT-20260810-011-001.yaml"
    completion = load_yaml(completion_path) if completion_path.exists() else {}
    handoff_path = ROOT / "research_control/handoffs/handoff-1008.yaml"
    handoff = load_yaml(handoff_path) if handoff_path.exists() else {}
    check(
        "CONTROL-TERMINAL-STATE",
        task.get("status") == "completed"
        and job.get("status") == "completed"
        and completion.get("completion_status") == "PASS"
        and handoff.get("handoff_id") == "handoff-1008",
        {
            "task_status": task.get("status"),
            "job_status": job.get("status"),
            "completion_status": completion.get("completion_status"),
            "handoff_id": handoff.get("handoff_id"),
        },
    )

    report = {
        "schema_id": "v22_p4_t02_b2_common_character_independent_variation_smuggling_validation_v1",
        "task_id": "RT-20260810-011",
        "job_id": "AJ-RT-20260810-011-001",
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

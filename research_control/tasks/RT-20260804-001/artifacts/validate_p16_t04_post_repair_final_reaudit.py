#!/usr/bin/env python3
"""Validate the bounded post-repair V21 P16-T04 final re-audit."""

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
TASK_ID = "RT-20260804-001"
JOB_ID = "AJ-RT-20260804-001-001"
RESULT_STATUS = "PASS_P16_T04_POST_REPAIR_FINAL_CLAIM_BOUNDARY_REAUDIT_NO_BLOCKING_OVERCLAIM"
ARTIFACTS = Path(__file__).resolve().parent
VALIDATION_PATH = ARTIFACTS / "v21_p16_t04_post_repair_validation.json"
RECEIPT_PATH = ARTIFACTS / "v21_p16_t04_post_repair_compact_receipt.json"

TASK_PATH = ROOT / f"research_control/tasks/{TASK_ID}/00_TASK.yaml"
JOB_PATH = ROOT / f"research_control/tasks/{TASK_ID}/jobs/{JOB_ID}.yaml"
ROLE_PATH = ROOT / (
    f"research_control/tasks/{TASK_ID}/roles/"
    "external-red-team-reviewer@0.1.0--RT-20260804-001.yaml"
)
COMPLETION_PATH = ROOT / (
    f"research_control/tasks/{TASK_ID}/jobs/completions/"
    "AJC-AJ-RT-20260804-001-001.yaml"
)
HANDOFF_PATH = ROOT / "research_control/handoffs/handoff-0962.yaml"

MATH_CHILD = ARTIFACTS / "child_phys_math_p16_t04_post_repair_reaudit.yaml"
PHIL_CHILD = ARTIFACTS / "child_phys_phil_p16_t04_post_repair_reaudit.yaml"
CONFLICT = ARTIFACTS / "parent_conflict_review_p16_t04_post_repair_reaudit.yaml"
FUSION = ARTIFACTS / "parent_fusion_notes_p16_t04_post_repair_reaudit.md"
REVIEW = ARTIFACTS / "p16_t04_post_repair_internal_skeptical_review.yaml"
REPORT = ARTIFACTS / "v21_p16_t04_post_repair_final_reaudit_report.md"
MATRIX = ARTIFACTS / "v21_p16_t04_post_repair_severity_matrix.yaml"
VERDICT = ARTIFACTS / "v21_p16_t04_post_repair_public_claim_verdict.yaml"

CURRENT_CONTRACT_HASHES = {
    ".agents/roles/physics/external-red-team-reviewer.v0.1.0.md": "652176faf604825f8084aa3584200e32331b8f6493bda038376bf7737995a6d7",
    ".agents/schemas/EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md": "f341828d74c15632944b2d25be4bf5e0506d60476bea90cf974d7ababcd5d840",
    "research_control/design/external_red_team_reviewer_role_design.md": "3c574cc9830b1c1a4045f45fb621b31f0b33e516754d07a3929b1832ab4c744d",
    "research_control/templates/RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml": "d021d204205b648bbf179e47afbcb632bdc93f393e50dd559dab30d02785eca8",
}

IMMUTABLE_DEPENDENCIES = {
    "research_control/tasks/RT-20260803-012/jobs/completions/AJC-AJ-RT-20260803-012-001.yaml": "32490ac7e5a57138f6de7a884825532ee17389d36634dbb9fc7f7cc076c0bf8d",
    "research_control/tasks/RT-20260803-013/jobs/completions/AJC-AJ-RT-20260803-013-001.yaml": "a0bd4691e276e5e0d97b45b734491f697deeb57ca0dc99b015bd7ea7d734fe91",
    "research_control/tasks/RT-20260803-014/jobs/completions/AJC-AJ-RT-20260803-014-001.yaml": "cf403db773c3aacc33bc127c067abf12218e56bb43f0e6dbe8de0790b31bd6a2",
    "research_control/tasks/RT-20260803-015/jobs/completions/AJC-AJ-RT-20260803-015-001.yaml": "bfec266a4824df117db6c8b4275f79df333e1294871d1b8ed769521639e6a690",
    "research_control/tasks/RT-20260803-015/artifacts/p16_t04_internal_review_label_contract_validation.json": "97edc8ab306c30ce453f978442226c9cae3fa012acf1efe842343266fb37f629",
    "research_control/tasks/RT-20260803-016/artifacts/p16_t04_internal_review_label_renderer_authority_binding_receipt.json": "6800a2456af413130aa9f0514bf376a34ac4d4da32b61e13be43b5713366e5f3",
    "research_control/tasks/RT-20260803-016/artifacts/p16_t04_validation_compatibility_recovery_receipt.json": "ddb7f69924164c10769520c76e1ca34466acad2b9910f3dfd507e4d8cc65290f",
    "research_control/tasks/RT-20260803-020/jobs/completions/AJC-AJ-RT-20260803-020-001.yaml": "95a7529a7a0c946f065b360b61d64a98a83f8dffc5f26f10375c8ce60fce2c97",
    "research_control/handoffs/handoff-0961.yaml": "462cb60c3553fe5e373b4ce30f4780e6714c2fb740fe622eb229b5d6295e908e",
}

GATE_SOURCES = {
    "research_control/tasks/RT-20260724-004/artifacts/ontology_regime_gate_chair_decision_v1.tex": "20ea795bbe93333b489e4f13601fd6bb1623f318b7847f9d2d24402c7490c934",
    "research_control/tasks/RT-20260727-004/artifacts/p6_t08_gate_b_separating_certificate_v1.yaml": "f3080ed6a6ba1d6847a3b7ed43c7a11ad7f7dae4deccd25486913ea9547f221b",
    "research_control/tasks/RT-20260729-001/artifacts/p7_t08_gate_c_decision_v1.tex": "85fbf32fb9b02aeae556149cbc5c6b51bd6fedf278a3bc401545c93e29fc4827",
    "research_control/tasks/RT-20260729-011/artifacts/p8_t07_gate_d_decision_v1.tex": "035ea88a612d861a00d0703ec2bd1094e01194c113d7ff2588e3a4ad8bf47d63",
    "research_control/tasks/RT-20260731-004/artifacts/p9_t09_gate_e_decision_v1.tex": "7f28103e40664f0a004af0134f3216932136f8efb160f0c7c59039efa5225b0b",
}

ONTOLOGY_AND_PUBLIC_SCAN_PATHS = [
    "README.md",
    "ontology/aether-and-aether-flow.md",
    "ontology/aether_flow_interpretation-lemen.md",
    "ontology/tex/aether_flow_foundations.tex",
    "ontology/tex/aether_flow_dynamics.tex",
    "ontology/tex/aether_flow_consistency.tex",
    "ontology/tex/aether_flow_relativistic_recovery.tex",
    "ontology/tex/aether_flow_geometry.tex",
    "ontology/tex/aether_flow_exact_closure_note.tex",
    "ontology/tex/aether_flow_exact_closure_sequence_overview.tex",
    "ontology/tex/aether_flow_exact_closure_flagship_article.tex",
]

COMMANDS = [
    (
        "semantic_smuggling_suite",
        [
            ".venv/bin/python",
            "research_control/tasks/RT-20260722-006/artifacts/validate_p11_t04_semantic_smuggling_suite.py",
            "--check",
            "--json",
        ],
    ),
    (
        "methodology_determinism",
        [
            ".venv/bin/python",
            "research_control/tasks/RT-20260802-008/artifacts/build_p15_t02_methodology_publication.py",
            "--check",
        ],
    ),
    (
        "methodology_boundary",
        [
            ".venv/bin/python",
            "research_control/tasks/RT-20260802-008/artifacts/validate_p15_t02_methodology_publication.py",
        ],
    ),
    (
        "explicit_ontology_and_public_claim_language",
        [
            ".venv/bin/python",
            "scripts/project_control/validate_claim_language.py",
            "--json",
            "--paths",
            *ONTOLOGY_AND_PUBLIC_SCAN_PATHS,
        ],
    ),
    (
        "strict_internal_skeptical_review",
        [
            ".venv/bin/python",
            "scripts/research_control/validate_red_team_review_artifact.py",
            REVIEW.relative_to(ROOT).as_posix(),
            "--json",
        ],
    ),
]

POSITIVE_REVIEW_KEYS = {
    "external_review_completed",
    "human_expert_review_completed",
    "independent_replication_completed",
}


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def render_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def is_truthy(value: Any) -> bool:
    if value is True:
        return True
    if isinstance(value, (int, float)) and value == 1:
        return True
    return isinstance(value, str) and value.strip().lower() in {"true", "yes", "1"}


def positive_review_claims(value: Any, source: str, prefix: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}.{key}"
            if str(key) in POSITIVE_REVIEW_KEYS and is_truthy(child):
                findings.append(f"{source}:{child_prefix}")
            findings.extend(positive_review_claims(child, source, child_prefix))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(positive_review_claims(child, source, f"{prefix}[{index}]"))
    return findings


def audit_artifact_structure() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    task = read_yaml(TASK_PATH)
    job = read_yaml(JOB_PATH)
    role = read_yaml(ROLE_PATH)
    completion = read_yaml(COMPLETION_PATH)
    handoff = read_yaml(HANDOFF_PATH)
    math_child = read_yaml(MATH_CHILD)
    phil_child = read_yaml(PHIL_CHILD)
    conflict = read_yaml(CONFLICT)
    review = read_yaml(REVIEW)
    matrix = read_yaml(MATRIX)
    verdict = read_yaml(VERDICT)

    exact_checks = {
        "task_identity": task.get("task_id") == TASK_ID,
        "task_completed": task.get("status") == "completed",
        "task_plan": (task.get("implementation_plan") or {}).get("plan_task_id") == "P16-T04",
        "task_closure": task.get("closure_status")
        == "p16_t04_qualifying_finalized_post_repair_no_blocking_overclaim",
        "job_identity": job.get("job_id") == JOB_ID,
        "job_route": (job.get("goal_receipt") or {}).get("generation") == 253
        and (job.get("goal_receipt") or {}).get("passes_consumed") == 224
        and (job.get("goal_receipt") or {}).get("worker_invocation_count") == 1
        and (job.get("goal_receipt") or {}).get("route_sha256")
        == "4691f9b1e070f2f6d42ed7d606d4af5f72d14e4fe8b14d0d3916ec138b47a56a",
        "role_identity": role.get("execution_role_ref")
        == "external-red-team-reviewer@0.1.0--RT-20260804-001",
        "completion_identity": completion.get("completion_id")
        == "AJC-AJ-RT-20260804-001-001",
        "completion_result": (completion.get("implementation_plan_receipt") or {}).get(
            "result_status"
        )
        == RESULT_STATUS,
        "handoff_identity": handoff.get("handoff_id") == "handoff-0962",
        "handoff_result": (handoff.get("plan_result") or {}).get("result_status")
        == RESULT_STATUS,
        "math_child_result": (math_child.get("result") or {}).get("result_status")
        == "PASS_CHILD_POST_REPAIR_BOUNDED_CLAIM_NONENTAILMENT",
        "phil_child_result": (phil_child.get("result") or {}).get("result_status")
        == "PASS_CHILD_POST_REPAIR_CURRENT_ROLE_LABEL_DEFECT_RESOLVED",
        "parent_conflict_resolved": conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_count") == 0
        and conflict.get("fusion_decision") == RESULT_STATUS,
        "strict_review_internal": review.get("reviewer_display_name")
        == "Internal Skeptical Reviewer"
        and review.get("reviewer_role_kind") == "scientific_adversarial_internal_review",
        "strict_review_verdict": review.get("verdict")
        == "no_blocking_defect_found_as_written",
        "matrix_result": matrix.get("result_status") == RESULT_STATUS,
        "verdict_result": verdict.get("status") == "PASS_BOUNDED_PUBLIC_CLAIMS_POST_REPAIR",
    }
    errors.extend(f"artifact_structure:{key}" for key, passed in exact_checks.items() if not passed)

    counts = matrix.get("finding_counts") or {}
    findings = matrix.get("findings") or []
    matrix_checks = {
        "finding_total": counts.get("total_findings") == 9 and len(findings) == 9,
        "zero_blocking_science": counts.get("blocking_scientific_findings") == 0,
        "zero_blocking_project": counts.get("blocking_project_system_findings") == 0,
        "zero_undisposed_high": counts.get("undisposed_critical_or_high_findings") == 0,
        "prior_blocker_resolved": any(
            item.get("finding_id") == "P16T04-POSTREPAIR-ROLE-LABEL-CONTRACT-001"
            and item.get("status") == "resolved_current_contract"
            and item.get("blocking_now") is False
            for item in findings
        ),
        "no_project_signal": matrix.get("project_improvement_signals") == [],
    }
    errors.extend(f"severity_matrix:{key}" for key, passed in matrix_checks.items() if not passed)

    typed = math_child.get("typed_claim_composition") or {}
    typed_checks = {
        "typed_schema": typed.get("schema_id") == "PostRepairClaimBoundaryNonEntailment_v1",
        "positive_atoms": set(typed.get("true_atoms") or []) == {"S", "V", "I", "M", "A", "N", "R"},
        "negative_atoms": set(typed.get("false_atoms") or []) == {"E", "D", "B", "G"},
        "countervaluation": (typed.get("countervaluation") or {}).get(
            "satisfies_explicit_claim_boundaries"
        )
        is True,
        "typed_result": typed.get("result")
        == "STRONGER_POST_REPAIR_CROSS_DOCUMENT_CLAIM_NOT_ENTAILED",
        "not_global_no_go": typed.get("global_no_go_claimed") is False,
    }
    errors.extend(f"typed_claim:{key}" for key, passed in typed_checks.items() if not passed)

    authority_keys = (
        "external_review_completed",
        "human_expert_review_completed",
        "independent_replication_completed",
        "benchmark_promotion_authorized",
        "publication_authorized",
        "public_release_authorized",
        "physics_promotion_authorized",
        "proof_authority",
    )
    authority_flags = {key: verdict.get(key) for key in authority_keys}
    if any(value is not False for value in authority_flags.values()):
        errors.append("public_verdict:positive_authority_flag")

    return {
        "exact_checks": exact_checks,
        "matrix_checks": matrix_checks,
        "typed_claim_checks": typed_checks,
        "public_authority_flags": authority_flags,
        "finding_count": len(findings),
    }, errors


def audit_hash_bindings() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    expected = {**CURRENT_CONTRACT_HASHES, **IMMUTABLE_DEPENDENCIES, **GATE_SOURCES}
    for artifact in (read_yaml(MATH_CHILD), read_yaml(PHIL_CHILD)):
        for item in artifact.get("inspected_sources") or []:
            relative = str(item.get("path") or "")
            value = str(item.get("sha256") or "")
            if relative and value:
                expected.setdefault(relative, value)
    for item in (read_yaml(VERDICT).get("source_paths") or []):
        relative = str(item.get("path") or "")
        value = str(item.get("source_sha256") or "")
        if relative and value:
            expected.setdefault(relative, value)

    checks: dict[str, Any] = {}
    for relative, expected_hash in sorted(expected.items()):
        path = ROOT / relative
        observed = digest(path) if path.is_file() else None
        checks[relative] = {
            "expected_sha256": expected_hash,
            "observed_sha256": observed,
            "match": observed == expected_hash,
        }
        if observed != expected_hash:
            errors.append(f"source_hash:{relative}")
    return {"binding_count": len(checks), "bindings": checks}, errors


def audit_current_contract() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    role_text = (ROOT / ".agents/roles/physics/external-red-team-reviewer.v0.1.0.md").read_text(
        encoding="utf-8"
    )
    schema_text = (ROOT / ".agents/schemas/EXTERNAL_RED_TEAM_REVIEW_ARTIFACT_SCHEMA.md").read_text(
        encoding="utf-8"
    )
    design_text = (ROOT / "research_control/design/external_red_team_reviewer_role_design.md").read_text(
        encoding="utf-8"
    )
    template = read_yaml(ROOT / "research_control/templates/RED_TEAM_REVIEW_ARTIFACT_TEMPLATE.yaml")
    checks = {
        "role_name_internal": 'role_name: "Internal Skeptical Reviewer"' in role_text,
        "role_kind_internal": 'role_kind: "scientific_adversarial_internal_review"' in role_text,
        "role_legacy_not_provenance": "legacy identifier" in role_text and "not evidence" in role_text,
        "schema_title_internal": "# Internal Skeptical Review Artifact Schema" in schema_text,
        "schema_legacy_not_provenance": "legacy identifier is not evidence" in schema_text,
        "design_current_internal": "current display name is `Internal Skeptical Reviewer`" in design_text,
        "template_name_internal": template.get("reviewer_display_name") == "Internal Skeptical Reviewer",
        "template_kind_internal": template.get("reviewer_role_kind")
        == "scientific_adversarial_internal_review",
    }
    errors.extend(f"current_contract:{key}" for key, passed in checks.items() if not passed)
    return {"checks": checks}, errors


def audit_firewall() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    protocol = (
        ROOT
        / "research_control/tasks/RT-20260729-012/artifacts/source_derived_benchmark_protocol_v1.tex"
    ).read_text(encoding="utf-8")
    audit = read_yaml(
        ROOT
        / "research_control/tasks/RT-20260731-001/artifacts/p9_t08_benchmark_smuggling_audit_v1.yaml"
    )
    cases = audit.get("case_audits") or []
    conclusion = audit.get("conclusion") or {}
    limits = audit.get("authority_limits") or {}
    checks = {
        "complete_edges_hypothesis": "every parent edge is complete" in protocol,
        "manifest_completeness_limit": "does not prove that the edge manifest is complete" in protocol,
        "human_knowledge_limit": "cannot erase target knowledge already held" in protocol,
        "training_prior_limit": "training data, priors" in protocol,
        "six_cases": len(cases) == 6,
        "six_inconclusive": all(item.get("outcome") == "INCONCLUSIVE" for item in cases),
        "zero_benchmark_passes": conclusion.get("benchmark_passes") == 0,
        "zero_independent_replications": conclusion.get("independent_replications") == 0,
        "manifest_not_proved": limits.get("target_import_absence_proves_manifest_completeness") is False,
    }
    errors.extend(f"firewall:{key}" for key, passed in checks.items() if not passed)
    return {"checks": checks, "case_count": len(cases)}, errors


def run_commands() -> tuple[list[dict[str, Any]], list[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for command_id, command in COMMANDS:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError:
            payload = {}
        passed = result.returncode == 0
        records.append(
            {
                "command_id": command_id,
                "command": " ".join(command),
                "exit_code": result.returncode,
                "passed": passed,
                "reported_status": payload.get("status") or payload.get("validation_status"),
                "stdout_sha256": digest_bytes(result.stdout.encode()),
                "stderr_sha256": digest_bytes(result.stderr.encode()),
            }
        )
        if not passed:
            errors.append(f"external_validator:{command_id}")
    return records, errors


def audit_registered_sources() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    checked = 0
    for relative in ("registries/MARKDOWN_SOURCE_REGISTRY.csv", "registries/TEX_SOURCE_REGISTRY.csv"):
        with (ROOT / relative).open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                source = str(row.get("path") or "")
                expected = str(row.get("source_hash") or "")
                if not source or not expected:
                    continue
                checked += 1
                path = ROOT / source
                if not path.is_file() or digest(path) != expected:
                    errors.append(f"registered_source_hash:{row.get('object_id')}:{source}")
    return {"content_address_count": checked, "mismatch_count": len(errors)}, errors


def audit_control_inventory() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    task_count = 0
    completion_count = 0
    positive_claims: list[str] = []
    for task_path in sorted((ROOT / "research_control/tasks").glob("RT-*/00_TASK.yaml")):
        task = read_yaml(task_path)
        plan = task.get("implementation_plan") or {}
        if plan.get("plan_id") != "recommendations_implementation_plan_continue_task-v21":
            continue
        task_count += 1
        task_id = str(task.get("task_id") or "")
        if task.get("status") not in {"completed", "blocked"}:
            errors.append(f"v21_task_nonterminal:{task_id}")
        job_id = str(task.get("current_job_id") or "")
        completion_path = task_path.parent / "jobs/completions" / f"AJC-{job_id}.yaml"
        if not job_id or not completion_path.is_file():
            errors.append(f"v21_completion_missing:{task_id}")
            continue
        completion_count += 1
        completion = read_yaml(completion_path)
        if completion.get("task_id") != task_id or completion.get("job_id") != job_id:
            errors.append(f"v21_completion_identity:{task_id}")
        positive_claims.extend(
            positive_review_claims(completion, completion_path.relative_to(ROOT).as_posix())
        )

    handoff_count = 0
    for handoff_path in sorted((ROOT / "research_control/handoffs").glob("handoff-*.yaml")):
        match = re.search(r"(\d+)$", handoff_path.stem)
        if not match or not 773 <= int(match.group(1)) <= 962:
            continue
        handoff = read_yaml(handoff_path)
        if not re.fullmatch(r"P\d+-T\d+", str(handoff.get("plan_task_id") or "")):
            continue
        handoff_count += 1
        positive_claims.extend(
            positive_review_claims(handoff, handoff_path.relative_to(ROOT).as_posix())
        )

    if task_count != 139:
        errors.append(f"v21_task_count:{task_count}")
    if completion_count != 139:
        errors.append(f"v21_completion_count:{completion_count}")
    if handoff_count != 143:
        errors.append(f"v21_handoff_count:{handoff_count}")
    if positive_claims:
        errors.extend(f"unsupported_positive_review_claim:{item}" for item in positive_claims)
    return {
        "v21_task_record_count": task_count,
        "v21_completion_identity_count": completion_count,
        "v21_handoff_record_count": handoff_count,
        "unsupported_positive_review_claim_count": len(positive_claims),
        "unsupported_positive_review_claims": positive_claims,
    }, errors


def artifact_hashes() -> dict[str, str]:
    paths = [MATH_CHILD, PHIL_CHILD, CONFLICT, FUSION, REVIEW, REPORT, MATRIX, VERDICT, Path(__file__)]
    return {
        path.relative_to(ROOT).as_posix(): digest(path)
        for path in paths
        if path.is_file()
    }


def build_outputs() -> tuple[dict[Path, str], dict[str, Any]]:
    errors: list[str] = []
    structure, found = audit_artifact_structure()
    errors.extend(found)
    hashes, found = audit_hash_bindings()
    errors.extend(found)
    contract, found = audit_current_contract()
    errors.extend(found)
    firewall, found = audit_firewall()
    errors.extend(found)
    command_results, found = run_commands()
    errors.extend(found)
    registered, found = audit_registered_sources()
    errors.extend(found)
    inventory, found = audit_control_inventory()
    errors.extend(found)

    status = "PASS_POST_REPAIR_QUALIFYING_FINAL_REAUDIT" if not errors else "FAIL"
    validation = {
        "schema_id": "v21_p16_t04_post_repair_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": "P16-T04",
        "status": status,
        "result_status": RESULT_STATUS if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "artifact_hashes": artifact_hashes(),
        "artifact_structure": structure,
        "source_hash_bindings": hashes,
        "current_reviewer_contract": contract,
        "firewall_boundary": firewall,
        "external_validators": command_results,
        "external_validator_pass_count": sum(item["passed"] for item in command_results),
        "registered_sources": registered,
        "control_inventory": inventory,
        "authority_boundary": {
            "scientific_status_changed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
            "proof_authority": False,
            "external_review_completed": False,
            "human_expert_review_completed": False,
            "independent_replication_completed": False,
            "benchmark_promotion_authorized": False,
            "publication_authorized": False,
            "public_release_authorized": False,
            "p16_t05_executed": False,
        },
    }
    receipt = {
        "schema_id": "v21_p16_t04_post_repair_compact_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": "P16-T04",
        "status": status,
        "result_status": validation["result_status"],
        "artifact_hashes": validation["artifact_hashes"],
        "finding_counts": {
            "total": structure["finding_count"],
            "blocking_scientific": 0,
            "blocking_project_system": 0,
            "unresolved_high_or_critical": 0,
        },
        "evidence_counts": {
            "source_hash_bindings": hashes["binding_count"],
            "registered_content_addresses": registered["content_address_count"],
            "v21_tasks": inventory["v21_task_record_count"],
            "v21_completions": inventory["v21_completion_identity_count"],
            "v21_handoffs": inventory["v21_handoff_record_count"],
            "external_validators_passed": validation["external_validator_pass_count"],
            "unsupported_positive_review_claims": inventory[
                "unsupported_positive_review_claim_count"
            ],
        },
        "prior_blocker_status": "resolved_current_internal_reviewer_contract",
        "claim_boundary_summary": (
            "The bounded post-repair P16-T04 audit resolves the current label defect, "
            "rejects entailment of external independence source derivation benchmark promotion "
            "and global no-go, and changes no science or protected authority."
        ),
        "authority_boundary": validation["authority_boundary"],
    }
    return {
        VALIDATION_PATH: render_json(validation),
        RECEIPT_PATH: render_json(receipt),
    }, validation


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-report", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    outputs, validation = build_outputs()
    if args.write_report:
        for path, text in outputs.items():
            path.write_text(text, encoding="utf-8")
    else:
        stale = [
            path.relative_to(ROOT).as_posix()
            for path, text in outputs.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != text
        ]
        if stale:
            validation["status"] = "FAIL"
            validation["result_status"] = "FAIL"
            validation["errors"].extend(f"stored_output_drift:{path}" for path in stale)
            validation["error_count"] = len(validation["errors"])
    if args.json:
        print(render_json(validation), end="")
    return 0 if validation["status"].startswith("PASS") else 1


if __name__ == "__main__":
    raise SystemExit(main())

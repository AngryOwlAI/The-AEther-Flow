#!/usr/bin/env python3
"""Validate the bounded V21 P16-T04 final claim-boundary red team."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK_ID = "RT-20260803-014"
JOB_ID = "AJ-RT-20260803-014-001"
COMPLETION_ID = "AJC-AJ-RT-20260803-014-001"
AUDIT_HEAD = "2c4c012c5b30425a2bd43f170f865a9a7033a10d"
PLAN_ID = "recommendations_implementation_plan_continue_task-v21"
PLAN_PATH = "implementations_plans/recommendations_implementation_plan_continue_task-v21.md"
RESULT_STATUS = "REPAIR_REQUIRED_P16_T04_INTERNAL_EXTERNAL_REVIEW_LABEL_CONTRACT_DRIFT"
ARTIFACTS = Path(__file__).resolve().parent
VALIDATION_PATH = ARTIFACTS / "v21_p16_t04_validation.json"
RECEIPT_PATH = ARTIFACTS / "v21_p16_t04_compact_receipt.json"

TASK_PATH = ROOT / f"research_control/tasks/{TASK_ID}/00_TASK.yaml"
JOB_PATH = ROOT / f"research_control/tasks/{TASK_ID}/jobs/{JOB_ID}.yaml"
ROLE_PATH = ROOT / (
    f"research_control/tasks/{TASK_ID}/roles/"
    "external-red-team-reviewer@0.1.0--RT-20260803-014.yaml"
)
COMPLETION_PATH = ROOT / (
    f"research_control/tasks/{TASK_ID}/jobs/completions/{COMPLETION_ID}.yaml"
)
HANDOFF_PATH = ROOT / "research_control/handoffs/handoff-0955.yaml"

MATH_CHILD = ARTIFACTS / "child_phys_math_p16_t04_final_red_team.yaml"
PHIL_CHILD = ARTIFACTS / "child_phys_phil_p16_t04_final_red_team.yaml"
CONFLICT = ARTIFACTS / "parent_conflict_review_p16_t04_final_red_team.yaml"
FUSION = ARTIFACTS / "parent_fusion_notes_p16_t04_final_red_team.md"
REPORT = ARTIFACTS / "v21_p16_t04_final_red_team_report.md"
MATRIX = ARTIFACTS / "v21_p16_t04_severity_repair_matrix.yaml"
VERDICT = ARTIFACTS / "v21_p16_t04_public_claim_verdict.yaml"

IMMUTABLE_DEPENDENCIES = {
    "research_control/handoffs/handoff-0954.yaml": (
        "fab7eaff90a4d8d22a039661e8bea73c4e2f2f95e73c01b5f750c7b5212ac099"
    ),
    "research_control/tasks/RT-20260803-012/jobs/completions/"
    "AJC-AJ-RT-20260803-012-001.yaml": (
        "32490ac7e5a57138f6de7a884825532ee17389d36634dbb9fc7f7cc076c0bf8d"
    ),
    "research_control/tasks/RT-20260803-013/jobs/completions/"
    "AJC-AJ-RT-20260803-013-001.yaml": (
        "a0bd4691e276e5e0d97b45b734491f697deeb57ca0dc99b015bd7ea7d734fe91"
    ),
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
            "research_control/tasks/RT-20260722-006/artifacts/"
            "validate_p11_t04_semantic_smuggling_suite.py",
            "--check",
            "--json",
        ],
    ),
    (
        "methodology_determinism",
        [
            ".venv/bin/python",
            "research_control/tasks/RT-20260802-008/artifacts/"
            "build_p15_t02_methodology_publication.py",
            "--check",
        ],
    ),
    (
        "methodology_boundary",
        [
            ".venv/bin/python",
            "research_control/tasks/RT-20260802-008/artifacts/"
            "validate_p15_t02_methodology_publication.py",
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


def snapshot_bytes(relative: str) -> bytes | None:
    result = subprocess.run(
        ["git", "show", f"{AUDIT_HEAD}:{relative}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    return result.stdout if result.returncode == 0 else None


def snapshot_digest(relative: str) -> str | None:
    value = snapshot_bytes(relative)
    return digest_bytes(value) if value is not None else None


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
    matrix = read_yaml(MATRIX)
    verdict = read_yaml(VERDICT)
    math_child = read_yaml(MATH_CHILD)
    phil_child = read_yaml(PHIL_CHILD)
    conflict = read_yaml(CONFLICT)

    exact_checks = {
        "task_identity": task.get("task_id") == TASK_ID,
        "task_plan": (task.get("implementation_plan") or {}).get("plan_task_id") == "P16-T04",
        "task_closure": task.get("closure_status")
        == "repair_required_internal_external_review_label_contract_drift",
        "job_identity": job.get("job_id") == JOB_ID,
        "job_route": (job.get("goal_receipt") or {}).get("generation") == 244
        and (job.get("goal_receipt") or {}).get("worker_invocation_count") == 1
        and (job.get("goal_receipt") or {}).get("route_sha256")
        == "46eeff9bbcfbd0773eecb4e745e34ebfd041ec27f61f769b8012409e74d51f57",
        "role_identity": role.get("execution_role_ref")
        == "external-red-team-reviewer@0.1.0--RT-20260803-014",
        "role_internal_provenance": str(role.get("provisional_role_name") or "").startswith(
            "Internal same-context"
        )
        and "classify this execution as same-context internal AI review"
        in (role.get("added_constraints") or []),
        "completion_identity": completion.get("completion_id") == COMPLETION_ID
        and completion.get("job_id") == JOB_ID
        and completion.get("task_id") == TASK_ID,
        "completion_result": (completion.get("implementation_plan_receipt") or {}).get(
            "result_status"
        )
        == RESULT_STATUS,
        "handoff_identity": handoff.get("handoff_id") == "handoff-0955"
        and handoff.get("plan_task_id") == "P16-T04",
        "handoff_result": (handoff.get("plan_result") or {}).get("result_status")
        == RESULT_STATUS,
        "math_child_result": (math_child.get("result") or {}).get("result_status")
        == "PASS_CHILD_BOUNDED_CLAIM_NONENTAILMENT",
        "phil_child_result": (phil_child.get("result") or {}).get("result_status")
        == "REPAIR_REQUIRED_CHILD_INTERNAL_EXTERNAL_ROLE_LABEL_DRIFT",
        "parent_conflict_resolved": conflict.get("status") == "resolved"
        and conflict.get("blocking_conflict_count") == 0
        and conflict.get("fusion_decision") == RESULT_STATUS,
        "matrix_result": matrix.get("result_status") == RESULT_STATUS,
        "verdict_result": verdict.get("status") == "REPAIR_REQUIRED_CURRENT_REVIEW_LABEL_CONTRACT",
    }
    errors.extend(f"artifact_structure:{key}" for key, passed in exact_checks.items() if not passed)

    counts = matrix.get("finding_counts") or {}
    findings = matrix.get("findings") or []
    open_repairs = [item for item in findings if item.get("status") == "open_repair_required"]
    signals = matrix.get("project_improvement_signals") or []
    matrix_checks = {
        "finding_total": counts.get("total_findings") == 9 and len(findings) == 9,
        "no_undisposed_high_guard": counts.get("undisposed_critical_or_high_findings") == 0,
        "one_blocking_project_finding": counts.get("blocking_project_system_findings") == 1,
        "zero_blocking_science": counts.get("blocking_scientific_findings") == 0,
        "one_exact_open_repair": len(open_repairs) == 1
        and open_repairs[0].get("finding_id") == "P16T04-ROLE-LABEL-CONTRACT-001",
        "one_exact_signal": len(signals) == 1
        and signals[0].get("signal_id") == "PIS-RT-20260803-014-001"
        and signals[0].get("status") == "open",
    }
    errors.extend(f"severity_matrix:{key}" for key, passed in matrix_checks.items() if not passed)

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
    verdict_authority = {key: verdict.get(key) for key in authority_keys}
    if any(value is not False for value in verdict_authority.values()):
        errors.append("public_verdict:positive_authority_flag")

    typed = math_child.get("typed_claim_composition") or {}
    countervaluation = typed.get("countervaluation") or {}
    typed_checks = {
        "typed_nonentailment": typed.get("result") == "STRONGER_CROSS_DOCUMENT_CLAIM_NOT_ENTAILED",
        "positive_atoms": set(countervaluation.get("true_atoms") or []) == {"S", "V", "I", "M", "A", "N"},
        "negative_atoms": set(countervaluation.get("false_atoms") or []) == {"E", "D", "G"},
        "claim_rules_satisfied": countervaluation.get("satisfies_registered_claim_rules") is True,
        "not_global_no_go": typed.get("global_no_go_claimed") is False,
    }
    errors.extend(f"typed_claim_composition:{key}" for key, passed in typed_checks.items() if not passed)

    return {
        "exact_checks": exact_checks,
        "matrix_checks": matrix_checks,
        "typed_claim_checks": typed_checks,
        "public_authority_flags": verdict_authority,
        "finding_count": len(findings),
        "open_repair_count": len(open_repairs),
    }, errors


def audit_snapshot_sources() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    bindings: dict[str, str] = {}
    for artifact in (read_yaml(MATH_CHILD), read_yaml(PHIL_CHILD)):
        for item in artifact.get("inspected_sources") or []:
            relative = str(item.get("path") or "")
            expected = str(item.get("sha256") or "")
            if relative and expected:
                bindings[relative] = expected
    verdict = read_yaml(VERDICT)
    for item in verdict.get("source_paths") or []:
        relative = str(item.get("path") or "")
        expected = str(item.get("source_sha256") or "")
        if relative and expected:
            bindings[relative] = expected

    checks: dict[str, Any] = {}
    for relative, expected in sorted(bindings.items()):
        observed = snapshot_digest(relative)
        checks[relative] = {
            "expected_sha256": expected,
            "snapshot_sha256": observed,
            "match": observed == expected,
        }
        if observed != expected:
            errors.append(f"audit_snapshot_source_hash:{relative}")

    dependency_checks: dict[str, Any] = {}
    for relative, expected in IMMUTABLE_DEPENDENCIES.items():
        path = ROOT / relative
        observed = digest(path) if path.is_file() else None
        dependency_checks[relative] = {
            "expected_sha256": expected,
            "observed_sha256": observed,
            "match": observed == expected,
        }
        if observed != expected:
            errors.append(f"immutable_dependency_hash:{relative}")

    return {
        "audit_head": AUDIT_HEAD,
        "source_binding_count": len(checks),
        "source_bindings": checks,
        "immutable_dependency_count": len(dependency_checks),
        "immutable_dependencies": dependency_checks,
    }, errors


def audit_review_contract() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    role_bytes = snapshot_bytes(".agents/roles/physics/external-red-team-reviewer.v0.1.0.md") or b""
    role_text = role_bytes.decode("utf-8", errors="replace")
    plan_text = (snapshot_bytes(PLAN_PATH) or b"").decode("utf-8", errors="replace")
    taxonomy_path = "research_control/tasks/RT-20260722-005/artifacts/review_independence_taxonomy.md"
    taxonomy_text = (snapshot_bytes(taxonomy_path) or b"").decode("utf-8", errors="replace")
    language_path = "research_control/tasks/RT-20260722-005/artifacts/review_claim_language_rules.md"
    language_text = (snapshot_bytes(language_path) or b"").decode("utf-8", errors="replace")

    checks = {
        "base_role_hash_bound": digest_bytes(role_bytes)
        == "b49de89caa4cb4f98f959e0ba7168a8223797679e5d0ab3c4700c14a5de9ace7",
        "base_role_name_external": 'role_name: "External Red-Team Reviewer"' in role_text,
        "base_role_kind_external": 'role_kind: "scientific_adversarial_external_review"' in role_text,
        "r38_internal_label_requirement": (
            "Label the current External Red-Team Reviewer honestly as an internal skeptical role"
            in plan_text
            and "reserve external-review language for epistemically independent review" in plan_text
        ),
        "taxonomy_evidence_not_title": (
            "Classify the evidence that exists, not the role title or intended setup." in taxonomy_text
        ),
        "taxonomy_independent_positive_evidence": (
            "independent data access, code base, and method" in taxonomy_text
        ),
        "language_role_name_not_provenance": (
            "An `external-red-team-reviewer` role name is not proof of external review." in language_text
        ),
    }
    errors.extend(f"review_contract:{key}" for key, passed in checks.items() if not passed)

    pilot_path = ROOT / (
        "research_control/tasks/RT-20260722-010/jobs/completions/"
        "AJC-AJ-RT-20260722-010-001.yaml"
    )
    pilot = read_yaml(pilot_path)
    pilot_result = pilot.get("review_pilot_result") or {}
    classes = pilot_result.get("review_context_classes") or {}
    pilot_checks = {
        "historical_task_type_risky": pilot.get("task_type") == "v21_independent_review_pilot",
        "four_internal_reviews": pilot_result.get("review_record_count") == 4,
        "two_blind_same_model": classes.get("blind_same_model_review") == 2,
        "two_same_context": classes.get("same_context_role_review") == 2,
        "external_false": pilot.get("external_review_completed") is False,
        "human_false": pilot.get("human_expert_review_completed") is False,
        "independent_false": pilot.get("independent_replication_completed") is False,
    }
    errors.extend(f"historical_pilot:{key}" for key, passed in pilot_checks.items() if not passed)
    return {"role_contract_checks": checks, "historical_pilot_checks": pilot_checks}, errors


def audit_firewall_and_methodology() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    protocol_path = ROOT / (
        "research_control/tasks/RT-20260729-012/artifacts/"
        "source_derived_benchmark_protocol_v1.tex"
    )
    protocol = protocol_path.read_text(encoding="utf-8")
    audit_path = ROOT / (
        "research_control/tasks/RT-20260731-001/artifacts/"
        "p9_t08_benchmark_smuggling_audit_v1.yaml"
    )
    audit = read_yaml(audit_path)
    cases = audit.get("case_audits") or []
    conclusion = audit.get("conclusion") or {}
    limits = audit.get("authority_limits") or {}
    checks = {
        "firewall_complete_edge_hypothesis": (
            "every parent edge is complete, so undeclared side channels are absent" in protocol
        ),
        "firewall_manifest_completeness_limit": (
            "does not prove that the edge manifest is complete" in protocol
        ),
        "firewall_human_knowledge_limit": (
            "cannot erase target knowledge already held by a" in protocol
        ),
        "firewall_training_prior_limit": "training data, priors" in protocol,
        "six_cases": len(cases) == 6,
        "six_inconclusive": all(item.get("outcome") == "INCONCLUSIVE" for item in cases),
        "zero_benchmark_passes": conclusion.get("benchmark_passes") == 0,
        "zero_independent_replications": conclusion.get("independent_replications") == 0,
        "manifest_not_proved": limits.get("target_import_absence_proves_manifest_completeness") is False,
        "shared_error_not_eliminated": limits.get("shared_systematic_error_eliminated") is False,
    }
    errors.extend(f"firewall_boundary:{key}" for key, passed in checks.items() if not passed)
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
        outcome = payload.get("status") or payload.get("validation_status")
        passed = result.returncode == 0 and str(outcome or "PASS_EXIT_ZERO").upper().startswith("PASS")
        summary = {
            key: payload.get(key)
            for key in (
                "status",
                "fixture_count",
                "attack_fixture_count",
                "benign_fixture_count",
                "check_count",
                "failed_check_count",
                "hard_fail_count",
                "warning_count",
                "finding_count",
                "scanned_path_count",
                "checked_output_count",
            )
            if key in payload
        }
        records.append(
            {
                "command_id": command_id,
                "command": " ".join(command),
                "exit_code": result.returncode,
                "outcome": outcome or ("PASS_EXIT_ZERO" if passed else "FAIL"),
                "passed": passed,
                "summary": summary,
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


def audit_control_records() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    task_count = 0
    completion_count = 0
    positive_claims: list[str] = []
    v21_task_ids: set[str] = set()

    for task_path in sorted((ROOT / "research_control/tasks").glob("RT-*/00_TASK.yaml")):
        task = read_yaml(task_path)
        plan = task.get("implementation_plan") or {}
        if plan.get("plan_id") != PLAN_ID and plan.get("plan_path") != PLAN_PATH:
            continue
        task_count += 1
        task_id = str(task.get("task_id") or "")
        v21_task_ids.add(task_id)
        if task.get("status") not in {"completed", "blocked"}:
            errors.append(f"v21_task_nonterminal:{task_id}")
            continue
        job_id = str(task.get("current_job_id") or "")
        completion_path = task_path.parent / "jobs/completions" / f"AJC-{job_id}.yaml"
        if not job_id or not completion_path.is_file():
            errors.append(f"v21_completion_missing:{task_id}")
            continue
        completion = read_yaml(completion_path)
        completion_count += 1
        if completion.get("task_id") != task_id or completion.get("job_id") != job_id:
            errors.append(f"v21_completion_identity:{task_id}")
        positive_claims.extend(
            positive_review_claims(completion, completion_path.relative_to(ROOT).as_posix())
        )

    handoff_count = 0
    current_hash_mismatches = 0
    resolved_transitions = 0
    recovery_text = (
        ROOT
        / "research_control/tasks/RT-20260725-005/artifacts/"
        "p5_t01_staged_control_contract_recovery_receipt.json"
    ).read_text(encoding="utf-8")
    for handoff_path in sorted((ROOT / "research_control/handoffs").glob("handoff-*.yaml")):
        match = re.search(r"(\d+)$", handoff_path.stem)
        if not match or not 773 <= int(match.group(1)) <= 955:
            continue
        handoff = read_yaml(handoff_path)
        if not re.fullmatch(r"P\d+-T\d+", str(handoff.get("plan_task_id") or "")):
            continue
        handoff_count += 1
        positive_claims.extend(
            positive_review_claims(handoff, handoff_path.relative_to(ROOT).as_posix())
        )
        relative = str(handoff.get("completion_path") or "")
        expected = str(handoff.get("completion_sha256") or "")
        if not relative or not expected:
            continue
        path = ROOT / relative
        observed = digest(path) if path.is_file() else None
        if observed == expected:
            continue
        current_hash_mismatches += 1
        known = (
            handoff.get("handoff_id") == "handoff-0864"
            and expected == "ff6ef8b39030b1bc64e3d977de6f9644f551c80a9315fec98c62caba6f9c6d72"
            and observed == "7e671b29d93cfe89a4ce4118dde3b8c40fe0c3bb29c6e797f504439286b49f2a"
            and observed in recovery_text
            and expected in recovery_text
        )
        if known:
            resolved_transitions += 1
        else:
            errors.append(f"unresolved_handoff_hash:{handoff.get('handoff_id')}")

    registry_positive_claims: list[str] = []
    positive_pattern = re.compile(
        r"(?:external_review_completed|human_expert_review_completed|"
        r"independent_replication_completed)\s*[:=]\s*(?:true|yes|1)\b",
        flags=re.IGNORECASE,
    )
    for registry in sorted((ROOT / "registries").glob("*.csv")):
        text = registry.read_text(encoding="utf-8")
        for match in positive_pattern.finditer(text):
            registry_positive_claims.append(
                f"{registry.relative_to(ROOT).as_posix()}:{match.group(0)}"
            )
    positive_claims.extend(registry_positive_claims)

    if task_count != 132:
        errors.append(f"v21_task_count:{task_count}")
    if completion_count != 132:
        errors.append(f"v21_completion_count:{completion_count}")
    if handoff_count != 136:
        errors.append(f"v21_handoff_count:{handoff_count}")
    if positive_claims:
        errors.extend(f"unsupported_positive_review_claim:{item}" for item in positive_claims)

    return {
        "v21_task_record_count": task_count,
        "v21_completion_identity_count": completion_count,
        "v21_handoff_record_count": handoff_count,
        "handoff_current_hash_mismatch_count": current_hash_mismatches,
        "resolved_historical_transition_count": resolved_transitions,
        "unsupported_positive_review_claim_count": len(positive_claims),
        "unsupported_positive_review_claims": positive_claims,
    }, errors


def artifact_hashes() -> dict[str, str]:
    paths = [MATH_CHILD, PHIL_CHILD, CONFLICT, FUSION, REPORT, MATRIX, VERDICT, Path(__file__)]
    return {
        path.relative_to(ROOT).as_posix(): digest(path)
        for path in paths
        if path.is_file()
    }


def build_outputs() -> tuple[dict[Path, str], dict[str, Any]]:
    errors: list[str] = []
    structure, found = audit_artifact_structure()
    errors.extend(found)
    sources, found = audit_snapshot_sources()
    errors.extend(found)
    review_contract, found = audit_review_contract()
    errors.extend(found)
    firewall, found = audit_firewall_and_methodology()
    errors.extend(found)
    command_results, found = run_commands()
    errors.extend(found)
    registered_sources, found = audit_registered_sources()
    errors.extend(found)
    control_records, found = audit_control_records()
    errors.extend(found)

    hashes = artifact_hashes()
    status = "PASS_REPAIR_REQUIRED_FINDING_PRESERVED" if not errors else "FAIL"
    validation = {
        "schema_id": "v21_p16_t04_validation_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": "P16-T04",
        "status": status,
        "result_status": RESULT_STATUS if not errors else "FAIL",
        "error_count": len(errors),
        "errors": errors,
        "artifact_hashes": hashes,
        "artifact_structure": structure,
        "audit_snapshot_sources": sources,
        "review_contract": review_contract,
        "firewall_and_methodology_boundary": firewall,
        "external_validators": command_results,
        "external_validator_pass_count": sum(item["passed"] for item in command_results),
        "registered_sources": registered_sources,
        "control_records": control_records,
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
        },
    }
    receipt = {
        "schema_id": "v21_p16_t04_compact_receipt_v1",
        "task_id": TASK_ID,
        "job_id": JOB_ID,
        "plan_task_id": "P16-T04",
        "status": status,
        "result_status": validation["result_status"],
        "artifact_hashes": hashes,
        "finding_counts": {
            "total": structure["finding_count"],
            "blocking_scientific": 0,
            "blocking_project_system": structure["open_repair_count"],
        },
        "evidence_counts": {
            "audit_snapshot_source_bindings": sources["source_binding_count"],
            "registered_content_addresses": registered_sources["content_address_count"],
            "v21_tasks": control_records["v21_task_record_count"],
            "v21_completions": control_records["v21_completion_identity_count"],
            "v21_handoffs": control_records["v21_handoff_record_count"],
            "external_validators_passed": validation["external_validator_pass_count"],
            "unsupported_positive_review_claims": control_records[
                "unsupported_positive_review_claim_count"
            ],
        },
        "project_improvement_signal_id": "PIS-RT-20260803-014-001",
        "repair_work_item_id": "P16-T04-internal-review-label-contract-repair",
        "claim_boundary_summary": (
            "The bounded P16-T04 audit rejects cross-document entailment of external independence, "
            "source derivation, benchmark promotion, and global no-go. It preserves one high-severity "
            "internal-versus-external review-label control defect and changes no science or authority."
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

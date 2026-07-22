#!/usr/bin/env python3
"""Validate and summarize the bounded v21 P11-T07 two-object review pilot."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
TASK = ROOT / "research_control/tasks/RT-20260722-010"
ART = TASK / "artifacts"
VALIDATOR_PATH = Path(__file__).resolve()

BLIND_BUILDER = ROOT / "research_control/tasks/RT-20260722-004/artifacts/build_blind_review_packet.py"
BLIND_VALIDATOR = ROOT / "research_control/tasks/RT-20260722-004/artifacts/validate_blind_review_packet.py"
SEMANTIC_PROBE = ROOT / "research_control/tasks/RT-20260722-006/artifacts/semantic_smuggling_mutator.py"
POSITIVE_GATE = ROOT / "research_control/tasks/RT-20260722-007/artifacts/validate_positive_provenance_gate.py"
METRIC_BUILDER = ROOT / "research_control/tasks/RT-20260722-008/artifacts/build_reviewer_agreement_report.py"

SELECTOR_SOURCE = ROOT / "research_control/tasks/RT-20260720-016/artifacts/eqsrc_no_selector_nonuniqueness_theorem_v1.tex"
LEAN_SOURCE = ROOT / "research_control/tasks/RT-20260720-018/artifacts/proof/SelectorKernel.lean"
SELECTOR_AUDIT = ROOT / "research_control/tasks/RT-20260720-019/artifacts/eqsrc_selector_theorem_smuggling_audit_v1.tex"
SELECTOR_STRESS = ROOT / "research_control/tasks/RT-20260720-020/artifacts/eqsrc_selector_theorem_refuter_stress_v1.tex"
GEFF_SOURCE = ROOT / "research_control/tasks/RT-20260614-216/artifacts/245_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_METRICFORMASSIGN_GEFF_CANDIDATE_OR_OBSTRUCTION.tex"
GEFF_AUDIT = ROOT / "research_control/tasks/RT-20260614-217/artifacts/246_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_METRICFORMASSIGN_GEFF_CANDIDATE_SMUGGLING_AUDIT.tex"
GEFF_STRESS = ROOT / "research_control/tasks/RT-20260614-218/artifacts/247_NONBOTTOM_METRICDATA_WITNESS_SRC_GSC_POST_GATE_METRICFORMASSIGN_GEFF_CANDIDATE_REFUTER_STRESS_TEST.tex"
PROOF_RECEIPT = ROOT / "research_control/tasks/RT-20260722-009/artifacts/proof_evidence_compact_receipt.json"

REVIEW_PATHS = (
    ART / "blind_same_model_selector_review.yaml",
    ART / "blind_same_model_geff_review.yaml",
    ART / "same_context_selector_review.yaml",
    ART / "same_context_geff_review.yaml",
)
BLIND_PREFIXES = ("selector", "geff")

DEPENDENCY_HASHES = {
    ROOT / "research_control/tasks/RT-20260722-009/jobs/completions/AJC-AJ-RT-20260722-009-001.yaml": "853d66f154dca54edbbd5f86adff2b974a4a14d72967682c1a701728df345bf8",
    ROOT / "research_control/tasks/RT-20260722-006/jobs/completions/AJC-AJ-RT-20260722-006-001.yaml": "c5f0a2fd66b31f854e911e608a3095b731c210a90dd061a0fdca25419f079379",
    ROOT / "research_control/tasks/RT-20260722-007/jobs/completions/AJC-AJ-RT-20260722-007-001.yaml": "fc47c54cefe9f6f3dd7a6a279c41b81fec8816e2bd72c4e58f2856b433dea3dd",
    ROOT / "research_control/tasks/RT-20260722-008/jobs/completions/AJC-AJ-RT-20260722-008-001.yaml": "4a1a2c041b97c3e8c712bae9be55e0e08de64c712aaf5f6fc275f33f20cfa494",
}
SOURCE_HASHES = {
    SELECTOR_SOURCE: "d6df090765c9da56d08fdac41d8d0af5575391a382206e853cfda756da9a56ae",
    LEAN_SOURCE: "6f23c92d72779e4fc5b13f56b34a8709ece2dfec27f7ce767170ed54d3d9f356",
    SELECTOR_AUDIT: "d093d7b0afbe322cf537644de54f17156ea2427fcc0988f4fc8fb305e93a0f76",
    SELECTOR_STRESS: "d519bcc9534af3b2ca3e3d44604bd56bf72c425e0d06322c33cc7e66abfd2b49",
    GEFF_SOURCE: "dd30573519ed1df66b3800d29ee0adc9fcc94d9c8d3b9b5a7fcffde503d5f0ef",
    GEFF_AUDIT: "c7071ec3efb285d0db35902987bb0814544fc0250055a906385749c2b1da6b10",
    GEFF_STRESS: "f2a92b6807cb676f91573456c1d3c3ffd0a1e9734c3444c3212e15f280b10e73",
    PROOF_RECEIPT: "dc1518be22a1628336e01362ebbc375379ee2ce536147da346af41f2c0cc78c0",
}

ANALYSIS_PATH = ART / "review_agreement_and_leakage_analysis.json"
GATE_DELTA_PATH = ART / "positive_provenance_readiness_delta.json"
VALIDATION_PATH = ART / "p11_t07_pilot_validation.json"
RECEIPT_PATH = ART / "p11_t07_pilot_compact_receipt.json"


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_yaml(path: Path) -> dict[str, Any]:
    from scripts.research_control import strict_yaml

    value = strict_yaml.load(path)
    if not isinstance(value, dict):
        raise ValueError(f"expected YAML map at {path}")
    return value


def blind_reports() -> dict[str, dict[str, Any]]:
    validator = load_module("p11_t07_blind_validator", BLIND_VALIDATOR)
    rows: dict[str, dict[str, Any]] = {}
    for prefix in BLIND_PREFIXES:
        manifest_path = ART / f"{prefix}_blind_source_manifest.json"
        packet_path = ART / f"{prefix}_blind_review_packet.json"
        context_path = ART / f"{prefix}_blind_context_manifest.json"
        rows[prefix] = validator.validate_objects(
            load_json(manifest_path),
            load_json(packet_path),
            load_json(context_path),
            packet_path=packet_path,
            context_path=context_path,
        )
    return rows


def red_team_receipt() -> dict[str, Any]:
    from scripts.research_control import validate_red_team_review_artifact as red_team

    return red_team.validate_files(list(REVIEW_PATHS))


def compact_text(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def is_boundary_false_positive(finding: dict[str, Any]) -> bool:
    evidence = compact_text(str(finding.get("evidence", "")))
    return any(
        marker in evidence
        for marker in (
            "evaluatestobottomsrc",
            "nomattercouplingactionfieldequationdetectorprotocolpropertimeinterpretationorbenchmarkresultissupplied",
            "notanadoptedsourcelaworphysicalmetric",
        )
    )


def semantic_rows() -> list[dict[str, Any]]:
    probe = load_module("p11_t07_semantic_probe", SEMANTIC_PROBE)
    rows: list[dict[str, Any]] = []
    for name in (
        "selector_blind_review_packet.json",
        "geff_blind_review_packet.json",
        "selector_context_rich_review_packet.json",
        "geff_context_rich_review_packet.json",
    ):
        findings = probe.semantic_scan(load_json(ART / name))
        false_positives = [finding for finding in findings if is_boundary_false_positive(finding)]
        confirmed = [finding for finding in findings if finding not in false_positives]
        rows.append(
            {
                "artifact_path": rel(ART / name),
                "artifact_sha256": sha256(ART / name),
                "raw_finding_count": len(findings),
                "boundary_false_positive_count": len(false_positives),
                "confirmed_smuggling_count": len(confirmed),
                "rule_ids": sorted({finding.get("rule_id") for finding in findings}),
                "findings": findings,
                "disposition": (
                    "No semantic-smuggling finding confirmed. Fail-closed or explicit negative metric language triggered the bounded probe and remains a P11-T08 false-positive pressure point."
                    if findings and not confirmed
                    else "No bounded-probe finding."
                    if not findings
                    else "Confirmed finding requires repair."
                ),
            }
        )
    return rows


def gate_records() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    gate = load_module("p11_t07_positive_gate", POSITIVE_GATE)
    contract = gate.extract_contract()
    fixtures = gate.load_fixtures()
    before = copy.deepcopy(fixtures["base_records"]["scoped_candidate"])
    before.update(
        {
            "record_id": "PPG-P11-T07-GEFF-BEFORE-001",
            "subject_id": "GEFF-GSC-SCOPED-SOURCE-RECORD-CANDIDATE-V1",
            "subject_scope": "scoped_candidate",
            "review_surface": "effective_metric",
            "review_executed": False,
            "outcome": "not_ready",
            "physics_promotion_authorized": False,
        }
    )
    before["no_target_purity"] = {
        "status": "passed",
        "evidence_refs": [rel(GEFF_AUDIT)],
    }
    before["validator_receipts"] = [
        "research_control/tasks/RT-20260722-006/artifacts/semantic_smuggling_compact_receipt.json",
        "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_gate_compact_receipt.json",
    ]
    before["dimensions"]["source_derivation"] = {
        "status": "proposed",
        "evidence_refs": [rel(GEFF_SOURCE)],
        "source_refs": [rel(GEFF_SOURCE)],
        "source_hashes": {rel(GEFF_SOURCE): sha256(GEFF_SOURCE)},
        "premise_kinds": ["source_extension"],
        "not_applicable_reason": "",
    }
    before["dimensions"]["uniqueness_or_quotient"] = {
        "status": "multiple_unresolved",
        "evidence_refs": [],
        "quotient_scope": "",
        "not_applicable_reason": "",
    }
    before["dimensions"]["naturality"] = {
        "status": "conditional",
        "evidence_refs": [rel(GEFF_SOURCE), rel(GEFF_STRESS)],
        "not_applicable_reason": "",
    }
    before["dimensions"]["dynamics"] = {
        "status": "missing",
        "evidence_refs": [],
        "not_applicable_reason": "",
    }
    before["dimensions"]["operational_systems"] = {
        "status": "missing",
        "evidence_refs": [],
        "device_or_protocol_refs": [],
        "not_applicable_reason": "",
    }
    before["dimensions"]["robustness"] = {
        "status": "fragile",
        "evidence_refs": [rel(GEFF_STRESS)],
        "perturbation_scope": "Declared beta-separated marked finite-graph context only; no general perturbation or continuum-limit theorem.",
        "not_applicable_reason": "",
    }
    before["dimensions"]["independent_review"] = {
        "status": "missing",
        "evidence_refs": [],
        "review_artifact_refs": [],
        "not_applicable_reason": "",
    }
    before["authority"] = {
        "status": "control_only",
        "authority_refs": [
            "research_control/tasks/RT-20260722-007/artifacts/positive_provenance_operational_meaning_gate_policy.md"
        ],
        "protected_gate_id": "Gate-B",
    }
    before["forbidden_conclusions"] = [
        "A scoped source record is not a physical effective metric.",
        "No-target purity validator receipts or internal review do not complete Gate B.",
    ]

    after = copy.deepcopy(before)
    after["record_id"] = "PPG-P11-T07-GEFF-AFTER-001"
    after["dimensions"]["independent_review"] = {
        "status": "blind_same_model_review",
        "evidence_refs": [
            rel(ART / "blind_same_model_geff_review.yaml"),
            rel(ART / "same_context_geff_review.yaml"),
        ],
        "review_artifact_refs": [
            rel(ART / "blind_same_model_geff_review.yaml"),
            rel(ART / "same_context_geff_review.yaml"),
        ],
        "not_applicable_reason": "",
    }
    after["review_executed"] = True

    before_result = gate.validate_record(before, contract)
    after_result = gate.validate_record(after, contract)
    report = {
        "schema_id": "v21_p11_t07_positive_provenance_readiness_delta_v1",
        "status": "PASS" if before_result["valid"] and after_result["valid"] else "FAIL",
        "subject_id": before["subject_id"],
        "gate_id": "gate_b",
        "before": {"record": before, "evaluation": before_result},
        "after": {"record": after, "evaluation": after_result},
        "delta": {
            "review_evidence_change": "missing_to_blind_same_model_review",
            "readiness_before": "not_ready",
            "readiness_after": "not_ready",
            "readiness_changed": False,
            "protected_gate_review_ready": False,
            "remaining_blockers": after_result["blocker_ids"],
        },
        "claim_boundary": {
            "blind_or_same_context_review_completes_gate": False,
            "external_review_completed": False,
            "human_expert_review_completed": False,
            "independent_replication_completed": False,
            "physics_promotion_authorized": False,
        },
    }
    return before, after, report


def metric_context(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": context["schema_id"],
        "classification": context["classification"],
        "review_executed": context["review_executed"],
        "replication_executed": context["replication_executed"],
        "dimensions": context["dimensions"],
        "evidence_paths": context["evidence_paths"],
        "limitations": context["limitations"],
        "claims": context["claims"],
    }


def metric_review_records(reviews: list[tuple[Path, dict[str, Any]]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path, review in reviews:
        selector = review["reviewed_object_id"].startswith("EQSRC-")
        source_path = SELECTOR_SOURCE if selector else GEFF_SOURCE
        blind = review["review_context"]["classification"] == "blind_same_model_review"
        assessments = copy.deepcopy(review["review_metrics"])
        for assessment in assessments.values():
            assessment["evidence_refs"] = [rel(path)] if assessment["finding_ids"] else []
        records.append(
            {
                "review_id": path.stem,
                "record_mode": "live_pilot",
                "reviewed_object_id": review["reviewed_object_id"],
                "source_object_path": rel(source_path),
                "source_object_sha256": sha256(source_path),
                "source_review_artifact_id": rel(path),
                "blind_packet_id": "V21-PILOT-SELECTOR-BLIND-V1" if selector else "V21-PILOT-GEFF-BLIND-V1",
                "configuration_blind_id": "cfg-blind-packet" if blind else "cfg-context-rich",
                "review_context": metric_context(review["review_context"]),
                "axis_assessments": assessments,
                "physics_promotion_authorized": False,
                "scientific_status_inference": "forbidden",
                "truth_status_inference": "forbidden",
                "forbidden_conclusions": [
                    "Agreement is not proof or scientific status.",
                    "Internal AI review is not external human review or independent replication.",
                ],
            }
        )
    return records


def disposition_coverage(review: dict[str, Any]) -> tuple[set[str], set[str]]:
    finding_ids = {
        finding_id
        for assessment in review.get("review_metrics", {}).values()
        for finding_id in assessment.get("finding_ids", [])
    }
    dispositions = {
        row.split("|", 1)[0]
        for row in review.get("finding_dispositions", [])
        if isinstance(row, str) and "|" in row
    }
    return finding_ids, dispositions


def build_analysis() -> dict[str, Any]:
    metric = load_module("p11_t07_metric_builder", METRIC_BUILDER)
    reviews = [(path, load_yaml(path)) for path in REVIEW_PATHS]
    records = metric_review_records(reviews)
    aggregate = metric.aggregate(records)
    blind = blind_reports()
    red = red_team_receipt()
    semantics = semantic_rows()
    revision = load_yaml(ART / "blind_packet_revision_history.yaml")
    finding_ids: set[str] = set()
    disposition_ids: set[str] = set()
    for _, review in reviews:
        current_findings, current_dispositions = disposition_coverage(review)
        finding_ids.update(current_findings)
        disposition_ids.update(current_dispositions)
    return {
        "schema_id": "v21_p11_t07_review_agreement_and_leakage_analysis_v1",
        "status": "PASS",
        "plan_task_id": "P11-T07",
        "reviewed_object_count": 2,
        "review_record_count": 4,
        "review_context_classification_counts": red["review_context_classification_counts"],
        "blind_packet_validation": {
            prefix: {
                "status": report["status"],
                "packet_sha256": report["packet_sha256"],
                "context_sha256": report["context_sha256"],
                "failed_check_count": report["failed_check_count"],
                "leak_finding_count": report["leak_finding_count"],
                "assumption_count": report["assumption_count"],
                "material_count": report["material_count"],
            }
            for prefix, report in blind.items()
        },
        "blind_packet_revision": revision,
        "semantic_smuggling_probe": {
            "probe_scope": "Bounded P11-T04 semantic probe applied to the four pilot packets; this is not a semantic-completeness check.",
            "rows": semantics,
            "raw_finding_count": sum(row["raw_finding_count"] for row in semantics),
            "boundary_false_positive_count": sum(row["boundary_false_positive_count"] for row in semantics),
            "confirmed_smuggling_count": sum(row["confirmed_smuggling_count"] for row in semantics),
            "shortcoming": "The bounded probe overflags explicit fail-closed or negated target-metric and proper-time language and emits many duplicate split-window findings.",
        },
        "reviewer_metric_aggregate": aggregate,
        "finding_disposition": {
            "finding_ids": sorted(finding_ids),
            "disposition_ids": sorted(disposition_ids),
            "undisposed_finding_ids": sorted(finding_ids - disposition_ids),
        },
        "parent_synthesis": {
            "mode": "parent_child_parallel_synthesis",
            "child_execution_units": ["child_phys_math", "child_phys_phil"],
            "resolution_round_count": 1,
            "preserved_metric_disagreement_count": aggregate["metrics"]["assessment_disagreement_count"],
            "false_consensus_risk_count": aggregate["metrics"]["false_consensus_risk_count"],
            "blocking_scientific_conflict_count": 0,
        },
        "authority_boundary": {
            "external_review_completed": False,
            "human_expert_review_completed": False,
            "independent_replication_completed": False,
            "consensus_sets_scientific_status": False,
            "proof_authority": False,
            "physics_promotion_authorized": False,
        },
    }


def build_validation(analysis: dict[str, Any], gate_delta: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, str]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    for path, expected in {**DEPENDENCY_HASHES, **SOURCE_HASHES}.items():
        observed = sha256(path) if path.is_file() else "missing"
        check(f"hash:{rel(path)}", observed == expected, f"expected={expected} observed={observed}")

    blind_rows = analysis["blind_packet_validation"]
    check(
        "blind_packet_rebuild_and_leakage",
        all(row["status"] == "PASS" and row["failed_check_count"] == 0 and row["leak_finding_count"] == 0 for row in blind_rows.values()),
        f"rows={blind_rows}",
    )
    revision = analysis["blind_packet_revision"]
    check(
        "blind_packet_scientific_self_containment_repair",
        str(revision.get("resolution_round_count")) == "1"
        and revision.get("final_review", {}).get("initial_packet_level_countermodel_survived") is False
        and revision.get("repair", {}).get("reviewed_science_source_edited") is False,
        "one task-local packet revision resolved the omission without a science-source edit",
    )
    classes = analysis["review_context_classification_counts"]
    check(
        "review_context_classes",
        classes == {"blind_same_model_review": 2, "same_context_role_review": 2},
        f"classes={classes}",
    )
    check(
        "external_red_team_artifact_schema",
        red_team_receipt().get("status") == "PASS",
        "four strict review artifacts pass the external red-team schema",
    )
    reviews = [load_yaml(path) for path in REVIEW_PATHS]
    check(
        "no_external_or_independent_overclaim",
        all(
            not any(review["review_context"]["claims"].values())
            and review["review_context"]["replication_executed"] is False
            and review["physics_promotion_authorized"] is False
            for review in reviews
        ),
        "all review and promotion claims remain false",
    )
    semantic = analysis["semantic_smuggling_probe"]
    check(
        "semantic_smuggling_disposition",
        semantic["raw_finding_count"] > 0
        and semantic["raw_finding_count"] == semantic["boundary_false_positive_count"]
        and semantic["confirmed_smuggling_count"] == 0,
        f"raw={semantic['raw_finding_count']} boundary_false_positive={semantic['boundary_false_positive_count']} confirmed={semantic['confirmed_smuggling_count']}",
    )
    check(
        "positive_provenance_gate_valid",
        gate_delta["status"] == "PASS"
        and gate_delta["before"]["evaluation"]["valid"] is True
        and gate_delta["after"]["evaluation"]["valid"] is True,
        "before and after records are valid policy records",
    )
    check(
        "positive_provenance_gate_still_blocked",
        gate_delta["delta"]["readiness_before"] == "not_ready"
        and gate_delta["delta"]["readiness_after"] == "not_ready"
        and gate_delta["delta"]["protected_gate_review_ready"] is False
        and "independent_review" in gate_delta["delta"]["remaining_blockers"],
        f"remaining={gate_delta['delta']['remaining_blockers']}",
    )
    metrics = analysis["reviewer_metric_aggregate"]["metrics"]
    check(
        "reviewer_agreement_metrics",
        metrics.get("review_record_count") == 4
        and metrics.get("reviewed_object_count") == 2
        and metrics.get("eligible_pair_axis_comparison_count") == 10
        and metrics.get("exact_assessment_agreement_count") == 7
        and metrics.get("assessment_disagreement_count") == 3
        and metrics.get("false_consensus_risk_count") == 7,
        f"metrics={metrics}",
    )
    check(
        "all_findings_disposed",
        analysis["finding_disposition"]["undisposed_finding_ids"] == [],
        f"undisposed={analysis['finding_disposition']['undisposed_finding_ids']}",
    )
    proof = load_json(PROOF_RECEIPT)
    check(
        "proof_evidence_scope",
        proof.get("status") == "PASS"
        and proof.get("p2_t05_migration_status") == "PASS_MACHINE_CHECKED_NO_AXIOM_DEPENDENCIES"
        and proof.get("proof_authority") is False
        and proof.get("physics_promotion_authorized") is False,
        "mechanized evidence remains bounded and non-promotional",
    )
    check(
        "new_mathematical_payload",
        (ART / "operational_nonidentifiability_witness.md").is_file()
        and "forgetful projection" in (ART / "operational_nonidentifiability_witness.md").read_text(encoding="utf-8"),
        "finite two-extension operational nonidentifiability witness exists",
    )
    check(
        "parent_child_synthesis",
        analysis["parent_synthesis"]["mode"] == "parent_child_parallel_synthesis"
        and analysis["parent_synthesis"]["resolution_round_count"] == 1
        and (ART / "parent_conflict_review_p11_t07.yaml").is_file()
        and (ART / "parent_fusion_notes_p11_t07.md").is_file(),
        "two child perspectives one bounded revision and parent fusion are preserved",
    )
    check(
        "claim_boundary_preserved",
        all(review["verdict"] == "no_blocking_defect_found_as_written" for review in reviews)
        and gate_delta["claim_boundary"]["physics_promotion_authorized"] is False,
        "exact scoped claims survive while physical readiness and promotion remain blocked",
    )

    failed = [row for row in checks if row["status"] == "FAIL"]
    source_paths = sorted(
        {
            *DEPENDENCY_HASHES,
            *SOURCE_HASHES,
            *REVIEW_PATHS,
            ART / "selector_blind_source_manifest.json",
            ART / "selector_blind_review_packet.json",
            ART / "selector_blind_context_manifest.json",
            ART / "selector_context_rich_review_packet.json",
            ART / "geff_blind_source_manifest.json",
            ART / "geff_blind_review_packet.json",
            ART / "geff_blind_context_manifest.json",
            ART / "geff_context_rich_review_packet.json",
            ART / "blind_packet_revision_history.yaml",
            ART / "operational_nonidentifiability_witness.md",
            ART / "p11_t07_repair_recommendations.md",
            ART / "parent_conflict_review_p11_t07.yaml",
            ART / "parent_fusion_notes_p11_t07.md",
            VALIDATOR_PATH,
        },
        key=lambda path: rel(path),
    )
    return {
        "schema_id": "v21_p11_t07_independent_review_pilot_validation_v1",
        "status": "PASS" if not failed else "FAIL",
        "plan_task_id": "P11-T07",
        "task_id": "RT-20260722-010",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
        "source_hashes": {rel(path): sha256(path) for path in source_paths},
        "counts": {
            "reviewed_object_count": 2,
            "review_record_count": 4,
            "review_context_class_count": 2,
            "packet_revision_count": 1,
            "raw_semantic_finding_count": semantic["raw_finding_count"],
            "semantic_boundary_false_positive_count": semantic["boundary_false_positive_count"],
            "confirmed_semantic_smuggling_count": semantic["confirmed_smuggling_count"],
            "metric_disagreement_count": metrics["assessment_disagreement_count"],
            "metric_false_consensus_risk_count": metrics["false_consensus_risk_count"],
            "positive_gate_ready_count": 0,
            "external_human_review_count": 0,
            "independent_replication_count": 0,
        },
        "claim_boundary": {
            "selector_theorem_promoted": False,
            "g_eff_adopted": False,
            "protected_gate_review_ready": False,
            "external_review_completed": False,
            "human_expert_review_completed": False,
            "independent_replication_completed": False,
            "proof_authority": False,
            "physics_promotion_authorized": False,
        },
    }


def generated_outputs() -> tuple[dict[Path, bytes], dict[str, Any]]:
    analysis = build_analysis()
    _, _, gate_delta = gate_records()
    validation = build_validation(analysis, gate_delta)
    analysis_bytes = canonical_bytes(analysis)
    gate_bytes = canonical_bytes(gate_delta)
    validation_bytes = canonical_bytes(validation)
    receipt = {
        "schema_id": "v21_p11_t07_independent_review_pilot_compact_receipt_v1",
        "status": validation["status"],
        "task_id": "RT-20260722-010",
        "plan_task_id": "P11-T07",
        "analysis_path": rel(ANALYSIS_PATH),
        "analysis_sha256": sha256_bytes(analysis_bytes),
        "gate_delta_path": rel(GATE_DELTA_PATH),
        "gate_delta_sha256": sha256_bytes(gate_bytes),
        "validation_path": rel(VALIDATION_PATH),
        "validation_sha256": sha256_bytes(validation_bytes),
        "counts": validation["counts"],
        "validator_ids": [row["check_id"] for row in validation["checks"]],
        "claim_boundary_summary": "Two internal AI review classes exercised the live QA controls on the selector theorem and scoped g_eff source record. Exact scoped claims survive; Gate B remains not ready and no external human review independent replication proof authority object adoption or physics promotion is created.",
        "physics_promotion_authorized": False,
        "proof_authority": False,
    }
    outputs = {
        ANALYSIS_PATH: analysis_bytes,
        GATE_DELTA_PATH: gate_bytes,
        VALIDATION_PATH: validation_bytes,
        RECEIPT_PATH: canonical_bytes(receipt),
    }
    return outputs, validation


def write_outputs() -> dict[str, Any]:
    outputs, validation = generated_outputs()
    for path, payload in outputs.items():
        path.write_bytes(payload)
    return {
        "status": validation["status"],
        "mode": "write",
        "written_paths": [rel(path) for path in outputs],
        "check_count": validation["check_count"],
        "failed_check_count": validation["failed_check_count"],
        **validation["counts"],
    }


def check_outputs() -> dict[str, Any]:
    outputs, validation = generated_outputs()
    drift = [rel(path) for path, payload in outputs.items() if not path.is_file() or path.read_bytes() != payload]
    return {
        "status": "PASS" if validation["status"] == "PASS" and not drift else "FAIL",
        "mode": "check",
        "drift_paths": drift,
        "check_count": validation["check_count"],
        "failed_check_count": validation["failed_check_count"],
        **validation["counts"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = write_outputs() if args.write else check_outputs()
    except Exception as exc:
        result = {"status": "FAIL", "mode": "write" if args.write else "check", "error": str(exc)}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['status']}: {result}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

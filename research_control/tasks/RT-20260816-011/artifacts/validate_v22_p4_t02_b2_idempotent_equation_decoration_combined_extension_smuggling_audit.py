#!/usr/bin/env python3
"""Focused validator for the RT011 idempotent-decoration Smuggling Audit."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260816-011"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_validation.json"
COMPACT = ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_compact_receipt.json"


class UniqueLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def no_nulls(value):
    if value is None:
        return False
    if isinstance(value, dict):
        return all(no_nulls(key) and no_nulls(item) for key, item in value.items())
    if isinstance(value, list):
        return all(no_nulls(item) for item in value)
    return True


def check(checks, check_id, condition, detail):
    checks.append({"check_id": check_id, "passed": bool(condition), "detail": detail})


def require_files(checks, paths):
    for path in paths:
        check(checks, f"FILE_{path.name}", path.is_file(), str(path.relative_to(ROOT)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    required = [
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260816-011.md",
        TASK / "jobs/AJ-RT-20260816-011-001.yaml",
        TASK / "jobs/completions/AJC-AJ-RT-20260816-011-001.yaml",
        TASK / "roles/smuggling-auditor@0.2.0--RT-20260816-011.yaml",
        TASK / "documentation_impact.yaml",
        ART / "child_phys_math_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_audit.yaml",
        ART / "child_phys_phil_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_audit.yaml",
        ART / "parent_conflict_review_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_audit.yaml",
        ART / "parent_fusion_notes_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_audit.md",
        ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_audit_v1.tex",
        ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_matrix_v1.yaml",
        ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_disposition_v1.yaml",
        ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_provenance_manifest_v1.yaml",
        ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_model.py",
        ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_latex_compile_receipt.json",
        ROOT / "research_control/handoffs/handoff-1054.yaml",
        ROOT / "research_control/handoffs/handoff-1054.md",
    ]
    checks = []
    require_files(checks, required)
    missing = [path for path in required if not path.is_file()]
    if missing:
        result = {"all_passed": False, "checks": checks, "missing": [str(p) for p in missing]}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1

    yaml_paths = [path for path in required if path.suffix in {".yaml", ".yml"}]
    documents = {}
    for path in yaml_paths:
        try:
            documents[path] = load_yaml(path)
            check(checks, f"YAML_{path.name}", no_nulls(documents[path]), "unique-key parse and no null values")
        except Exception as exc:
            check(checks, f"YAML_{path.name}", False, str(exc))

    task = documents[TASK / "00_TASK.yaml"]
    job = documents[TASK / "jobs/AJ-RT-20260816-011-001.yaml"]
    completion = documents[TASK / "jobs/completions/AJC-AJ-RT-20260816-011-001.yaml"]
    role = documents[TASK / "roles/smuggling-auditor@0.2.0--RT-20260816-011.yaml"]
    matrix = documents[ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_matrix_v1.yaml"]
    disposition = documents[ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_disposition_v1.yaml"]
    conflict = documents[ART / "parent_conflict_review_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_audit.yaml"]
    provenance = documents[ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_provenance_manifest_v1.yaml"]
    handoff = documents[ROOT / "research_control/handoffs/handoff-1054.yaml"]

    canonical_packet = "PKT-V22-P4T02-B2-IDEMPOTENT-EQUATION-DECORATION-COMBINED-EXTENSION-SOURCE-EXTENSION-SMUGGLING-AUDIT-V1"
    successor = "PKT-V22-P4T02-B2-IDEMPOTENT-EQUATION-DECORATION-NULL-SEMANTICS-RANK-TOPOLOGY-REFUTER-STRESS-V1"
    check(checks, "TASK_ID", task.get("task_id") == "RT-20260816-011", "canonical task identity")
    check(checks, "TASK_TERMINAL", task.get("status") == "completed" and str(task.get("validation_status", "")).startswith("PASS"), "task completed and precheckpoint ready")
    check(checks, "JOB_TERMINAL", job.get("status") == "completed" and str(job.get("validation_status", "")).startswith("PASS"), "job completed and precheckpoint ready")
    check(checks, "ROLE_TERMINAL", role.get("status") == "completed", "one-job overlay expired by completion")
    check(checks, "PACKET_ID", task.get("selected_packet_id") == canonical_packet and job.get("selected_packet_id") == canonical_packet, "selected audit packet identity")
    check(checks, "ROLE_DECOMPOSITION", job.get("role_decomposition", {}).get("mode") == "parent_child_parallel_synthesis" and job.get("role_decomposition", {}).get("subagent_count") == 2, "required parent-child synthesis")
    check(checks, "AUDIT_DIMENSIONS", len(matrix.get("audit_dimensions", [])) == 12, "exactly twelve audit dimensions")
    check(checks, "VERDICT", matrix.get("aggregate_disposition", {}).get("verdict") == "source_pure_as_written" and disposition.get("smuggling_audit_result", {}).get("result_type") == "source_pure_as_written", "one narrow source-purity verdict")
    check(checks, "EXTENSION_CLASS", disposition.get("source_extension_classification", {}).get("category") == "new_ontology_primitive" and disposition.get("source_extension_classification", {}).get("algebraic_carrier_definitionally_available") is True, "semantic primitive with definable algebraic sublayer")
    check(checks, "PAYLOADS", len(disposition.get("new_mathematical_payload", [])) >= 6 and all(item.get("falsifier") for item in disposition.get("new_mathematical_payload", [])), "six proof-and-falsifier payloads")
    check(checks, "FREEZES", len(disposition.get("preserved_freeze_labels", [])) == 9 and len(set(disposition.get("preserved_freeze_labels", []))) == 9, "nine unique inherited freezes")
    distance_rows = disposition.get("distance_to_gr_status", [])
    check(checks, "DISTANCE", len(distance_rows) == 14 and sum(row.get("task_delta") == "no_delta" for row in distance_rows) == 14, "fourteen literal no-delta rows")
    selected = disposition.get("selected_successor", {})
    check(checks, "SUCCESSOR", selected.get("packet_id") == successor and selected.get("status") == "selected_not_executed" and selected.get("executed") is False, "one exact unexecuted successor")
    check(checks, "OBLIGATIONS", job.get("audit_contract", {}).get("proof_obligation_count") == 16 and len(job.get("audit_contract", {}).get("proof_obligations", [])) == 16, "sixteen proof obligations")
    check(checks, "FAILURE_BRANCHES", job.get("audit_contract", {}).get("failure_branch_count") == 14 and len(job.get("audit_contract", {}).get("failure_branches", [])) == 14, "fourteen failure branches")
    check(checks, "CONFLICT", conflict.get("status") == "resolved" and conflict.get("unresolved_conflict_count") == 0 and conflict.get("shared_result_type") == "source_pure_as_written", "parent conflict review resolved")
    check(checks, "COMPLETION", completion.get("status") == "completed" and completion.get("validation_status", "").startswith("PASS") and completion.get("selected_next_packet", {}).get("packet_id") == successor, "completion is decisive and successor remains unexecuted")
    check(checks, "HANDOFF", handoff.get("handoff_id") == "handoff-1054" and successor in handoff.get("next_action", "") and handoff.get("status", "").endswith("checkpoint"), "handoff selects exact post-checkpoint action")

    source_checks = []
    for item in provenance.get("governing_sources", []):
        path = ROOT / item.get("path", "")
        passed = path.is_file() and sha256(path) == item.get("sha256")
        source_checks.append(passed)
    check(checks, "SOURCE_HASHES", bool(source_checks) and all(source_checks), f"{sum(source_checks)}/{len(source_checks)} governing source hashes")

    model_path = ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_model.py"
    proc = subprocess.run([sys.executable, str(model_path), "--json"], cwd=ROOT, capture_output=True, text=True)
    try:
        model = json.loads(proc.stdout)
    except json.JSONDecodeError:
        model = {}
    check(checks, "MODEL", proc.returncode == 0 and model.get("all_passed") is True and model.get("check_count") == 20, "exact model passes twenty controls")
    check(checks, "MODEL_HASH", disposition.get("exact_model", {}).get("payload_sha256") == model.get("payload_sha256"), "model receipt hash matches disposition")

    fusion_text = (ART / "parent_fusion_notes_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_audit.md").read_text(encoding="utf-8")
    tex_text = (ART / "v22_p4_t02_b2_idempotent_equation_decoration_combined_extension_smuggling_audit_v1.tex").read_text(encoding="utf-8")
    required_phrases = ["source_pure_as_written", "new_ontology_primitive", "zero and identity", "rank-topology", successor]
    check(checks, "FUSION_PHRASES", all(phrase in fusion_text for phrase in required_phrases), "fusion preserves decisive boundaries")
    check(checks, "TEX_PHRASES", all(phrase.replace("_", "\\_") in tex_text or phrase in tex_text for phrase in required_phrases), "TeX preserves decisive boundaries")
    blocked = [
        completion.get("source_law_adopted") is False,
        completion.get("d7_reevaluated") is False,
        completion.get("b2_activated") is False,
        completion.get("p4_t03_unlocked") is False,
        completion.get("physics_promotion_authorized") is False,
        completion.get("publication_authorized") is False,
        completion.get("push_authorized") is False,
        completion.get("external_action_authorized") is False,
    ]
    check(checks, "AUTHORITY", all(blocked), "all adoption and outward-action blocks remain false")

    all_passed = all(item["passed"] for item in checks)
    result = {
        "schema_id": "v22_p4_t02_b2_idempotent_equation_decoration_smuggling_validation_v1",
        "task_id": "RT-20260816-011",
        "job_id": "AJ-RT-20260816-011-001",
        "check_count": len(checks),
        "passed_count": sum(item["passed"] for item in checks),
        "failed_count": sum(not item["passed"] for item in checks),
        "all_passed": all_passed,
        "checks": checks,
        "model_payload_sha256": model.get("payload_sha256", ""),
    }
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_idempotent_equation_decoration_smuggling_compact_receipt_v1",
            "task_id": "RT-20260816-011",
            "job_id": "AJ-RT-20260816-011-001",
            "status": "PASS" if all_passed else "FAIL",
            "verdict": "source_pure_as_written",
            "source_extension_classification": "new_ontology_primitive",
            "check_count": result["check_count"],
            "passed_count": result["passed_count"],
            "failed_count": result["failed_count"],
            "model_payload_sha256": result["model_payload_sha256"],
            "successor_packet_id": successor,
            "successor_executed": False,
            "distance_to_gr_changed": False,
            "physics_promotion_authorized": False,
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"{result['passed_count']}/{result['check_count']} checks passed")
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Focused deterministic validator for RT-20260812-002."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
ART = ROOT / "research_control/tasks/RT-20260812-002/artifacts"
REPORT = ART / "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_validation.json"
COMPACT = ART / "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_compact_receipt.json"
OBSTRUCTION = "OB-V22-P4T02-B2-FINITE-TYPED-PRESENTATION-ADMISSION-BRIDGE-SOURCE-PROVENANCE-001"
SUCCESSOR = "PKT-V22-P4T02-B2-POST-FINITE-TYPED-PRESENTATION-ADMISSION-BRIDGE-PROVENANCE-OBSTRUCTION-THEORETICAL-CONTINUATION-SELECTION-V1"
FREEZES = {
    "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
    "NDCL-V22-P4T02-B2-REPAIRED-QUOTIENT-DESCENT-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-COMMON-CHARACTER-HOLONOMY-PROTECTION",
    "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
    "NDCL-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-ROBUSTNESS",
}
SOURCE_HASHES = {
    "implementations_plans/recommendations_implementation_plan_continue_task-v22.md":
        "04628b66c60229f4a1411018fe3da49cb8fbecba1d93aef6f163f9eaf6046c65",
    "research_control/handoffs/handoff-1028.yaml":
        "5119eb3dda31707a85ab95f6dabd3e105c0c1777b287b61de5babb2abc9f33f5",
    "research_control/tasks/RT-20260812-001/artifacts/"
    "v22_p4_t02_b2_post_bounded_current_signature_census_selected_future_packet_v1.yaml":
        "123c27c6236a0e0d70abc0cc3a86d11c2e28572343d000c18cc5eaed0950e83c",
    "research_control/tasks/RT-20260812-001/artifacts/"
    "parent_fusion_notes_p4_t02_b2_post_bounded_current_signature_census_selector.md":
        "9b14e071aa96bf1158052abe8716941d1e58dd20a04bb6d5ce397082207999c8",
    "research_control/tasks/RT-20260811-013/artifacts/"
    "v22_p4_t02_b2_bounded_natural_invariant_presentation_admission_census_v1.tex":
        "cc085f8c1eba1da27cdab75941f975e0310ac05d785609f2eac9495067b7af7d",
    "ontology/tex/aether_flow_foundations.tex":
        "4749d9e8b6858a43230e99029cccc3274b55fc2ae2a2cdf45a983a60c98e5b59",
    "ontology/tex/aether_flow_dynamics.tex":
        "fd6e579e71ef7f2ac4c9668ceede051ad57033ee52357b2552a9e3a5a53939c7",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueKeyLoader, node: yaml.Node, deep: bool = False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def add(checks: list[dict[str, object]], check_id: str, passed: bool, detail: str) -> None:
    checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})


def model_output() -> dict[str, object]:
    command = [
        sys.executable,
        str(ART / "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_model.py"),
        "--json",
    ]
    result = subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True)
    return json.loads(result.stdout)


def validate() -> dict[str, object]:
    checks: list[dict[str, object]] = []
    required = [
        "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_or_provenance_obstruction_v1.tex",
        "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_or_provenance_obstruction_record_v1.yaml",
        "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_fixtures_v1.yaml",
        "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_source_provenance_manifest_v1.yaml",
        "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_model.py",
        "child_phys_math_p4_t02_b2_finite_typed_presentation_admission_bridge_witness.yaml",
        "child_phys_phil_p4_t02_b2_finite_typed_presentation_admission_bridge_witness.yaml",
        "parent_conflict_review_p4_t02_b2_finite_typed_presentation_admission_bridge_witness.yaml",
        "parent_fusion_notes_p4_t02_b2_finite_typed_presentation_admission_bridge_witness.md",
        "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_latex_compile_receipt.json",
    ]
    missing = [name for name in required if not (ART / name).is_file()]
    add(checks, "required_artifacts", not missing, f"missing={missing}")

    record = load_yaml(ART / required[1])
    fixtures = load_yaml(ART / required[2])
    provenance = load_yaml(ART / required[3])
    child_math = load_yaml(ART / required[5])
    child_phil = load_yaml(ART / required[6])
    conflict = load_yaml(ART / required[7])
    compile_receipt = json.loads((ART / required[9]).read_text(encoding="utf-8"))
    model = model_output()

    result = record["candidate_constructor_result"]
    add(checks, "primary_result", result["result_type"] == "precise_obstruction", str(result))
    add(checks, "scientific_subresult", result["scientific_subresult"] == "source_provenance_obstruction", str(result))
    add(checks, "obstruction_identity", result["obstruction_id"] == OBSTRUCTION, result["obstruction_id"])
    add(checks, "no_fog", result["no_fog_check"] is True, result["no_fog_explanation"])
    bridge = record["bridge_attempt_status"]
    add(checks, "bridge_attempt", bridge["status"] == "precisely_obstructed_before_positive_construction" and bridge["positive_branch_executed"] is False, str(bridge))

    gates = record["gate_results"]
    gate_status = {row["gate_id"]: row["status"] for row in gates}
    add(checks, "six_gates", len(gates) == 6, str(gate_status))
    add(checks, "gate_four_only_failure", gate_status.get("GATE-04") == "fail" and sum(v == "fail" for v in gate_status.values()) == 1, str(gate_status))
    add(checks, "proof_obligations", len(record["proof_obligations"]) == 14, str(len(record["proof_obligations"])))
    branches = record["failure_branches"]
    add(checks, "failure_branches", len(branches) == 12 and [row["failure_id"] for row in branches if row["triggered"]] == ["FB-06"], str(branches))
    add(checks, "new_mathematical_payload", len(record["new_mathematical_payload"]) >= 1, str(len(record["new_mathematical_payload"])))
    add(checks, "six_freezes", set(record["preserved_freeze_labels"]) == FREEZES, str(record["preserved_freeze_labels"]))
    distance = record["distance_to_gr_status"]
    add(checks, "distance_to_gr", len(distance) == 14 and all(row["status"] == "no_delta" for row in distance), str(distance))
    locks = record["downstream_locks"]
    add(checks, "downstream_locks", locks["d7_reevaluated"] is False and locks["b2_activated"] is False and locks["p4_t03_locked"] is True, str(locks))
    successor = record["selected_successor"]
    add(checks, "successor_unexecuted", successor["packet_id"] == SUCCESSOR and successor["status"] == "selected_not_executed", str(successor))
    authority = record["authority_limits"]
    add(checks, "authority_blocks", all(value is False for value in authority.values()), str(authority))

    pair = fixtures["pair_groupoid_control"]
    add(checks, "fixture_cardinalities", len(pair["object_carrier"]) == 2 and len(pair["arrow_carrier"]) == 4 and len(pair["all_boolean_predicates"]) == 4 and len(pair["natural_boolean_predicates"]) == 2, str(pair))
    add(checks, "fixture_no_unique_natural_admission", pair["unique_natural_admission_count"] == 0, str(pair))
    add(checks, "provenance_failure", provenance["provenance_verdict"]["independent_source_provenance_passed"] is False and provenance["provenance_verdict"]["positive_branch_executed"] is False, str(provenance["provenance_verdict"]))

    add(checks, "model_status", model["status"] == "PASS" and model["pass_count"] == model["check_count"] == 16, str(model.get("checks")))
    add(checks, "model_result", model["result_type"] == "precise_obstruction" and model["scientific_subresult"] == "source_provenance_obstruction", str(model))

    for label, child in (("math", child_math), ("phil", child_phil)):
        child_text = json.dumps(child, sort_keys=True)
        add(checks, f"child_{label}_result", "source_provenance_obstruction" in child_text and "precise_obstruction" in child_text, child_text[:500])
        add(checks, f"child_{label}_freezes", all(item in child_text for item in FREEZES), f"freeze_mentions={sum(item in child_text for item in FREEZES)}")
        add(checks, f"child_{label}_distance", child_text.count('no_delta') >= 14, f"no_delta_mentions={child_text.count('no_delta')}")

    conflict_text = json.dumps(conflict, sort_keys=True)
    add(checks, "parent_conflict_review", "unresolved" in conflict_text and ("0" in conflict_text or "false" in conflict_text.lower()), conflict_text[:600])
    tex = (ART / required[0]).read_text(encoding="utf-8")
    for token in (OBSTRUCTION, "source\\_provenance\\_obstruction", "No natural root", "Theory-scope old-language conservativity"):
        add(checks, f"tex_{hashlib.sha256(token.encode()).hexdigest()[:8]}", token in tex, token)
    add(checks, "compile_receipt", compile_receipt.get("status") == "PASS", str(compile_receipt))

    for path, expected in SOURCE_HASHES.items():
        actual = sha256(ROOT / path)
        add(checks, f"source_hash_{hashlib.sha256(path.encode()).hexdigest()[:8]}", actual == expected, f"{path}:{actual}")

    status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    return {
        "schema_id": "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_validation_v1",
        "status": status,
        "task_id": "RT-20260812-002",
        "job_id": "AJ-RT-20260812-002-001",
        "result_type": "precise_obstruction",
        "scientific_subresult": "source_provenance_obstruction",
        "check_count": len(checks),
        "pass_count": sum(row["status"] == "PASS" for row in checks),
        "fail_count": sum(row["status"] == "FAIL" for row in checks),
        "checks": checks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        compact = {
            "schema_id": "v22_p4_t02_b2_finite_typed_presentation_admission_bridge_witness_compact_receipt_v1",
            "status": report["status"],
            "task_id": report["task_id"],
            "job_id": report["job_id"],
            "result_type": report["result_type"],
            "scientific_subresult": report["scientific_subresult"],
            "check_count": report["check_count"],
            "pass_count": report["pass_count"],
            "fail_count": report["fail_count"],
            "validation_report_path": str(REPORT.relative_to(ROOT)),
            "validation_report_sha256": sha256(REPORT),
        }
        COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

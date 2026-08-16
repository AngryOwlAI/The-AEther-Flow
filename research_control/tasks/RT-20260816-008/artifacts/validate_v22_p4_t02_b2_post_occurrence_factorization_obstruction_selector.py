#!/usr/bin/env python3
"""Focused validator for the RT008 post-obstruction theoretical selector."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


REPO = Path(__file__).resolve().parents[4]
ART = Path(__file__).resolve().parent
VALIDATION = ART / "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selector_validation.json"
COMPACT = ART / "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selector_compact_receipt.json"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top level must be mapping")
    return value


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    paths = {
        "task": REPO / "research_control/tasks/RT-20260816-008/00_TASK.yaml",
        "job": REPO / "research_control/tasks/RT-20260816-008/jobs/AJ-RT-20260816-008-001.yaml",
        "role": REPO / "research_control/tasks/RT-20260816-008/roles/theoretical-continuation-selector@0.1.0--RT-20260816-008.yaml",
        "math": ART / "child_phys_math_p4_t02_b2_post_occurrence_factorization_obstruction_selector.yaml",
        "phil": ART / "child_phys_phil_p4_t02_b2_post_occurrence_factorization_obstruction_selector.yaml",
        "comparison": ART / "v22_p4_t02_b2_post_occurrence_factorization_obstruction_route_comparison_v1.yaml",
        "decision": ART / "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selector_decision_v1.yaml",
        "future": ART / "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selected_future_packet_v1.yaml",
        "conflict": ART / "parent_conflict_review_p4_t02_b2_post_occurrence_factorization_obstruction_selector.yaml",
        "fusion": ART / "parent_fusion_notes_p4_t02_b2_post_occurrence_factorization_obstruction_selector.md",
        "tex": ART / "v22_p4_t02_b2_post_occurrence_factorization_obstruction_route_selection_v1.tex",
        "model": ART / "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selector_model.py",
        "provenance": ART / "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selector_provenance_manifest_v1.yaml",
    }
    missing = [name for name, path in paths.items() if not path.is_file()]
    check("V01_REQUIRED_FILES", not missing, repr(missing))
    if missing:
        return emit(checks)

    loaded: dict[str, dict[str, Any]] = {}
    try:
        for name in ("task", "job", "role", "math", "phil", "comparison", "decision", "future", "conflict", "provenance"):
            loaded[name] = load_yaml(paths[name])
        check("V02_STRICT_UNIQUE_YAML", True, "all YAML files parsed with duplicate-key rejection")
    except Exception as exc:
        check("V02_STRICT_UNIQUE_YAML", False, str(exc))
        return emit(checks)

    comparison = loaded["comparison"]
    decision = loaded["decision"]
    future = loaded["future"]
    routes = comparison.get("routes", [])
    selected = [row for row in routes if isinstance(row, dict) and row.get("selected") is True]
    check("V03_EXACT_FOUR_ROUTES_ONE_SELECTED", len(routes) == 4 and len(selected) == 1, f"routes={len(routes)} selected={len(selected)}")
    selected_route = comparison.get("selection", {}).get("selected_route_id")
    check("V04_ROUTE_B_SELECTED", selected_route == "B_MINIMAL_PROPOSAL_ONLY_COMBINED_OCCURRENCE_EXTENSION_LAW", str(selected_route))

    packet_id = comparison.get("selection", {}).get("selected_packet_id")
    aligned = (
        packet_id
        and packet_id == decision.get("decisive_result", {}).get("packet_id")
        and packet_id == decision.get("theoretical_decision_output", {}).get("selected_packet_id")
        and packet_id == future.get("packet_id")
    )
    check("V05_CANONICAL_PACKET_ID_ALIGNED", bool(aligned), str(packet_id))
    check(
        "V06_PACKET_TYPE_ROLE_STATUS",
        comparison.get("selection", {}).get("selected_packet_type") == "ontology_law_research_packet"
        and comparison.get("selection", {}).get("selected_next_role_family") == "ontology-formalizer@0.2.0"
        and future.get("selected_packet_executed") is False
        and future.get("execution_authorized") is False,
        "ontology-law packet / ontology-formalizer / unexecuted",
    )

    child_texts = {name: paths[name].read_text(encoding="utf-8") for name in ("math", "phil")}
    child_route_ok = all("B_MINIMAL_PROPOSAL_ONLY_COMBINED_OCCURRENCE_EXTENSION_LAW" in text for text in child_texts.values())
    child_packet_ok = all(packet_id in text for text in child_texts.values())
    check("V07_CHILD_ROUTE_CONSENSUS", child_route_ok, "both children contain Route B")
    check("V08_CHILD_PACKET_ID_CONSENSUS", child_packet_ok, "both children contain canonical packet ID")

    conflict = loaded["conflict"]
    check(
        "V09_NO_UNRESOLVED_CONFLICT",
        conflict.get("unresolved_blocking_conflict_count") == 0
        and conflict.get("parent_disposition") == "consensus_route_B_selected",
        repr({key: conflict.get(key) for key in ("unresolved_blocking_conflict_count", "parent_disposition")}),
    )

    freezes = decision.get("preserved_freeze_labels", [])
    check("V10_NINE_UNIQUE_FREEZES", len(freezes) == len(set(freezes)) == 9, str(len(freezes)))
    distance = decision.get("distance_to_gr_status", [])
    check(
        "V11_FOURTEEN_LITERAL_NO_DELTA",
        len(distance) == 14 and all(row.get("status") == "no_delta" for row in distance if isinstance(row, dict)),
        str(len(distance)),
    )
    limits = decision.get("downstream_locks", {})
    check(
        "V12_DOWNSTREAM_LOCKS",
        limits.get("d7_reevaluated") is False
        and limits.get("b2_activated") is False
        and limits.get("p4_t03_locked") is True
        and limits.get("selected_packet_executed") is False,
        repr(limits),
    )

    model_run = subprocess.run([sys.executable, str(paths["model"])], cwd=REPO, text=True, capture_output=True)
    try:
        model_payload = json.loads(model_run.stdout)
    except Exception:
        model_payload = {}
    check(
        "V13_EXACT_MODEL_22_OF_22",
        model_run.returncode == 0 and model_payload.get("check_count") == 22 and model_payload.get("pass_count") == 22,
        model_run.stderr or repr({key: model_payload.get(key) for key in ("check_count", "pass_count", "fail_count")}),
    )

    provenance = loaded["provenance"]
    source_rows = provenance.get("sources", [])
    hash_errors: list[str] = []
    for row in source_rows:
        if not isinstance(row, dict):
            hash_errors.append("non-mapping source row")
            continue
        source = REPO / str(row.get("path", ""))
        expected = str(row.get("sha256", ""))
        if not source.is_file() or sha256(source) != expected:
            hash_errors.append(str(row.get("path", "")))
    check("V14_PROVENANCE_HASHES", not hash_errors and len(source_rows) >= 8, repr(hash_errors))

    tex_text = paths["tex"].read_text(encoding="utf-8")
    fusion_text = paths["fusion"].read_text(encoding="utf-8")
    check("V15_TEX_DECISION_IDENTITY", packet_id in tex_text and "selected_not_executed" in tex_text, packet_id)
    check("V16_FUSION_DECISION_IDENTITY", packet_id in fusion_text and "Route B" in fusion_text, packet_id)

    whitespace_errors: list[str] = []
    for name, path in paths.items():
        if not path.is_file() or path.suffix not in {".yaml", ".md", ".tex", ".py"}:
            continue
        text = path.read_text(encoding="utf-8")
        for index, line in enumerate(text.splitlines(), start=1):
            if "\t" in line or line.rstrip() != line:
                whitespace_errors.append(f"{name}:{index}")
        if text and not text.endswith("\n"):
            whitespace_errors.append(f"{name}:missing-final-newline")
    check("V17_WHITESPACE_AND_EOF", not whitespace_errors, repr(whitespace_errors[:20]))

    task = loaded["task"]
    job = loaded["job"]
    check(
        "V18_ONE_OUTER_JOB_TWO_CHILDREN",
        task.get("current_job_id") == "AJ-RT-20260816-008-001"
        and job.get("role_decomposition", {}).get("outer_agentjob_count") == 1
        and job.get("role_decomposition", {}).get("subagent_count") == 2,
        "1 outer / 2 internal children",
    )
    check("V19_SELECTED_PACKET_NOT_EXECUTED", "selected_not_executed" in tex_text and future.get("selected_packet_executed") is False, "selection only")
    check("V20_NO_PHYSICS_PROMOTION", decision.get("authority_limits", {}).get("physics_promotion_authorized") is False, "blocked")

    return emit(checks, model_payload=model_payload)


def emit(checks: list[dict[str, Any]], model_payload: dict[str, Any] | None = None) -> int:
    passed = sum(row["status"] == "PASS" for row in checks)
    failed = len(checks) - passed
    payload = {
        "schema_id": "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selector_validation_v1",
        "status": "PASS" if failed == 0 else "FAIL",
        "check_count": len(checks),
        "pass_count": passed,
        "fail_count": failed,
        "checks": checks,
        "model_payload_sha256": (model_payload or {}).get("payload_sha256", ""),
        "physics_claim_authority": False,
    }
    VALIDATION.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    compact = {
        "schema_id": "v22_p4_t02_b2_post_occurrence_factorization_obstruction_selector_compact_receipt_v1",
        "status": payload["status"],
        "validation_path": str(VALIDATION.relative_to(REPO)),
        "validation_sha256": sha256(VALIDATION),
        "check_count": len(checks),
        "pass_count": passed,
        "fail_count": failed,
        "failed_check_ids": [row["check_id"] for row in checks if row["status"] != "PASS"],
        "physics_claim_authority": False,
    }
    COMPACT.write_text(json.dumps(compact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(compact, indent=2, sort_keys=True))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

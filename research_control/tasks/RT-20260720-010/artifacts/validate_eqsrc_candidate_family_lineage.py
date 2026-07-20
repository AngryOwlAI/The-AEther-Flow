#!/usr/bin/env python3
"""Validate the bounded v21 P1-T02 EqSrc candidate-family lineage packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


ARTIFACT_DIR = Path(__file__).resolve().parent
REPO_ROOT = ARTIFACT_DIR.parents[3]
INVENTORY_PATH = ARTIFACT_DIR / "eqsrc_canonical_choice_family_inventory.json"
GRAPH_PATH = ARTIFACT_DIR / "eqsrc_candidate_lineage_graph.json"
DELTA_PATH = ARTIFACT_DIR / "eqsrc_family_assumption_delta.csv"
TEX_PATH = ARTIFACT_DIR / "eqsrc_canonical_choice_family_map.tex"
REPORT_PATH = ARTIFACT_DIR / "eqsrc_candidate_family_lineage_validation.json"


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def theorem_statement_payload(source_text: str) -> tuple[int, bytes]:
    blocks = re.findall(
        r"\\begin\{(?:theorem|proposition)\}.*?\\end\{(?:theorem|proposition)\}",
        source_text,
        flags=re.DOTALL,
    )
    normalized = [block.replace("\r\n", "\n").replace("\r", "\n") for block in blocks]
    return len(normalized), "\n".join(normalized).encode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def validate() -> dict[str, Any]:
    errors: list[str] = []
    checks: list[dict[str, Any]] = []

    inventory = load_json(INVENTORY_PATH)
    graph = load_json(GRAPH_PATH)
    with DELTA_PATH.open(newline="", encoding="utf-8") as handle:
        delta_rows = list(csv.DictReader(handle))
    tex = TEX_PATH.read_text(encoding="utf-8")

    def record(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        if not passed:
            errors.append(f"{check_id}: {detail}")

    candidates = inventory.get("candidates", [])
    families = inventory.get("families", [])
    candidate_ids = [candidate.get("immutable_candidate_id") for candidate in candidates]
    family_ids = [family.get("family_id") for family in families]
    record("inventory_shape", len(candidates) == 7 and len(families) == 5, f"candidates={len(candidates)} families={len(families)}")
    record("candidate_ids_unique", len(candidate_ids) == len(set(candidate_ids)), f"count={len(candidate_ids)}")
    record("family_ids_unique", len(family_ids) == len(set(family_ids)), f"count={len(family_ids)}")

    ontology = inventory.get("ontology_anchor", {})
    ontology_path = REPO_ROOT / str(ontology.get("path", ""))
    ontology_ok = ontology_path.is_file() and file_sha256(ontology_path) == ontology.get("sha256")
    record("ontology_anchor_hash", ontology_ok, str(ontology_path.relative_to(REPO_ROOT)) if ontology_path.exists() else "missing")

    candidate_hash_errors = 0
    signature_hash_errors = 0
    identity_tuples: list[tuple[str, str, str, str]] = []
    for candidate in candidates:
        candidate_id = str(candidate.get("immutable_candidate_id", ""))
        source_path = REPO_ROOT / str(candidate.get("artifact_path", ""))
        if not source_path.is_file() or file_sha256(source_path) != candidate.get("artifact_sha256"):
            candidate_hash_errors += 1
        source_text = source_path.read_text(encoding="utf-8") if source_path.is_file() else ""
        theorem_count, theorem_payload = theorem_statement_payload(source_text)
        theorem_hash = hashlib.sha256(theorem_payload).hexdigest()
        assumption_hash = canonical_sha256(candidate.get("assumption_signature"))
        if (
            theorem_count != candidate.get("theorem_statement_block_count")
            or theorem_hash != candidate.get("theorem_statement_sha256")
            or assumption_hash != candidate.get("assumption_sha256")
            or not candidate.get("theorem_signature")
        ):
            signature_hash_errors += 1
        if candidate.get("status_label") != "proposal-only" or candidate.get("exact_duplicate_of") is not None:
            errors.append(f"candidate_status: {candidate_id}")
        identity_tuples.append(
            (
                str(candidate.get("artifact_sha256")),
                str(candidate.get("theorem_statement_sha256")),
                str(candidate.get("assumption_sha256")),
                str(candidate.get("ontology_anchor_sha256")),
            )
        )
    record("candidate_artifact_hashes", candidate_hash_errors == 0, f"mismatches={candidate_hash_errors}")
    record("theorem_and_assumption_hashes", signature_hash_errors == 0, f"mismatches={signature_hash_errors}")
    record("exact_duplicate_count", len(identity_tuples) == len(set(identity_tuples)), "expected=0")

    family_members = []
    for family in families:
        family_members.extend(family.get("member_candidate_ids", []))
        if family.get("global_no_go") is not False:
            errors.append(f"family_global_no_go: {family.get('family_id')}")
    record("family_membership_partition", sorted(family_members) == sorted(candidate_ids), f"member_refs={len(family_members)}")

    order = graph.get("node_order", {})
    edges = graph.get("candidate_edges", [])
    stage_records = graph.get("stage_records", [])
    record("graph_node_parity", set(order) == set(candidate_ids), f"nodes={len(order)}")
    record("graph_edge_count", len(edges) == 6, f"edges={len(edges)}")
    record("stage_count", len(stage_records) == 22, f"stages={len(stage_records)}")

    edge_ids: list[str] = []
    adjacency: dict[str, list[str]] = {candidate_id: [] for candidate_id in candidate_ids}
    indegree: dict[str, int] = {candidate_id: 0 for candidate_id in candidate_ids}
    edge_errors = 0
    for edge in edges:
        edge_id = str(edge.get("edge_id", ""))
        source = str(edge.get("from_candidate_id", ""))
        target = str(edge.get("to_candidate_id", ""))
        edge_ids.append(edge_id)
        if source not in order or target not in order or order[source] >= order[target]:
            edge_errors += 1
            continue
        adjacency[source].append(target)
        indegree[target] += 1
        evidence_path_value = edge.get("evidence_path")
        if evidence_path_value:
            evidence_path = REPO_ROOT / str(evidence_path_value)
            if not evidence_path.is_file() or file_sha256(evidence_path) != edge.get("evidence_sha256"):
                edge_errors += 1
        if edge.get("edge_type") == "distinct_family_route_successor_after_local_freeze" and edge.get("supersedes") is not False:
            edge_errors += 1
    record("edge_identity_and_order", edge_errors == 0 and len(edge_ids) == len(set(edge_ids)), f"errors={edge_errors}")

    ready = [node for node, degree in indegree.items() if degree == 0]
    visited = 0
    while ready:
        node = ready.pop()
        visited += 1
        for target in adjacency[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                ready.append(target)
    record("lineage_acyclic", visited == len(candidate_ids), f"visited={visited}")

    stage_ids: list[str] = []
    stage_errors = 0
    for stage in stage_records:
        stage_ids.append(str(stage.get("stage_id", "")))
        if stage.get("candidate_id") not in candidate_ids:
            stage_errors += 1
        artifact_path = REPO_ROOT / str(stage.get("artifact_path", ""))
        if not artifact_path.is_file() or file_sha256(artifact_path) != stage.get("artifact_sha256"):
            stage_errors += 1
    record("stage_identity_and_hashes", stage_errors == 0 and len(stage_ids) == len(set(stage_ids)), f"errors={stage_errors}")

    delta_edge_ids = [row.get("edge_id", "") for row in delta_rows]
    delta_classes = {"semantic_claim_scope_repair", "typed_theorem_interface_repair", "genuine_source_assumption_change"}
    delta_ok = (
        len(delta_rows) == 6
        and set(delta_edge_ids) == set(edge_ids)
        and all(row.get("change_class") in delta_classes for row in delta_rows)
        and all(row.get("representation_only") == "false" for row in delta_rows)
    )
    record("assumption_delta_parity", delta_ok, f"rows={len(delta_rows)}")

    required_tex_tokens = [
        "Acyclicity of the exact candidate graph",
        "Distinct selected lines give distinct relations",
        "blocked\\_adoption\\_open\\_continuation",
        "No global no-go",
        "P1-T03",
        "Distance-to-GR ledger & Unchanged",
        "does not establish source provenance",
    ]
    missing_tex_tokens = [token for token in required_tex_tokens if token not in tex]
    record("formal_artifact_boundary", not missing_tex_tokens, f"missing={missing_tex_tokens}")

    authority = inventory.get("authority_boundary", {})
    freeze = inventory.get("freeze_boundary", {})
    authority_ok = (
        authority.get("classification") == "blocked_adoption_open_continuation"
        and authority.get("canonical_ontology_edit_authorized") is False
        and authority.get("source_law_adoption_authorized") is False
        and authority.get("family_freeze_authorized") is False
        and authority.get("physics_promotion_authorized") is False
        and authority.get("distance_to_gr_delta_changed") is False
        and freeze.get("active_family_freeze_decision") == "freeze_review_required"
        and freeze.get("decision_owner") == "P1-T03"
        and freeze.get("p1_t03_executed") is False
    )
    record("authority_and_freeze_boundary", authority_ok, "P1-T03 reserved; promotion false")

    status = "PASS" if not errors else "FAIL"
    return {
        "schema_id": "v21_p1_t02_eqsrc_candidate_family_lineage_validation_v1",
        "task_id": "RT-20260720-010",
        "status": status,
        "operational_evidence_only": True,
        "physics_proof_authority": False,
        "physics_promotion_authorized": False,
        "counts": {
            "families": len(families),
            "candidates": len(candidates),
            "candidate_edges": len(edges),
            "stage_records": len(stage_records),
            "assumption_delta_rows": len(delta_rows),
            "exact_duplicates": len(identity_tuples) - len(set(identity_tuples)),
            "errors": len(errors),
        },
        "artifact_hashes": {
            "inventory": file_sha256(INVENTORY_PATH),
            "lineage_graph": file_sha256(GRAPH_PATH),
            "assumption_delta": file_sha256(DELTA_PATH),
            "formal_map": file_sha256(TEX_PATH),
        },
        "checks": checks,
        "errors": errors,
        "claim_boundary_summary": "Structural PASS cannot prove source-law derivation adoption family freeze general EqSrc downstream GR or benchmark promotion. P1-T03 remains reserved.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.write_report:
        atomic_write_json(REPORT_PATH, report)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: {report['counts']}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Focused deterministic validator for RT-20260816-012."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260816-012"
ART = TASK / "artifacts"
PREFIX = "v22_p4_t02_b2_idempotent_equation_decoration_null_semantics_rank_topology_refuter_stress"


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


UniqueLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def load_yaml(path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueLoader)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--verified-at", default="2026-08-16T22:18:00Z")
    args = parser.parse_args()

    checks = []

    def add(check_id, condition, evidence):
        checks.append({"id": check_id, "pass": bool(condition), "evidence": evidence})

    task = load_yaml(TASK / "00_TASK.yaml")
    job = load_yaml(TASK / "jobs/AJ-RT-20260816-012-001.yaml")
    role = load_yaml(TASK / "roles/refuter@0.2.0--RT-20260816-012.yaml")
    matrix_path = ART / f"{PREFIX}_matrix_v1.yaml"
    disposition_path = ART / f"{PREFIX}_disposition_v1.yaml"
    obstruction_path = ART / f"{PREFIX}_obstruction_v1.yaml"
    model_path = ART / f"{PREFIX}_model.py"
    tex_path = ART / f"{PREFIX}_v1.tex"
    matrix = load_yaml(matrix_path)
    disposition = load_yaml(disposition_path)
    obstruction = load_yaml(obstruction_path)

    add("VAL-01", task["task_id"] == "RT-20260816-012", "task identity")
    add("VAL-02", job["job_id"] == "AJ-RT-20260816-012-001", "job identity")
    add("VAL-03", role["execution_role_ref"] == "refuter@0.2.0--RT-20260816-012", "role identity")
    add("VAL-04", matrix["result_type"] == "scoped_obstruction" and matrix["result_type_count"] == 1, "exclusive Refuter class")
    add("VAL-05", len(matrix["stress_dimensions"]) == 10, "ten stress dimensions")
    add("VAL-06", len(matrix["proof_obligations"]) == 16 and all(x["status"] == "discharged" for x in matrix["proof_obligations"]), "sixteen discharged obligations")
    add("VAL-07", len(matrix["failure_branches"]) == 14, "fourteen failure branches")
    add("VAL-08", len(matrix["inherited_freezes"]) == 9 and all(x["status"] == "preserved" for x in matrix["inherited_freezes"]), "nine preserved freezes")
    add("VAL-09", len(matrix["distance_to_gr_status"]) == 14 and all(x["task_delta"] == "no_delta" for x in matrix["distance_to_gr_status"]), "fourteen literal no-delta rows")
    add("VAL-10", matrix["candidate_local_freeze"]["status"] in {"recommended_for_parent_fusion", "locally_frozen"}, "candidate-local freeze")
    add("VAL-11", disposition["exclusive_result"]["result_type"] == "scoped_obstruction", "disposition identity")
    add("VAL-12", obstruction["refuter_class"] == "scoped_obstruction", "formal obstruction record")
    add("VAL-13", obstruction["obstruction_id"] == matrix["obstruction_id"], "obstruction ID convergence")
    add("VAL-14", disposition["successor"]["status"] == "selected_not_executed" and not disposition["successor"]["executed"], "one unexecuted successor")
    add("VAL-15", not any(disposition["authority"].values()), "all disposition authority booleans false")

    model = json.loads(subprocess.check_output([sys.executable, str(model_path)], text=True))
    add("VAL-16", model["check_count"] == 24 and model["pass_count"] == 24, "exact model 24/24")
    add("VAL-17", model["payload_sha256"] == matrix["model_receipt"]["payload_sha256"], "model payload bound")

    child_math = ART / "child_phys_math_p4_t02_b2_idempotent_equation_decoration_null_semantics_rank_topology_refuter_stress.yaml"
    child_phil = ART / "child_phys_phil_p4_t02_b2_idempotent_equation_decoration_null_semantics_rank_topology_refuter_stress.yaml"
    add("VAL-18", child_math.exists() and child_phil.exists(), "two child artifacts")
    child_text = (child_math.read_text(encoding="utf-8") if child_math.exists() else "") + (child_phil.read_text(encoding="utf-8") if child_phil.exists() else "")
    add("VAL-19", child_text.count("scoped_obstruction") >= 2, "child result convergence")

    review = ART / "parent_conflict_review_p4_t02_b2_idempotent_equation_decoration_null_semantics_rank_topology_refuter_stress.yaml"
    fusion = ART / "parent_fusion_notes_p4_t02_b2_idempotent_equation_decoration_null_semantics_rank_topology_refuter_stress.md"
    add("VAL-20", review.exists() and fusion.exists(), "parent review and fusion")
    if review.exists():
        review_doc = load_yaml(review)
        add("VAL-21", review_doc.get("unresolved_conflict_count") == 0, "zero unresolved conflicts")
    else:
        add("VAL-21", False, "review missing")

    tex = tex_path.read_text(encoding="utf-8")
    add("VAL-22", "scoped\\_obstruction" in tex and "24 of 24" in tex, "manuscript decisive result and model")
    add("VAL-23", all(path.read_bytes().endswith(b"\n") for path in TASK.rglob("*") if path.is_file()), "all task files end with newline")
    add("VAL-24", all(b"\t" not in path.read_bytes() and not any(line.endswith(b" ") for line in path.read_bytes().splitlines()) for path in TASK.rglob("*") if path.is_file()), "no tabs or trailing whitespace")

    payload = {
        "schema_id": "v22_p4_t02_b2_idempotent_null_rank_topology_refuter_validation_v1",
        "task_id": "RT-20260816-012",
        "job_id": "AJ-RT-20260816-012-001",
        "status": "PASS" if all(c["pass"] for c in checks) else "FAIL",
        "verified_at": args.verified_at,
        "check_count": len(checks),
        "pass_count": sum(c["pass"] for c in checks),
        "failure_count": sum(not c["pass"] for c in checks),
        "checks": checks,
        "artifact_sha256": {
            "matrix": sha256(matrix_path),
            "disposition": sha256(disposition_path),
            "obstruction": sha256(obstruction_path),
            "model": sha256(model_path),
            "tex": sha256(tex_path),
        },
        "model_payload_sha256": model["payload_sha256"],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    if args.write:
        out = ART / f"{PREFIX}_validation.json"
        out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    raise SystemExit(0 if payload["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()

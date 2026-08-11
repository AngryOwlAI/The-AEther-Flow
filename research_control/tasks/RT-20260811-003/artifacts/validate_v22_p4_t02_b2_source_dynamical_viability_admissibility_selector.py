#!/usr/bin/env python3
"""Focused deterministic validator for RT-20260811-003."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[4]
TASK = ROOT / "research_control/tasks/RT-20260811-003"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_validation.json"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_unique(path: Path) -> Any:
    return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, Any]] = []

    def check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})

    required = [
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260811-003.md",
        TASK / "jobs/AJ-RT-20260811-003-001.yaml",
        TASK / "roles/ontology-formalizer@0.2.0--RT-20260811-003.yaml",
        ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_law_v1.tex",
        ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_spec_v1.yaml",
        ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_provenance_manifest_v1.yaml",
        ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_disposition_v1.yaml",
        ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_model.py",
        ART / "child_phys_math_p4_t02_b2_source_dynamical_viability_admissibility_selector.yaml",
        ART / "child_phys_phil_p4_t02_b2_source_dynamical_viability_admissibility_selector.yaml",
        ART / "parent_conflict_review_p4_t02_b2_source_dynamical_viability_admissibility_selector.yaml",
        ART / "parent_fusion_notes_p4_t02_b2_source_dynamical_viability_admissibility_selector.md",
        ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_latex_compile_receipt.json",
        TASK / "documentation_impact.yaml",
    ]
    for path in required:
        check(f"exists:{path.relative_to(ROOT)}", path.is_file(), "required artifact exists")

    parsed: dict[Path, Any] = {}
    yaml_paths = [p for p in required if p.suffix == ".yaml" and p.is_file()]
    for path in yaml_paths:
        try:
            parsed[path] = load_unique(path)
            check(f"yaml_unique:{path.relative_to(ROOT)}", True, "strict unique-key parse")
        except Exception as exc:  # noqa: BLE001
            check(f"yaml_unique:{path.relative_to(ROOT)}", False, str(exc))

    spec_path = ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_spec_v1.yaml"
    spec = parsed.get(spec_path, {})
    if isinstance(spec, dict):
        check("spec:result", spec.get("formalization_attempt_status") == "proposal_only_candidate_source_law_formalized_pending_smuggling_audit", "decisive candidate status")
        check("spec:objects", len(spec.get("formal_objects", [])) == 10, "exactly ten formal objects")
        check("spec:maps", len(spec.get("formal_maps", [])) == 8, "exactly eight formal maps")
        check("spec:theorems", len(spec.get("theorems", [])) == 6, "exactly six theorem records")
        obligations = spec.get("proof_obligations", [])
        check("spec:obligations", len(obligations) == 14, "exactly fourteen proof obligations")
        check("spec:obligations_discharged", all(str(x.get("status", "")).startswith("discharged") for x in obligations), "all obligations discharged with explicit debt where applicable")
        check("spec:failure_branches", len(spec.get("failure_branches", [])) == 11, "exactly eleven failure branches")
        freezes = spec.get("preserved_freezes", [])
        check("spec:freezes", len(freezes) == 4 and all(x.get("status") == "active_untouched" for x in freezes), "four freezes active and untouched")
        distance = spec.get("distance_to_gr_status", [])
        check("spec:distance_rows", len(distance) == 14, "fourteen Distance-to-GR rows")
        check("spec:distance_no_delta", all(x.get("task_delta") == "no_delta" for x in distance), "all Distance-to-GR rows literal no_delta")
        added = spec.get("source_roots", {}).get("added_proposal_only", [])
        check("spec:proposal_roots", {x.get("root_id") for x in added} == {"POSITIVE-CUBIC-COEFFICIENT", "BOUNDED-STEP-HORIZON", "AMPLITUDE-REFERENCE", "SOURCE-ORIENTATION-TOKEN"}, "all proposal roots disclosed")
        map_rows = {x.get("map_id"): x for x in spec.get("formal_maps", [])}
        regrad = str(map_rows.get("POSITIVE-REGRADUATION", {}).get("signature", ""))
        check("spec:simultaneous_regraduation", "gamma/(c*d^2)" in regrad, "simultaneous regraduation coefficient is exact")

    disp_path = ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_disposition_v1.yaml"
    disp = parsed.get(disp_path, {})
    if isinstance(disp, dict):
        result = disp.get("decisive_result", {})
        successor = disp.get("selected_successor", {})
        check("disposition:result", result.get("result_status") == "proposal_only_candidate_source_law_formalized_pending_smuggling_audit" and result.get("candidate_constructed") is True, "candidate constructed pending audit")
        check("disposition:no_fog", result.get("no_fog_check") == "PASS", "no obligations-only fog")
        check("disposition:successor", successor.get("packet_id") == "PKT-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-SOURCE-EXTENSION-SMUGGLING-AUDIT-V1" and successor.get("next_role_family") == "smuggling-auditor@0.2.0" and successor.get("status") == "selected_not_executed", "one canonical unexecuted successor")
        check("disposition:payloads", len(disp.get("mathematical_payloads", [])) >= 5, "at least five new mathematical payloads")
        limits = disp.get("authority_limits", {})
        blocked_true = [
            limits.get("source_law_adopted"),
            limits.get("canonical_ontology_modified"),
            limits.get("successor_executed"),
            limits.get("adequacy_reevaluated"),
            limits.get("b2_activated_or_disposed"),
            limits.get("p4_t03_unlocked"),
            limits.get("distance_to_gr_changed"),
            limits.get("physics_promotion_authorized"),
            limits.get("proof_authority"),
            limits.get("publication_authorized"),
            limits.get("push_authorized"),
            limits.get("external_action_authorized"),
            limits.get("completed_derivation_claimed"),
        ]
        check("disposition:authority_blocks", all(x is False for x in blocked_true), "all protected authority limits false")

    manifest_path = ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_provenance_manifest_v1.yaml"
    manifest = parsed.get(manifest_path, {})
    if isinstance(manifest, dict):
        sources = manifest.get("sources", [])
        check("manifest:source_count", len(sources) == manifest.get("source_count") == 13, "thirteen source records")
        hash_ok = True
        for row in sources:
            path = ROOT / str(row.get("path", ""))
            hash_ok = hash_ok and path.is_file() and sha256(path) == row.get("sha256")
        check("manifest:source_hashes", hash_ok, "all live source hashes match")
        scan = manifest.get("forbidden_import_scan", {})
        check("manifest:forbidden_imports", all(value is False for value in scan.values()), "no forbidden import recorded")

    model_path = ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_model.py"
    if model_path.is_file():
        proc = subprocess.run([sys.executable, str(model_path), "--json"], cwd=ROOT, text=True, capture_output=True, check=False)
        try:
            model = json.loads(proc.stdout)
        except json.JSONDecodeError:
            model = {}
        check("model:exit", proc.returncode == 0, proc.stderr.strip() or "model exit zero")
        check("model:status", model.get("status") == "PASS", "exact model PASS")
        check("model:counts", model.get("check_count") == model.get("passed_check_count") == 10 and model.get("fixture_count") == 20, "10/10 checks and 20 fixtures")

    tex_path = ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_law_v1.tex"
    if tex_path.is_file():
        tex = tex_path.read_text(encoding="utf-8")
        phrases = [
            "Normalized bounded-step propagation",
            "Exact viability kernel",
            "Occurrence--viability independence",
            "Reflection-equivariant candidate family",
            "Positive regraduation covariance",
            "proposal\\_only\\_candidate\\_source\\_law\\_formalized\\_pending\\_smuggling\\_audit",
            "NDCL-V22-P4T02-B2-SHARED-TAU-SELECTOR",
            "NDCL-V22-P4T02-B2-ORIENTED-MATROID-BRIDGE-SELECTION-ROBUSTNESS",
        ]
        check("tex:semantic_phrases", all(p in tex for p in phrases), "theorem status and freeze phrases present")

    child_paths = [
        ART / "child_phys_math_p4_t02_b2_source_dynamical_viability_admissibility_selector.yaml",
        ART / "child_phys_phil_p4_t02_b2_source_dynamical_viability_admissibility_selector.yaml",
    ]
    for path in child_paths:
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            check(f"child:result:{path.name}", "proposal_only_candidate_source_law_formalized_pending_smuggling_audit" in text or "constructed_candidate" in text, "child supports one complete candidate result")
            check(f"child:successor:{path.name}", "PKT-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-SOURCE-EXTENSION-SMUGGLING-AUDIT-V1" in text and "selected_not_executed" in text, "child converges on canonical successor")
            check(f"child:no_delta:{path.name}", text.count("no_delta") >= 14, "child contains fourteen literal no_delta entries")

    conflict_path = ART / "parent_conflict_review_p4_t02_b2_source_dynamical_viability_admissibility_selector.yaml"
    conflict = parsed.get(conflict_path, {})
    if isinstance(conflict, dict):
        check("conflict:resolved", conflict.get("unresolved_blocking_conflict_count") == 0 and conflict.get("status") == "resolved", "no unresolved blocking parent-child conflict")

    compile_path = ART / "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_latex_compile_receipt.json"
    if compile_path.is_file():
        receipt = json.loads(compile_path.read_text(encoding="utf-8"))
        visual = receipt.get("visual_inspection", {})
        check("latex:compile", receipt.get("status") == "PASS" and receipt.get("exit_code") == 0, "LaTeX compile PASS")
        check("latex:visual", visual.get("status") == "PASS" and visual.get("clipped_text") is False and visual.get("overlapping_text") is False, "rendered visual inspection PASS")

    failed = [row for row in checks if row["status"] != "PASS"]
    report = {
        "schema_id": "v22_p4_t02_b2_source_dynamical_viability_admissibility_selector_validation_v1",
        "task_id": "RT-20260811-003",
        "job_id": "AJ-RT-20260811-003-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "checks": checks,
    }
    if args.write_report:
        REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

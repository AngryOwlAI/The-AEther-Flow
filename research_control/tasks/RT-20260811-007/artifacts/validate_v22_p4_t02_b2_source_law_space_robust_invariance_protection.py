#!/usr/bin/env python3
"""Focused deterministic validator for RT-20260811-007."""

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
TASK = ROOT / "research_control/tasks/RT-20260811-007"
ART = TASK / "artifacts"
REPORT = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_validation.json"
SUCCESSOR = "PKT-V22-P4T02-B2-SOURCE-LAW-SPACE-ROBUST-INVARIANCE-PROTECTION-SMUGGLING-AUDIT-V1"


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(
    loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise ValueError(
                f"duplicate YAML key {key!r} at line {key_node.start_mark.line + 1}"
            )
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
        checks.append(
            {
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )

    required = [
        TASK / "00_TASK.yaml",
        TASK / "DDR-20260811-007.md",
        TASK / "jobs/AJ-RT-20260811-007-001.yaml",
        TASK / "roles/ontology-formalizer@0.2.0--RT-20260811-007.yaml",
        ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_v1.tex",
        ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_record_v1.yaml",
        ART / "v22_p4_t02_b2_source_law_space_robust_invariance_controls_v1.yaml",
        ART / "v22_p4_t02_b2_source_law_space_robust_invariance_provenance_manifest_v1.yaml",
        ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_model.py",
        ART / "child_phys_math_p4_t02_b2_source_law_space_robust_invariance_protection.yaml",
        ART / "child_phys_phil_p4_t02_b2_source_law_space_robust_invariance_protection.yaml",
        ART / "parent_conflict_review_p4_t02_b2_source_law_space_robust_invariance_protection.yaml",
        ART / "parent_fusion_notes_p4_t02_b2_source_law_space_robust_invariance_protection.md",
        ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_latex_compile_receipt.json",
        TASK / "documentation_impact.yaml",
    ]
    for path in required:
        check(
            f"exists:{path.relative_to(ROOT)}",
            path.is_file(),
            "required artifact exists",
        )

    parsed: dict[Path, Any] = {}
    for path in [p for p in required if p.suffix == ".yaml" and p.is_file()]:
        try:
            parsed[path] = load_unique(path)
            check(
                f"yaml_unique:{path.relative_to(ROOT)}",
                True,
                "strict unique-key parse",
            )
        except Exception as exc:  # noqa: BLE001
            check(f"yaml_unique:{path.relative_to(ROOT)}", False, str(exc))

    record_path = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_record_v1.yaml"
    record = parsed.get(record_path, {})
    if isinstance(record, dict):
        result = record.get("decisive_result", {})
        check(
            "record:result",
            result.get("result_type") == "theorem_with_hypotheses_and_proof"
            and result.get("no_fog_check") == "PASS",
            "exactly one permitted theorem result and no fog",
        )
        check(
            "record:domains",
            len(record.get("formal_domains", [])) == 8,
            "exactly eight formal domains",
        )
        check(
            "record:objects",
            len(record.get("formal_objects", [])) == 10,
            "exactly ten formal objects",
        )
        check(
            "record:maps",
            len(record.get("formal_maps", [])) == 8,
            "exactly eight formal maps",
        )
        check(
            "record:theorems",
            len(record.get("theorems", [])) == 7,
            "exactly seven theorem or proposition records",
        )
        obligations = record.get("proof_obligations", [])
        check(
            "record:obligations",
            len(obligations) == 14,
            "exactly fourteen proof obligations",
        )
        check(
            "record:obligations_pass",
            all(str(row.get("status", "")).startswith("PASS") for row in obligations),
            "all obligations pass at their explicit proposal-only scope",
        )
        check(
            "record:failure_branches",
            len(record.get("failure_branches", [])) == 11,
            "exactly eleven failure branches",
        )
        check(
            "record:freezes",
            len(record.get("preserved_freeze_labels", [])) == 5,
            "all five freezes preserved",
        )
        distance = record.get("distance_to_gr_status", [])
        check(
            "record:distance_rows",
            len(distance) == 14,
            "fourteen Distance-to-GR rows",
        )
        check(
            "record:distance_no_delta",
            all(row.get("status") == "no_delta" for row in distance),
            "all Distance-to-GR rows literal no_delta",
        )
        successor = record.get("selected_successor", {})
        check(
            "record:successor",
            successor.get("packet_id") == SUCCESSOR
            and successor.get("packet_type") == "source_extension_smuggling_audit"
            and successor.get("role_family") == "smuggling-auditor@0.2.0"
            and successor.get("status") == "selected_not_executed"
            and successor.get("executed") is False,
            "one canonical successor selected and unexecuted",
        )
        limits = record.get("authority_limits", {})
        blocked_true = [
            limits.get("source_law_derived_from_current_ontology"),
            limits.get("source_law_adopted"),
            limits.get("canonical_ontology_modified"),
            limits.get("smuggling_audit_completed"),
            limits.get("refuter_stress_completed"),
            limits.get("physical_component_selected"),
            limits.get("physical_causal_cone_constructed"),
            limits.get("empirical_response_constructed"),
            limits.get("universal_matter_propagation_derived"),
            limits.get("adequacy_reevaluated"),
            limits.get("b2_activated"),
            limits.get("p4_t03_unlocked"),
            limits.get("effective_metric_constructed"),
            limits.get("distance_to_gr_changed"),
            limits.get("gate_b_verdict_issued"),
            limits.get("global_no_go_claimed"),
            limits.get("future_source_extension_impossibility_claimed"),
            limits.get("physics_promotion_authorized"),
            limits.get("proof_authority"),
            limits.get("publication_authorized"),
            limits.get("push_authorized"),
            limits.get("external_action_authorized"),
        ]
        check(
            "record:authority_blocks",
            all(value is False for value in blocked_true),
            "all protected authority limits false",
        )

    controls_path = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_controls_v1.yaml"
    controls = parsed.get(controls_path, {})
    if isinstance(controls, dict):
        check(
            "controls:positive",
            controls.get("positive_control", {}).get("exact_residual_margins")
            == [2, 2, 2]
            and controls.get("positive_control", {}).get("all_faces_strictly_inward")
            is True,
            "positive orthant control has exact strict margins",
        )
        check(
            "controls:transport",
            controls.get("certificate_regraduation_control", {}).get(
                "scaled_residual_margins"
            )
            == [4, 6, 10]
            and controls.get("presentation_transport_control", {}).get(
                "transported_residual_margins"
            )
            == [4, 6, 10],
            "regraduation and presentation transport controls exact",
        )
        check(
            "controls:balanced",
            controls.get("balanced_normal_countercontrol", {}).get(
                "exact_normal_signs"
            )
            == [1, -1],
            "balanced normal countercontrol exact",
        )

    manifest_path = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_provenance_manifest_v1.yaml"
    manifest = parsed.get(manifest_path, {})
    if isinstance(manifest, dict):
        sources = manifest.get("sources", [])
        check(
            "manifest:source_count",
            len(sources) == manifest.get("source_count"),
            "manifest source count exact",
        )
        hash_ok = True
        for row in sources:
            path = ROOT / str(row.get("path", ""))
            hash_ok = hash_ok and path.is_file() and sha256(path) == row.get("sha256")
        check("manifest:source_hashes", hash_ok, "all live source hashes match")
        scan = manifest.get("forbidden_import_scan", {})
        check(
            "manifest:forbidden_imports",
            all(value is False for value in scan.values()),
            "no forbidden import recorded",
        )

    model_path = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_model.py"
    if model_path.is_file():
        proc = subprocess.run(
            [sys.executable, str(model_path), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        try:
            model = json.loads(proc.stdout)
        except json.JSONDecodeError:
            model = {}
        check("model:exit", proc.returncode == 0, proc.stderr.strip() or "model exit zero")
        check(
            "model:counts",
            model.get("all_pass") is True
            and model.get("check_count") == model.get("pass_count") == 12,
            "exact model 12/12 PASS",
        )
        check(
            "model:payload",
            model.get("payload_sha256")
            == "6999f3d64ce4a1f2f1265d19ed84195df1b366f3d2afdefa49ea34e4e4b7cecc",
            "exact model payload stable",
        )

    tex_path = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_v1.tex"
    if tex_path.is_file():
        tex = tex_path.read_text(encoding="utf-8")
        phrases = [
            "theorem\\_with\\_hypotheses\\_and\\_proof",
            "Strict source-law-space strong invariance",
            "Finite conormal certificate",
            "presentation transport",
            "Balanced-normal obstruction",
            "proposal-only source-extension data",
            "NDCL-V22-P4T02-B2-SIGNED-CUBIC-VIABILITY-SELECTOR-ROBUSTNESS",
            "selected\\_not\\_executed",
        ]
        check(
            "tex:semantic_phrases",
            all(phrase in tex for phrase in phrases),
            "theorem status, payload, freezes, and stop phrases present",
        )

    child_paths = [
        ART / "child_phys_math_p4_t02_b2_source_law_space_robust_invariance_protection.yaml",
        ART / "child_phys_phil_p4_t02_b2_source_law_space_robust_invariance_protection.yaml",
    ]
    for path in child_paths:
        if path.is_file():
            child_text = path.read_text(encoding="utf-8")
            check(
                f"child:result:{path.name}",
                "theorem_with_hypotheses_and_proof" in child_text,
                "child supports the canonical theorem result",
            )
            check(
                f"child:successor:{path.name}",
                SUCCESSOR in child_text
                and (
                    "selected_not_executed" in child_text
                    or "selected_packet_executed: false" in child_text
                ),
                "child converges on canonical unexecuted successor",
            )
            check(
                f"child:no_delta:{path.name}",
                child_text.count("no_delta") >= 14,
                "child contains fourteen literal no_delta entries",
            )

    conflict_path = ART / "parent_conflict_review_p4_t02_b2_source_law_space_robust_invariance_protection.yaml"
    conflict = parsed.get(conflict_path, {})
    if isinstance(conflict, dict):
        check(
            "conflict:resolved",
            conflict.get("unresolved_blocking_conflict_count") == 0
            and conflict.get("status") == "resolved",
            "no unresolved blocking parent-child conflict",
        )

    compile_path = ART / "v22_p4_t02_b2_source_law_space_robust_invariance_protection_latex_compile_receipt.json"
    if compile_path.is_file():
        receipt = json.loads(compile_path.read_text(encoding="utf-8"))
        visual = receipt.get("visual_inspection", {})
        check(
            "latex:compile",
            receipt.get("status") == "PASS" and receipt.get("exit_code") == 0,
            "LaTeX compile PASS",
        )
        check(
            "latex:visual",
            visual.get("status") == "PASS"
            and visual.get("clipped_text") is False
            and visual.get("overlapping_text") is False
            and visual.get("all_pages_inspected") is True,
            "every rendered page visually inspected",
        )

    failed = [row for row in checks if row["status"] != "PASS"]
    report = {
        "schema_id": "v22_p4_t02_b2_source_law_space_robust_invariance_protection_validation_v1",
        "task_id": "RT-20260811-007",
        "job_id": "AJ-RT-20260811-007-001",
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(failed),
        "failed_check_count": len(failed),
        "checks": checks,
    }
    if args.write_report:
        REPORT.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["status"])
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

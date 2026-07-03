#!/usr/bin/env python3
"""Validate the v15 P4-T03 semantic-layer separation control note."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
NOTE_PATH = ROOT / "research_control/design/semantic_layer_separation_control_note.md"


def contains_all(text: str, snippets: list[str]) -> bool:
    normalized = " ".join(text.split())
    return all(snippet in text or snippet in normalized for snippet in snippets)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    checks: list[dict[str, object]] = []

    def add_check(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"id": check_id, "passed": passed, "detail": detail})

    note_exists = NOTE_PATH.exists()
    add_check("note_exists", note_exists, str(NOTE_PATH.relative_to(ROOT)))
    text = NOTE_PATH.read_text(encoding="utf-8") if note_exists else ""

    add_check(
        "authority_marker",
        text.startswith("<!-- authority: control -->"),
        "note starts with control authority marker",
    )

    required_layers = [
        "SourceMatterSemantics_src",
        "DetectorSemantics_det",
        "StressEnergyAction_sem",
    ]
    for layer in required_layers:
        add_check(
            f"layer_present_{layer}",
            layer in text,
            f"required layer token {layer} present",
        )

    section_requirements = {
        "SourceMatterSemantics_src": [
            "### `SourceMatterSemantics_src`",
            "Allowed reuse:",
            "Blocked reuse:",
            "conditional theorem support only when explicit source certificates",
            "do not reuse as detector",
            "do not reuse as stress-energy semantics",
        ],
        "DetectorSemantics_det": [
            "### `DetectorSemantics_det`",
            "Allowed reuse:",
            "Blocked reuse:",
            "cite as a blocked downstream target",
            "do not infer detector semantics from `SourceMatterSemantics_src`",
            "do not treat no-target certificate success as detector semantics",
        ],
        "StressEnergyAction_sem": [
            "### `StressEnergyAction_sem`",
            "Allowed reuse:",
            "Blocked reuse:",
            "cite as a blocked downstream target",
            "do not infer stress-energy semantics from `SourceMatterSemantics_src`",
            "do not infer a matter action or variational principle",
        ],
    }
    for layer, snippets in section_requirements.items():
        add_check(
            f"allowed_blocked_reuse_{layer}",
            contains_all(text, snippets),
            f"{layer} lists allowed and blocked reuse with layer-specific guards",
        )

    no_target_snippets = [
        "No-target certificates are hygiene only.",
        "They prevent forbidden imports and process-authority laundering.",
        "They do not supply positive matter theory",
        "no-target certificates are hygiene only and do not supply positive matter theory",
        "hygiene_only: true",
        "positive_matter_theory: false",
    ]
    add_check(
        "no_target_hygiene_only",
        contains_all(text, no_target_snippets),
        "no-target certificates are explicitly hygiene only and not positive matter theory",
    )

    bad_fixture_snippets = [
        "semantic_layer_bad_source_as_detector",
        "semantic_layer_bad_source_as_stress_energy",
        "semantic_layer_bad_no_target_as_matter_theory",
        "semantic_layer_bad_rr_e_as_unrestricted_theorem",
        "semantic_layer_bad_positive_profile_as_adoption",
        "semantic_layer_bad_geff_as_unscoped_metric",
        "semantic_layer_bad_evidence_as_coupling_law",
        "semantic_layer_bad_scoped_evidence_as_einstein_premise",
    ]
    pass_fixture_snippets = [
        "semantic_layer_pass_source_scope",
        "semantic_layer_pass_detector_blocked",
        "semantic_layer_pass_stress_action_blocked",
        "semantic_layer_pass_no_target_hygiene",
        "semantic_layer_pass_scoped_evidence",
    ]
    add_check(
        "linter_bad_fixtures_proposed",
        contains_all(text, bad_fixture_snippets),
        "all P4-T04 required bad fixture families are proposed",
    )
    add_check(
        "linter_pass_fixtures_proposed",
        contains_all(text, pass_fixture_snippets),
        "passing semantic-layer fixture families are proposed",
    )

    source_snippets = [
        "src_plan_v15",
        "src_dag_schema",
        "src_dag",
        "src_no_target_map",
        "src_certificate_checklist",
        "src_moratorium",
        "src_pre_adoption",
        "src_p2_manifest",
        "src_p2_theorem",
        "src_p2_audit",
        "src_p2_stress",
        "src_p3_laws",
    ]
    add_check(
        "source_inventory",
        contains_all(text, source_snippets),
        "source inventory cites plan DAG certificate and P2/P3 authority surfaces",
    )

    blocked_conclusion_snippets = [
        "not matter-semantics adoption",
        "not detector-semantics adoption",
        "not stress-energy semantics",
        "not a stress-energy tensor",
        "not a matter action",
        "not matter-coupling derivation or adoption",
        "not Einstein equations",
        "not benchmark promotion",
        "not a completed derivation",
    ]
    add_check(
        "blocked_conclusions_visible",
        contains_all(text, blocked_conclusion_snippets),
        "downstream forbidden conclusions remain visible",
    )

    machine_summary_snippets = [
        "schema_id: \"semantic_layer_separation_control_note_v1\"",
        "physics_promotion_authorized: false",
        "proof_authority: false",
        "linter_fixtures:",
        "status: \"proposed\"",
        "next_plan_task_id: \"P4-T04\"",
    ]
    add_check(
        "machine_summary",
        contains_all(text, machine_summary_snippets),
        "machine-readable control summary is present",
    )

    apa_snippets = [
        "The AEther-Flow Research Project. (2026, July 2). *Recommendations",
        "The AEther-Flow Research Project. (2026, July 3). *Matter-coupling dependency",
        "[Internal control source]",
        "[Research-control TeX",
    ]
    add_check(
        "apa_source_materials",
        contains_all(text, apa_snippets),
        "source materials are cited in APA-style internal-source entries",
    )

    failed = [check for check in checks if not check["passed"]]
    report = {
        "validator": "validate_p4_t03_semantic_layer_separation_note",
        "note_path": str(NOTE_PATH.relative_to(ROOT)),
        "status": "PASS" if not failed else "FAIL",
        "check_count": len(checks),
        "failed_check_count": len(failed),
        "checks": checks,
    }

    if args.output:
        Path(args.output).write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: {report['check_count']} checks")

    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())

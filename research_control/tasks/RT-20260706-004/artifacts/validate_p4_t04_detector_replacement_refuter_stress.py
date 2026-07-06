#!/usr/bin/env python3
"""Validate the v17 P4-T04 detector-replacement Refuter stress artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


TASK_DIR = Path(__file__).resolve().parents[1]
ARTIFACT = TASK_DIR / "artifacts" / "detector_replacement_refuter_stress_v1.tex"
REPORT = TASK_DIR / "artifacts" / "p4_t04_detector_replacement_refuter_stress_report.json"
REQUIRED_STRINGS = [
    "survives_as_source_replacement_candidate",
    "bridge_facing_candidate_path",
    "readout_interface_erasure",
    "empirical_detector_protocol_substitution",
    "proper_time_substitution",
    "target_metric_response_definition",
    "placeholder_as_detector_semantics_adoption",
    "finite_local_witness_stability",
    "process_authority_import",
    "source_law_adopted: false",
    "detector_semantics_adopted: false",
    "coupling_law_adopted: false",
    "matter_coupling_derived: false",
    "stress_energy_semantics_imported: false",
    "matter_action_imported: false",
    "einstein_equations_derived: false",
    "benchmark_promoted: false",
]


def validate() -> dict[str, object]:
    text = ARTIFACT.read_text(encoding="utf-8") if ARTIFACT.exists() else ""
    missing = [needle for needle in REQUIRED_STRINGS if needle not in text]
    status = "PASS" if ARTIFACT.exists() and not missing else "FAIL"
    return {
        "status": status,
        "artifact_path": str(ARTIFACT.relative_to(TASK_DIR.parents[1])),
        "missing_required_strings": missing,
        "required_string_count": len(REQUIRED_STRINGS),
        "checked_result_type": "survives_as_source_replacement_candidate",
        "checked_bridge_or_fail_category": "bridge_facing_candidate_path",
        "claim_boundary_checked": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    result = validate()
    if args.write_report:
        REPORT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Support-only checker for detector-placeholder semantic collapse.

This checker exercises finite text/record cases for the v18 P7-T06 burden:
prevent placeholder or draft/control source-readout language from being read
as adopted detector semantics. It is support-only tooling. It is not proof
authority, not detector-semantics adoption, not source detector/readout
semantics adoption, not matter coupling, not Einstein equations, not benchmark
promotion, and not completed derivation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
RESEARCH_CONTROL_SCRIPT_DIR = SCRIPT_DIR.parent
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

import strict_yaml  # noqa: E402


CHECKER_ID = "detector_placeholder_collapse_checker"
CHECKER_VERSION = "0.1.0"
SUPPORT_ONLY = True
PROOF_AUTHORITY = False
PHYSICS_PROMOTION_AUTHORIZED = False

BOUNDARY_STATEMENT = (
    "This detector-placeholder collapse checker is support-only finite-record "
    "and text tooling. It has proof_authority=false and does not adopt "
    "Det_src, adopt Readout_src, adopt detector semantics, derive matter "
    "coupling, derive Einstein equations, promote a benchmark, issue a Gate "
    "Chair verdict, or complete the derivation."
)

SEMANTIC_STATES = (
    "explicit_placeholder_block",
    "draft_control_source_readout_candidate",
    "adopted_detector_semantics",
    "unknown",
)

AUTHORITY_FLAGS = (
    "detector_semantics_adopted",
    "det_src_adopted",
    "readout_src_adopted",
    "source_detector_readout_semantics_adopted",
    "empirical_detector_protocol_authorized",
    "proper_time_normalization_authorized",
    "target_metric_imported",
    "matter_coupling_derived",
    "stress_energy_semantics_imported",
    "matter_action_imported",
    "einstein_equations_derived",
    "benchmark_promoted",
    "gate_chair_verdict_issued",
    "completed_derivation_claimed",
    "proof_authority",
)

COLLAPSE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "implies_detector_semantics",
        re.compile(
            r"\b(implies|proves|establishes|supplies|gives|entails|therefore)\b"
            r".{0,90}\b(adopted\s+)?detector[- ]semantics\b",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "counts_as_detector_semantics",
        re.compile(
            r"\b(counts\s+as|functions\s+as|serves\s+as)\b"
            r".{0,70}\b(adopted\s+)?detector[- ]semantics\b",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "is_detector_semantics",
        re.compile(
            r"\b(is|are)\s+(?:now\s+)?(?:adopted\s+)?detector[- ]semantics\b",
            re.IGNORECASE,
        ),
    ),
    (
        "adopts_detector_semantics",
        re.compile(
            r"\b(adopts|adopted|authorizes)\b.{0,60}\bdetector[- ]semantics\b",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "det_src_adoption_follows",
        re.compile(
            r"\b(Det_src|Det\\?_?src)\b.{0,80}\b(adopted|adoption\s+follows)\b",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "readout_src_adoption_follows",
        re.compile(
            r"\b(Readout_src|Readout\\?_?src)\b.{0,80}\b(adopted|adoption\s+follows)\b",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
    (
        "matter_coupling_follows",
        re.compile(
            r"\b(derives|establishes|proves)\b.{0,80}\bmatter[- ]coupling\b",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
)

NEGATED_SAFE_PHRASES = (
    "not detector semantics",
    "not detector-semantics adoption",
    "not detector semantics adoption",
    "does not adopt detector semantics",
    "detector semantics adopted: false",
    "detector_semantics_adopted: false",
    "det_src_adopted: false",
    "readout_src_adopted: false",
)


@dataclass(frozen=True)
class CaseSpec:
    case_id: str
    semantic_state: str
    text: str
    authority_flags: Mapping[str, bool]
    expected_status: str
    expected_status_codes: tuple[str, ...]

    def as_record(self) -> dict[str, Any]:
        return {
            "authority_flags": dict(self.authority_flags),
            "case_id": self.case_id,
            "semantic_state": self.semantic_state,
            "text": self.text,
        }


CASES: tuple[CaseSpec, ...] = (
    CaseSpec(
        case_id="explicit_placeholder_block_safe",
        semantic_state="explicit_placeholder_block",
        text=(
            "DetPlaceholder(E_*) = missing_and_blocked. The placeholder is an "
            "explicit block and is not detector semantics."
        ),
        authority_flags={
            "detector_semantics_adopted": False,
            "det_src_adopted": False,
            "readout_src_adopted": False,
            "matter_coupling_derived": False,
        },
        expected_status="pass",
        expected_status_codes=("pass_placeholder_block_preserved",),
    ),
    CaseSpec(
        case_id="draft_control_source_readout_candidate_safe",
        semantic_state="draft_control_source_readout_candidate",
        text=(
            "SourceReadoutCandidate_EStar_v1 is a draft_control_candidate. "
            "Det_src(E_*) and Readout_src(E_*) are task-local source-side "
            "candidate names; detector_semantics_adopted: false."
        ),
        authority_flags={
            "detector_semantics_adopted": False,
            "det_src_adopted": False,
            "readout_src_adopted": False,
            "source_detector_readout_semantics_adopted": False,
            "matter_coupling_derived": False,
        },
        expected_status="pass",
        expected_status_codes=("pass_draft_control_candidate_preserved",),
    ),
    CaseSpec(
        case_id="placeholder_as_adopted_detector_semantics",
        semantic_state="explicit_placeholder_block",
        text=(
            "DetPlaceholder(E_*) supplies adopted detector semantics for the "
            "matter-coupling step."
        ),
        authority_flags={"detector_semantics_adopted": False},
        expected_status="fail",
        expected_status_codes=("fail_placeholder_as_detector_semantics_collapse",),
    ),
    CaseSpec(
        case_id="source_readout_candidate_as_detector_semantics",
        semantic_state="draft_control_source_readout_candidate",
        text=(
            "SourceReadoutCandidate_EStar_v1 implies adopted detector semantics "
            "and therefore derives matter coupling."
        ),
        authority_flags={
            "detector_semantics_adopted": False,
            "matter_coupling_derived": False,
        },
        expected_status="fail",
        expected_status_codes=(
            "fail_candidate_as_detector_semantics_collapse",
            "fail_matter_coupling_overread",
        ),
    ),
    CaseSpec(
        case_id="unprotected_adopted_detector_semantics_state",
        semantic_state="adopted_detector_semantics",
        text=(
            "This record asserts adopted detector semantics without a protected "
            "Gate Chair authority reference."
        ),
        authority_flags={"detector_semantics_adopted": True},
        expected_status="fail",
        expected_status_codes=("fail_unprotected_adopted_detector_semantics",),
    ),
)

CASE_IDS = tuple(case.case_id for case in CASES)


def _as_map(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y"}
    return bool(value)


def _lower_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _nonnegated_pattern_hits(text: str) -> list[str]:
    lowered = _lower_text(text)
    hits: list[str] = []
    for code, pattern in COLLAPSE_PATTERNS:
        for match in pattern.finditer(text):
            snippet = _lower_text(match.group(0))
            if any(phrase in snippet for phrase in NEGATED_SAFE_PHRASES):
                continue
            hits.append(code)
            break
    if "detector_semantics_adopted: true" in lowered:
        hits.append("detector_semantics_adopted_true_literal")
    return sorted(set(hits))


def infer_semantic_state(record: Mapping[str, Any]) -> str:
    declared = str(record.get("semantic_state", "")).strip()
    if declared in SEMANTIC_STATES:
        return declared
    text = str(record.get("text", ""))
    lowered = _lower_text(text)
    if "adopted detector semantics" in lowered or "detector_semantics_adopted: true" in lowered:
        return "adopted_detector_semantics"
    if (
        "sourcereadoutcandidate" in lowered
        or "draft_control_candidate" in lowered
        or "det_src" in lowered
        or "readout_src" in lowered
    ):
        return "draft_control_source_readout_candidate"
    if "detplaceholder" in lowered or "missing_and_blocked" in lowered:
        return "explicit_placeholder_block"
    return "unknown"


def true_authority_flags(record: Mapping[str, Any]) -> list[str]:
    flags = _as_map(record.get("authority_flags"))
    found: list[str] = []
    for key in AUTHORITY_FLAGS:
        if _as_bool(flags.get(key, False)):
            found.append(key)
    return found


def check_record(record: Mapping[str, Any]) -> dict[str, Any]:
    case_id = str(record.get("case_id") or record.get("fixture_id") or "inline_record")
    text = str(record.get("text") or record.get("surface_text") or "")
    semantic_state = infer_semantic_state(record)
    pattern_hits = _nonnegated_pattern_hits(text)
    true_flags = true_authority_flags(record)

    status_codes: list[str] = []
    if semantic_state == "explicit_placeholder_block":
        if pattern_hits or any(flag.endswith("_adopted") for flag in true_flags):
            status_codes.append("fail_placeholder_as_detector_semantics_collapse")
        else:
            status_codes.append("pass_placeholder_block_preserved")
    elif semantic_state == "draft_control_source_readout_candidate":
        if pattern_hits or any(
            flag
            in {
                "detector_semantics_adopted",
                "det_src_adopted",
                "readout_src_adopted",
                "source_detector_readout_semantics_adopted",
            }
            for flag in true_flags
        ):
            status_codes.append("fail_candidate_as_detector_semantics_collapse")
        else:
            status_codes.append("pass_draft_control_candidate_preserved")
    elif semantic_state == "adopted_detector_semantics":
        status_codes.append("fail_unprotected_adopted_detector_semantics")
    else:
        status_codes.append("fail_unknown_detector_semantic_state")

    downstream_flags = {
        "matter_coupling_derived": "fail_matter_coupling_overread",
        "stress_energy_semantics_imported": "fail_stress_energy_overread",
        "matter_action_imported": "fail_matter_action_overread",
        "einstein_equations_derived": "fail_einstein_equations_overread",
        "benchmark_promoted": "fail_benchmark_promotion_overread",
        "gate_chair_verdict_issued": "fail_gate_chair_verdict_overread",
        "completed_derivation_claimed": "fail_completed_derivation_overread",
        "proof_authority": "fail_proof_authority_overread",
    }
    for flag, code in downstream_flags.items():
        if flag in true_flags:
            status_codes.append(code)
    if "matter_coupling_follows" in pattern_hits:
        status_codes.append("fail_matter_coupling_overread")

    status_codes = sorted(set(status_codes))
    observed_status = "fail" if any(code.startswith("fail_") for code in status_codes) else "pass"
    return {
        "case_id": case_id,
        "collapse_detected": observed_status == "fail",
        "observed_status": observed_status,
        "observed_status_codes": status_codes,
        "pattern_hits": pattern_hits,
        "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
        "proof_authority": PROOF_AUTHORITY,
        "semantic_state": semantic_state,
        "support_only": SUPPORT_ONLY,
        "text": text,
        "true_authority_flags": true_flags,
    }


def select_cases(selection: str) -> tuple[CaseSpec, ...]:
    if selection == "all":
        return CASES
    for case in CASES:
        if case.case_id == selection:
            return (case,)
    raise ValueError(f"unknown case: {selection}")


def evaluate_case(case: CaseSpec) -> dict[str, Any]:
    result = check_record(case.as_record())
    missing_codes = [
        code for code in case.expected_status_codes if code not in result["observed_status_codes"]
    ]
    status_match = result["observed_status"] == case.expected_status and not missing_codes
    result.update(
        {
            "expected_status": case.expected_status,
            "expected_status_codes": list(case.expected_status_codes),
            "missing_expected_status_codes": missing_codes,
            "status_match": status_match,
        }
    )
    return result


def generate_report(selection: str = "all") -> dict[str, Any]:
    cases = select_cases(selection)
    results = [evaluate_case(case) for case in cases]
    failed_cases = [result["case_id"] for result in results if not result["status_match"]]
    state_counts = {state: 0 for state in SEMANTIC_STATES}
    for result in results:
        state_counts[result["semantic_state"]] = state_counts.get(result["semantic_state"], 0) + 1
    return {
        "boundary_statement": BOUNDARY_STATEMENT,
        "case_count": len(results),
        "case_results": results,
        "checker_id": CHECKER_ID,
        "checker_version": CHECKER_VERSION,
        "configured_cases": list(CASE_IDS),
        "failed_case_count": len(failed_cases),
        "failed_cases": failed_cases,
        "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
        "proof_authority": PROOF_AUTHORITY,
        "schema_id": "detector_placeholder_collapse_checker_report_v1",
        "semantic_state_counts": state_counts,
        "status": "PASS" if not failed_cases else "FAIL",
        "support_only": SUPPORT_ONLY,
        "validator_behavior_changed": False,
    }


def load_record(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if path.suffix == ".json" or stripped.startswith("{"):
        parsed = json.loads(text)
    else:
        parsed = strict_yaml.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("record must be a map")
    return parsed


def evaluate_record_file(path: Path) -> dict[str, Any]:
    result = check_record(load_record(path))
    return {
        "boundary_statement": BOUNDARY_STATEMENT,
        "checker_id": CHECKER_ID,
        "checker_version": CHECKER_VERSION,
        "file_result": result,
        "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
        "proof_authority": PROOF_AUTHORITY,
        "schema_id": "detector_placeholder_record_check_v1",
        "status": "PASS" if result["observed_status"] == "pass" else "FAIL",
        "support_only": SUPPORT_ONLY,
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Detector-Placeholder Collapse Checker Report",
        "",
        BOUNDARY_STATEMENT,
        "",
        f"- Status: `{report['status']}`",
        f"- Case count: `{report.get('case_count', 1)}`",
        f"- Failed case count: `{report.get('failed_case_count', 0)}`",
        "",
        "## Case Results",
        "",
    ]
    for result in report.get("case_results", []):
        lines.extend(
            [
                f"### `{result['case_id']}`",
                "",
                f"- Semantic state: `{result['semantic_state']}`",
                f"- Observed status: `{result['observed_status']}`",
                "- Observed codes: "
                + ", ".join(f"`{code}`" for code in result["observed_status_codes"]),
                f"- Status match: `{str(result.get('status_match', False)).lower()}`",
                "",
            ]
        )
    if "file_result" in report:
        result = report["file_result"]
        lines.extend(
            [
                f"### `{result['case_id']}`",
                "",
                f"- Semantic state: `{result['semantic_state']}`",
                f"- Observed status: `{result['observed_status']}`",
                "- Observed codes: "
                + ", ".join(f"`{code}`" for code in result["observed_status_codes"]),
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _json_dump(data: Mapping[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run support-only detector-placeholder collapse checks."
    )
    parser.add_argument(
        "--case",
        default="all",
        choices=("all",) + CASE_IDS,
        help="Built-in case to run; default runs all configured cases.",
    )
    parser.add_argument("--record", type=Path, help="Check one JSON or YAML record file.")
    parser.add_argument("--json", action="store_true", help="Print JSON report.")
    parser.add_argument("--json-output", type=Path, help="Write JSON report.")
    parser.add_argument("--markdown", type=Path, help="Write Markdown report.")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    report = evaluate_record_file(args.record) if args.record else generate_report(args.case)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(_json_dump(report), encoding="utf-8")
    if args.markdown:
        write_markdown(report, args.markdown)
    if args.json or not any((args.json_output, args.markdown)):
        print(_json_dump(report), end="")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

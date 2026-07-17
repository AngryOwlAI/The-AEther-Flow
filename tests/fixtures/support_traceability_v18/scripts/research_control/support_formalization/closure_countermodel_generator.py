#!/usr/bin/env python3
"""Support-only generator for finite missing-closure countermodel records.

This generator creates deterministic finite mock records for the v18 P7-T03
missing-closure modes. It is support-only tooling. It is not proof authority,
not a general EqSrc theorem, not RetainH or GenH adoption, not target metric
import, not MetricData(E) adoption, not g_eff adoption or scope expansion, not
matter coupling, not Einstein equations, not benchmark promotion, and not a
completed derivation.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
RESEARCH_CONTROL_SCRIPT_DIR = SCRIPT_DIR.parent
if str(RESEARCH_CONTROL_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_SCRIPT_DIR))

from support_formalization import typed_eqsrc_orbit_checker as orbit_checker  # noqa: E402


GENERATOR_ID = "closure_countermodel_generator"
GENERATOR_VERSION = "0.1.0"
SUPPORT_ONLY = True
PROOF_AUTHORITY = False
PHYSICS_PROMOTION_AUTHORIZED = False

MODES = (
    "missing_identity",
    "missing_inverse",
    "missing_composition",
    "non_family_stable_invariant",
    "RetainH_required",
    "GenH_required",
)

EXPECTED_CHECKER_STATUS = {
    "missing_identity": "fail_identity_map",
    "missing_inverse": "fail_inverse_map",
    "missing_composition": "fail_malformed_record",
    "non_family_stable_invariant": "fail_invariant_preservation",
    "RetainH_required": "fail_invariant_preservation",
    "GenH_required": "fail_malformed_record",
}

MODE_SUMMARY = {
    "missing_identity": (
        "A declared source type lacks an explicit identity map, so finite "
        "EqSrc closure cannot be checked."
    ),
    "missing_inverse": (
        "A finite map family supplies no inverse-map rows, so inverse closure "
        "is absent."
    ),
    "missing_composition": (
        "The composition table is empty, so missing data fails closed instead "
        "of being inferred."
    ),
    "non_family_stable_invariant": (
        "A source-only invariant flag is not family-stable across the declared "
        "orbit."
    ),
    "RetainH_required": (
        "The finite record marks RetainH as required for invariant retention "
        "while preserving adoption=false."
    ),
    "GenH_required": (
        "The finite record introduces a generated source member whose closure "
        "arrows require GenH while preserving adoption=false."
    ),
}

BOUNDARY_STATEMENT = (
    "This closure countermodel generator is support-only finite-record tooling. "
    "It has proof_authority=false and does not prove general EqSrc, adopt "
    "RetainH or GenH, adopt a source law, import a target metric, adopt "
    "MetricData(E), adopt or expand g_eff, derive matter coupling, derive "
    "Einstein equations, promote a benchmark, issue a Gate Chair verdict, or "
    "complete the derivation."
)


@dataclass(frozen=True)
class CountermodelCase:
    """One support-only finite mock missing-closure record."""

    case_id: str
    mode: str
    record: dict[str, Any]
    expected_checker_status: str
    countermodel_interpretation: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "countermodel_interpretation": self.countermodel_interpretation,
            "expected_checker_status": self.expected_checker_status,
            "mode": self.mode,
            "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
            "proof_authority": PROOF_AUTHORITY,
            "record": self.record,
            "support_only": SUPPORT_ONLY,
        }


def _forbidden_authority_flags() -> dict[str, bool]:
    return {key: False for key in orbit_checker.REQUIRED_FALSE_AUTHORITY_FLAGS}


def _base_record() -> dict[str, Any]:
    """Return the finite typed record that each mode mutates."""

    return {
        "metadata": {
            "fixture_id": "closure_countermodel_base_valid_v1",
            "support_only": True,
            "proof_authority": False,
            "physics_promotion_authorized": False,
            "eqsrc_theorem_authority": False,
            "boundary_statement": orbit_checker.BOUNDARY_STATEMENT,
            "countermodel_generator_id": GENERATOR_ID,
            "countermodel_generator_version": GENERATOR_VERSION,
            "countermodel_mode": "base",
            "source_artifact_paths": [
                "implementations_plans/recommendations_implementation_plan_continue_task-v18.md",
                "research_control/design/source_equivalence_typed_object_schema_v1.md",
                "research_control/tasks/RT-20260708-020/artifacts/typed_eqsrc_orbit_checker_spec_v1.md",
            ],
        },
        "typed_objects": [
            {"id": "a0", "type": "fiber_A", "source_only": True},
            {"id": "a1", "type": "fiber_A", "source_only": True},
            {"id": "b0", "type": "fiber_B", "source_only": True},
        ],
        "identity_maps": [
            {
                "id": "id_A",
                "type": "fiber_A",
                "arrows": [
                    {"from": "a0", "to": "a0"},
                    {"from": "a1", "to": "a1"},
                ],
            },
            {
                "id": "id_B",
                "type": "fiber_B",
                "arrows": [
                    {"from": "b0", "to": "b0"},
                ],
            },
        ],
        "maps": [
            {
                "id": "flip_A",
                "source_type": "fiber_A",
                "target_type": "fiber_A",
                "arrows": [
                    {"from": "a0", "to": "a1"},
                    {"from": "a1", "to": "a0"},
                ],
            }
        ],
        "inverse_maps": [
            {"map": "id_A", "inverse": "id_A"},
            {"map": "id_B", "inverse": "id_B"},
            {"map": "flip_A", "inverse": "flip_A"},
        ],
        "composition_table": [
            {"left": "id_A", "right": "id_A", "result": "id_A"},
            {"left": "id_A", "right": "flip_A", "result": "flip_A"},
            {"left": "flip_A", "right": "id_A", "result": "flip_A"},
            {"left": "flip_A", "right": "flip_A", "result": "id_A"},
            {"left": "id_B", "right": "id_B", "result": "id_B"},
        ],
        "orbits": [
            {
                "id": "orbit_A",
                "type": "fiber_A",
                "members": ["a0", "a1"],
                "invariant_flags": {
                    "source_only_invariants_preserved": True,
                    "target_import_used": False,
                    "proof_authority": False,
                },
            },
            {
                "id": "orbit_B",
                "type": "fiber_B",
                "members": ["b0"],
                "invariant_flags": {
                    "source_only_invariants_preserved": True,
                    "target_import_used": False,
                    "proof_authority": False,
                },
            },
        ],
        "eqsrc_pairs": [
            {"left": "a0", "right": "a1", "orbit": "orbit_A"},
            {"left": "b0", "right": "b0", "orbit": "orbit_B"},
        ],
        "invariant_flags": {
            "source_only_invariants_preserved": True,
            "target_import_used": False,
            "proof_authority": False,
            "physics_promotion_authorized": False,
            "fail_closed_for_missing_data": True,
        },
        "primitive_requirements": {
            "retainh": {
                "status": "not_required",
                "adopted": False,
                "gate_protected_adoption": True,
            },
            "genh": {
                "status": "not_required",
                "adopted": False,
                "gate_protected_adoption": True,
            },
        },
        "countermodel_metadata": {
            "support_only": True,
            "global_no_go_claimed": False,
            "missing_closure_mode": "base",
            "minimal_finite_record": True,
        },
        "forbidden_authority": _forbidden_authority_flags(),
    }


def _set_mode(record: dict[str, Any], mode: str) -> None:
    record["metadata"]["fixture_id"] = f"closure_countermodel_{mode}_v1"
    record["metadata"]["countermodel_mode"] = mode
    record["countermodel_metadata"]["missing_closure_mode"] = mode


def _a_only_identity_rows(record: dict[str, Any]) -> None:
    record["identity_maps"] = [
        item for item in record["identity_maps"] if item.get("id") == "id_A"
    ]
    record["inverse_maps"] = [
        item for item in record["inverse_maps"] if item.get("map") != "id_B"
    ]
    record["composition_table"] = [
        item
        for item in record["composition_table"]
        if item.get("left") != "id_B" and item.get("right") != "id_B"
    ]


def _mark_invariant_unstable(record: dict[str, Any]) -> None:
    record["invariant_flags"]["source_only_invariants_preserved"] = False
    record["orbits"][0]["invariant_flags"]["source_only_invariants_preserved"] = False


def _add_generated_member_without_action(record: dict[str, Any]) -> None:
    record["typed_objects"].append(
        {"id": "a2", "type": "fiber_A", "source_only": True}
    )
    record["identity_maps"][0]["arrows"].append({"from": "a2", "to": "a2"})
    record["orbits"][0]["members"].append("a2")
    record["eqsrc_pairs"].append({"left": "a0", "right": "a2", "orbit": "orbit_A"})


def generate_record(mode: str) -> dict[str, Any]:
    """Generate one finite mock record for a configured missing-closure mode."""

    if mode not in MODES:
        raise ValueError(f"unknown countermodel mode: {mode}")
    record = copy.deepcopy(_base_record())
    _set_mode(record, mode)

    if mode == "missing_identity":
        _a_only_identity_rows(record)
    elif mode == "missing_inverse":
        record["inverse_maps"] = []
    elif mode == "missing_composition":
        record["composition_table"] = []
    elif mode == "non_family_stable_invariant":
        _mark_invariant_unstable(record)
    elif mode == "RetainH_required":
        _mark_invariant_unstable(record)
        record["primitive_requirements"]["retainh"]["status"] = "required"
        record["primitive_requirements"]["retainh"][
            "requirement_statement"
        ] = "RetainH is required to retain the source-only invariant over orbit_A."
    elif mode == "GenH_required":
        _add_generated_member_without_action(record)
        record["primitive_requirements"]["genh"]["status"] = "required"
        record["primitive_requirements"]["genh"][
            "requirement_statement"
        ] = "GenH is required to generate action data for the new source member a2."
    return record


def generate_case(mode: str) -> CountermodelCase:
    record = generate_record(mode)
    return CountermodelCase(
        case_id=f"CCG-{mode}-v1",
        mode=mode,
        record=record,
        expected_checker_status=EXPECTED_CHECKER_STATUS[mode],
        countermodel_interpretation=MODE_SUMMARY[mode],
    )


def generate_bundle(modes: Iterable[str] = MODES) -> dict[str, Any]:
    cases = [generate_case(mode).to_dict() for mode in modes]
    return {
        "boundary_statement": BOUNDARY_STATEMENT,
        "case_count": len(cases),
        "cases": cases,
        "configured_modes": list(MODES),
        "generator_id": GENERATOR_ID,
        "generator_version": GENERATOR_VERSION,
        "physics_promotion_authorized": PHYSICS_PROMOTION_AUTHORIZED,
        "proof_authority": PROOF_AUTHORITY,
        "support_only": SUPPORT_ONLY,
    }


def json_text(value: MappingLike) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


MappingLike = dict[str, Any]


def markdown_text(bundle: MappingLike) -> str:
    lines = [
        "# Closure Countermodel Generator Report",
        "",
        BOUNDARY_STATEMENT,
        "",
        f"- Generator: `{bundle['generator_id']}`",
        f"- Version: `{bundle['generator_version']}`",
        f"- Support only: `{str(bundle['support_only']).lower()}`",
        f"- Proof authority: `{str(bundle['proof_authority']).lower()}`",
        f"- Case count: `{bundle['case_count']}`",
        "",
        "## Cases",
        "",
    ]
    for case in bundle["cases"]:
        lines.append(
            f"- `{case['mode']}`: expected checker status "
            f"`{case['expected_checker_status']}`; "
            f"{case['countermodel_interpretation']}"
        )
    lines.extend(
        [
            "",
            "## Authority",
            "",
            "These generated records are finite support artifacts only. They do not "
            "adopt RetainH, GenH, source laws, target metrics, or any downstream "
            "physics claim.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text_if_requested(path: Path | None, text: str) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_fixture_dir(bundle: MappingLike, fixture_dir: Path | None) -> None:
    if fixture_dir is None:
        return
    fixture_dir.mkdir(parents=True, exist_ok=True)
    for case in bundle["cases"]:
        path = fixture_dir / f"{case['mode']}.json"
        path.write_text(json_text(case["record"]), encoding="utf-8")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("all", *MODES),
        default="all",
        help="Countermodel mode to generate, or all modes.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON bundle on stdout")
    parser.add_argument("--json-output", type=Path, help="Write JSON bundle to a file")
    parser.add_argument("--markdown", type=Path, help="Write a Markdown report to a file")
    parser.add_argument(
        "--fixture-dir",
        type=Path,
        help="Write one finite mock record JSON fixture per generated mode",
    )
    args = parser.parse_args(argv)

    modes = MODES if args.mode == "all" else (args.mode,)
    bundle = generate_bundle(modes)
    output = json_text(bundle)
    write_text_if_requested(args.json_output, output)
    write_text_if_requested(args.markdown, markdown_text(bundle))
    write_fixture_dir(bundle, args.fixture_dir)
    if args.json or not (args.json_output or args.markdown or args.fixture_dir):
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

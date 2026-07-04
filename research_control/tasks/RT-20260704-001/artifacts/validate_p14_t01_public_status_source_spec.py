#!/usr/bin/env python3
"""Validate the v15 P14-T01 public status exists/does-not-exist source spec."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
SPEC_PATH = REPO_ROOT / "research_control/design/public_status_exists_does_not_exist_source_spec.md"

REQUIRED_ROWS = {
    "AEther-flow ontology": (
        "proposed research ontology / explanatory frame",
        "established physical ontology",
    ),
    "`M_src`": (
        "scoped source-only object",
        "target manifold, metric, GR derivation",
    ),
    "`g_eff`": (
        "scoped source-extension object",
        "unscoped Lorentzian metric, matter coupling, Einstein equations",
    ),
    "Matter-sector evidence": (
        "scoped evidence/preconditions",
        "matter semantics, detector semantics, coupling law, matter coupling",
    ),
    "`RR_E` transport/invariance evidence": (
        "certificate-indexed scoped evidence/precondition",
        "source-law adoption, unrestricted theorem",
    ),
    "Einstein equations": (
        "not started",
        "field-equation derivation",
    ),
    "Benchmark promotion": (
        "blocked",
        "exact-GR derivation or closure",
    ),
    "Completed derivation": (
        "no",
        "no completed derivation",
    ),
}

REQUIRED_SOURCE_TOKENS = [
    "registries/DISTANCE_TO_GR_LEDGER.csv",
    "research_control/design/scoped_positive_claim_vocabulary.md",
    "research_control/design/distance_to_gr_status_aliases.yaml",
    "research_control/design/public_status_table_source_spec.md",
    "research_control/design/einstein_equation_route_moratorium_v1.md",
]

REQUIRED_RENDERING_TOKENS = [
    "GR has not been derived",
    "not an established physical ontology",
    "matter coupling",
    "Einstein equations",
    "benchmark promotion",
    "completed derivation",
]


def parse_table(text: str) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    in_table = False
    headers: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("| Object or target |"):
            in_table = True
            headers = [cell.strip() for cell in line.strip("|").split("|")]
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if cells and set(cells[0]) == {"-"}:
            continue
        if len(cells) != len(headers):
            continue
        row = dict(zip(headers, cells))
        rows[row["Object or target"]] = row
    return rows


def validate() -> dict[str, object]:
    text = SPEC_PATH.read_text(encoding="utf-8")
    rows = parse_table(text)
    findings: list[str] = []

    for object_name, (exists_text, missing_text) in REQUIRED_ROWS.items():
        row = rows.get(object_name)
        if row is None:
            findings.append(f"missing required row: {object_name}")
            continue
        if row.get("What exists") != exists_text:
            findings.append(f"{object_name}: unexpected What exists cell")
        if row.get("What does not exist") != missing_text:
            findings.append(f"{object_name}: unexpected What does not exist cell")
        if not row.get("Source basis"):
            findings.append(f"{object_name}: missing source basis")
        if not row.get("Public-safe wording rule"):
            findings.append(f"{object_name}: missing public-safe wording rule")

    for token in REQUIRED_SOURCE_TOKENS:
        if token not in text:
            findings.append(f"missing source token: {token}")

    for token in REQUIRED_RENDERING_TOKENS:
        if token not in text:
            findings.append(f"missing rendering token: {token}")

    forbidden_promotions = [
        "GR is derived",
        "matter coupling is derived",
        "benchmark is promoted",
        "has completed GR derivation",
        "GR derivation is complete",
    ]
    for token in forbidden_promotions:
        if token in text:
            findings.append(f"forbidden promotion wording present: {token}")

    return {
        "status": "PASS" if not findings else "FAIL",
        "spec_path": str(SPEC_PATH.relative_to(REPO_ROOT)),
        "required_row_count": len(REQUIRED_ROWS),
        "parsed_row_count": len(rows),
        "source_backed": not any("source" in finding for finding in findings),
        "physics_delta": "none",
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate()
    payload = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

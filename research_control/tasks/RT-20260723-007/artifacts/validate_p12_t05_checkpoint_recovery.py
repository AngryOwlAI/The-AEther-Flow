#!/usr/bin/env python3
"""Validate the byte-bounded P12-T05 checkpoint recovery."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
EXPECTED = {
    "research_control/tasks/RT-20260723-004/artifacts/fixtures/"
    "scientific_quality_metric_cases.json": {
        "size": 9575,
        "sha256": "60bcb8819734e5e565b08a46b29e85ebffde14f6c1e33dd13cfdd1c02628d003",
    },
    "research_control/tasks/RT-20260723-004/artifacts/"
    "scientific_quality_calibration_warning_policy_v1.md": {
        "size": 3093,
        "sha256": "b9b4e4fcc603c9eee508456999936a4e0378b188235f73f35c454009728648cb",
    },
    "research_control/tasks/RT-20260723-004/artifacts/"
    "scientific_quality_metric_taxonomy_v1.md": {
        "size": 5239,
        "sha256": "b2e31738a445e68e4de6ea20381886bcd6c3747cccd693187f0904a7742ad308",
    },
    "tests/test_scientific_quality_metrics.py": {
        "size": 5854,
        "sha256": "3b3cf70b7169d17a4f5fb1c59947b470582d61449768a1d4570d8fb4f28ad87a",
    },
}


def main() -> int:
    checks: list[dict[str, object]] = []
    for relative, expected in EXPECTED.items():
        data = (ROOT / relative).read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        checks.extend(
            [
                {
                    "check": f"{relative}:sha256",
                    "status": "PASS" if actual_hash == expected["sha256"] else "FAIL",
                    "actual": actual_hash,
                    "expected": expected["sha256"],
                },
                {
                    "check": f"{relative}:size",
                    "status": "PASS" if len(data) == expected["size"] else "FAIL",
                    "actual": len(data),
                    "expected": expected["size"],
                },
                {
                    "check": f"{relative}:single_final_newline",
                    "status": (
                        "PASS"
                        if data.endswith(b"\n") and not data.endswith(b"\n\n")
                        else "FAIL"
                    ),
                },
            ]
        )

    fixture_path = (
        ROOT
        / "research_control/tasks/RT-20260723-004/artifacts/fixtures/"
        "scientific_quality_metric_cases.json"
    )
    json.loads(fixture_path.read_text(encoding="utf-8"))
    checks.append({"check": "fixture_json_parse", "status": "PASS"})

    handoff = (ROOT / "research_control/handoffs/handoff-0839.md").read_text(
        encoding="utf-8"
    )
    checks.append(
        {
            "check": "handoff_0839_canonical_identity",
            "status": "PASS" if "handoff-0839" in handoff else "FAIL",
        }
    )

    status = "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL"
    print(json.dumps({"status": status, "checks": checks}, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

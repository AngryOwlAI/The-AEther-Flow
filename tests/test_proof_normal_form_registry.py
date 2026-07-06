from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.research_control import validate_proof_normal_form_registry as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "research_control" / "validate_proof_normal_form_registry.py"


def valid_row() -> dict[str, str]:
    row = {field: "" for field in validator.REQUIRED_HEADER}
    row.update(
        {
            "proof_normal_form_row_id": "PNF-TEST-001",
            "object_id": "TEST-GATE-DECISION",
            "source_artifact_path": "sources/gate_decision.tex",
            "claim_type": "decision",
            "authority_status": "scientific_gate",
            "status": "scoped_adopted",
            "premises": "declared source certificate",
            "forbidden_premises": "target metric;matter coupling",
            "conclusion": "Candidate is adopted only as scoped source-extension evidence",
            "scope": "scoped source-extension decision under declared source scope",
            "allowed_uses": "bounded matter-coupling precondition routing",
            "non_conclusions": "not target metric;not matter coupling;not Einstein equations;not benchmark promotion;not completed derivation",
            "depends_on": "none",
            "eligible_next_routes": "proof_normal_form_validator",
            "machine_checkable_fragment": "false",
            "created_at": "2026-07-06T00:00:00Z",
            "notes": "Test row preserves source authority.",
        }
    )
    return row


def write_registry(root: Path, rows: list[dict[str, str]]) -> Path:
    source_dir = root / "sources"
    source_dir.mkdir(parents=True)
    (source_dir / "gate_decision.tex").write_text("source\n", encoding="utf-8")
    registry_dir = root / "registries"
    registry_dir.mkdir(parents=True)
    registry_path = registry_dir / "PROOF_NORMAL_FORM_REGISTRY.csv"
    with registry_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=validator.REQUIRED_HEADER)
        writer.writeheader()
        writer.writerows(rows)
    return registry_path


class ProofNormalFormRegistryTests(unittest.TestCase):
    def test_current_registry_validates(self) -> None:
        receipt = validator.validate_registry()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["checked_row_count"], 7)
        self.assertFalse(receipt["proof_authority"])

    def test_cli_json_output_is_deterministic(self) -> None:
        command = [sys.executable, str(SCRIPT_PATH), "--json"]
        first = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        second = subprocess.run(command, cwd=REPO_ROOT, check=True, text=True, capture_output=True)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(json.loads(first.stdout)["status"], "PASS")

    def test_missing_source_artifact_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row = valid_row()
            row["source_artifact_path"] = ""
            registry_path = write_registry(root, [row])
            with self.assertRaises(validator.ProofNormalFormRegistryError) as raised:
                validator.validate_registry(registry_path, repo_root=root)
        self.assertIn("missing source_artifact_path", "\n".join(raised.exception.errors))

    def test_high_risk_row_requires_non_conclusions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row = valid_row()
            row["non_conclusions"] = ""
            registry_path = write_registry(root, [row])
            with self.assertRaises(validator.ProofNormalFormRegistryError) as raised:
                validator.validate_registry(registry_path, repo_root=root)
        self.assertIn("high-risk row missing non_conclusions", "\n".join(raised.exception.errors))

    def test_forbidden_premise_cannot_appear_in_premises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row = valid_row()
            row["premises"] = "declared source certificate;target metric"
            registry_path = write_registry(root, [row])
            with self.assertRaises(validator.ProofNormalFormRegistryError) as raised:
                validator.validate_registry(registry_path, repo_root=root)
        self.assertIn("forbidden premise appears in premises", "\n".join(raised.exception.errors))

    def test_scientific_gate_decision_must_stay_scoped(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row = valid_row()
            row["conclusion"] = "Candidate is adopted"
            registry_path = write_registry(root, [row])
            with self.assertRaises(validator.ProofNormalFormRegistryError) as raised:
                validator.validate_registry(registry_path, repo_root=root)
        self.assertIn("scientific_gate conclusion must use scoped or only language", "\n".join(raised.exception.errors))

    def test_support_only_row_cannot_claim_proof_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            row = valid_row()
            row["proof_normal_form_row_id"] = "PNF-TEST-002"
            row["claim_type"] = "boundary"
            row["authority_status"] = "support_only"
            row["status"] = "draft_control"
            row["conclusion"] = "This support row is proof authority"
            row["scope"] = "support-only validation row"
            registry_path = write_registry(root, [row])
            with self.assertRaises(validator.ProofNormalFormRegistryError) as raised:
                validator.validate_registry(registry_path, repo_root=root)
        self.assertIn("support_only row claims proof authority", "\n".join(raised.exception.errors))


if __name__ == "__main__":
    unittest.main()

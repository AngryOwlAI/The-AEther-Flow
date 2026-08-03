from __future__ import annotations

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / (
    "research_control/tasks/RT-20260803-011/artifacts/"
    "validate_p16_t02_gate_a_registry_validator_identity_parity.py"
)
SPEC = importlib.util.spec_from_file_location("gate_a_exact_object_validator", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class GateAExactObjectRegistryValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        registry = ROOT / "registries/TEX_SOURCE_REGISTRY.csv"
        with registry.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            cls.fieldnames = list(reader.fieldnames or [])
            cls.rows = list(reader)

    def report_for(self, rows: list[dict[str, str]]) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            registry_path = Path(temporary_directory) / "TEX_SOURCE_REGISTRY.csv"
            with registry_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
            return VALIDATOR.build_report(ROOT, registry_path)

    def copied_rows(self) -> list[dict[str, str]]:
        return [dict(row) for row in self.rows]

    def exact_row(self, rows: list[dict[str, str]]) -> dict[str, str]:
        return next(
            row for row in rows if row["object_id"] == VALIDATOR.GATE_A_OBJECT_ID
        )

    def test_live_registry_passes_exact_identity_contract(self) -> None:
        report = self.report_for(self.copied_rows())
        self.assertEqual(report["validation_status"], "PASS")

    def test_foundations_pass_cannot_substitute_for_pending_gate_a(self) -> None:
        rows = self.copied_rows()
        self.exact_row(rows)["validation_status"] = "PENDING"
        report = self.report_for(rows)
        self.assertEqual(report["validation_status"], "FAIL")
        self.assertIn("exact_object_validation_status_mismatch", report["errors"])
        self.assertIn("cross_object_substitution_not_rejected", report["errors"])

    def test_missing_exact_object_fails_closed(self) -> None:
        rows = [row for row in self.copied_rows() if row["object_id"] != VALIDATOR.GATE_A_OBJECT_ID]
        report = self.report_for(rows)
        self.assertEqual(report["validation_status"], "FAIL")
        self.assertIn("exact_object_row_count_mismatch", report["errors"])

    def test_duplicate_exact_object_fails_closed(self) -> None:
        rows = self.copied_rows()
        rows.append(dict(self.exact_row(rows)))
        report = self.report_for(rows)
        self.assertEqual(report["validation_status"], "FAIL")
        self.assertIn("exact_object_row_count_mismatch", report["errors"])

    def test_wrong_exact_path_fails_closed(self) -> None:
        rows = self.copied_rows()
        self.exact_row(rows)["path"] = "ontology/tex/aether_flow_foundations.tex"
        report = self.report_for(rows)
        self.assertEqual(report["validation_status"], "FAIL")
        self.assertIn("exact_object_path_mismatch", report["errors"])

    def test_wrong_exact_hash_fails_closed(self) -> None:
        rows = self.copied_rows()
        self.exact_row(rows)["source_hash"] = "0" * 64
        report = self.report_for(rows)
        self.assertEqual(report["validation_status"], "FAIL")
        self.assertIn("exact_object_registry_sha256_mismatch", report["errors"])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ARTIFACT_DIR = Path(__file__).resolve().parent
MODULE_PATH = ARTIFACT_DIR / "bootstrap_fresh_environment.py"
SPEC = importlib.util.spec_from_file_location("p13_t06_bootstrap", MODULE_PATH)
assert SPEC and SPEC.loader
bootstrap = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bootstrap)


class FreshEnvironmentContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.definition = bootstrap._load_json(bootstrap.DEFAULT_DEFINITION)

    def test_live_definition_and_source_hashes_pass(self) -> None:
        receipt = bootstrap.validate_definition(self.definition)
        self.assertEqual(receipt["status"], "PASS", receipt["errors"])
        self.assertTrue(receipt["source_hashes_match"])
        self.assertEqual(receipt["excluded_input_finding_count"], 0)

    def test_local_cache_source_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.definition)
        mutated["source_manifest"].append(
            {"path": ".local/secret.bin", "sha256": "0" * 64}
        )
        receipt = bootstrap.validate_definition(mutated, verify_live_sources=False)
        self.assertEqual(receipt["status"], "FAIL")
        self.assertIn("source_exclusion", {item["check_id"] for item in receipt["errors"]})

    def test_source_hash_drift_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.definition)
        mutated["source_manifest"][0]["sha256"] = "0" * 64
        receipt = bootstrap.validate_definition(mutated)
        self.assertEqual(receipt["status"], "FAIL")
        self.assertIn("source_hash", {item["check_id"] for item in receipt["errors"]})

    def test_target_inside_checkout_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside the repository"):
            bootstrap.validate_external_target(
                bootstrap.REPO_ROOT / ".local/p13-t06-illegal-target"
            )

    def test_source_manifest_digest_is_deterministic(self) -> None:
        first = bootstrap.validate_definition(self.definition)
        second = bootstrap.validate_definition(copy.deepcopy(self.definition))
        self.assertEqual(
            first["source_manifest_sha256"],
            second["source_manifest_sha256"],
        )

    def test_authority_flag_cannot_be_promoted(self) -> None:
        mutated = copy.deepcopy(self.definition)
        mutated["authority"]["proof_authority"] = True
        receipt = bootstrap.validate_definition(mutated, verify_live_sources=False)
        self.assertEqual(receipt["status"], "FAIL")
        self.assertIn(
            "authority_boundary",
            {item["check_id"] for item in receipt["errors"]},
        )


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import importlib.util
import json
import unicodedata
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "research_control/tasks/RT-20260722-002/artifacts/artifact_identity.py"
SPEC = importlib.util.spec_from_file_location("p10_t07_artifact_identity", MODULE_PATH)
assert SPEC and SPEC.loader
artifact_identity = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(artifact_identity)


class ArtifactIdentityPolicyTests(unittest.TestCase):
    def test_policy_fixture_path_is_portable(self) -> None:
        path = "research_control/tasks/RT-20260722-002/artifacts/artifact_path_policy.md"
        self.assertEqual(artifact_identity.lint_relative_path(path), [])

    def test_content_addressed_filename_is_portable(self) -> None:
        path = f"research_control/tasks/RT-20260722-002/artifacts/ca/{'a' * 64}.json"
        self.assertEqual(artifact_identity.lint_relative_path(path), [])

    def test_absolute_path_is_rejected(self) -> None:
        codes = {item["code"] for item in artifact_identity.lint_relative_path("/tmp/a.json")}
        self.assertIn("absolute_path", codes)

    def test_backslash_is_rejected(self) -> None:
        codes = {item["code"] for item in artifact_identity.lint_relative_path(r"artifacts\a.json")}
        self.assertIn("backslash_separator", codes)

    def test_windows_reserved_name_is_rejected(self) -> None:
        codes = {item["code"] for item in artifact_identity.lint_relative_path("artifacts/Con.md")}
        self.assertIn("windows_reserved_name", codes)

    def test_trailing_period_or_space_is_rejected(self) -> None:
        codes = {item["code"] for item in artifact_identity.lint_relative_path("artifacts/name. ")}
        self.assertIn("trailing_space_or_period", codes)

    def test_parent_segment_is_rejected(self) -> None:
        codes = {item["code"] for item in artifact_identity.lint_relative_path("artifacts/../name.md")}
        self.assertIn("unsafe_segment", codes)

    def test_non_nfc_path_is_rejected(self) -> None:
        path = "artifacts/cafe\u0301.md"
        self.assertNotEqual(path, unicodedata.normalize("NFC", path))
        codes = {item["code"] for item in artifact_identity.lint_relative_path(path)}
        self.assertIn("non_nfc", codes)

    def test_component_length_is_bounded(self) -> None:
        codes = {item["code"] for item in artifact_identity.lint_relative_path(f"artifacts/{'x' * 97}.md")}
        self.assertIn("component_chars", codes)

    def test_casefold_collision_is_detected(self) -> None:
        collisions = artifact_identity.casefold_collisions(["artifacts/Report.md", "artifacts/report.md"])
        self.assertEqual(len(collisions), 1)

    def test_manifest_uses_unique_full_sha256_identities(self) -> None:
        manifest, copies = artifact_identity.build_manifest()
        refs = manifest["references"]
        self.assertEqual(len(refs), 3)
        self.assertEqual(len({item["stable_alias"] for item in refs}), 3)
        for item in refs:
            digest = item["content_sha256"]
            self.assertEqual(len(digest), 64)
            self.assertEqual(item["identity"], f"sha256:{digest}")
            self.assertEqual(artifact_identity.sha256_bytes(copies[item["content_path"]]), digest)
            self.assertFalse(item["historical_source_path_changed"])

    def test_expected_outputs_are_deterministic_and_valid(self) -> None:
        first_outputs, first_validation = artifact_identity.expected_outputs()
        second_outputs, second_validation = artifact_identity.expected_outputs()
        self.assertEqual(first_outputs, second_outputs)
        self.assertEqual(first_validation, second_validation)
        self.assertEqual(first_validation["status"], "PASS")
        self.assertEqual(first_validation["failed_check_count"], 0)
        manifest = json.loads(first_outputs[artifact_identity.rel_path(artifact_identity.MANIFEST_PATH)])
        self.assertFalse(manifest["historical_paths_changed"])
        self.assertFalse(manifest["physics_promotion_authorized"])


if __name__ == "__main__":
    unittest.main()

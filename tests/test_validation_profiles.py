from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
from unittest import mock
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"

from scripts.project_control.classify_project_changes import classify_paths
from scripts.validation.plan import load_manifest
from scripts.validation.profiles import (
    CHECKPOINT_OBLIGATIONS,
    DEFAULT_LOCAL_PROFILE,
    PERMANENT_PROFILES,
    SHADOW_MODIFIER,
    ProfileError,
    build_membership_audit,
    profile_definition,
    resolve_profile,
)


class ValidationProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(MANIFEST_PATH)

    def test_exactly_five_permanent_profiles_are_defined(self) -> None:
        self.assertEqual(
            PERMANENT_PROFILES,
            ("fast", "affected", "checkpoint", "full", "doctor"),
        )
        self.assertNotIn(SHADOW_MODIFIER, PERMANENT_PROFILES)
        self.assertNotEqual(DEFAULT_LOCAL_PROFILE, "full")

    def test_each_profile_has_one_purpose_and_planner_command(self) -> None:
        purposes: set[str] = set()
        commands: set[str] = set()
        for name in PERMANENT_PROFILES:
            definition = profile_definition(name)
            self.assertTrue(definition.purpose)
            self.assertIn(f"--profile {name}", definition.command)
            purposes.add(definition.purpose)
            commands.add(definition.command)
        self.assertEqual(len(purposes), len(PERMANENT_PROFILES))
        self.assertEqual(len(commands), len(PERMANENT_PROFILES))

    def test_current_manifest_membership_audit_passes(self) -> None:
        audit = build_membership_audit(self.manifest)
        self.assertEqual(audit["status"], "PASS")
        self.assertEqual(audit["permanent_profiles"], list(PERMANENT_PROFILES))
        self.assertFalse(audit["authority"]["physics_claim_authority"])
        self.assertFalse(audit["authority"]["proof_authority"])
        self.assertEqual(audit["legacy_execution_authority"], "legacy")

    def test_full_retains_every_nontransactional_blocking_gate(self) -> None:
        audit = build_membership_audit(self.manifest)
        memberships = set(audit["profile_membership"]["full"])
        expected = {
            gate["gate_id"]
            for gate in self.manifest["gates"]
            if gate["severity"] == "blocking"
            and gate["gate_id"] != "checkpoint_transaction"
        }
        self.assertEqual(expected - memberships, set())
        self.assertIn("test_shard_repository", memberships)
        self.assertIn("profile_ci_project_control", memberships)
        resolution = resolve_profile(
            self.manifest,
            classify_paths([]),
            requested_profile="full",
        )
        self.assertEqual(expected - set(resolution.plan.selected_gate_ids), set())
        self.assertNotIn("checkpoint_transaction", resolution.plan.selected_gate_ids)

    def test_checkpoint_retains_staged_safeguards(self) -> None:
        audit = build_membership_audit(self.manifest)
        checkpoint_obligations = set(
            audit["profile_obligations"]["checkpoint"]
        )
        self.assertEqual(set(CHECKPOINT_OBLIGATIONS) - checkpoint_obligations, set())
        self.assertIn(
            "checkpoint_transaction",
            audit["profile_membership"]["checkpoint"],
        )

    def test_doctor_has_no_blocking_members_and_cannot_satisfy_checkpoint(self) -> None:
        audit = build_membership_audit(self.manifest)
        self.assertEqual(audit["doctor_blocking_gate_ids"], [])
        self.assertEqual(audit["doctor_checkpoint_obligation_overlap"], [])
        with self.assertRaisesRegex(ProfileError, "doctor.*checkpoint"):
            resolve_profile(
                self.manifest,
                classify_paths([]),
                requested_profile="doctor",
                role_obligations=("checkpoint_transaction",),
            )

    def test_profile_selection_cannot_override_human_gate(self) -> None:
        with self.assertRaisesRegex(ProfileError, "human gate"):
            resolve_profile(
                self.manifest,
                classify_paths([]),
                requested_profile="full",
                human_gate_required=True,
            )

    def test_shadow_modifier_changes_no_gate_membership(self) -> None:
        classification = classify_paths(["scripts/validation/profiles.py"])
        plain = resolve_profile(
            self.manifest,
            classification,
            requested_profile="affected",
        )
        shadow = resolve_profile(
            self.manifest,
            classification,
            requested_profile="affected",
            shadow=True,
        )
        self.assertEqual(plain.plan.canonical_json(), shadow.plan.canonical_json())
        self.assertEqual(plain.plan.selected_gate_ids, shadow.plan.selected_gate_ids)
        self.assertFalse(plain.shadow_modifier_active)
        self.assertTrue(shadow.shadow_modifier_active)
        self.assertTrue(shadow.comparison_required)

    def test_empty_fast_plan_is_deterministic_and_not_full(self) -> None:
        left = resolve_profile(
            self.manifest,
            classify_paths([]),
            requested_profile="fast",
        )
        right = resolve_profile(
            self.manifest,
            classify_paths([]),
            requested_profile="fast",
        )
        self.assertEqual(left.plan.canonical_json(), right.plan.canonical_json())
        self.assertEqual(left.effective_profile, "fast")
        self.assertIn("classify_changes", left.plan.selected_gate_ids)
        self.assertIn("git_diff_check", left.plan.selected_gate_ids)

    def test_unknown_governed_path_fails_safe_to_full(self) -> None:
        resolution = resolve_profile(
            self.manifest,
            classify_paths(["future_governed_surface/example.rule"]),
            requested_profile="affected",
        )
        self.assertEqual(resolution.effective_profile, "full")
        self.assertEqual(
            resolution.plan.unknown_paths,
            ("future_governed_surface/example.rule",),
        )

    def test_doctor_local_retrieval_is_non_authoritative(self) -> None:
        resolution = resolve_profile(
            self.manifest,
            classify_paths([".local/example.db"]),
            requested_profile="doctor",
            scopes=("local_retrieval",),
        )
        self.assertIn("local_retrieval_sync", resolution.plan.selected_gate_ids)
        payload = resolution.to_dict()
        self.assertFalse(payload["authority"]["repository_acceptance_authority"])
        self.assertFalse(payload["authority"]["physics_claim_authority"])

    def test_profile_resolution_executes_no_subprocesses(self) -> None:
        with mock.patch(
            "subprocess.run",
            side_effect=AssertionError("command executed"),
        ):
            resolution = resolve_profile(
                self.manifest,
                classify_paths(["scripts/validation/profiles.py"]),
                requested_profile="affected",
                shadow=True,
            )
        self.assertFalse(resolution.to_dict()["profile_executes_commands"])

    def test_planner_authoritative_profile_reports_executor_authority(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["migration_epoch"] = "planner_authoritative"
        manifest["execution_authority"] = "manifest_planner"
        resolution = resolve_profile(
            manifest,
            classify_paths(["scripts/validation/profiles.py"]),
            requested_profile="affected",
        )
        self.assertTrue(resolution.to_dict()["profile_executes_commands"])
        audit = build_membership_audit(manifest)
        self.assertEqual(audit["execution_authority"], "manifest_planner")
        self.assertFalse(audit["authority"]["legacy_execution_authoritative"])
        self.assertTrue(audit["authority"]["planner_execution_authoritative"])

    def test_missing_full_blocking_membership_fails_closed(self) -> None:
        manifest = deepcopy(self.manifest)
        gate = next(
            item for item in manifest["gates"] if item["gate_id"] == "memory_core"
        )
        gate["profiles"].remove("full")
        with self.assertRaisesRegex(ProfileError, "full profile omits"):
            build_membership_audit(manifest)

    def test_missing_checkpoint_safeguard_fails_closed(self) -> None:
        manifest = deepcopy(self.manifest)
        gate = next(
            item
            for item in manifest["gates"]
            if item["gate_id"] == "checkpoint_transaction"
        )
        gate["profiles"] = ["full"]
        with self.assertRaisesRegex(ProfileError, "checkpoint profile omits"):
            build_membership_audit(manifest)

    def test_blocking_doctor_membership_fails_closed(self) -> None:
        manifest = deepcopy(self.manifest)
        gate = next(
            item for item in manifest["gates"] if item["gate_id"] == "memory_core"
        )
        gate["profiles"].append("doctor")
        with self.assertRaisesRegex(ProfileError, "doctor profile contains blocking"):
            build_membership_audit(manifest)

    def test_audit_is_canonical_and_reports_shadow_comparison(self) -> None:
        left = build_membership_audit(self.manifest)
        right = build_membership_audit(self.manifest)
        self.assertEqual(
            json.dumps(left, sort_keys=True, separators=(",", ":")),
            json.dumps(right, sort_keys=True, separators=(",", ":")),
        )
        comparison = left["affected_blocking_shadow_comparison"]
        self.assertEqual(comparison["status"], "PASS")
        self.assertEqual(comparison["unexplained_mismatch_gate_ids"], [])
        self.assertEqual(
            comparison["planner_gate_ids"],
            comparison["legacy_compatible_gate_ids"],
        )

    def test_audit_cli_is_deterministic_json(self) -> None:
        command = [
            str(ROOT / ".venv/bin/python"),
            str(ROOT / "scripts/validation/profiles.py"),
            "audit",
            "--json",
        ]
        first = subprocess.run(
            command,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        second = subprocess.run(
            command,
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
        self.assertEqual(first, second)
        self.assertEqual(json.loads(first)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()

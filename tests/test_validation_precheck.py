from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "research_control/design/validation_gate_manifest_v1.yaml"

from scripts.validation.plan import load_manifest
from scripts.validation.precheck import (
    CommandResult,
    _shadow_comparison,
    render_json_summary,
    run_precheck,
    select_affected_tests,
)


WORKING_HASH = "working-sha256:" + ("a" * 64)


def classification(
    paths: list[str],
    *,
    blocked: list[str] | None = None,
    unknown: list[str] | None = None,
) -> dict[str, object]:
    unknown = unknown or []
    details = [
        {
            "path": path,
            "tags": ["unknown_governed_path"] if path in unknown else ["validator_code"],
            "reasons": [],
            "canonical_paths": [],
            "generated_derivatives": [],
            "affected_source_object_ids": [],
        }
        for path in paths
    ]
    return {
        "changed_paths": sorted(paths),
        "blocked_paths": sorted(blocked or []),
        "ignored_paths": [],
        "path_family_tags": (
            ["unknown_governed_path"] if unknown else (["validator_code"] if paths else [])
        ),
        "path_family_details": details,
        "recommended_validation_profile": "full" if unknown else ("affected" if paths else ""),
    }


class RecordingRunner:
    def __init__(self, failures: dict[str, CommandResult] | None = None) -> None:
        self.failures = failures or {}
        self.commands: list[tuple[str, ...]] = []

    def __call__(
        self,
        command: tuple[str, ...],
        *,
        cwd: Path,
        timeout_seconds: int,
        env: dict[str, str] | None = None,
    ) -> CommandResult:
        del cwd, timeout_seconds, env
        self.commands.append(command)
        rendered = " ".join(command)
        for marker, result in self.failures.items():
            if marker in rendered:
                return result
        return CommandResult(exit_code=0, stdout="", stderr="")


class ValidationPrecheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest(MANIFEST_PATH)

    def run_checked(
        self,
        repo_root: Path,
        paths: list[str],
        *,
        runner: RecordingRunner | None = None,
        classifier=None,
        only_gate: str | None = None,
        manifest: dict[str, object] | None = None,
    ) -> dict[str, object]:
        return run_precheck(
            repo_root,
            paths,
            only_gate=only_gate,
            manifest=manifest or self.manifest,
            command_runner=runner or RecordingRunner(),
            classifier=classifier or (lambda values, **_: classification(list(values))),
            tree_hash=WORKING_HASH,
        )

    def test_empty_diff_pass_is_working_only_and_cannot_satisfy_checkpoint(self) -> None:
        receipt = self.run_checked(ROOT, [])
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(receipt["scope"], "working")
        self.assertEqual(receipt["tree_hash"], WORKING_HASH)
        self.assertFalse(receipt["evidence_reuse"]["checkpoint_acceptance"])
        self.assertFalse(receipt["evidence_reuse"]["staged_pass_reusable"])
        self.assertEqual(receipt["authority"]["repository_acceptance"], False)
        self.assertEqual(receipt["counts"]["selected_path_count"], 0)

    def test_python_and_json_syntax_failures_are_reported_before_tests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "broken.py").write_text("def broken(:\n", encoding="utf-8")
            (root / "broken.json").write_text("{\"broken\":", encoding="utf-8")
            (root / "broken.yaml").write_text("broken: [\n", encoding="utf-8")
            runner = RecordingRunner()
            receipt = self.run_checked(
                root,
                ["broken.py", "broken.json", "broken.yaml"],
                runner=runner,
            )
        by_id = {gate["gate_id"]: gate for gate in receipt["gate_results"]}
        self.assertEqual(receipt["status"], "FAIL")
        self.assertEqual(by_id["syntax_schema"]["status"], "FAIL")
        self.assertEqual(by_id["syntax_schema"]["finding_count"], 3)
        self.assertEqual(by_id["affected_fast_tests"]["status"], "SKIP_NOT_APPLICABLE")
        self.assertFalse(any("unittest" in " ".join(command) for command in runner.commands))

    def test_unknown_and_blocked_paths_fail_closed(self) -> None:
        paths = ["future/surface.rule", "wiki/generated.md"]
        receipt = self.run_checked(
            ROOT,
            paths,
            classifier=lambda values, **_: classification(
                list(values),
                blocked=["wiki/generated.md"],
                unknown=["future/surface.rule"],
            ),
        )
        gate = next(item for item in receipt["gate_results"] if item["gate_id"] == "path_policy_sanity")
        self.assertEqual(gate["status"], "FAIL")
        self.assertEqual(gate["finding_count"], 2)

    def test_changed_claim_language_failure_remains_authoritative(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("claim text\n", encoding="utf-8")
            runner = RecordingRunner(
                {
                    "validate_claim_language.py": CommandResult(
                        exit_code=1,
                        stdout=json.dumps(
                            {
                                "status": "FAIL",
                                "hard_fail_count": 1,
                                "finding_count": 1,
                                "findings": [{"class_id": "overclaim", "path": "README.md", "line": 1}],
                            }
                        ),
                        stderr="",
                    )
                }
            )
            receipt = self.run_checked(root, ["README.md"], runner=runner)
        gate = next(item for item in receipt["gate_results"] if item["gate_id"] == "changed_claim_language")
        self.assertEqual(gate["status"], "FAIL")
        self.assertEqual(gate["details"]["legacy_result_authoritative"], True)
        self.assertIn("validate_claim_language.py", " ".join(runner.commands[0]))

    def test_whitespace_failure_is_preserved(self) -> None:
        runner = RecordingRunner(
            {"git diff --check": CommandResult(2, "bad.py:1: trailing whitespace\n", "")}
        )
        receipt = self.run_checked(ROOT, ["scripts/validation/precheck.py"], runner=runner)
        gate = next(item for item in receipt["gate_results"] if item["gate_id"] == "git_diff_check")
        self.assertEqual(gate["status"], "FAIL")
        self.assertIn("trailing whitespace", gate["stdout"])

    def test_untracked_trailing_whitespace_is_not_missed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "new.py").write_text("value = 1  \n", encoding="utf-8")
            runner = RecordingRunner(
                {"git ls-files": CommandResult(0, "new.py\0", "")}
            )
            receipt = self.run_checked(root, ["new.py"], runner=runner)
        gate = next(item for item in receipt["gate_results"] if item["gate_id"] == "git_diff_check")
        self.assertEqual(gate["status"], "FAIL")
        self.assertEqual(gate["findings"][0]["code"], "untracked_trailing_whitespace")

    def test_representative_path_families_pass_the_cheap_policy_gate(self) -> None:
        cases = (
            "scripts/validation/precheck.py",
            "research_control/tasks/RT-20260716-017/00_TASK.yaml",
            "README.md",
            ".local/example.db",
        )
        for path in cases:
            with self.subTest(path=path):
                receipt = run_precheck(
                    ROOT,
                    [path],
                    only_gate="path_policy_sanity",
                    manifest=self.manifest,
                    command_runner=RecordingRunner(),
                    tree_hash=WORKING_HASH,
                )
                self.assertEqual(receipt["status"], "PASS")

    def test_affected_test_selection_is_bounded_and_deterministic(self) -> None:
        selected = select_affected_tests(
            ROOT,
            [
                "scripts/validation/precheck.py",
                "scripts/project_control/classify_project_changes.py",
                "tests/test_validation_profiles.py",
                "README.md",
            ],
        )
        self.assertEqual(
            selected,
            (
                "tests/test_project_change_classifier.py",
                "tests/test_validation_precheck.py",
                "tests/test_validation_profiles.py",
            ),
        )

    def test_single_gate_rerun_executes_only_prerequisites_and_requested_gate(self) -> None:
        runner = RecordingRunner()
        receipt = self.run_checked(
            ROOT,
            ["scripts/validation/precheck.py"],
            runner=runner,
            only_gate="affected_fast_tests",
        )
        self.assertEqual(
            [gate["gate_id"] for gate in receipt["gate_results"]],
            ["classify_changes", "path_policy_sanity", "affected_fast_tests"],
        )
        self.assertEqual(len(runner.commands), 1)
        self.assertIn("tests/test_validation_precheck.py", runner.commands[0])

    def test_shadow_excludes_mutators_and_blocks_unexplained_mismatch(self) -> None:
        comparison = _shadow_comparison(
            self.manifest,
            classification(["scripts/validation/precheck.py"]),
        )
        self.assertEqual(comparison["status"], "PASS")
        excluded = {item["gate_id"]: item["reason"] for item in comparison["excluded_gate_ids"]}
        self.assertEqual(
            excluded["continue_memory_preflight"],
            "precheck_forbids_mutating_gates",
        )
        self.assertEqual(comparison["unexplained_mismatch_gate_ids"], [])

        changed = deepcopy(self.manifest)
        gate = next(item for item in changed["gates"] if item["gate_id"] == "continue_memory_preflight")
        gate["mutating"] = False
        mismatch = _shadow_comparison(
            changed,
            classification(["scripts/validation/precheck.py"]),
        )
        self.assertEqual(mismatch["status"], "BLOCKED_CONFIGURATION")
        self.assertEqual(mismatch["unexplained_mismatch_gate_ids"], ["continue_memory_preflight"])

    def test_compact_json_output_names_scope_receipt_and_authority(self) -> None:
        receipt = self.run_checked(ROOT, [])
        output = render_json_summary(receipt, Path(".local/receipt.json"))
        payload = json.loads(output)
        self.assertEqual(payload["status"], "PASS")
        self.assertEqual(payload["scope"], "working")
        self.assertFalse(payload["checkpoint_acceptance"])
        self.assertEqual(payload["full_receipt"], ".local/receipt.json")
        self.assertLessEqual(len(output.encode("utf-8")), 2048)


if __name__ == "__main__":
    unittest.main()

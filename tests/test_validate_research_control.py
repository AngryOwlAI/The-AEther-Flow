from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts" / "research_control"
FIXTURE_ROOT = REPO_ROOT / "tests" / "fixtures" / "research_control"


def load_module(name: str, filename: str):
    if str(SCRIPT_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPT_DIR))
    spec = importlib.util.spec_from_file_location(name, SCRIPT_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def yaml_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return json.dumps(str(value))


def markdown_scalar(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return f"`{value}`" if str(value) in {"none", "latest_research_handoff"} else str(value)


class ActiveStateSidecarValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module("validate_research_control", "validate_research_control.py")

    def load_scenario(self, path: Path) -> dict:
        return self.validator.load_yaml(path)

    def write_scenario_root(
        self,
        root: Path,
        scenario: dict,
        *,
        compact_overrides: dict | None = None,
        sidecar_fixture_dir: Path | None = None,
    ) -> dict[str, dict[str, str]]:
        control_dir = root / "research_control"
        handoff_dir = control_dir / "handoffs"
        task_dir = control_dir / "tasks" / scenario["active_task_id"]
        output_dir = root / "output"
        handoff_dir.mkdir(parents=True)
        task_dir.mkdir(parents=True)
        output_dir.mkdir(parents=True)

        bifurcation = scenario["bifurcation"]
        (control_dir / "program_state.yaml").write_text(
            "\n".join(
                [
                    'mode: "director_led_research_control"',
                    f"active_task_id: {yaml_scalar(scenario['active_task_id'])}",
                    f"latest_handoff_id: {yaml_scalar(scenario['latest_handoff_id'])}",
                    f"current_status: {yaml_scalar(scenario['current_status'])}",
                    'claim_boundary_summary: "test boundary"',
                    f"next_recommended_action: {yaml_scalar(scenario['next_action'])}",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        (task_dir / "00_TASK.yaml").write_text(
            "\n".join(
                [
                    f"task_id: {yaml_scalar(scenario['active_task_id'])}",
                    'status: "completed"',
                    "",
                ]
            ),
            encoding="utf-8",
        )
        handoff_lines = [
            f"handoff_id: {yaml_scalar(scenario['latest_handoff_id'])}",
            'created_at: "2026-07-07T08:32:47Z"',
            f"task_id: {yaml_scalar(scenario['active_task_id'])}",
            'job_id: "AJ-TEST-001"',
            'completion_path: "research_control/tasks/RT-TEST-002/jobs/completions/AJC-AJ-TEST-001.yaml"',
            f"next_action: {yaml_scalar(scenario['next_action'])}",
            "active_state_bifurcation:",
        ]
        for field_name in self.validator.ACTIVE_STATE_BIFURCATION_FIELDS:
            handoff_lines.append(f"  {field_name}: {yaml_scalar(bifurcation[field_name])}")
        handoff_lines.extend(
            [
                "distance_to_gr:",
                '  milestone: "none"',
                '  burden_id: "none"',
                '  status: "no_distance_delta"',
                "  changed: false",
                "",
            ]
        )
        (handoff_dir / f"{scenario['latest_handoff_id']}.yaml").write_text(
            "\n".join(handoff_lines),
            encoding="utf-8",
        )

        frontier_lines = [
            "# Current Frontier",
            "",
            "## Active Research State",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Active task ID | `{scenario['active_task_id']}` |",
            f"| Latest handoff ID | `{scenario['latest_handoff_id']}` |",
            f"| Current status | {scenario['current_status']} |",
            "| Target derivation milestone | `none` |",
            "| Current burden | `none` |",
            f"| Next recommended action | {scenario['next_action']} |",
            "",
            "## Active-State Bifurcation",
            "",
            "| Field | Value |",
            "| --- | --- |",
        ]
        label_by_key = {value: key for key, value in self.validator.CURRENT_FRONTIER_BIFURCATION_FIELD_MAP.items()}
        for field_name in self.validator.ACTIVE_STATE_BIFURCATION_FIELDS:
            frontier_lines.append(f"| {label_by_key[field_name]} | {markdown_scalar(bifurcation[field_name])} |")
        frontier_lines.append("")
        (control_dir / "current_frontier.md").write_text("\n".join(frontier_lines), encoding="utf-8")

        compact_bifurcation = copy.deepcopy(bifurcation)
        if compact_overrides:
            compact_bifurcation.update(compact_overrides)
        (output_dir / "compact_current_frontier_v16.json").write_text(
            json.dumps({"active_state_bifurcation": compact_bifurcation}, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

        if sidecar_fixture_dir:
            sidecar_dir = control_dir / "project_improvement_handoffs"
            sidecar_dir.mkdir(parents=True)
            for fixture in sidecar_fixture_dir.glob("improve-project-handoff_*.yaml"):
                shutil.copyfile(fixture, sidecar_dir / fixture.name)

        return {scenario["active_task_id"]: {"task_id": scenario["active_task_id"]}}

    def run_bifurcation_validation(
        self,
        scenario: dict,
        *,
        compact_overrides: dict | None = None,
        sidecar_fixture_dir: Path | None = None,
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tasks = self.write_scenario_root(
                root,
                scenario,
                compact_overrides=compact_overrides,
                sidecar_fixture_dir=sidecar_fixture_dir,
            )
            report = self.validator.ValidationReport()
            with (
                mock.patch.object(self.validator, "REPO_ROOT", root),
                mock.patch.object(self.validator, "CONTROL_DIR", root / "research_control"),
                mock.patch.object(self.validator, "REGISTRY_DIR", root / "registries"),
            ):
                self.validator.validate_active_state_bifurcation(report, tasks)
            return report.errors

    def test_project_system_sidecar_status_does_not_supersede_research_handoff(self) -> None:
        scenario = self.load_scenario(
            FIXTURE_ROOT / "active_state_sidecar_valid" / "ordinary_research_handoff.yaml"
        )

        self.assertEqual(self.run_bifurcation_validation(scenario), [])

    def test_sidecar_supersession_without_authorization_fails(self) -> None:
        scenario = self.load_scenario(
            FIXTURE_ROOT / "active_state_sidecar_invalid" / "sidecar_supersedes_without_authorization.yaml"
        )

        errors = self.run_bifurcation_validation(scenario)

        self.assertTrue(any("may not supersede" in error for error in errors), errors)

    def test_sidecar_physics_promotion_claim_fails(self) -> None:
        scenario = self.load_scenario(
            FIXTURE_ROOT / "active_state_sidecar_invalid" / "sidecar_physics_promotion.yaml"
        )

        errors = self.run_bifurcation_validation(
            scenario,
            sidecar_fixture_dir=FIXTURE_ROOT / "active_state_sidecar_invalid",
        )

        self.assertTrue(any("protected physics-authority claim flags" in error for error in errors), errors)

    def test_later_ordinary_research_handoff_is_accepted(self) -> None:
        scenario = copy.deepcopy(
            self.load_scenario(FIXTURE_ROOT / "active_state_sidecar_valid" / "ordinary_research_handoff.yaml")
        )
        scenario["active_task_id"] = "RT-TEST-003"
        scenario["latest_handoff_id"] = "handoff-0003"
        scenario["bifurcation"]["latest_research_task_id"] = "RT-TEST-003"
        scenario["bifurcation"]["latest_research_handoff_id"] = "handoff-0003"

        self.assertEqual(self.run_bifurcation_validation(scenario), [])

    def test_compact_frontier_bifurcation_mismatch_fails(self) -> None:
        scenario = self.load_scenario(
            FIXTURE_ROOT / "active_state_sidecar_valid" / "ordinary_research_handoff.yaml"
        )

        errors = self.run_bifurcation_validation(
            scenario,
            compact_overrides={"latest_research_handoff_id": "handoff-0001"},
        )

        self.assertTrue(any("output/compact_current_frontier_v16.json" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()

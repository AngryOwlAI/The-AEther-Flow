from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MakeValidationOrchestrationTests(unittest.TestCase):
    def test_validate_project_control_runs_one_research_control_spine(self) -> None:
        completed = subprocess.run(
            ["make", "-n", "PYTHON=.venv/bin/python", "validate-project-control"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        research_control_commands = [
            line.strip()
            for line in completed.stdout.splitlines()
            if "scripts/research_control/validate_research_control.py" in line
        ]

        self.assertEqual(
            research_control_commands,
            [
                ".venv/bin/python scripts/research_control/validate_research_control.py "
                "--check-diff"
            ],
        )


if __name__ == "__main__":
    unittest.main()

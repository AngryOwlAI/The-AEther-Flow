from __future__ import annotations

import copy
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "scripts/research_control"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import generated_report_provenance as provenance  # noqa: E402
import validate_generated_report_freshness as validator  # noqa: E402


class GeneratedReportProvenanceTests(unittest.TestCase):
    def test_source_manifest_is_order_independent(self) -> None:
        hashes = {"b.txt": "b" * 64, "a.txt": "a" * 64}
        self.assertEqual(
            provenance.source_manifest_sha256(hashes),
            provenance.source_manifest_sha256(dict(reversed(list(hashes.items())))),
        )

    def test_metadata_marker_round_trip(self) -> None:
        metadata = {
            "schema_id": provenance.SCHEMA_ID,
            "source_commit": "1" * 40,
            "source_hashes": [{"path": "a", "sha256": "2" * 64}],
        }
        marker = provenance.metadata_comment(metadata)
        self.assertEqual(provenance.parse_metadata_comment(marker), metadata)

    def test_mutated_hash_fails_exact_metadata_comparison(self) -> None:
        payload, _ = validator.current_frontier.render_payload(
            REPO_ROOT,
            source_commit=provenance.git_head(REPO_ROOT),
        )
        expected = payload["report_provenance"]
        observed = copy.deepcopy(expected)
        observed["source_hashes"][0]["sha256"] = "0" * 64
        result = provenance.validate_metadata(
            repo_root=REPO_ROOT,
            observed=observed,
            expected=expected,
            strict=True,
        )
        self.assertEqual(result["status"], "FAIL")
        self.assertIn(
            "generated_report_source_metadata_stale",
            [item["finding_id"] for item in result["findings"]],
        )

    def test_second_unrefreshed_commit_exceeds_lag(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
            subprocess.run(
                ["git", "-C", str(root), "config", "user.name", "Fixture"], check=True
            )
            subprocess.run(
                ["git", "-C", str(root), "config", "user.email", "fixture@example.invalid"],
                check=True,
            )
            source = root / "source.txt"
            source.write_text("source\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "source.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(root), "commit", "-q", "-m", "source"], check=True
            )
            source_commit = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            metadata = provenance.build_metadata(
                report_class="current_frontier",
                source_commit=source_commit,
                source_hashes={"source.txt": provenance.sha256_bytes(source.read_bytes())},
                primary_source_paths=["source.txt"],
                generation_time="1970-01-01T00:00:00Z",
                task_count=1,
                renderer_path=provenance.HELPER_PATH,
                renderer_sha256=provenance.HELPER_SHA256,
                strict=False,
            )
            for index in (1, 2):
                path = root / f"unrelated-{index}.txt"
                path.write_text(f"{index}\n", encoding="utf-8")
                subprocess.run(["git", "-C", str(root), "add", path.name], check=True)
                subprocess.run(
                    ["git", "-C", str(root), "commit", "-q", "-m", f"unrelated {index}"],
                    check=True,
                )
            result = provenance.validate_metadata(
                repo_root=root,
                observed=metadata,
                expected=metadata,
                strict=False,
            )
            self.assertEqual(result["observed_commit_lag"], 2)
            self.assertIn(
                "generated_report_commit_lag_exceeded",
                [item["finding_id"] for item in result["findings"]],
            )

    def test_live_generated_reports_are_fresh(self) -> None:
        result = validator.validate_live_reports(REPO_ROOT)
        self.assertEqual(result["report_count"], 4)
        self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()

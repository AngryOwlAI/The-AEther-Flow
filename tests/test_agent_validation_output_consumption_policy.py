from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "research_control/design/agent_validation_output_consumption_policy_v1.md"
SKILLS = (
    ROOT / ".codex/skills/continue-research/SKILL.md",
    ROOT / ".codex/skills/improve-project-system/SKILL.md",
    ROOT / ".codex/skills/user-modified-project/SKILL.md",
)


def normalized(text: str) -> str:
    return " ".join(text.lower().split())


class AgentValidationOutputConsumptionPolicyTests(unittest.TestCase):
    def test_policy_requires_summary_first_and_bounded_failure_expansion(self) -> None:
        text = normalized(POLICY.read_text(encoding="utf-8"))
        for phrase in (
            "summary-first sequence",
            "compact summary first",
            "failed or warning",
            "bounded tail of at most 200 lines",
            "retransmit unchanged output",
            "relevant finding ids",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_policy_requires_compact_completion_evidence(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        for field in (
            "gate_id:",
            "status:",
            "receipt_path:",
            "content_hash:",
            "counts:",
            "relevant_finding_ids:",
            "tree_fingerprint:",
        ):
            with self.subTest(field=field):
                self.assertIn(field, text)

    def test_local_full_receipts_remain_untracked_and_non_authoritative(self) -> None:
        text = POLICY.read_text(encoding="utf-8")
        self.assertIn("`.local/validation-receipts`", text)
        self.assertIn("untracked, non-authoritative", text)
        self.assertIn("must not be registered as canonical sources", normalized(text))

    def test_each_skill_adopts_the_same_consumption_boundary(self) -> None:
        for path in SKILLS:
            text = path.read_text(encoding="utf-8")
            lowered = normalized(text)
            with self.subTest(path=path.relative_to(ROOT).as_posix()):
                self.assertIn("## Validation-Output Consumption", text)
                self.assertIn("read the compact summary first", lowered)
                self.assertIn("failed or warning gate group", lowered)
                self.assertIn("bounded receipt section or tail", lowered)
                self.assertIn("unchanged output", lowered)
                self.assertIn("receipt path", lowered)
                self.assertIn("content hash", lowered)
                self.assertIn("relevant finding ids", lowered)
                self.assertIn("`.local/validation-receipts`", text)
                self.assertIn("untracked and", lowered)
                self.assertIn("non-authoritative", lowered)

    def test_continue_research_requests_the_summary_packet_first(self) -> None:
        text = SKILLS[0].read_text(encoding="utf-8")
        self.assertIn("scripts/research_control/continue_research.py --summary", text)
        self.assertNotIn(
            "The script emits JSON by default. Use `--summary` only",
            text,
        )

    def test_policy_contains_no_unbounded_receipt_examples(self) -> None:
        texts = [POLICY.read_text(encoding="utf-8")]
        texts.extend(path.read_text(encoding="utf-8") for path in SKILLS)
        combined = "\n".join(texts).lower()
        for forbidden in (
            "cat .local/validation-receipts",
            "open the full json on pass",
            "print the entire receipt",
            "embed the entire receipt",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, combined)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Validate AEther-Flow teaching Q&A packets and teaching-enabled specs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCH_CONTROL_DIR = REPO_ROOT / "scripts" / "research_control"
if str(RESEARCH_CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_CONTROL_DIR))

from strict_yaml import StrictYamlError, load_frontmatter  # noqa: E402


REQUIRED_PACKET_FIELDS = {
    "packet_id",
    "topic_slug",
    "source_spec",
    "derived_outputs",
    "audience_model",
    "student_role",
    "teacher_role",
    "rounds",
    "source_materials",
    "claim_boundary",
    "authority_status",
}
REQUIRED_SYNTHESIS_HEADINGS = {
    "Concepts that must appear in the HTML explainer",
    "Concepts that must appear in GitHub-facing Markdown",
    "Glossary candidates",
    "Common confusions to repair",
    "Examples and non-examples",
    "Next reading notes",
    "Source gaps",
    "Claims intentionally not made",
}
REQUIRED_TEACHING_BLOCKS = {
    "plain_language_model",
    "glossary",
    "guided_walkthrough",
    "common_questions",
    "examples_and_non_examples",
    "misconception_repairs",
    "check_your_understanding",
}
TEACHER_ANSWER_FIELDS = {
    "Plain answer:",
    "Technical anchor:",
    "Source paths:",
    "Boundary note:",
    "Curator note:",
}
GENERATED_AUTHORITY_PREFIXES = (
    "html/",
    "wiki/",
    ".local/",
    "ontology/pdfs/",
    "manuscripts/pdfs/",
)
POSITIVE_AUTHORITY_RE = re.compile(
    r"\b(this|it)\s+(changes|authorizes|permits|promotes|creates)\b",
    re.IGNORECASE,
)


def list_value(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def mapping_value(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def is_enabled(frontmatter: dict[str, Any]) -> bool:
    teaching_loop = mapping_value(frontmatter.get("teaching_loop"))
    return teaching_loop.get("enabled") is True or str(teaching_loop.get("enabled", "")).lower() == "true"


def round_count(value: Any) -> int:
    try:
        return int(str(value))
    except ValueError:
        return 0


def markdown_sections(body: str, level: int = 2) -> dict[str, str]:
    marker = "#" * level
    pattern = re.compile(rf"(?m)^{re.escape(marker)}\s+(.+?)\s*$")
    matches = list(pattern.finditer(body))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections[match.group(1).strip()] = body[start:end].strip()
    return sections


def heading_ids(section_text: str, prefix: str) -> list[str]:
    return re.findall(rf"(?m)^###\s+{re.escape(prefix)}(\d+)\b", section_text)


def answer_chunks(section_text: str) -> list[str]:
    parts = re.split(r"(?m)^###\s+A\d+\b.*$", section_text)
    return [part.strip() for part in parts[1:] if part.strip()]


def student_lines(section_text: str) -> list[str]:
    output: list[str] = []
    for raw in section_text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        line = line.removeprefix("- ").strip()
        if line:
            output.append(line)
    return output


def is_generated_authority_path(path: str) -> bool:
    return path.startswith(GENERATED_AUTHORITY_PREFIXES) or path.endswith(".pdf")


def validate_packet(
    *,
    root: Path,
    spec_path: Path,
    spec_frontmatter: dict[str, Any],
    spec_body: str,
    errors: list[str],
) -> None:
    relative_spec = spec_path.relative_to(root).as_posix()
    teaching_loop = mapping_value(spec_frontmatter.get("teaching_loop"))
    packet_text = str(teaching_loop.get("qa_packet", "")).strip()
    if not packet_text:
        errors.append(f"{relative_spec}: teaching_loop.enabled requires qa_packet")
        return
    if not packet_text.startswith("markdown/teaching-packets/"):
        errors.append(f"{relative_spec}: qa_packet must live under markdown/teaching-packets/")
        return
    packet_path = root / packet_text
    if not packet_path.exists():
        errors.append(f"{relative_spec}: missing qa_packet {packet_text}")
        return

    try:
        packet_frontmatter, packet_body = load_frontmatter(packet_path)
    except StrictYamlError as exc:
        errors.append(f"{packet_text}: {exc}")
        return

    missing = sorted(REQUIRED_PACKET_FIELDS - set(packet_frontmatter))
    if missing:
        errors.append(f"{packet_text}: missing packet frontmatter fields {', '.join(missing)}")
    if str(packet_frontmatter.get("authority_status", "")) != "curated_explanatory_support":
        errors.append(f"{packet_text}: authority_status must be curated_explanatory_support")
    if str(packet_frontmatter.get("source_spec", "")) != relative_spec:
        errors.append(f"{packet_text}: source_spec must match {relative_spec}")
    if round_count(packet_frontmatter.get("rounds")) != round_count(teaching_loop.get("rounds")):
        errors.append(f"{packet_text}: rounds must match spec teaching_loop.rounds")

    spec_sources = set(list_value(spec_frontmatter.get("source_materials")))
    packet_sources = set(list_value(packet_frontmatter.get("source_materials")))
    missing_sources = sorted(packet_sources - spec_sources)
    if missing_sources:
        errors.append(f"{packet_text}: packet source_materials not declared by spec: {', '.join(missing_sources)}")
    generated_sources = sorted(path for path in packet_sources if is_generated_authority_path(path))
    if generated_sources:
        errors.append(f"{packet_text}: packet cites generated output as authority: {', '.join(generated_sources)}")

    derived_outputs = list_value(packet_frontmatter.get("derived_outputs"))
    expected_output = str(spec_frontmatter.get("output_path", "")).strip()
    if expected_output and expected_output not in derived_outputs:
        errors.append(f"{packet_text}: derived_outputs must include spec output_path {expected_output}")

    if "## Teaching Q&A Basis" not in spec_body:
        errors.append(f"{relative_spec}: missing Teaching Q&A Basis section")
    if packet_text not in spec_body:
        errors.append(f"{relative_spec}: Teaching Q&A Basis must cite {packet_text}")
    if "explanatory support only" not in spec_body.lower():
        errors.append(f"{relative_spec}: Teaching Q&A Basis must state explanatory support only")

    required_blocks = set(list_value(teaching_loop.get("required_teaching_blocks")))
    missing_blocks = sorted(REQUIRED_TEACHING_BLOCKS - required_blocks)
    if missing_blocks:
        errors.append(f"{relative_spec}: required_teaching_blocks missing {', '.join(missing_blocks)}")

    sections = markdown_sections(packet_body)
    for section in [
        "Curator Feature Selection",
        "Round 1 Student Questions",
        "Round 1 Teacher Answers",
        "Round 2 Student Follow-up Questions",
        "Round 2 Teacher Answers",
        "Curator Synthesis Notes",
    ]:
        if section not in sections:
            errors.append(f"{packet_text}: missing section {section}")

    rounds = round_count(packet_frontmatter.get("rounds"))
    for index in range(1, rounds + 1):
        student_name = "Round 1 Student Questions" if index == 1 else f"Round {index} Student Follow-up Questions"
        teacher_name = f"Round {index} Teacher Answers"
        student = sections.get(student_name, "")
        teacher = sections.get(teacher_name, "")
        question_ids = heading_ids(student, "Q")
        answer_ids = heading_ids(teacher, "A")
        if not question_ids:
            errors.append(f"{packet_text}: {student_name} has no Q headings")
        if question_ids != answer_ids:
            errors.append(f"{packet_text}: {teacher_name} answers {answer_ids} do not match questions {question_ids}")
        for line in student_lines(student):
            if not line.endswith("?"):
                errors.append(f"{packet_text}: {student_name} contains non-question text: {line[:80]}")
        for answer in answer_chunks(teacher):
            for required in TEACHER_ANSWER_FIELDS:
                if required not in answer:
                    errors.append(f"{packet_text}: {teacher_name} answer missing {required}")
            if not re.search(r"(?ms)^Source paths:\s*(?:\n- .+)+", answer):
                errors.append(f"{packet_text}: {teacher_name} answer must list source paths")
            if "not answered" in answer and "Source gap:" not in answer:
                errors.append(f"{packet_text}: source gaps must be explicitly labeled")
            if POSITIVE_AUTHORITY_RE.search(answer):
                errors.append(f"{packet_text}: teacher answer appears to claim new authority")

    synthesis = sections.get("Curator Synthesis Notes", "")
    synthesis_headings = set(re.findall(r"(?m)^###\s+(.+?)\s*$", synthesis))
    missing_synthesis = sorted(REQUIRED_SYNTHESIS_HEADINGS - synthesis_headings)
    if missing_synthesis:
        errors.append(f"{packet_text}: Curator synthesis missing {', '.join(missing_synthesis)}")


def validate_root(root: Path) -> list[str]:
    errors: list[str] = []
    spec_dir = root / "markdown" / "html-explainer-specs"
    for spec_path in sorted(spec_dir.glob("*-explainer.md")):
        try:
            frontmatter, body = load_frontmatter(spec_path)
        except StrictYamlError:
            continue
        if is_enabled(frontmatter):
            validate_packet(
                root=root,
                spec_path=spec_path,
                spec_frontmatter=frontmatter,
                spec_body=body,
                errors=errors,
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    root = args.root.resolve()
    errors = validate_root(root)
    if errors:
        print("\n".join(errors))
        print(f"\nTeaching Q&A validation found {len(errors)} error(s).")
        return 2
    print("Teaching Q&A validation PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

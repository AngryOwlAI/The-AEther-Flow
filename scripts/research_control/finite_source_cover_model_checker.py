#!/usr/bin/env python3
"""Finite source-cover model checker for draft/control witness data.

This checker is deterministic tooling. A pass result is not proof, source-law
adoption, M_src adoption, g_eff construction, or downstream GR authority.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    import strict_yaml
except ImportError:  # pragma: no cover - only used when imported from outside this dir.
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import strict_yaml


CONTROLLED_STATUSES = (
    "pass_candidate_local",
    "fail_nonseparation",
    "fail_topology_noncanonical",
    "fail_transition_incoherent",
    "fail_rank_incoherent",
    "fail_soldering_nonunique",
    "fail_variation_fragile",
    "fail_target_import",
    "bottom",
    "not_applicable",
)

STATUS_PRIORITY = (
    "fail_target_import",
    "fail_nonseparation",
    "fail_topology_noncanonical",
    "fail_transition_incoherent",
    "fail_rank_incoherent",
    "fail_soldering_nonunique",
    "fail_variation_fragile",
    "bottom",
)

FORBIDDEN_KEY_FRAGMENTS = (
    "target_metric",
    "target_atlas",
    "target_topology",
    "target_open_set",
    "target_coordinate",
    "proper_time",
    "benchmark_success",
    "g_eff",
    "geff",
    "matter_coupling",
    "einstein_equation",
)

BOTTOM_CONTEXT_KEYS = {
    "authority_note",
    "bottom_if",
    "bottom_demonstrations",
    "trigger",
    "forbidden_overread",
}

ALLOWED_VARIATION_RESULTS = {
    "preserved_equivalently",
    "preserved_under_bounded_refinement",
    "bottom",
    "not_applicable",
}


class CheckerInputError(ValueError):
    """Raised when finite source-cover input cannot be parsed."""


@dataclass(frozen=True)
class Failure:
    id: str
    status: str
    check: str
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, str]:
        output = {
            "id": self.id,
            "status": self.status,
            "check": self.check,
            "message": self.message,
        }
        if self.path:
            output["path"] = self.path
        return output


@dataclass
class CheckResult:
    status: str
    checked_objects: list[str] = field(default_factory=list)
    failures: list[Failure] = field(default_factory=list)
    bottom_demonstrations_checked: int = 0
    physics_claim_authority: bool = False
    source_law_adoption_authority: bool = False
    m_src_adoption_authority: bool = False
    g_eff_authority: bool = False
    benchmark_promotion_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "checked_objects": self.checked_objects,
            "failures": [failure.to_dict() for failure in self.failures],
            "bottom_demonstrations_checked": self.bottom_demonstrations_checked,
            "physics_claim_authority": self.physics_claim_authority,
            "source_law_adoption_authority": self.source_law_adoption_authority,
            "m_src_adoption_authority": self.m_src_adoption_authority,
            "g_eff_authority": self.g_eff_authority,
            "benchmark_promotion_authority": self.benchmark_promotion_authority,
        }


def _clean_lines(text: str) -> list[tuple[int, str, int]]:
    lines: list[tuple[int, str, int]] = []
    for line_number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.strip() in {"---", "..."}:
            continue
        if "\t" in raw:
            raise CheckerInputError(f"line {line_number}: tabs are not supported")
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise CheckerInputError(f"line {line_number}: indentation must use two spaces")
        lines.append((indent, raw.strip(), line_number))
    return lines


def _parse_scalar(token: str, line_number: int) -> Any:
    token = token.strip()
    if token == "":
        return ""
    if token in {"true", "false"}:
        return token == "true"
    if token in {"null", "~"}:
        raise CheckerInputError(f"line {line_number}: null values are not supported")
    if token.startswith("["):
        try:
            return json.loads(token)
        except json.JSONDecodeError as exc:
            raise CheckerInputError(f"line {line_number}: invalid inline list") from exc
    if token.startswith('"') or token.startswith("'"):
        if not token.endswith(token[0]):
            raise CheckerInputError(f"line {line_number}: unterminated quoted scalar")
        if token[0] == "'":
            return token[1:-1]
        try:
            return json.loads(token)
        except json.JSONDecodeError as exc:
            raise CheckerInputError(f"line {line_number}: invalid quoted scalar") from exc
    return token


def _parse_key_value(text: str, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise CheckerInputError(f"line {line_number}: expected key/value pair")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key:
        raise CheckerInputError(f"line {line_number}: empty key")
    if value.startswith(" "):
        value = value[1:]
    elif value:
        raise CheckerInputError(f"line {line_number}: expected a space after ':'")
    return key, value


def _parse_block(lines: list[tuple[int, str, int]], index: int, indent: int) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    current_indent, stripped, line_number = lines[index]
    if current_indent < indent:
        return {}, index
    if current_indent > indent:
        raise CheckerInputError(f"line {line_number}: unexpected indentation")

    if stripped.startswith("- "):
        values: list[Any] = []
        while index < len(lines):
            item_indent, item_text, item_line = lines[index]
            if item_indent < indent:
                break
            if item_indent > indent:
                raise CheckerInputError(f"line {item_line}: unexpected list indentation")
            if not item_text.startswith("- "):
                break
            rest = item_text[2:].strip()
            index += 1
            if rest == "":
                child, index = _parse_block(lines, index, indent + 2)
                values.append(child)
            elif ":" in rest and not rest.startswith(("[", '"', "'")):
                key, value = _parse_key_value(rest, item_line)
                item_map: dict[str, Any] = {
                    key: _parse_scalar(value, item_line) if value else ""
                }
                if index < len(lines) and lines[index][0] == indent + 2:
                    child, index = _parse_block(lines, index, indent + 2)
                    if not isinstance(child, dict):
                        raise CheckerInputError(
                            f"line {item_line}: list item map cannot merge a list"
                        )
                    item_map.update(child)
                values.append(item_map)
            else:
                values.append(_parse_scalar(rest, item_line))
        return values, index

    values: dict[str, Any] = {}
    while index < len(lines):
        item_indent, item_text, item_line = lines[index]
        if item_indent < indent:
            break
        if item_indent > indent:
            raise CheckerInputError(f"line {item_line}: unexpected map indentation")
        if item_text.startswith("- "):
            break
        key, value = _parse_key_value(item_text, item_line)
        index += 1
        if value:
            values[key] = _parse_scalar(value, item_line)
        elif index < len(lines) and lines[index][0] > indent:
            values[key], index = _parse_block(lines, index, indent + 2)
        else:
            values[key] = ""
    return values, index


def relaxed_yaml_loads(text: str) -> dict[str, Any]:
    lines = _clean_lines(text)
    if not lines:
        return {}
    parsed, index = _parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        _, _, line_number = lines[index]
        raise CheckerInputError(f"line {line_number}: trailing unsupported content")
    if not isinstance(parsed, dict):
        raise CheckerInputError("top-level input must be a map")
    return parsed


def load_input(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    stripped = text.lstrip()
    if path.suffix == ".json" or stripped.startswith("{"):
        parsed = json.loads(text)
    else:
        try:
            parsed = strict_yaml.loads(text)
        except Exception:
            parsed = relaxed_yaml_loads(text)
    if not isinstance(parsed, dict):
        raise CheckerInputError("top-level input must be a map")
    return parsed


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_map(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _ids(items: Sequence[Any]) -> set[str]:
    return {str(item.get("id", "")).strip() for item in items if isinstance(item, dict)}


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            output.append(value)
    return output


def _failure(index: int, status: str, check: str, message: str, path: str = "") -> Failure:
    return Failure(
        id=f"{check.upper().replace('_', '-')}-{index:03d}",
        status=status,
        check=check,
        message=message,
        path=path,
    )


def _relation_signature(relation: Any) -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = []
    for item in _as_list(relation):
        if isinstance(item, (list, tuple)) and len(item) == 2:
            pairs.append((str(item[0]), str(item[1])))
    return tuple(sorted(pairs))


def _invert(relation: tuple[tuple[str, str], ...]) -> tuple[tuple[str, str], ...]:
    return tuple(sorted((right, left) for left, right in relation))


def _compose(
    left: tuple[tuple[str, str], ...], right: tuple[tuple[str, str], ...]
) -> tuple[tuple[str, str], ...] | None:
    left_map = dict(left)
    output: list[tuple[str, str]] = []
    for source, middle in right:
        if middle not in left_map:
            return None
        output.append((source, left_map[middle]))
    return tuple(sorted(output))


def check_target_import_flags(data: Mapping[str, Any]) -> list[Failure]:
    failures: list[Failure] = []

    def visit(value: Any, path: str, bottom_context: bool) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                key_text = str(key)
                child_path = f"{path}.{key_text}" if path else key_text
                child_bottom = bottom_context or key_text in BOTTOM_CONTEXT_KEYS
                key_lower = key_text.lower()
                if not child_bottom and any(fragment in key_lower for fragment in FORBIDDEN_KEY_FRAGMENTS):
                    failures.append(
                        _failure(
                            len(failures) + 1,
                            "fail_target_import",
                            "check_target_import_flags",
                            f"forbidden target or downstream authority field {key_text!r}",
                            child_path,
                        )
                    )
                visit(child, child_path, child_bottom)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]", bottom_context)

    visit(data, "", False)
    return failures


def check_sep_src(data: Mapping[str, Any]) -> list[Failure]:
    failures: list[Failure] = []
    tokens = _as_list(data.get("source_tokens"))
    token_ids = _ids(tokens)
    quotient = _as_map(data.get("quotient_support"))
    classes = _as_list(quotient.get("classes"))
    class_ids = _ids(classes)

    if not token_ids:
        failures.append(
            _failure(1, "fail_nonseparation", "check_sep_src", "source_tokens is empty")
        )
    if not class_ids:
        failures.append(
            _failure(2, "fail_nonseparation", "check_sep_src", "quotient classes are empty")
        )

    member_sets: dict[tuple[str, ...], str] = {}
    for item in classes:
        if not isinstance(item, dict):
            continue
        class_id = str(item.get("id", "")).strip()
        members = tuple(str(member) for member in _as_list(item.get("members")))
        if not members:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_nonseparation",
                    "check_sep_src",
                    f"quotient class {class_id!r} has no members",
                    f"quotient_support.classes.{class_id}",
                )
            )
        missing = [member for member in members if member not in token_ids]
        if missing:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_nonseparation",
                    "check_sep_src",
                    f"quotient class {class_id!r} references missing tokens {missing}",
                    f"quotient_support.classes.{class_id}.members",
                )
            )
        key = tuple(sorted(members))
        if key in member_sets:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_nonseparation",
                    "check_sep_src",
                    f"quotient class {class_id!r} is indistinguishable from {member_sets[key]!r}",
                    f"quotient_support.classes.{class_id}",
                )
            )
        member_sets[key] = class_id

    sep_src = _as_map(quotient.get("sep_src"))
    if str(sep_src.get("result", "")).strip() == "bottom":
        failures.append(
            _failure(
                len(failures) + 1,
                "fail_nonseparation",
                "check_sep_src",
                "sep_src result is bottom",
                "quotient_support.sep_src.result",
            )
        )
    for pair in _as_list(sep_src.get("separated_pairs")):
        left, _, right = str(pair).partition(",")
        if left and right and (left not in class_ids or right not in class_ids):
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_nonseparation",
                    "check_sep_src",
                    f"separated pair {pair!r} references unknown class",
                    "quotient_support.sep_src.separated_pairs",
                )
            )
    return failures


def check_chart_and_overlap_support(data: Mapping[str, Any]) -> list[Failure]:
    failures: list[Failure] = []
    quotient = _as_map(data.get("quotient_support"))
    class_ids = _ids(_as_list(quotient.get("classes")))
    seen_charts: set[str] = set()
    for chart in _as_list(data.get("chart_candidates")):
        if not isinstance(chart, dict):
            continue
        chart_id = str(chart.get("id", "")).strip()
        support = [str(item) for item in _as_list(chart.get("support"))]
        if not chart_id or chart_id in seen_charts:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_topology_noncanonical",
                    "check_chart_support",
                    f"chart id {chart_id!r} is blank or duplicated",
                    "chart_candidates",
                )
            )
        seen_charts.add(chart_id)
        missing = [item for item in support if item not in class_ids]
        if not support or missing:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_topology_noncanonical",
                    "check_chart_support",
                    f"chart {chart_id!r} has invalid support {missing or support}",
                    f"chart_candidates.{chart_id}.support",
                )
            )
    topreg = _as_map(_as_map(data.get("chart_support")).get("topreg_src"))
    for overlap in _as_list(topreg.get("overlaps")):
        if not isinstance(overlap, dict):
            continue
        support = [str(item) for item in _as_list(overlap.get("support"))]
        missing = [item for item in support if item not in class_ids]
        if not support or missing:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_topology_noncanonical",
                    "check_overlap_support",
                    f"overlap {overlap.get('id', '')!r} has invalid support {missing or support}",
                    f"chart_support.topreg_src.overlaps.{overlap.get('id', '')}",
                )
            )
    return failures


def check_transition_tokens(data: Mapping[str, Any]) -> list[Failure]:
    failures: list[Failure] = []
    quotient = _as_map(data.get("quotient_support"))
    class_ids = _ids(_as_list(quotient.get("classes")))
    chart_ids = _ids(_as_list(data.get("chart_candidates")))
    transitions: dict[str, dict[str, Any]] = {}
    relations: dict[str, tuple[tuple[str, str], ...]] = {}

    for token in _as_list(data.get("transition_tokens")):
        if not isinstance(token, dict):
            continue
        token_id = str(token.get("id", "")).strip()
        if not token_id or token_id in transitions:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_inverse_tokens",
                    f"transition token id {token_id!r} is blank or duplicated",
                    "transition_tokens",
                )
            )
        transitions[token_id] = token
        if token.get("source_chart") not in chart_ids or token.get("target_chart") not in chart_ids:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_inverse_tokens",
                    f"transition {token_id!r} references an unknown chart",
                    f"transition_tokens.{token_id}",
                )
            )
        relation = _relation_signature(token.get("relation"))
        relations[token_id] = relation
        if not relation:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_inverse_tokens",
                    f"transition {token_id!r} has no relation pairs",
                    f"transition_tokens.{token_id}.relation",
                )
            )
        for left, right in relation:
            if left not in class_ids or right not in class_ids:
                failures.append(
                    _failure(
                        len(failures) + 1,
                        "fail_transition_incoherent",
                        "check_inverse_tokens",
                        f"transition {token_id!r} references unknown quotient class",
                        f"transition_tokens.{token_id}.relation",
                    )
                )

    certificates = _as_map(data.get("transition_certificates"))
    inverse_re = re.compile(r"^\s*([A-Za-z0-9_./:-]+)\s+is\s+inv_src\(([A-Za-z0-9_./:-]+)\)\s*$")
    for statement in _as_list(certificates.get("inverse_checks")):
        match = inverse_re.match(str(statement))
        if not match:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_inverse_tokens",
                    f"cannot parse inverse check {statement!r}",
                    "transition_certificates.inverse_checks",
                )
            )
            continue
        inverse_id, original_id = match.groups()
        if inverse_id not in relations or original_id not in relations:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_inverse_tokens",
                    f"inverse check references missing transition {statement!r}",
                    "transition_certificates.inverse_checks",
                )
            )
            continue
        if relations[inverse_id] != _invert(relations[original_id]):
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_inverse_tokens",
                    f"{inverse_id} is not the inverse of {original_id}",
                    "transition_certificates.inverse_checks",
                )
            )

    cocycle_re = re.compile(
        r"^\s*comp_src\(([A-Za-z0-9_./:-]+),([A-Za-z0-9_./:-]+)\)=([A-Za-z0-9_./:-]+)\s*$"
    )
    for statement in _as_list(certificates.get("cocycle_checks")):
        match = cocycle_re.match(str(statement))
        if not match:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_cocycle_tokens",
                    f"cannot parse cocycle check {statement!r}",
                    "transition_certificates.cocycle_checks",
                )
            )
            continue
        left_id, right_id, expected_id = match.groups()
        if left_id not in relations or right_id not in relations or expected_id not in relations:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_cocycle_tokens",
                    f"cocycle check references missing transition {statement!r}",
                    "transition_certificates.cocycle_checks",
                )
            )
            continue
        composed = _compose(relations[left_id], relations[right_id])
        if composed != relations[expected_id]:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_transition_incoherent",
                    "check_cocycle_tokens",
                    f"composition comp_src({left_id},{right_id}) does not equal {expected_id}",
                    "transition_certificates.cocycle_checks",
                )
            )
    return failures


def check_rank_coherence(data: Mapping[str, Any]) -> list[Failure]:
    failures: list[Failure] = []
    supports = {
        str(chart.get("id", "")).strip(): _as_list(chart.get("support"))
        for chart in _as_list(data.get("chart_candidates"))
        if isinstance(chart, dict)
    }
    rank = _as_map(data.get("rank_analogue"))
    values = _as_map(rank.get("value_by_chart"))
    if values:
        for chart_id, value in values.items():
            expected = len(supports.get(str(chart_id), []))
            try:
                observed = int(value)
            except (TypeError, ValueError):
                observed = -1
            if observed != expected:
                failures.append(
                    _failure(
                        len(failures) + 1,
                        "fail_rank_incoherent",
                        "check_rank_coherence",
                        f"rank for {chart_id!r} is {value!r} but support cardinality is {expected}",
                        f"rank_analogue.value_by_chart.{chart_id}",
                    )
                )
    if rank.get("overlap_stable") is False:
        failures.append(
            _failure(
                len(failures) + 1,
                "fail_rank_incoherent",
                "check_rank_coherence",
                "rank analogue is not overlap stable",
                "rank_analogue.overlap_stable",
            )
        )
    return failures


def check_soldering_uniqueness(data: Mapping[str, Any]) -> list[Failure]:
    failures: list[Failure] = []
    class_ids = _ids(_as_list(_as_map(data.get("quotient_support")).get("classes")))
    chart_ids = _ids(_as_list(data.get("chart_candidates")))
    resp_ids = _ids(_as_list(data.get("resp_lc_tokens")))
    attachments: dict[str, set[tuple[str, ...]]] = {}
    soldering = _as_map(data.get("soldering"))
    for candidate in _as_list(soldering.get("candidates")):
        if not isinstance(candidate, dict):
            continue
        resp_token = str(candidate.get("resp_token", "")).strip()
        chart_id = str(candidate.get("chart_id", "")).strip()
        support = tuple(str(item) for item in _as_list(candidate.get("support")))
        if resp_token not in resp_ids or chart_id not in chart_ids:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_soldering_nonunique",
                    "check_soldering_uniqueness",
                    f"soldering candidate references unknown resp token or chart: {resp_token!r} {chart_id!r}",
                    "soldering.candidates",
                )
            )
        missing = [item for item in support if item not in class_ids]
        if not support or missing:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_soldering_nonunique",
                    "check_soldering_uniqueness",
                    f"soldering candidate has invalid support {missing or support}",
                    "soldering.candidates.support",
                )
            )
        attachments.setdefault(resp_token, set()).add(tuple(sorted(support)))
    for resp_token, support_set in attachments.items():
        if len(support_set) > 1:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_soldering_nonunique",
                    "check_soldering_uniqueness",
                    f"Resp token {resp_token!r} solders to incompatible source supports",
                    f"soldering.candidates.{resp_token}",
                )
            )
    return failures


def check_variation_preservation(data: Mapping[str, Any]) -> list[Failure]:
    failures: list[Failure] = []
    for variation in _as_list(data.get("finite_variations")):
        if not isinstance(variation, dict):
            continue
        variation_id = str(variation.get("id", "")).strip()
        operation = str(variation.get("operation", "")).lower()
        result = str(variation.get("result", "")).strip()
        preserved = _as_list(variation.get("preserved_objects"))
        if result not in ALLOWED_VARIATION_RESULTS:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_variation_fragile",
                    "check_variation_preservation",
                    f"variation {variation_id!r} has unsupported result {result!r}",
                    f"finite_variations.{variation_id}.result",
                )
            )
        if result != "bottom" and not preserved:
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_variation_fragile",
                    "check_variation_preservation",
                    f"variation {variation_id!r} claims preservation with no preserved objects",
                    f"finite_variations.{variation_id}.preserved_objects",
                )
            )
        if "merge" in operation and result != "bottom":
            failures.append(
                _failure(
                    len(failures) + 1,
                    "fail_variation_fragile",
                    "check_variation_preservation",
                    f"merge variation {variation_id!r} must fail closed to bottom",
                    f"finite_variations.{variation_id}.result",
                )
            )
    return failures


def check_bottom_conditions(data: Mapping[str, Any]) -> tuple[list[Failure], int]:
    failures: list[Failure] = []
    demonstrations = _as_list(data.get("bottom_demonstrations"))
    for demo in demonstrations:
        if not isinstance(demo, dict):
            continue
        if str(demo.get("result", "")).strip() != "bottom":
            failures.append(
                _failure(
                    len(failures) + 1,
                    "bottom",
                    "check_bottom_conditions",
                    f"bottom demonstration {demo.get('id', '')!r} does not fail closed",
                    "bottom_demonstrations",
                )
            )
    return failures, len(demonstrations)


def select_status(failures: Sequence[Failure]) -> str:
    if not failures:
        return "pass_candidate_local"
    statuses = {failure.status for failure in failures}
    for status in STATUS_PRIORITY:
        if status in statuses:
            return status
    return "not_applicable"


def check_finite_source_cover(data: Mapping[str, Any]) -> CheckResult:
    checked_objects = [
        "Sep_src",
        "ChartSupp_src",
        "OverlapSupp_src",
        "Inv_src",
        "Cocycle_src",
        "Rank_src",
        "Solder_src",
        "Var_reg_src",
        "NoTargetImport",
        "Bottom_src",
    ]
    failures: list[Failure] = []
    failures.extend(check_target_import_flags(data))
    failures.extend(check_sep_src(data))
    failures.extend(check_chart_and_overlap_support(data))
    failures.extend(check_transition_tokens(data))
    failures.extend(check_rank_coherence(data))
    failures.extend(check_soldering_uniqueness(data))
    failures.extend(check_variation_preservation(data))
    bottom_failures, bottom_count = check_bottom_conditions(data)
    failures.extend(bottom_failures)
    return CheckResult(
        status=select_status(failures),
        checked_objects=_dedupe(checked_objects),
        failures=failures,
        bottom_demonstrations_checked=bottom_count,
    )


def check_path(path: Path) -> CheckResult:
    return check_finite_source_cover(load_input(path))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Finite source-cover YAML or JSON input")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args(argv)
    try:
        result = check_path(args.input)
    except (CheckerInputError, strict_yaml.StrictYamlError, json.JSONDecodeError) as exc:
        print(
            json.dumps(
                {
                    "status": "not_applicable",
                    "checked_objects": [],
                    "failures": [
                        {
                            "id": "INPUT-001",
                            "status": "not_applicable",
                            "check": "parse_input",
                            "message": str(exc),
                        }
                    ],
                    "physics_claim_authority": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

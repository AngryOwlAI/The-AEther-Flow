"""Strict YAML-subset parsing and deterministic writing helpers.

This module intentionally supports only the small contract format used by the
research-control spine: maps, lists, quoted scalars, booleans, and nested
maps/lists by two-space indentation. It rejects general YAML features so
control files stay predictable and dependency-free.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class StrictYamlError(ValueError):
    """Raised when a control file uses unsupported YAML syntax."""


KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
BARE_RE = re.compile(r"^[A-Za-z0-9_./@:+-]+$")


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _clean_lines(text: str) -> list[tuple[int, str, int]]:
    output: list[tuple[int, str, int]] = []
    for line_number, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if "\t" in raw:
            raise StrictYamlError(f"line {line_number}: tabs are not allowed")
        indent = _indent_of(raw)
        if indent % 2 != 0:
            raise StrictYamlError(f"line {line_number}: indentation must use two spaces")
        stripped = raw.strip()
        output.append((indent, stripped, line_number))
    return output


def parse_scalar(token: str, line_number: int = 0) -> Any:
    token = token.strip()
    if token == "":
        return ""
    if token == "true":
        return True
    if token == "false":
        return False
    if token == "null" or token == "~":
        raise StrictYamlError(f"line {line_number}: null values are not allowed")
    if token.startswith('"') or token.startswith("'"):
        if not token.endswith(token[0]):
            raise StrictYamlError(f"line {line_number}: unterminated quoted scalar")
        if token[0] == "'":
            return token[1:-1]
        try:
            value = json.loads(token)
        except json.JSONDecodeError as exc:
            raise StrictYamlError(f"line {line_number}: invalid quoted scalar") from exc
        if not isinstance(value, str):
            raise StrictYamlError(f"line {line_number}: quoted scalar must decode to string")
        return value
    if ":" in token:
        raise StrictYamlError(f"line {line_number}: unquoted scalars cannot contain ':'")
    if not BARE_RE.fullmatch(token):
        raise StrictYamlError(f"line {line_number}: unsupported unquoted scalar")
    return token


def _parse_key_value(text: str, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise StrictYamlError(f"line {line_number}: expected key/value pair")
    key, value = text.split(":", 1)
    key = key.strip()
    if not KEY_RE.fullmatch(key):
        raise StrictYamlError(f"line {line_number}: invalid key {key!r}")
    if value.startswith(" "):
        value = value[1:]
    elif value:
        raise StrictYamlError(f"line {line_number}: expected a space after ':'")
    return key, value


def _parse_block(
    lines: list[tuple[int, str, int]], index: int, indent: int
) -> tuple[Any, int]:
    if index >= len(lines):
        return {}, index
    current_indent, stripped, line_number = lines[index]
    if current_indent < indent:
        return {}, index
    if current_indent > indent:
        raise StrictYamlError(f"line {line_number}: unexpected indentation")

    if stripped.startswith("- "):
        values: list[Any] = []
        while index < len(lines):
            item_indent, item_text, item_line = lines[index]
            if item_indent < indent:
                break
            if item_indent > indent:
                raise StrictYamlError(f"line {item_line}: unexpected list indentation")
            if not item_text.startswith("- "):
                break
            rest = item_text[2:].strip()
            index += 1
            if rest == "":
                child, index = _parse_block(lines, index, indent + 2)
                values.append(child)
            elif ":" in rest and not rest.startswith('"') and not rest.startswith("'"):
                key, value = _parse_key_value(rest, item_line)
                item_map: dict[str, Any] = {
                    key: parse_scalar(value, item_line) if value else ""
                }
                if index < len(lines) and lines[index][0] == indent + 2:
                    child, index = _parse_block(lines, index, indent + 2)
                    if not isinstance(child, dict):
                        raise StrictYamlError(
                            f"line {item_line}: list item map cannot merge a list"
                        )
                    item_map.update(child)
                values.append(item_map)
            else:
                values.append(parse_scalar(rest, item_line))
        return values, index

    values: dict[str, Any] = {}
    while index < len(lines):
        item_indent, item_text, item_line = lines[index]
        if item_indent < indent:
            break
        if item_indent > indent:
            raise StrictYamlError(f"line {item_line}: unexpected map indentation")
        if item_text.startswith("- "):
            break
        key, value = _parse_key_value(item_text, item_line)
        index += 1
        if value:
            values[key] = parse_scalar(value, item_line)
        else:
            if index < len(lines) and lines[index][0] > indent:
                values[key], index = _parse_block(lines, index, indent + 2)
            else:
                values[key] = ""
    return values, index


def loads(text: str) -> dict[str, Any]:
    lines = _clean_lines(text)
    if not lines:
        return {}
    parsed, index = _parse_block(lines, 0, lines[0][0])
    if index != len(lines):
        _, _, line_number = lines[index]
        raise StrictYamlError(f"line {line_number}: trailing unsupported content")
    if not isinstance(parsed, dict):
        raise StrictYamlError("top-level YAML value must be a map")
    return parsed


def load(path: Path) -> dict[str, Any]:
    return loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        raise StrictYamlError("missing strict frontmatter opener")
    marker = "\n---\n"
    end = text.find(marker, 4)
    if end == -1:
        raise StrictYamlError("missing strict frontmatter closer")
    frontmatter = text[4:end]
    body = text[end + len(marker) :]
    return loads(frontmatter), body


def load_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    return parse_frontmatter(path.read_text(encoding="utf-8"))


def quote_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return json.dumps(str(value), ensure_ascii=False)


def dumps(data: dict[str, Any], field_order: list[str] | None = None) -> str:
    ordered_keys = list(field_order or [])
    ordered_keys.extend(key for key in data if key not in ordered_keys)
    lines: list[str] = []

    def emit(key: str, value: Any, indent: int) -> None:
        prefix = " " * indent
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            for child_key, child_value in value.items():
                emit(child_key, child_value, indent + 2)
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"{prefix}  -")
                    for child_key, child_value in item.items():
                        emit(child_key, child_value, indent + 4)
                else:
                    lines.append(f"{prefix}  - {quote_scalar(item)}")
        else:
            lines.append(f"{prefix}{key}: {quote_scalar(value)}")

    for key in ordered_keys:
        if key in data:
            emit(key, data[key], 0)
    return "\n".join(lines) + "\n"

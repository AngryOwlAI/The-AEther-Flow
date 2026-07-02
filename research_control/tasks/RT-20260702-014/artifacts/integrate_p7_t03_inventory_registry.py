#!/usr/bin/env python3
"""Integrate P7-T03 frontier theorem inventory registry metadata."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
REGISTRY_PATH = ROOT / "registries" / "MARKDOWN_SOURCE_REGISTRY.csv"
RECEIPT_PATH = (
    ROOT
    / "research_control"
    / "tasks"
    / "RT-20260702-014"
    / "artifacts"
    / "p7_t03_frontier_theorem_inventory_registry_integration_receipt.md"
)

INVENTORY_ID = "MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY"
SCHEMA_ID = "MD-RESEARCH-CONTROL-DESIGN-FRONTIER-THEOREM-INVENTORY-SCHEMA-V1"

INVENTORY_NOTE = (
    "V12 P2-T03 populated and RT-20260701-031 synchronized the canonical "
    "Markdown frontier theorem inventory; RT-20260702-013 added explicit v14 "
    "fields and separate live-core matter-semantics/precondition rows; "
    "RT-20260702-014 crosslinked the inventory row to its schema object as "
    "control registry metadata only, not physics proof authority."
)

SCHEMA_NOTE = (
    "V12 P2-T01 frontier theorem inventory schema registered as control schema "
    "only; RT-20260702-012 reconciled explicit v14 field mapping; "
    "RT-20260702-014 preserves the schema as registry-linked control metadata "
    "and not physics authority."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def row_for(rows: list[dict[str, str]], object_id: str) -> dict[str, str]:
    for row in rows:
        if row.get("object_id") == object_id:
            return row
    raise SystemExit(f"missing registry row: {object_id}")


def main() -> int:
    pre_hash = sha256(REGISTRY_PATH)
    fieldnames, rows = read_rows(REGISTRY_PATH)

    before_inventory = dict(row_for(rows, INVENTORY_ID))
    before_schema = dict(row_for(rows, SCHEMA_ID))

    inventory = row_for(rows, INVENTORY_ID)
    schema = row_for(rows, SCHEMA_ID)

    inventory["related_source"] = SCHEMA_ID
    inventory["notes"] = INVENTORY_NOTE
    schema["notes"] = SCHEMA_NOTE

    write_rows(REGISTRY_PATH, fieldnames, rows)
    post_hash = sha256(REGISTRY_PATH)

    after_inventory = dict(row_for(read_rows(REGISTRY_PATH)[1], INVENTORY_ID))
    after_schema = dict(row_for(read_rows(REGISTRY_PATH)[1], SCHEMA_ID))

    receipt = f"""<!-- authority: control -->

# P7-T03 Frontier Theorem Inventory Registry Integration Receipt

## Result

RT-20260702-014 integrated the populated frontier theorem inventory with the
Markdown source registry.

## Registry Evidence

- Registry path: `registries/MARKDOWN_SOURCE_REGISTRY.csv`
- Pre-registry hash: `{pre_hash}`
- Post-registry hash: `{post_hash}`
- Inventory object ID: `{INVENTORY_ID}`
- Schema object ID: `{SCHEMA_ID}`
- Inventory `related_source` after integration: `{after_inventory.get('related_source', '')}`

## Row Updates

- Inventory row notes now record P7-T02 live-core population and P7-T03
  schema crosslinking.
- Schema row notes now record P7-T01 v14 field reconciliation and P7-T03
  registry-link preservation.
- Existing generated output paths remain unchanged.

## Boundary

This receipt proves registry integration only. It does not create theorem
statements, source-law adoption, `RR_ETransportCompletenessOrInvarianceLaw_v1`
adoption, `PositiveMSProfile_v1` adoption,
`SourceMatterSemanticsAdoptionReadinessLaw_v1` law adoption, matter-semantics
adoption, detector-semantics adoption, coupling-law adoption, matter-coupling
derivation or adoption, stress-energy semantics, matter action, Einstein
equations, benchmark promotion, or completed derivation.

## Machine Summary

```json
{json.dumps({
    "pre_registry_hash": pre_hash,
    "post_registry_hash": post_hash,
    "inventory_before": before_inventory,
    "inventory_after": after_inventory,
    "schema_before": before_schema,
    "schema_after": after_schema,
}, indent=2, sort_keys=True)}
```
"""
    RECEIPT_PATH.write_text(receipt, encoding="utf-8")

    print(json.dumps({
        "status": "PASS",
        "registry_path": str(REGISTRY_PATH.relative_to(ROOT)),
        "receipt_path": str(RECEIPT_PATH.relative_to(ROOT)),
        "pre_registry_hash": pre_hash,
        "post_registry_hash": post_hash,
        "inventory_related_source": after_inventory.get("related_source", ""),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

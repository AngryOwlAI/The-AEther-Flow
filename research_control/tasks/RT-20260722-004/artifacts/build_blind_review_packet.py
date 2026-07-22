#!/usr/bin/env python3
"""Build one deterministic blind-review packet and separate context manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
ARTIFACT_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = ARTIFACT_DIR / "blind_review_source_fixture.json"
DEFAULT_PACKET = ARTIFACT_DIR / "blind_review_packet_fixture.json"
DEFAULT_CONTEXT = ARTIFACT_DIR / "blind_review_context_manifest_fixture.json"


class BuildError(ValueError):
    """Raised when source binding or scientific-content checks fail."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise BuildError(f"expected object at {path}")
    return value


def _validate_manifest_shape(manifest: dict[str, Any]) -> None:
    required = {
        "schema_id",
        "packet_id",
        "review_target",
        "sources",
        "assumption_register",
        "scientific_material",
        "claim_boundary",
        "process_metadata",
    }
    if set(manifest) != required:
        raise BuildError(f"manifest keys differ: expected {sorted(required)}")
    if manifest["schema_id"] != "v21_blind_review_source_manifest_v1":
        raise BuildError("unexpected source-manifest schema")
    for field in ("sources", "assumption_register", "scientific_material", "claim_boundary"):
        if not isinstance(manifest[field], list) or not manifest[field]:
            raise BuildError(f"{field} must be a nonempty list")
    if not isinstance(manifest["process_metadata"], dict) or not manifest["process_metadata"]:
        raise BuildError("process_metadata must be a nonempty object")


def build_objects(manifest: dict[str, Any], repo_root: Path = REPO_ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    _validate_manifest_shape(manifest)

    source_map: dict[str, dict[str, str]] = {}
    context_sources: list[dict[str, str]] = []
    for source in manifest["sources"]:
        required = {"blind_source_id", "path", "sha256"}
        if not isinstance(source, dict) or set(source) != required:
            raise BuildError("each source must contain blind_source_id, path, and sha256")
        blind_id = source["blind_source_id"]
        if blind_id in source_map:
            raise BuildError(f"duplicate blind source id: {blind_id}")
        path = repo_root / source["path"]
        if not path.is_file():
            raise BuildError(f"missing source: {source['path']}")
        actual_hash = sha256_file(path)
        if actual_hash != source["sha256"]:
            raise BuildError(f"source hash mismatch: {source['path']}")
        text = path.read_text(encoding="utf-8")
        source_map[blind_id] = {"sha256": actual_hash, "text": text}
        context_sources.append(
            {
                "blind_source_id": blind_id,
                "path": source["path"],
                "sha256": actual_hash,
            }
        )

    assumptions: list[dict[str, str]] = []
    assumption_ids: set[str] = set()
    for assumption in manifest["assumption_register"]:
        if not isinstance(assumption, dict) or set(assumption) != {"assumption_id", "statement"}:
            raise BuildError("malformed assumption")
        if assumption["assumption_id"] in assumption_ids:
            raise BuildError(f"duplicate assumption: {assumption['assumption_id']}")
        assumption_ids.add(assumption["assumption_id"])
        assumptions.append(dict(assumption))

    materials: list[dict[str, Any]] = []
    material_ids: set[str] = set()
    referenced_assumptions: set[str] = set()
    for item in manifest["scientific_material"]:
        required = {"material_id", "kind", "provenance_kind", "source_id", "assumption_ids", "content"}
        if not isinstance(item, dict) or set(item) != required:
            raise BuildError("malformed scientific material")
        if item["material_id"] in material_ids:
            raise BuildError(f"duplicate material id: {item['material_id']}")
        material_ids.add(item["material_id"])
        source = source_map.get(item["source_id"])
        if source is None:
            raise BuildError(f"unknown source id: {item['source_id']}")
        if item["provenance_kind"] != "source_excerpt":
            raise BuildError("fixture scientific material must be source_excerpt")
        if item["content"] not in source["text"]:
            raise BuildError(f"source excerpt not found: {item['material_id']}")
        item_assumptions = item["assumption_ids"]
        if not isinstance(item_assumptions, list) or not item_assumptions:
            raise BuildError(f"material has no assumptions: {item['material_id']}")
        unknown = set(item_assumptions) - assumption_ids
        if unknown:
            raise BuildError(f"unknown assumptions for {item['material_id']}: {sorted(unknown)}")
        referenced_assumptions.update(item_assumptions)
        materials.append(
            {
                "assumption_ids": list(item_assumptions),
                "content": item["content"],
                "content_sha256": sha256_bytes(item["content"].encode("utf-8")),
                "kind": item["kind"],
                "material_id": item["material_id"],
                "provenance_kind": item["provenance_kind"],
                "source_id": item["source_id"],
                "source_sha256": source["sha256"],
            }
        )
    if referenced_assumptions != assumption_ids:
        missing = assumption_ids - referenced_assumptions
        raise BuildError(f"assumptions not referenced by scientific material: {sorted(missing)}")

    packet = {
        "assumption_register": assumptions,
        "claim_boundary": manifest["claim_boundary"],
        "packet_id": manifest["packet_id"],
        "review_target": {
            "scientific_scope": manifest["review_target"]["scientific_scope"],
            "source_bindings": [
                {"source_id": source["blind_source_id"], "sha256": source["sha256"]}
                for source in context_sources
            ],
            "title": manifest["review_target"]["title"],
        },
        "schema_id": "v21_blind_review_packet_v1",
        "scientific_material": materials,
    }
    packet_bytes = canonical_bytes(packet)
    process_metadata_bytes = canonical_bytes(manifest["process_metadata"])
    context = {
        "blind_packet_sha256": sha256_bytes(packet_bytes),
        "context_manifest_separate_from_packet": True,
        "packet_id": manifest["packet_id"],
        "reviewer_independence_claimed": False,
        "reviewer_not_received": {
            "process_metadata_field_names": sorted(manifest["process_metadata"]),
            "process_metadata_sha256": sha256_bytes(process_metadata_bytes),
            "source_paths_withheld": True,
        },
        "reviewer_received": {
            "assumption_ids": [item["assumption_id"] for item in assumptions],
            "claim_boundary_ids": [item["boundary_id"] for item in manifest["claim_boundary"]],
            "material_ids": [item["material_id"] for item in materials],
            "scientific_material_sha256": sha256_bytes(canonical_bytes(materials)),
            "source_bindings": context_sources,
        },
        "schema_id": "v21_blind_review_context_manifest_v1",
    }
    return packet, context


def write_objects(source_path: Path, packet_path: Path, context_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    if packet_path.resolve() == context_path.resolve():
        raise BuildError("blind packet and context manifest paths must differ")
    manifest = load_json(source_path)
    packet, context = build_objects(manifest)
    packet_path.write_bytes(canonical_bytes(packet))
    context_path.write_bytes(canonical_bytes(context))
    return packet, context


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        packet, context = write_objects(args.source, args.packet, args.context)
    except (BuildError, OSError, json.JSONDecodeError) as exc:
        result = {"status": "FAIL", "error": str(exc)}
        print(json.dumps(result, sort_keys=True) if args.json else f"FAIL: {exc}")
        return 1
    result = {
        "status": "PASS",
        "packet_path": str(args.packet),
        "packet_sha256": sha256_bytes(canonical_bytes(packet)),
        "context_path": str(args.context),
        "context_sha256": sha256_bytes(canonical_bytes(context)),
    }
    print(json.dumps(result, sort_keys=True) if args.json else "PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

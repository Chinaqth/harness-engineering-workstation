#!/usr/bin/env python3
"""Validate canonical protocol versions against Kernel contracts and source requirements."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_validation import validate_instance


CONTRACT_DOCUMENTS = {
    "domain_pack_source": (
        "config/domain-pack-sources.json",
        "schemas/domain-pack-source.schema.json",
    ),
    "task_envelope": (
        "examples/task-envelope.json",
        "schemas/task-envelope.schema.json",
    ),
    "routing_plan": (
        "examples/routing-plan.json",
        "schemas/routing-plan.schema.json",
    ),
    "task_workflow_registry": (
        "config/task-workflows.json",
        "schemas/task-workflow-registry.schema.json",
    ),
    "project_domain_overlay": (
        "examples/project-domain-overlay.json",
        "schemas/project-domain-overlay.schema.json",
    ),
}


def load_object(path: Path, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path}: top-level value must be an object")
        return {}
    return value


def schema_document_version(schema: dict) -> object:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return None
    version = properties.get("schema_version")
    return version.get("const") if isinstance(version, dict) else None


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    manifest = load_object(root / "config" / "protocol-versions.json", errors)
    manifest_schema = load_object(
        root / "schemas" / "protocol-versions.schema.json", errors
    )
    for error in validate_instance(manifest, manifest_schema):
        errors.append(f"protocol version manifest: {error}")

    contracts = manifest.get("contracts")
    if not isinstance(contracts, dict):
        return errors
    for contract_id, (document_path, schema_path) in CONTRACT_DOCUMENTS.items():
        expected = contracts.get(contract_id)
        document = load_object(root / document_path, errors)
        schema = load_object(root / schema_path, errors)
        if document.get("schema_version") != expected:
            errors.append(
                f"{contract_id}: {document_path} schema_version must equal manifest {expected!r}"
            )
        if schema_document_version(schema) != expected:
            errors.append(
                f"{contract_id}: {schema_path} schema_version const must equal manifest {expected!r}"
            )

    source_config = load_object(
        root / "config" / "domain-pack-sources.json", errors
    )
    sources = source_config.get("sources")
    if not isinstance(sources, list):
        return errors
    current_tuple = (
        manifest.get("kernel_protocol_version"),
        contracts.get("domain_pack"),
        contracts.get("domain_registry"),
    )
    compatibility = manifest.get("domain_compatibility")
    supported_tuples: list[tuple[object, object, object]] = []
    all_tuples: list[tuple[object, object, object]] = []
    if isinstance(compatibility, list):
        for item in compatibility:
            if not isinstance(item, dict):
                continue
            value = (
                item.get("kernel_protocol_version"),
                item.get("domain_pack_contract_version"),
                item.get("domain_registry_version"),
            )
            all_tuples.append(value)
            if item.get("status") == "supported":
                supported_tuples.append(value)
    if len(all_tuples) != len(set(all_tuples)):
        errors.append("protocol version manifest: compatibility tuples must be unique")
    if current_tuple not in supported_tuples:
        errors.append(
            "protocol version manifest: current Kernel/Domain tuple must be explicitly supported"
        )

    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            continue
        source_tuple = (
            source.get("required_kernel_protocol_version"),
            source.get("required_domain_pack_contract_version"),
            source.get("required_domain_registry_version"),
        )
        if source_tuple != current_tuple:
            errors.append(
                f"domain source[{index}]: required versions must equal the current manifest tuple"
            )
        if source_tuple not in supported_tuples:
            errors.append(
                f"domain source[{index}]: required compatibility tuple is not supported"
            )
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Protocol version manifest validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

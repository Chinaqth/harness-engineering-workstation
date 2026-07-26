"""Small dependency-free validator for the JSON Schema keywords used by this repository."""

from __future__ import annotations

import json
import re
from typing import Any


def _matches_type(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def validate_instance(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    errors: list[str] = []
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: must equal {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: must be one of {schema['enum']!r}")

    expected_type = schema.get("type")
    if expected_type and not _matches_type(value, expected_type):
        errors.append(f"{path}: must be {expected_type}")
        return errors

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: must contain at least {schema['minLength']} character(s)")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, value) is None:
            errors.append(f"{path}: does not match required pattern")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: must be at least {schema['minimum']}")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: must contain at least {schema['minItems']} item(s)")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path}: items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                errors.extend(validate_instance(item, item_schema, f"{path}[{index}]"))

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}: missing required property {required!r}")
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{path}: unexpected property {key!r}")
        for key, child_schema in properties.items():
            if key in value:
                errors.extend(validate_instance(value[key], child_schema, f"{path}.{key}"))
    return errors

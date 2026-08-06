from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_protocol_versions.py"
SPEC = importlib.util.spec_from_file_location("validate_protocol_versions", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class ProtocolVersionValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "config", self.root / "config")
        shutil.copytree(ROOT / "examples", self.root / "examples")
        shutil.copytree(ROOT / "schemas", self.root / "schemas")

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def save(path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def test_repository_contract_versions_are_consistent(self) -> None:
        self.assertEqual(MODULE.validate(self.root), [])

    def test_document_version_drift_is_rejected(self) -> None:
        path = self.root / "examples" / "task-envelope.json"
        document = self.load(path)
        document["schema_version"] = "1.0"
        self.save(path, document)
        errors = MODULE.validate(self.root)
        self.assertTrue(any("task_envelope" in error for error in errors))

    def test_schema_const_drift_is_rejected(self) -> None:
        path = self.root / "schemas" / "routing-plan.schema.json"
        schema = self.load(path)
        schema["properties"]["schema_version"]["const"] = "1.0"
        self.save(path, schema)
        errors = MODULE.validate(self.root)
        self.assertTrue(any("routing_plan" in error for error in errors))

    def test_current_tuple_must_be_supported(self) -> None:
        path = self.root / "config" / "protocol-versions.json"
        manifest = self.load(path)
        manifest["domain_compatibility"][0]["status"] = "deprecated"
        self.save(path, manifest)
        errors = MODULE.validate(self.root)
        self.assertTrue(any("must be explicitly supported" in error for error in errors))

    def test_domain_source_requirements_must_match_manifest(self) -> None:
        path = self.root / "config" / "domain-pack-sources.json"
        source = self.load(path)
        source["sources"][0]["required_domain_pack_contract_version"] = "2.0"
        self.save(path, source)
        errors = MODULE.validate(self.root)
        self.assertTrue(any("must equal the current manifest tuple" in error for error in errors))

    def test_compatibility_tuples_must_be_unique(self) -> None:
        path = self.root / "config" / "protocol-versions.json"
        manifest = self.load(path)
        manifest["domain_compatibility"].append(
            dict(manifest["domain_compatibility"][0])
        )
        self.save(path, manifest)
        errors = MODULE.validate(self.root)
        self.assertTrue(any("must be unique" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

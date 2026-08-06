from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_domain_source.py"
SPEC = importlib.util.spec_from_file_location("validate_domain_source", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class DomainSourceValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.kernel = self.base / "kernel"
        self.domain = self.base / "domain-packs"
        (self.kernel / "config").mkdir(parents=True)
        (self.domain / "registry").mkdir(parents=True)
        self.pack = self.domain / "domains" / "engineering" / "web"
        for directory in ("workflows", "skills/web-delivery", "evaluators"):
            (self.pack / directory).mkdir(parents=True, exist_ok=True)

        self.write_json(
            self.domain / "registry" / "domains.json",
            {
                "schema_version": "1.0",
                "domains": [
                    {
                        "id": "engineering.web",
                        "path": "domains/engineering/web",
                        "version": "1.0.0",
                        "status": "active",
                        "owner": "web-team",
                    }
                ],
            },
        )
        self.write_json(
            self.pack / "domain.json",
            {
                "schema_version": "1.0",
                "id": "engineering.web",
                "display_name": "Web Engineering",
                "description": "Test fixture.",
                "version": "1.0.0",
                "status": "active",
                "owner": "web-team",
                "inherits": [],
                "applicability": {"task_types": ["web-change"], "repository_signals": ["html"]},
                "compatibility": {
                    "kernel_protocol_version": "1.0",
                    "statement": "Compatible fixture.",
                },
                "activation": {"evidence": ["fixture"]},
            },
        )
        self.write_json(
            self.pack / "routes.json",
            {
                "schema_version": "1.0",
                "domain_id": "engineering.web",
                "routes": [
                    {
                        "id": "web-change",
                        "priority": 100,
                        "task_types": ["web-change"],
                        "signals": ["html"],
                        "capabilities": ["web-engineering"],
                    }
                ],
            },
        )
        self.write_json(
            self.pack / "capabilities.json",
            {
                "schema_version": "1.0",
                "domain_id": "engineering.web",
                "capabilities": [
                    {
                        "id": "web-engineering",
                        "description": "Reusable Web engineering.",
                        "task_types": ["web-change"],
                        "workflows": ["WORKFLOW.md"],
                        "skills": ["web-delivery"],
                        "tools": [],
                        "evaluators": ["EVALUATOR.md"],
                        "permissions": [],
                        "dependencies": [],
                    }
                ],
            },
        )
        self.write_json(
            self.pack / "owners.json",
            {
                "schema_version": "1.0",
                "domain_id": "engineering.web",
                "primary_owner": "web-team",
                "reviewers": [],
            },
        )
        (self.pack / "workflows" / "WORKFLOW.md").write_text("# Workflow\n", encoding="utf-8")
        (self.pack / "skills" / "web-delivery" / "SKILL.md").write_text(
            "# Skill\n", encoding="utf-8"
        )
        (self.pack / "evaluators" / "EVALUATOR.md").write_text(
            "# Evaluator\n", encoding="utf-8"
        )
        self.git("init", "-b", "main")
        self.git("config", "user.email", "fixture@example.com")
        self.git("config", "user.name", "Fixture")
        self.git("remote", "add", "origin", "git@github.com:example/domain-packs.git")
        self.revision = self.commit("fixture")
        self.write_source_config(self.revision)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.domain), *args],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    @staticmethod
    def write_json(path: Path, value: dict) -> None:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def write_source_config(
        self,
        revision: str,
        repository: str = "git@github.com:example/domain-packs.git",
        protocol: str = "1.0",
    ) -> None:
        self.write_json(
            self.kernel / "config" / "domain-pack-sources.json",
            {
                "schema_version": "2.0",
                "sources": [
                    {
                        "id": "fixture",
                        "repository": repository,
                        "ref": revision,
                        "registry": "registry/domains.json",
                        "required_kernel_protocol_version": protocol,
                        "required_domain_pack_contract_version": "1.0",
                        "required_domain_registry_version": "1.0",
                    }
                ],
                "runtime": {
                    "domain_root": "fixture",
                    "global_skill_root": "fixture",
                    "project_overlay": "fixture",
                },
            },
        )

    def errors(self) -> list[str]:
        return MODULE.validate(self.kernel, self.domain)

    def test_valid_pinned_source_passes(self) -> None:
        self.assertEqual(self.errors(), [])

    def test_absent_pinned_revision_is_rejected(self) -> None:
        self.write_source_config("0" * 40)
        self.assertTrue(any("revision is absent" in error for error in self.errors()))

    def test_repository_identity_mismatch_is_rejected(self) -> None:
        self.write_source_config(
            self.revision, repository="git@github.com:other/domain-packs.git"
        )
        self.assertTrue(any("origin does not match" in error for error in self.errors()))

    def test_protocol_mismatch_is_rejected(self) -> None:
        self.write_source_config(self.revision, protocol="2.0")
        self.assertTrue(any("required '2.0'" in error for error in self.errors()))

    def test_missing_skill_at_pinned_revision_is_rejected(self) -> None:
        (self.pack / "skills" / "web-delivery" / "SKILL.md").unlink()
        revision = self.commit("remove skill")
        self.write_source_config(revision)
        self.assertTrue(any("missing" in error and "SKILL.md" in error for error in self.errors()))

    def test_unknown_route_capability_is_rejected(self) -> None:
        routes_path = self.pack / "routes.json"
        routes = json.loads(routes_path.read_text(encoding="utf-8"))
        routes["routes"][0]["capabilities"] = ["task-specific-fix"]
        self.write_json(routes_path, routes)
        revision = self.commit("break route")
        self.write_source_config(revision)
        self.assertTrue(any("unknown capability" in error for error in self.errors()))

    def test_registry_manifest_identity_mismatch_is_rejected(self) -> None:
        manifest_path = self.pack / "domain.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["version"] = "2.0.0"
        self.write_json(manifest_path, manifest)
        revision = self.commit("break manifest identity")
        self.write_source_config(revision)
        self.assertTrue(
            any("Registry and Manifest disagree on version" in error for error in self.errors())
        )

    def test_unknown_capability_dependency_is_rejected(self) -> None:
        capabilities_path = self.pack / "capabilities.json"
        capabilities = json.loads(capabilities_path.read_text(encoding="utf-8"))
        capabilities["capabilities"][0]["dependencies"] = ["missing-capability"]
        self.write_json(capabilities_path, capabilities)
        revision = self.commit("break dependency")
        self.write_source_config(revision)
        self.assertTrue(any("unknown dependency" in error for error in self.errors()))

    def test_dirty_working_tree_does_not_change_pinned_evidence(self) -> None:
        (self.pack / "skills" / "web-delivery" / "SKILL.md").unlink()
        self.assertEqual(self.errors(), [])


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sync_domain_pin.py"


class DomainPinSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.kernel = self.base / "kernel"
        self.domain = self.base / "domain-packs"
        self.origin = self.base / "origin.git"
        (self.kernel / "config").mkdir(parents=True)
        (self.kernel / "examples").mkdir(parents=True)
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

        subprocess.run(
            ["git", "init", "--bare", "-b", "main", str(self.origin)],
            check=True,
            capture_output=True,
        )
        self.git("init", "-b", "main")
        self.git("config", "user.email", "fixture@example.com")
        self.git("config", "user.name", "Fixture")
        self.git("remote", "add", "origin", str(self.origin))
        self.revision = self.commit("fixture")
        self.git("push", "-u", "origin", "main")
        self.git("remote", "set-head", "origin", "main")
        self.write_source_config(self.revision)
        self.write_routing_example(self.revision)

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

    def write_source_config(self, revision: str) -> None:
        self.write_json(
            self.kernel / "config" / "domain-pack-sources.json",
            {
                "schema_version": "2.0",
                "sources": [
                    {
                        "id": "fixture",
                        "repository": str(self.origin),
                        "ref": revision,
                        "registry": "registry/domains.json",
                        "required_kernel_protocol_version": "1.0",
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

    def write_routing_example(self, revision: str) -> None:
        self.write_json(
            self.kernel / "examples" / "routing-plan.json",
            {
                "schema_version": "2.0",
                "task_id": "fixture",
                "source": {
                    "source_id": "fixture",
                    "repository": str(self.origin),
                    "revision": revision,
                    "registry": "registry/domains.json",
                },
            },
        )

    def config_ref(self) -> str:
        config = json.loads(
            (self.kernel / "config" / "domain-pack-sources.json").read_text(
                encoding="utf-8"
            )
        )
        return config["sources"][0]["ref"]

    def example_revision(self) -> str:
        example = json.loads(
            (self.kernel / "examples" / "routing-plan.json").read_text(encoding="utf-8")
        )
        return example["source"]["revision"]

    def run_sync(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                str(self.kernel),
                "--domain-root",
                str(self.domain),
                *args,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    def test_valid_candidate_updates_pin_and_example(self) -> None:
        (self.pack / "workflows" / "WORKFLOW.md").write_text(
            "# Workflow v2\n", encoding="utf-8"
        )
        revision = self.commit("update workflow")
        self.git("push", "origin", "main")

        result = self.run_sync("--no-fetch")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(self.config_ref(), revision)
        self.assertEqual(self.example_revision(), revision)
        self.assertIn("1 new commit(s)", result.stdout)

    def test_invalid_candidate_leaves_files_untouched(self) -> None:
        (self.pack / "skills" / "web-delivery" / "SKILL.md").unlink()
        self.commit("remove skill")
        self.git("push", "origin", "main")

        result = self.run_sync("--no-fetch")
        self.assertEqual(result.returncode, 1)
        self.assertIn("left unchanged", result.stdout)
        self.assertEqual(self.config_ref(), self.revision)
        self.assertEqual(self.example_revision(), self.revision)

    def test_current_pin_is_noop(self) -> None:
        result = self.run_sync("--no-fetch")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("nothing to do", result.stdout)
        self.assertEqual(self.config_ref(), self.revision)

    def test_dry_run_validates_without_writing(self) -> None:
        (self.pack / "workflows" / "WORKFLOW.md").write_text(
            "# Workflow v2\n", encoding="utf-8"
        )
        self.commit("update workflow")
        self.git("push", "origin", "main")

        result = self.run_sync("--no-fetch", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertIn("would update", result.stdout)
        self.assertEqual(self.config_ref(), self.revision)
        self.assertEqual(self.example_revision(), self.revision)

    def test_fetch_path_picks_up_pushed_commits(self) -> None:
        (self.pack / "workflows" / "WORKFLOW.md").write_text(
            "# Workflow v2\n", encoding="utf-8"
        )
        revision = self.commit("update workflow")
        self.git("push", "origin", "main")
        # Rewind the local remote-tracking ref to simulate a stale checkout.
        self.git("update-ref", "refs/remotes/origin/main", self.revision)

        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(self.config_ref(), revision)


if __name__ == "__main__":
    unittest.main()

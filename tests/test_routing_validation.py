from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_routing.py"
SPEC = importlib.util.spec_from_file_location("validate_routing", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class RoutingValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "config", self.root / "config")
        shutil.copytree(ROOT / "examples", self.root / "examples")
        shutil.copytree(ROOT / "schemas", self.root / "schemas")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def plan(self) -> tuple[Path, dict]:
        path = self.root / "examples" / "routing-plan.json"
        return path, json.loads(path.read_text(encoding="utf-8"))

    def save_plan(self, path: Path, plan: dict) -> list[str]:
        path.write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
        return MODULE.validate(self.root)

    def selection(self) -> dict:
        return {
            "domain_id": "engineering.ios",
            "version": "1.0.0",
            "route_id": "feature",
            "capability_ids": ["delivery"],
            "workflows": ["WORKFLOW.md"],
            "skills": [],
            "tools": [],
            "evaluators": ["EVALUATOR.md"],
            "permissions": ["repository:write"],
            "reason": "The task and repository signals match.",
        }

    def test_repository_examples_are_valid(self) -> None:
        self.assertEqual(MODULE.validate(self.root), [])

    def test_routed_plan_passes_with_complete_selection(self) -> None:
        path, plan = self.plan()
        plan.update(
            {
                "status": "routed",
                "selections": [self.selection()],
                "approvals": [],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        self.assertEqual(self.save_plan(path, plan), [])

    def test_contradictory_states_are_rejected(self) -> None:
        cases = {
            "unroutable with selection": {
                "status": "unroutable",
                "selections": [self.selection()],
                "approvals": [],
                "conflicts": ["No compatible Pack."],
                "missing_inputs": [],
            },
            "routed with conflict": {
                "status": "routed",
                "selections": [self.selection()],
                "approvals": [],
                "conflicts": ["Unresolved conflict."],
                "missing_inputs": [],
            },
            "needs approval without approval": {
                "status": "needs_approval",
                "selections": [self.selection()],
                "approvals": [],
                "conflicts": [],
                "missing_inputs": [],
            },
            "needs input without missing input": {
                "status": "needs_input",
                "selections": [],
                "approvals": [],
                "conflicts": [],
                "missing_inputs": [],
            },
        }
        for label, state in cases.items():
            with self.subTest(label=label):
                path, plan = self.plan()
                plan.update(state)
                self.assertTrue(self.save_plan(path, plan))

    def test_empty_selection_identifiers_are_rejected_by_schema(self) -> None:
        path, plan = self.plan()
        selection = self.selection()
        selection.update(
            {
                "domain_id": "",
                "version": "",
                "route_id": "",
                "capability_ids": [""],
            }
        )
        plan.update(
            {
                "status": "routed",
                "selections": [selection],
                "approvals": [],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("routing plan: $" in error for error in errors))

    def test_domain_id_must_match_domain_identity_contract(self) -> None:
        path, plan = self.plan()
        selection = self.selection()
        selection["domain_id"] = "INVALID DOMAIN"
        plan.update(
            {
                "status": "routed",
                "selections": [selection],
                "approvals": [],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("required pattern" in error for error in errors))

    def test_plan_must_reference_same_task(self) -> None:
        path, plan = self.plan()
        plan["task_id"] = "other-task"
        self.assertTrue(
            any("must match" in error for error in self.save_plan(path, plan))
        )

    def test_source_revision_must_be_immutable_and_match_config(self) -> None:
        path, plan = self.plan()
        plan["source"]["revision"] = "main"
        errors = self.save_plan(path, plan)
        self.assertTrue(any("required pattern" in error for error in errors))
        self.assertTrue(any("must match configured ref" in error for error in errors))

    def test_overlay_supports_mappings_and_disabled_capabilities(self) -> None:
        path = self.root / "examples" / "project-domain-overlay.json"
        overlay = {
            "schema_version": "1.0",
            "domains": [
                {
                    "id": "engineering.ios",
                    "version": "1.0.0",
                    "enabled": True,
                    "local_owner": "mobile-team",
                    "additional_signals": ["swift"],
                    "constraints": ["Use project signing policy."],
                    "disabled_capabilities": ["legacy-release"],
                    "mappings": [
                        {
                            "capability_id": "delivery",
                            "project_paths": ["ios/"],
                            "commands": ["make test-ios"],
                        }
                    ],
                }
            ],
        }
        path.write_text(json.dumps(overlay, indent=2) + "\n", encoding="utf-8")
        self.assertEqual(MODULE.validate(self.root), [])


if __name__ == "__main__":
    unittest.main()

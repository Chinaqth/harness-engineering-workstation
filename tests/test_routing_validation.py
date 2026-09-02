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
            "skills": [
                {
                    "skill_id": "ios-change-delivery",
                    "capability_id": "delivery",
                    "source_path": "skills/ios-change-delivery/SKILL.md",
                    "reuse_scope": "domain",
                }
            ],
            "tools": [],
            "evaluators": ["EVALUATOR.md"],
            "permissions": ["repository:write"],
            "reason": "The task and repository signals match.",
        }

    def gate(self, plan: dict, status: str = "pending") -> dict:
        return {
            "gate_id": "implementation-approval",
            "kind": "implementation",
            "required_role": "task-owner",
            "status": status,
            "scope": ["Approved implementation plan"],
            "scope_fingerprint": plan["scope_fingerprint"],
            "evidence": [] if status == "pending" else ["Owner decision record"],
        }

    def execution_plan(self, status: str = "presented") -> dict:
        return {
            "required": True,
            "status": status,
            "artifact": None if status == "missing" else "changes/example/task.md",
            "sha256": None if status == "missing" else f"sha256:{'a' * 64}",
            "domain_ids": ["engineering.ios"],
            "presentation_evidence": [] if status != "presented" else ["User-visible Markdown plan"],
        }

    def overlay_domain(self) -> dict:
        return {
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

    def test_repository_examples_are_valid(self) -> None:
        self.assertEqual(MODULE.validate(self.root), [])

    def test_routed_plan_passes_with_complete_selection(self) -> None:
        path, plan = self.plan()
        plan.update(
            {
                "status": "routed",
                "execution_mode": "domain_augmented",
                "execution_plan": self.execution_plan(),
                "fallbacks": [],
                "selections": [self.selection()],
                "approval_gates": [self.gate(plan, "approved")],
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
                "approval_gates": [],
                "conflicts": ["No compatible Pack."],
                "missing_inputs": [],
            },
            "routed with conflict": {
                "status": "routed",
                "selections": [self.selection()],
                "approval_gates": [],
                "conflicts": ["Unresolved conflict."],
                "missing_inputs": [],
            },
            "needs approval without approval": {
                "status": "needs_approval",
                "selections": [self.selection()],
                "approval_gates": [],
                "conflicts": [],
                "missing_inputs": [],
            },
            "needs input without missing input": {
                "status": "needs_input",
                "selections": [],
                "approval_gates": [],
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
                "approval_gates": [],
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
                "approval_gates": [],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("required pattern" in error for error in errors))

    def test_pending_approval_gate_requires_needs_approval_status(self) -> None:
        path, plan = self.plan()
        plan.update(
            {
                "status": "needs_approval",
                "execution_mode": "domain_augmented",
                "execution_plan": self.execution_plan("missing"),
                "fallbacks": [],
                "selections": [self.selection()],
                "approval_gates": [self.gate(plan)],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        self.assertEqual(self.save_plan(path, plan), [])

        plan["status"] = "routed"
        errors = self.save_plan(path, plan)
        self.assertTrue(any("requires every gate approved" in error for error in errors))

    def test_domain_implementation_decision_requires_presented_execution_plan(self) -> None:
        path, plan = self.plan()
        plan.update(
            {
                "status": "routed",
                "execution_mode": "domain_augmented",
                "execution_plan": self.execution_plan("draft"),
                "fallbacks": [],
                "selections": [self.selection()],
                "approval_gates": [self.gate(plan, "approved")],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("requires the current execution plan to be presented" in error for error in errors))

    def test_domain_execution_plan_covers_every_selected_domain(self) -> None:
        path, plan = self.plan()
        execution_plan = self.execution_plan("missing")
        execution_plan["domain_ids"] = []
        plan.update(
            {
                "status": "needs_approval",
                "execution_mode": "domain_augmented",
                "execution_plan": execution_plan,
                "fallbacks": [],
                "selections": [self.selection()],
                "approval_gates": [self.gate(plan)],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("cover every selected Domain" in error for error in errors))

    def test_integrated_execution_plan_can_cover_multiple_domains(self) -> None:
        path, plan = self.plan()
        second = json.loads(json.dumps(self.selection()))
        second["domain_id"] = "engineering.security"
        execution_plan = self.execution_plan()
        execution_plan["domain_ids"] = ["engineering.ios", "engineering.security"]
        plan.update(
            {
                "status": "routed",
                "execution_mode": "domain_augmented",
                "execution_plan": execution_plan,
                "fallbacks": [],
                "selections": [self.selection(), second],
                "approval_gates": [self.gate(plan, "approved")],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        self.assertEqual(self.save_plan(path, plan), [])

    def test_mutating_domain_route_cannot_mark_execution_plan_not_required(self) -> None:
        path, plan = self.plan()
        plan.update(
            {
                "status": "needs_approval",
                "execution_mode": "domain_augmented",
                "execution_plan": {
                    "required": False,
                    "status": "not-required",
                    "artifact": None,
                    "sha256": None,
                    "domain_ids": [],
                    "presentation_evidence": [],
                },
                "fallbacks": [],
                "selections": [self.selection()],
                "approval_gates": [self.gate(plan)],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("requires a Domain execution plan" in error for error in errors))

    def test_mutating_workflow_requires_implementation_approval(self) -> None:
        path, plan = self.plan()
        plan.update(
            {
                "status": "routed",
                "selections": [self.selection()],
                "approval_gates": [],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("require an implementation approval gate" in error for error in errors))

    def test_approved_gate_requires_evidence(self) -> None:
        path, plan = self.plan()
        gate = self.gate(plan, "approved")
        gate["evidence"] = []
        plan.update(
            {
                "status": "routed",
                "selections": [self.selection()],
                "approval_gates": [gate],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("require decision evidence" in error for error in errors))

    def test_approval_gate_must_bind_to_current_scope(self) -> None:
        path, plan = self.plan()
        gate = self.gate(plan, "approved")
        gate["scope_fingerprint"] = f"sha256:{'b' * 64}"
        plan.update(
            {
                "status": "routed",
                "selections": [self.selection()],
                "approval_gates": [gate],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("bind to the current scope fingerprint" in error for error in errors))

    def test_workflow_must_be_registered_for_task_class(self) -> None:
        path, plan = self.plan()
        plan["workflow_selection"]["workflow_id"] = "task.feature-delivery"
        errors = self.save_plan(path, plan)
        self.assertTrue(any("must declare the Task Envelope task class" in error for error in errors))

    def test_workflow_registry_task_classes_are_unambiguous(self) -> None:
        registry_path = self.root / "config" / "task-workflows.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        registry["workflows"][0]["task_classes"].append("defect")
        registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
        errors = MODULE.validate(self.root)
        self.assertTrue(any("exactly one workflow" in error for error in errors))

    def test_skill_binding_must_be_domain_reusable_and_capability_bound(self) -> None:
        path, plan = self.plan()
        selection = self.selection()
        selection["skills"][0]["reuse_scope"] = "task"
        plan.update(
            {
                "status": "routed",
                "selections": [selection],
                "approval_gates": [],
                "conflicts": [],
                "missing_inputs": [],
            }
        )
        errors = self.save_plan(path, plan)
        self.assertTrue(any("reuse_scope" in error for error in errors))

        selection["skills"][0]["reuse_scope"] = "domain"
        selection["skills"][0]["capability_id"] = "login-timeout-spinner-fix"
        errors = self.save_plan(path, plan)
        self.assertTrue(any("must bind to a selected capability" in error for error in errors))

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
            "domains": [self.overlay_domain()],
        }
        path.write_text(json.dumps(overlay, indent=2) + "\n", encoding="utf-8")
        self.assertEqual(MODULE.validate(self.root), [])

    def test_overlay_domain_id_must_match_domain_identity_contract(self) -> None:
        path = self.root / "examples" / "project-domain-overlay.json"
        overlay = {
            "schema_version": "1.0",
            "domains": [self.overlay_domain()],
        }
        overlay["domains"][0]["id"] = "INVALID DOMAIN"
        path.write_text(json.dumps(overlay, indent=2) + "\n", encoding="utf-8")
        errors = MODULE.validate(self.root)
        self.assertTrue(any("required pattern" in error for error in errors))

    def test_overlay_domain_ids_must_be_unique(self) -> None:
        path = self.root / "examples" / "project-domain-overlay.json"
        domain = self.overlay_domain()
        duplicate = dict(domain)
        duplicate.update(
            {
                "version": "2.0.0",
                "enabled": not domain["enabled"],
                "local_owner": "conflicting-team",
            }
        )
        overlay = {
            "schema_version": "1.0",
            "domains": [domain, duplicate],
        }
        path.write_text(json.dumps(overlay, indent=2) + "\n", encoding="utf-8")
        errors = MODULE.validate(self.root)
        self.assertTrue(any("Domain IDs must be unique" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

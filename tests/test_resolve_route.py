from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "resolve_route.py"
SPEC = importlib.util.spec_from_file_location("resolve_route", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

ROUTING_SPEC = importlib.util.spec_from_file_location(
    "validate_routing", ROOT / "scripts" / "validate_routing.py"
)
assert ROUTING_SPEC and ROUTING_SPEC.loader
ROUTING_MODULE = importlib.util.module_from_spec(ROUTING_SPEC)
ROUTING_SPEC.loader.exec_module(ROUTING_MODULE)

SCHEMA_SPEC = importlib.util.spec_from_file_location(
    "schema_validation", ROOT / "scripts" / "schema_validation.py"
)
assert SCHEMA_SPEC and SCHEMA_SPEC.loader
SCHEMA_MODULE = importlib.util.module_from_spec(SCHEMA_SPEC)
SCHEMA_SPEC.loader.exec_module(SCHEMA_MODULE)

PLAN_SCHEMA = json.loads(
    (ROOT / "schemas" / "routing-plan.schema.json").read_text(encoding="utf-8")
)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


class ResolveRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.kernel = self.base / "kernel"
        self.domain = self.base / "domain-packs"
        (self.kernel / "config").mkdir(parents=True)
        (self.kernel / "schemas").mkdir(parents=True)
        (self.domain / "registry").mkdir(parents=True)

        for schema in (
            "task-envelope.schema.json",
            "project-domain-overlay.schema.json",
            "approval-decisions.schema.json",
        ):
            (self.kernel / "schemas" / schema).write_text(
                (ROOT / "schemas" / schema).read_text(encoding="utf-8"),
                encoding="utf-8",
            )

        write_json(
            self.kernel / "config" / "task-workflows.json",
            {
                "schema_version": "1.0",
                "workflows": [
                    {
                        "id": "task.defect-remediation",
                        "version": "1.0.0",
                        "description": "Defect fixture.",
                        "task_classes": ["defect"],
                        "governing_workflow": "workflows/3-plus-1.md",
                        "stages": ["assess", "propose", "approve"],
                        "approval_policy": "always-before-implementation",
                    },
                    {
                        "id": "task.investigation",
                        "version": "1.0.0",
                        "description": "Investigation fixture.",
                        "task_classes": ["investigation"],
                        "governing_workflow": "workflows/3-plus-1.md",
                        "stages": ["assess"],
                        "approval_policy": "risk-proportional",
                    },
                ],
            },
        )
        self.revision = self.build_domain_repo()
        write_json(
            self.kernel / "config" / "domain-pack-sources.json",
            {
                "schema_version": "2.0",
                "sources": [
                    {
                        "id": "test-source",
                        "repository": "https://example.test/domain-packs.git",
                        "ref": self.revision,
                        "registry": "registry/domains.json",
                        "required_kernel_protocol_version": "1.0",
                        "required_domain_pack_contract_version": "1.0",
                        "required_domain_registry_version": "1.0",
                    }
                ],
            },
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def build_domain_repo(self, skill_present: bool = True) -> str:
        pack = self.domain / "domains" / "engineering" / "web"
        for directory in ("workflows", "evaluators", "skills/web-delivery"):
            (pack / directory).mkdir(parents=True, exist_ok=True)
        (pack / "workflows" / "WORKFLOW.md").write_text("# Workflow\n", encoding="utf-8")
        (pack / "evaluators" / "EVALUATOR.md").write_text("# Evaluator\n", encoding="utf-8")
        if skill_present:
            (pack / "skills" / "web-delivery" / "SKILL.md").write_text(
                "# Skill\n", encoding="utf-8"
            )
        write_json(
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
        write_json(
            pack / "domain.json",
            {
                "schema_version": "1.0",
                "id": "engineering.web",
                "applicability": {
                    "task_types": ["web-change"],
                    "repository_signals": ["html"],
                },
            },
        )
        write_json(
            pack / "routes.json",
            {
                "schema_version": "1.0",
                "domain_id": "engineering.web",
                "routes": [
                    {
                        "id": "web-delivery-route",
                        "priority": 500,
                        "task_types": ["web-change"],
                        "signals": ["html"],
                        "capabilities": ["web-delivery"],
                    }
                ],
            },
        )
        write_json(
            pack / "capabilities.json",
            {
                "schema_version": "1.0",
                "domain_id": "engineering.web",
                "capabilities": [
                    {
                        "id": "web-delivery",
                        "description": "Fixture capability.",
                        "task_types": ["web-change"],
                        "workflows": ["WORKFLOW.md"],
                        "skills": ["web-delivery"],
                        "tools": ["browser inspection"],
                        "evaluators": ["EVALUATOR.md"],
                        "permissions": ["task-scoped source modification"],
                        "dependencies": [],
                    }
                ],
            },
        )
        subprocess.run(["git", "-C", str(self.domain), "init"], check=True, capture_output=True)
        subprocess.run(
            ["git", "-C", str(self.domain), "add", "."], check=True, capture_output=True
        )
        subprocess.run(
            [
                "git", "-C", str(self.domain),
                "-c", "user.name=test", "-c", "user.email=test@test",
                "commit", "-m", "fixture",
            ],
            check=True,
            capture_output=True,
        )
        result = subprocess.run(
            ["git", "-C", str(self.domain), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def envelope(self, **overrides) -> dict:
        value = {
            "schema_version": "2.0",
            "task_id": "test-task",
            "intent": "Exercise the resolver.",
            "task_class": "defect",
            "task_type": "web-change",
            "operation": "modify",
            "deliverables": ["repair"],
            "constraints": [],
            "repository_signals": ["html"],
            "affected_surfaces": ["login page"],
            "expected_behavior": ["timeout ends loading"],
            "required_evidence": ["unit tests"],
        }
        value.update(overrides)
        return value

    def run_resolver(self, envelope: dict, *extra: str) -> subprocess.CompletedProcess[str]:
        envelope_path = self.base / "envelope.json"
        write_json(envelope_path, envelope)
        return subprocess.run(
            [
                "python3",
                str(SCRIPT),
                str(envelope_path),
                "--root",
                str(self.kernel),
                "--domain-root",
                str(self.domain),
                *extra,
            ],
            capture_output=True,
            text=True,
        )

    def execution_plan(self, content: str = "# Domain execution plan\n\n1. Repair the login state.\n") -> Path:
        path = self.base / "project" / "changes" / "test-task" / "task.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    @staticmethod
    def presented_plan(plan: dict) -> dict:
        execution_plan = plan["execution_plan"]
        return {
            "artifact": execution_plan["artifact"],
            "sha256": execution_plan["sha256"],
            "evidence": [
                {
                    "evidence_type": "user-visible-markdown",
                    "issuer": "platform-adapter",
                    "channel": "test",
                    "reference": "message:plan-presentation",
                    "recorded_at": "2026-09-02T00:00:00Z",
                    "plan_sha256": execution_plan["sha256"],
                }
            ],
        }

    @staticmethod
    def decision_evidence(plan: dict, reference: str = "message:owner-decision") -> list[dict]:
        return [
            {
                "evidence_type": "explicit-user-decision",
                "actor_role": "Owner",
                "actor_id": "user:test-owner",
                "channel": "test",
                "reference": reference,
                "recorded_at": "2026-09-02T00:00:01Z",
                "scope_fingerprint": plan["scope_fingerprint"],
            }
        ]

    def parse_plan(self, result: subprocess.CompletedProcess[str]) -> dict:
        self.assertEqual(result.returncode, 0, result.stderr)
        plan = json.loads(result.stdout)
        schema_errors = SCHEMA_MODULE.validate_instance(plan, PLAN_SCHEMA)
        self.assertEqual(schema_errors, [])
        state_errors: list[str] = []
        ROUTING_MODULE.validate_plan_state(plan, state_errors)
        self.assertEqual(state_errors, [])
        return plan

    def test_needs_approval_with_implementation_gate(self) -> None:
        plan = self.parse_plan(self.run_resolver(self.envelope()))
        self.assertEqual(plan["status"], "needs_approval")
        self.assertEqual(plan["workflow_selection"]["workflow_id"], "task.defect-remediation")
        self.assertEqual(len(plan["selections"]), 1)
        selection = plan["selections"][0]
        self.assertEqual(selection["domain_id"], "engineering.web")
        self.assertEqual(selection["route_id"], "web-delivery-route")
        self.assertEqual(
            selection["skills"][0]["source_path"], "skills/web-delivery/SKILL.md"
        )
        gates = plan["approval_gates"]
        self.assertEqual(len(gates), 1)
        self.assertEqual(gates[0]["kind"], "implementation")
        self.assertEqual(gates[0]["status"], "pending")
        self.assertEqual(gates[0]["scope_fingerprint"], plan["scope_fingerprint"])
        self.assertTrue(plan["execution_plan"]["required"])
        self.assertEqual(plan["execution_plan"]["status"], "missing")

    def test_model_native_fallback_when_no_capability_matches(self) -> None:
        plan = self.parse_plan(
            self.run_resolver(self.envelope(task_type="android-application-change"))
        )
        self.assertEqual(plan["status"], "needs_approval")
        self.assertEqual(plan["selections"], [])
        self.assertEqual(plan["execution_mode"], "model_native")
        self.assertTrue(plan["approval_gates"])
        self.assertTrue(plan["fallbacks"])
        self.assertEqual(plan["conflicts"], [])
        self.assertFalse(plan["execution_plan"]["required"])

    def test_needs_input_for_defect_without_expected_behavior(self) -> None:
        envelope = self.envelope()
        del envelope["expected_behavior"]
        plan = self.parse_plan(self.run_resolver(envelope))
        self.assertEqual(plan["status"], "needs_input")
        self.assertTrue(plan["missing_inputs"])
        self.assertEqual(plan["approval_gates"], [])
        self.assertEqual(plan["conflicts"], [])

    def test_unregistered_task_class_rejected_at_input_boundary(self) -> None:
        result = self.run_resolver(self.envelope(task_class="unknown-class"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("no registered", result.stderr)

    def test_invalid_envelope_rejected(self) -> None:
        envelope = self.envelope()
        del envelope["task_type"]
        result = self.run_resolver(envelope)
        self.assertEqual(result.returncode, 2)

    def test_missing_optional_skill_uses_governed_fallback(self) -> None:
        (self.domain / "domains" / "engineering" / "web" / "skills" / "web-delivery" / "SKILL.md").unlink()
        subprocess.run(
            ["git", "-C", str(self.domain), "add", "."], check=True, capture_output=True
        )
        subprocess.run(
            [
                "git", "-C", str(self.domain),
                "-c", "user.name=test", "-c", "user.email=test@test",
                "commit", "-m", "remove skill",
            ],
            check=True,
            capture_output=True,
        )
        new_revision = subprocess.run(
            ["git", "-C", str(self.domain), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        config = json.loads(
            (self.kernel / "config" / "domain-pack-sources.json").read_text(encoding="utf-8")
        )
        config["sources"][0]["ref"] = new_revision
        write_json(self.kernel / "config" / "domain-pack-sources.json", config)
        plan = self.parse_plan(self.run_resolver(self.envelope()))
        self.assertEqual(plan["status"], "needs_approval")
        self.assertEqual(plan["execution_mode"], "domain_augmented")
        self.assertEqual(plan["selections"][0]["skills"], [])
        self.assertTrue(any("Optional Skill" in item for item in plan["fallbacks"]))
        self.assertEqual(plan["conflicts"], [])

    def test_g0_investigation_routes_without_gates(self) -> None:
        plan = self.parse_plan(
            self.run_resolver(
                self.envelope(
                    task_class="investigation",
                    operation="inspect",
                    external_effects=[],
                )
            )
        )
        self.assertEqual(plan["status"], "routed")
        self.assertEqual(plan["approval_gates"], [])
        self.assertEqual(plan["assessment"]["risk_level"], "G0")
        self.assertEqual(plan["execution_plan"]["status"], "not-required")

    def test_decisions_record_transitions_to_routed(self) -> None:
        plan_path = self.execution_plan()
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--execution-plan", str(plan_path))
        )
        decisions = {
            "schema_version": "2.0",
            "scope_fingerprint": plan["scope_fingerprint"],
            "presented_execution_plan": self.presented_plan(plan),
            "decisions": [
                {
                    "gate_id": "implementation-approval",
                    "decision": "approved",
                    "evidence": self.decision_evidence(plan),
                }
            ],
        }
        decisions_path = self.base / "decisions.json"
        write_json(decisions_path, decisions)
        routed = self.parse_plan(
            self.run_resolver(
                self.envelope(),
                "--execution-plan", str(plan_path),
                "--decisions", str(decisions_path),
            )
        )
        self.assertEqual(routed["status"], "routed")
        self.assertEqual(routed["approval_gates"][0]["status"], "approved")
        self.assertTrue(routed["approval_gates"][0]["evidence"])
        self.assertEqual(routed["execution_plan"]["status"], "presented")
        self.assertTrue(routed["execution_plan"]["presentation_evidence"])

    def test_decisions_record_rejection(self) -> None:
        plan_path = self.execution_plan()
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--execution-plan", str(plan_path))
        )
        decisions = {
            "schema_version": "2.0",
            "scope_fingerprint": plan["scope_fingerprint"],
            "presented_execution_plan": self.presented_plan(plan),
            "decisions": [
                {
                    "gate_id": "implementation-approval",
                    "decision": "rejected",
                    "evidence": self.decision_evidence(plan, "message:owner-rejection"),
                }
            ],
        }
        decisions_path = self.base / "decisions.json"
        write_json(decisions_path, decisions)
        rejected = self.parse_plan(
            self.run_resolver(
                self.envelope(),
                "--execution-plan", str(plan_path),
                "--decisions", str(decisions_path),
            )
        )
        self.assertEqual(rejected["status"], "approval_rejected")

    def test_stale_decisions_record_rejected(self) -> None:
        plan_path = self.execution_plan()
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--execution-plan", str(plan_path))
        )
        decisions = {
            "schema_version": "2.0",
            "scope_fingerprint": "sha256:" + "0" * 64,
            "presented_execution_plan": self.presented_plan(plan),
            "decisions": [
                {
                    "gate_id": "implementation-approval",
                    "decision": "approved",
                    "evidence": self.decision_evidence(plan),
                }
            ],
        }
        decisions_path = self.base / "decisions.json"
        write_json(decisions_path, decisions)
        result = self.run_resolver(
            self.envelope(),
            "--execution-plan", str(plan_path),
            "--decisions", str(decisions_path),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("stale", result.stderr)

    def test_domain_implementation_decision_requires_execution_plan(self) -> None:
        plan = self.parse_plan(self.run_resolver(self.envelope()))
        decisions = {
            "schema_version": "2.0",
            "scope_fingerprint": plan["scope_fingerprint"],
            "decisions": [
                {
                    "gate_id": "implementation-approval",
                    "decision": "approved",
                    "evidence": self.decision_evidence(plan),
                }
            ],
        }
        decisions_path = self.base / "decisions.json"
        write_json(decisions_path, decisions)
        result = self.run_resolver(self.envelope(), "--decisions", str(decisions_path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("requires --execution-plan", result.stderr)

    def test_domain_implementation_decision_requires_presentation_evidence(self) -> None:
        plan_path = self.execution_plan()
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--execution-plan", str(plan_path))
        )
        decisions = {
            "schema_version": "2.0",
            "scope_fingerprint": plan["scope_fingerprint"],
            "decisions": [
                {
                    "gate_id": "implementation-approval",
                    "decision": "approved",
                    "evidence": self.decision_evidence(plan),
                }
            ],
        }
        decisions_path = self.base / "decisions.json"
        write_json(decisions_path, decisions)
        result = self.run_resolver(
            self.envelope(),
            "--execution-plan", str(plan_path),
            "--decisions", str(decisions_path),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("presented_execution_plan", result.stderr)

    def test_agent_self_report_strings_cannot_satisfy_plan_confirmation(self) -> None:
        plan_path = self.execution_plan()
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--execution-plan", str(plan_path))
        )
        decisions = {
            "schema_version": "2.0",
            "scope_fingerprint": plan["scope_fingerprint"],
            "presented_execution_plan": {
                "artifact": plan["execution_plan"]["artifact"],
                "sha256": plan["execution_plan"]["sha256"],
                "evidence": ["agent self-reports plan was shown"],
            },
            "decisions": [
                {
                    "gate_id": "implementation-approval",
                    "decision": "approved",
                    "evidence": ["agent asserts owner approval"],
                }
            ],
        }
        decisions_path = self.base / "decisions.json"
        write_json(decisions_path, decisions)
        result = self.run_resolver(
            self.envelope(),
            "--execution-plan", str(plan_path),
            "--decisions", str(decisions_path),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("decisions record", result.stderr)

    def test_decision_evidence_must_match_required_role_and_scope(self) -> None:
        plan_path = self.execution_plan()
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--execution-plan", str(plan_path))
        )
        evidence = self.decision_evidence(plan)
        evidence[0]["actor_role"] = "Generator"
        decisions = {
            "schema_version": "2.0",
            "scope_fingerprint": plan["scope_fingerprint"],
            "presented_execution_plan": self.presented_plan(plan),
            "decisions": [
                {
                    "gate_id": "implementation-approval",
                    "decision": "approved",
                    "evidence": evidence,
                }
            ],
        }
        decisions_path = self.base / "decisions.json"
        write_json(decisions_path, decisions)
        result = self.run_resolver(
            self.envelope(),
            "--execution-plan", str(plan_path),
            "--decisions", str(decisions_path),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("required role", result.stderr)

    def test_execution_plan_change_invalidates_prior_decision(self) -> None:
        plan_path = self.execution_plan()
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--execution-plan", str(plan_path))
        )
        decisions = {
            "schema_version": "2.0",
            "scope_fingerprint": plan["scope_fingerprint"],
            "presented_execution_plan": self.presented_plan(plan),
            "decisions": [
                {
                    "gate_id": "implementation-approval",
                    "decision": "approved",
                    "evidence": self.decision_evidence(plan),
                }
            ],
        }
        decisions_path = self.base / "decisions.json"
        write_json(decisions_path, decisions)
        plan_path.write_text("# Revised Domain execution plan\n", encoding="utf-8")
        result = self.run_resolver(
            self.envelope(),
            "--execution-plan", str(plan_path),
            "--decisions", str(decisions_path),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("stale", result.stderr)

    def test_fingerprint_determinism_and_scope_sensitivity(self) -> None:
        first = self.parse_plan(self.run_resolver(self.envelope()))
        second = self.parse_plan(self.run_resolver(self.envelope()))
        self.assertEqual(first["scope_fingerprint"], second["scope_fingerprint"])
        changed = self.parse_plan(
            self.run_resolver(self.envelope(affected_surfaces=["login page", "settings"]))
        )
        self.assertNotEqual(first["scope_fingerprint"], changed["scope_fingerprint"])

    def test_overlay_disabled_domain_uses_model_native_fallback(self) -> None:
        overlay = {
            "schema_version": "1.0",
            "domains": [
                {
                    "id": "engineering.web",
                    "version": "1.0.0",
                    "enabled": False,
                    "local_owner": "project-owner",
                    "additional_signals": [],
                    "constraints": [],
                    "disabled_capabilities": [],
                    "mappings": [],
                }
            ],
        }
        overlay_path = self.base / "overlay.json"
        write_json(overlay_path, overlay)
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--overlay", str(overlay_path))
        )
        self.assertEqual(plan["status"], "needs_approval")
        self.assertEqual(plan["execution_mode"], "model_native")

    def test_overlay_version_mismatch_records_conflict(self) -> None:
        overlay = {
            "schema_version": "1.0",
            "domains": [
                {
                    "id": "engineering.web",
                    "version": "9.9.9",
                    "enabled": True,
                    "local_owner": "project-owner",
                    "additional_signals": [],
                    "constraints": [],
                    "disabled_capabilities": [],
                    "mappings": [],
                }
            ],
        }
        overlay_path = self.base / "overlay.json"
        write_json(overlay_path, overlay)
        plan = self.parse_plan(
            self.run_resolver(self.envelope(), "--overlay", str(overlay_path))
        )
        self.assertEqual(plan["status"], "unroutable")
        self.assertTrue(any("version" in c for c in plan["conflicts"]))

    def test_unsatisfied_soft_capability_dependency_records_fallback(self) -> None:
        caps_path = (
            self.domain / "domains" / "engineering" / "web" / "capabilities.json"
        )
        caps = json.loads(caps_path.read_text(encoding="utf-8"))
        caps["capabilities"][0]["dependencies"] = ["quality/gate-keeping"]
        write_json(caps_path, caps)
        subprocess.run(
            ["git", "-C", str(self.domain), "add", "."], check=True, capture_output=True
        )
        subprocess.run(
            [
                "git", "-C", str(self.domain),
                "-c", "user.name=test", "-c", "user.email=test@test",
                "commit", "-m", "add dependency",
            ],
            check=True,
            capture_output=True,
        )
        new_revision = subprocess.run(
            ["git", "-C", str(self.domain), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        config = json.loads(
            (self.kernel / "config" / "domain-pack-sources.json").read_text(encoding="utf-8")
        )
        config["sources"][0]["ref"] = new_revision
        write_json(self.kernel / "config" / "domain-pack-sources.json", config)
        plan = self.parse_plan(self.run_resolver(self.envelope()))
        self.assertEqual(plan["status"], "needs_approval")
        self.assertTrue(any("Soft capability dependencies" in item for item in plan["fallbacks"]))
        self.assertEqual(plan["conflicts"], [])

    def test_route_priority_tie_requires_disambiguation(self) -> None:
        routes_path = self.domain / "domains" / "engineering" / "web" / "routes.json"
        routes = json.loads(routes_path.read_text(encoding="utf-8"))
        routes["routes"].append(
            {
                "id": "web-delivery-route-alt",
                "priority": 500,
                "task_types": ["web-change"],
                "signals": ["css"],
                "capabilities": ["web-delivery"],
            }
        )
        write_json(routes_path, routes)
        subprocess.run(
            ["git", "-C", str(self.domain), "add", "."], check=True, capture_output=True
        )
        subprocess.run(
            [
                "git", "-C", str(self.domain),
                "-c", "user.name=test", "-c", "user.email=test@test",
                "commit", "-m", "tie routes",
            ],
            check=True,
            capture_output=True,
        )
        new_revision = subprocess.run(
            ["git", "-C", str(self.domain), "rev-parse", "HEAD"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        config = json.loads(
            (self.kernel / "config" / "domain-pack-sources.json").read_text(encoding="utf-8")
        )
        config["sources"][0]["ref"] = new_revision
        write_json(self.kernel / "config" / "domain-pack-sources.json", config)
        plan = self.parse_plan(self.run_resolver(self.envelope()))
        self.assertEqual(plan["status"], "needs_input")
        self.assertTrue(any("disambiguation" in item for item in plan["missing_inputs"]))

    def test_external_effects_raise_risk_and_add_gate(self) -> None:
        plan = self.parse_plan(
            self.run_resolver(
                self.envelope(external_effects=["calls external payment webhook"])
            )
        )
        self.assertEqual(plan["assessment"]["risk_level"], "G2")
        kinds = {gate["kind"] for gate in plan["approval_gates"]}
        self.assertIn("external-effect", kinds)
        self.assertIn("implementation", kinds)


REAL_DOMAIN_ROOT = ROOT.parent / "harness-domain-packs"
EXPECTED_ANDROID_PLAN = json.loads(
    (ROOT / "examples" / "routing-plan.json").read_text(encoding="utf-8")
)


@unittest.skipUnless(
    (REAL_DOMAIN_ROOT / ".git").is_dir(),
    "authorized sibling Domain Packs checkout not available",
)
class RealRegistryIntegrationTests(unittest.TestCase):
    """Integration against the pinned production Domain registry."""

    def run_resolver(self, envelope: dict) -> dict:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as handle:
            json.dump(envelope, handle)
            envelope_path = Path(handle.name)
        try:
            result = subprocess.run(
                [
                    "python3",
                    str(SCRIPT),
                    str(envelope_path),
                    "--root",
                    str(ROOT),
                    "--domain-root",
                    str(REAL_DOMAIN_ROOT),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
        finally:
            envelope_path.unlink(missing_ok=True)
        schema_errors = SCHEMA_MODULE.validate_instance(plan, PLAN_SCHEMA)
        self.assertEqual(schema_errors, [])
        state_errors: list[str] = []
        ROUTING_MODULE.validate_plan_state(plan, state_errors)
        self.assertEqual(state_errors, [])
        return plan

    def test_android_example_reproduces_checked_in_plan(self) -> None:
        envelope = json.loads(
            (ROOT / "examples" / "task-envelope.json").read_text(encoding="utf-8")
        )
        plan = self.run_resolver(envelope)
        self.assertEqual(plan, EXPECTED_ANDROID_PLAN)
        self.assertEqual(plan["status"], "needs_approval")
        self.assertEqual(plan["execution_mode"], "model_native")

    def test_web_frontend_task_routes_against_engineering_web(self) -> None:
        envelope = {
            "schema_version": "2.0",
            "task_id": "integration-web-form",
            "intent": "Repair the profile form submit button that stays disabled.",
            "task_class": "defect",
            "task_type": "web-frontend-implementation",
            "operation": "modify",
            "deliverables": ["Approved repair plan", "Verification evidence"],
            "constraints": ["No new dependencies"],
            "repository_signals": ["html", "css", "typescript"],
            "affected_surfaces": ["profile form"],
            "current_behavior": ["submit stays disabled after valid input"],
            "expected_behavior": ["submit enables when the form is valid"],
            "required_evidence": ["browser test"],
        }
        plan = self.run_resolver(envelope)
        self.assertEqual(plan["status"], "needs_approval")
        self.assertEqual(
            plan["workflow_selection"]["workflow_id"], "task.defect-remediation"
        )
        selection = plan["selections"][0]
        self.assertEqual(selection["domain_id"], "engineering.web")
        skill_paths = {skill["source_path"] for skill in selection["skills"]}
        self.assertIn("skills/web-interface-delivery/SKILL.md", skill_paths)
        gate_kinds = {gate["kind"] for gate in plan["approval_gates"]}
        self.assertIn("implementation", gate_kinds)


if __name__ == "__main__":
    unittest.main()

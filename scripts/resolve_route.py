#!/usr/bin/env python3
"""Resolve a Task Envelope into one governed Routing Plan.

Deterministic Router/Resolver v2 (change 20260809-governed-model-fallback).

Inputs:
- A schema-valid Task Envelope (contract 2.0);
- the Kernel task-workflow registry;
- an optional project overlay;
- the pinned Domain registry, routes, capabilities, and Skill artifacts read
  exclusively from the pinned Git commit of an authorized Domain checkout;
- an optional decisions record applying approval-gate decisions.

The resolver never synthesizes a Domain, capability, or Skill. Missing optional
professional assets produce an explicit model-native fallback. An envelope that
fails schema validation or whose
task_class matches no registered workflow is rejected at the input boundary
(exit 2) because no conforming Routing Plan can be emitted for it.

Deterministic mapping and fingerprint rules are documented in docs/ROUTING.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_validation import validate_instance  # noqa: E402
import validate_domain_source as vds  # noqa: E402

SENSITIVE_HINT_KEYWORDS = (
    "authentication",
    "credential",
    "password",
    "token",
    "biometric",
    "payment",
    "personal",
    "pii",
    "health",
    "regulated",
)

ELEVATED_PERMISSION_KEYWORDS = ("production", "deploy", "publish", "release")
DESTRUCTIVE_KEYWORDS = ("destructive", "irreversible", "delete-data", "drop")


def load_json(path: Path, label: str, errors: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{label}: invalid JSON: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{label}: top-level value must be an object")
        return {}
    return value


def fail_input(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 2


def canonical_fingerprint(scope: dict) -> str:
    blob = json.dumps(scope, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "sha256:" + hashlib.sha256(blob.encode("utf-8")).hexdigest()


def select_workflow(envelope: dict, registry: dict) -> dict | None:
    task_class = envelope.get("task_class")
    matches = [
        workflow
        for workflow in registry.get("workflows", [])
        if isinstance(workflow, dict) and task_class in workflow.get("task_classes", [])
    ]
    return matches[0] if len(matches) == 1 else None


def derive_assessment(envelope: dict, domain_count: int) -> dict:
    surfaces = list(envelope.get("affected_surfaces", []))
    hints = [str(hint).lower() for hint in envelope.get("risk_hints", [])]
    external = list(envelope.get("external_effects", []))
    permission_hints = [str(hint).lower() for hint in envelope.get("permission_hints", [])]
    operation = envelope.get("operation")

    if any(any(k in hint for k in SENSITIVE_HINT_KEYWORDS) for hint in hints):
        sensitivity = "sensitive"
    elif hints:
        sensitivity = "internal"
    else:
        sensitivity = "unknown"

    if operation == "inspect":
        reversibility = "high"
    elif operation == "remove":
        reversibility = "low"
    else:
        reversibility = "unknown"

    joined_permissions = " ".join(permission_hints + [str(e).lower() for e in external])
    if any(k in joined_permissions for k in DESTRUCTIVE_KEYWORDS):
        risk = "G3"
    elif external:
        risk = "G2"
    elif operation in {"publish", "operate"}:
        risk = "G2"
    elif operation == "inspect" and not external:
        risk = "G0"
    else:
        risk = "G1"

    rationale = (
        f"Preliminary Kernel assessment from envelope facts: operation={operation}, "
        f"surfaces={len(surfaces)}, external_effects={len(external)}, "
        f"risk_hints={len(hints)}. Domain professional assessment may refine this level."
    )
    return {
        "risk_level": risk,
        "impact_surfaces": surfaces,
        "affected_units": len(surfaces),
        "change_points": 0,
        "domain_count": domain_count,
        "reversibility": reversibility,
        "data_sensitivity": sensitivity,
        "external_effects": external,
        "rationale": rationale,
    }


class DomainResolver:
    """Read Domain metadata exclusively from the pinned commit."""

    def __init__(self, domain_root: Path, revision: str) -> None:
        self.domain_root = domain_root
        self.revision = revision
        self.errors: list[str] = []

    def read_json(self, relative: str) -> dict:
        return vds.revision_json(self.domain_root, self.revision, relative, self.errors)

    def exists(self, relative: str) -> bool:
        return vds.revision_path_exists(self.domain_root, self.revision, relative)


def resolve_domains(
    envelope: dict,
    resolver: DomainResolver,
    registry_path: str,
    overlay: dict | None,
) -> tuple[list[dict], list[str], list[str], list[str]]:
    """Return selections, hard conflicts, missing inputs, and soft fallbacks."""
    selections: list[dict] = []
    selection_dependencies: list[list[str]] = []
    conflicts: list[str] = []
    missing: list[str] = []
    fallbacks: list[str] = []
    task_type = envelope.get("task_type")

    registry = resolver.read_json(registry_path)
    entries = registry.get("domains")
    if not isinstance(entries, list):
        return [], [f"Domain registry at {registry_path} has no domains array"], [], []

    overlay_domains: dict[str, dict] = {}
    if overlay is not None:
        for entry in overlay.get("domains", []):
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                overlay_domains[entry["id"]] = entry

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        domain_id = entry.get("id")
        domain_path = entry.get("path")
        if entry.get("status") != "active" or not domain_id or not domain_path:
            continue

        if overlay is not None:
            overlay_entry = overlay_domains.get(domain_id)
            if overlay_entry is None or overlay_entry.get("enabled") is not True:
                continue
            if overlay_entry.get("version") != entry.get("version"):
                conflicts.append(
                    f"Overlay pins {domain_id} version {overlay_entry.get('version')} "
                    f"but the pinned registry declares {entry.get('version')}."
                )
                continue
            disabled = set(overlay_entry.get("disabled_capabilities", []))
        else:
            disabled = set()

        domain_doc = resolver.read_json(f"{domain_path}/domain.json")
        applicability = domain_doc.get("applicability", {})
        if task_type not in applicability.get("task_types", []):
            continue

        routes_doc = resolver.read_json(f"{domain_path}/routes.json")
        routes = [
            route
            for route in routes_doc.get("routes", [])
            if isinstance(route, dict) and task_type in route.get("task_types", [])
        ]
        if not routes:
            continue
        best_priority = max(route.get("priority", 0) for route in routes)
        best = [route for route in routes if route.get("priority", 0) == best_priority]
        if len(best) > 1:
            tied = ", ".join(str(route.get("id")) for route in best)
            missing.append(
                f"Route disambiguation for {domain_id}: routes {tied} tie at "
                f"priority {best_priority} for task_type '{task_type}'."
            )
            continue
        route = best[0]

        capabilities_doc = resolver.read_json(f"{domain_path}/capabilities.json")
        declared = {
            capability.get("id"): capability
            for capability in capabilities_doc.get("capabilities", [])
            if isinstance(capability, dict)
        }
        capability_ids = list(route.get("capabilities", []))
        broken = False
        capability_records: list[dict] = []
        for capability_id in capability_ids:
            capability = declared.get(capability_id)
            if capability is None:
                conflicts.append(
                    f"{domain_id}: route '{route.get('id')}' declares unknown "
                    f"capability '{capability_id}'."
                )
                broken = True
                continue
            if capability_id in disabled:
                conflicts.append(
                    f"{domain_id}: required capability '{capability_id}' is disabled "
                    "by the project overlay."
                )
                broken = True
                continue
            capability_records.append(capability)
        if broken:
            continue

        skills: list[dict] = []
        workflows: list[str] = []
        tools: list[str] = []
        evaluators: list[str] = []
        permissions: list[str] = []
        qualified_dependencies: list[str] = []
        for capability in capability_records:
            for skill_id in capability.get("skills", []):
                source_path = f"skills/{skill_id}/SKILL.md"
                if not resolver.exists(f"{domain_path}/{source_path}"):
                    fallbacks.append(
                        f"Optional Skill {domain_id}/{skill_id} is unavailable at the pinned "
                        "revision; execute its declared capability through the Kernel workflow "
                        "with model reasoning, permitted retrieval, and task evidence."
                    )
                    continue
                skills.append(
                    {
                        "skill_id": skill_id,
                        "capability_id": capability["id"],
                        "source_path": source_path,
                        "reuse_scope": "domain",
                    }
                )
            for field, directory in (
                ("workflows", "workflows"),
                ("evaluators", "evaluators"),
            ):
                for relative in capability.get(field, []):
                    artifact = f"{domain_path}/{directory}/{relative}"
                    if not resolver.exists(artifact):
                        conflicts.append(
                            f"{domain_id}: capability '{capability['id']}' references "
                            f"'{directory}/{relative}' which is absent at the pinned revision."
                        )
                        broken = True
            workflows.extend(capability.get("workflows", []))
            tools.extend(capability.get("tools", []))
            evaluators.extend(capability.get("evaluators", []))
            permissions.extend(capability.get("permissions", []))
            for dependency in capability.get("dependencies", []):
                qualified = (
                    dependency
                    if "/" in dependency
                    else f"{domain_id}/{dependency}"
                )
                qualified_dependencies.append(qualified)
        if broken:
            continue

        selections.append(
            {
                "domain_id": domain_id,
                "version": entry.get("version", ""),
                "route_id": route.get("id", ""),
                "capability_ids": capability_ids,
                "workflows": sorted(set(workflows)),
                "skills": skills,
                "tools": sorted(set(tools)),
                "evaluators": sorted(set(evaluators)),
                "permissions": sorted(set(permissions)),
                "reason": (
                    f"task_type '{task_type}' matches route '{route.get('id')}' "
                    f"(priority {best_priority}) of active Domain {domain_id}."
                ),
            }
        )
        selection_dependencies.append(qualified_dependencies)

    selected_qualified = {
        f"{selection['domain_id']}/{capability_id}"
        for selection in selections
        for capability_id in selection["capability_ids"]
    }
    for selection, dependencies in zip(selections, selection_dependencies):
        unsatisfied = sorted(
            {dep for dep in dependencies if dep not in selected_qualified}
        )
        if unsatisfied:
            fallbacks.append(
                f"Soft capability dependencies for {selection['domain_id']}/"
                f"{selection['route_id']} are not selected: {', '.join(unsatisfied)}; "
                "cover these professional concerns through model reasoning and explicit evidence."
            )

    return selections, conflicts, missing, sorted(set(fallbacks))


def build_gates(
    envelope: dict, workflow: dict, assessment: dict, fingerprint: str
) -> list[dict]:
    gates: list[dict] = []
    operation = envelope.get("operation")
    surfaces = list(envelope.get("affected_surfaces", []))
    external = list(envelope.get("external_effects", []))
    permission_hints = list(envelope.get("permission_hints", []))

    policy = workflow.get("approval_policy")
    risk = assessment.get("risk_level")
    needs_implementation_gate = policy == "always-before-implementation" or risk in {
        "G1",
        "G2",
        "G3",
    }
    if needs_implementation_gate:
        gates.append(
            {
                "gate_id": "implementation-approval",
                "kind": "implementation",
                "required_role": "Owner",
                "status": "pending",
                "scope": [f"operation: {operation}"] + surfaces,
                "scope_fingerprint": fingerprint,
                "evidence": [],
            }
        )
    if external:
        gates.append(
            {
                "gate_id": "external-effect-approval",
                "kind": "external-effect",
                "required_role": "Owner",
                "status": "pending",
                "scope": external,
                "scope_fingerprint": fingerprint,
                "evidence": [],
            }
        )
    elevated = [
        hint
        for hint in permission_hints
        if any(k in hint.lower() for k in ELEVATED_PERMISSION_KEYWORDS)
    ]
    if elevated:
        gates.append(
            {
                "gate_id": "elevated-permission-approval",
                "kind": "permission",
                "required_role": "Owner",
                "status": "pending",
                "scope": elevated,
                "scope_fingerprint": fingerprint,
                "evidence": [],
            }
        )
    return gates


def scope_fingerprint(
    envelope: dict, workflow: dict, selections: list[dict], fallbacks: list[str]
) -> str:
    scope = {
        "task_id": envelope.get("task_id"),
        "operation": envelope.get("operation"),
        "affected_surfaces": envelope.get("affected_surfaces", []),
        "constraints": envelope.get("constraints", []),
        "non_goals": envelope.get("non_goals", []),
        "deliverables": envelope.get("deliverables", []),
        "external_effects": envelope.get("external_effects", []),
        "workflow_id": workflow.get("id"),
        "workflow_version": workflow.get("version"),
        "selections": [
            {
                "domain_id": selection["domain_id"],
                "version": selection["version"],
                "route_id": selection["route_id"],
                "capability_ids": sorted(selection["capability_ids"]),
                "skill_ids": sorted(skill["skill_id"] for skill in selection["skills"]),
            }
            for selection in selections
        ],
        "fallbacks": sorted(fallbacks),
    }
    return canonical_fingerprint(scope)


def apply_decisions(
    plan: dict, decisions: dict, errors: list[str]
) -> bool:
    records = decisions.get("decisions")
    if not isinstance(records, list):
        errors.append("decisions record: decisions must be an array")
        return False
    if decisions.get("scope_fingerprint") != plan.get("scope_fingerprint"):
        errors.append(
            "decisions record: scope_fingerprint does not match the current plan; "
            "the approval is stale or belongs to a different scope"
        )
        return False
    gates = {gate["gate_id"]: gate for gate in plan.get("approval_gates", [])}
    for record in records:
        if not isinstance(record, dict):
            errors.append("decisions record: every decision must be an object")
            return False
        gate_id = record.get("gate_id")
        decision = record.get("decision")
        evidence = record.get("evidence")
        if gate_id not in gates:
            errors.append(f"decisions record: unknown gate '{gate_id}'")
            return False
        if decision not in {"approved", "rejected"}:
            errors.append(
                f"decisions record: gate '{gate_id}' decision must be approved or rejected"
            )
            return False
        if not isinstance(evidence, list) or not evidence:
            errors.append(
                f"decisions record: gate '{gate_id}' requires non-empty decision evidence"
            )
            return False
        gates[gate_id]["status"] = decision
        gates[gate_id]["evidence"] = sorted({str(item) for item in evidence})
    return True


def derive_status(plan: dict) -> str:
    if plan["missing_inputs"]:
        return "needs_input"
    if plan["conflicts"]:
        return "unroutable"
    gates = plan["approval_gates"]
    if any(gate["status"] == "rejected" for gate in gates):
        return "approval_rejected"
    if any(gate["status"] == "pending" for gate in gates):
        return "needs_approval"
    return "routed"


def discover_domain_root(root: Path) -> Path | None:
    candidate = os.environ.get("HARNESS_DOMAIN_PACKS_CHECKOUT", "")
    if candidate:
        path = Path(candidate)
        return path if (path / ".git").is_dir() else None
    sibling = root.resolve().parent / "harness-domain-packs"
    return sibling if (sibling / ".git").is_dir() else None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve a Task Envelope into one fail-closed Routing Plan."
    )
    parser.add_argument("envelope", type=Path, help="Task Envelope JSON (contract 2.0)")
    parser.add_argument("--root", type=Path, default=Path("."), help="Kernel root")
    parser.add_argument(
        "--domain-root",
        type=Path,
        default=None,
        help="Authorized Domain Packs checkout "
        "(default: HARNESS_DOMAIN_PACKS_CHECKOUT or sibling harness-domain-packs)",
    )
    parser.add_argument(
        "--overlay", type=Path, default=None, help="Optional project overlay JSON"
    )
    parser.add_argument(
        "--decisions", type=Path, default=None, help="Optional decisions record JSON"
    )
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output path")
    args = parser.parse_args()

    root = args.root.resolve()
    errors: list[str] = []

    envelope = load_json(args.envelope, "task envelope", errors)
    envelope_schema = load_json(
        root / "schemas" / "task-envelope.schema.json", "task envelope schema", errors
    )
    if errors:
        return fail_input(errors)
    schema_errors = [
        f"task envelope: {error}"
        for error in validate_instance(envelope, envelope_schema)
    ]
    if schema_errors:
        return fail_input(schema_errors)

    workflow_registry = load_json(
        root / "config" / "task-workflows.json", "task workflow registry", errors
    )
    source_config = load_json(
        root / "config" / "domain-pack-sources.json", "source configuration", errors
    )
    if errors:
        return fail_input(errors)

    workflow = select_workflow(envelope, workflow_registry)
    if workflow is None:
        return fail_input(
            [
                f"task_class '{envelope.get('task_class')}' matches no registered "
                "Kernel task workflow; the envelope is rejected at the input "
                "boundary because no conforming Routing Plan can be emitted"
            ]
        )

    source = vds.select_source(source_config, None, errors)
    if errors:
        return fail_input(errors)

    plan: dict = {
        "schema_version": "3.0",
        "task_id": envelope["task_id"],
        "source": {
            "source_id": source.get("id", ""),
            "repository": source.get("repository", ""),
            "revision": source.get("ref", ""),
            "registry": source.get("registry", ""),
        },
        "workflow_selection": {
            "workflow_id": workflow["id"],
            "version": workflow["version"],
            "registry": "config/task-workflows.json",
            "reason": (
                f"task_class '{envelope['task_class']}' is declared by registered "
                f"workflow '{workflow['id']}'."
            ),
        },
        "assessment": {},
        "scope_fingerprint": "",
        "execution_mode": "model_native",
        "fallbacks": [],
        "status": "",
        "selections": [],
        "approval_gates": [],
        "conflicts": [],
        "missing_inputs": [],
    }

    if envelope.get("task_class") == "defect" and not envelope.get("expected_behavior"):
        plan["missing_inputs"].append(
            "expected_behavior: defect remediation requires the expected accepted "
            "behavior to define the contract deviation"
        )

    overlay: dict | None = None
    if args.overlay is not None:
        overlay = load_json(args.overlay, "project overlay", errors)
        overlay_schema = load_json(
            root / "schemas" / "project-domain-overlay.schema.json",
            "project overlay schema",
            errors,
        )
        if errors:
            return fail_input(errors)
        overlay_errors = [
            f"project overlay: {error}"
            for error in validate_instance(overlay, overlay_schema)
        ]
        if overlay_errors:
            return fail_input(overlay_errors)

    if not plan["missing_inputs"]:
        domain_root = args.domain_root or discover_domain_root(root)
        if domain_root is None:
            return fail_input(
                [
                    "no authorized Domain Packs checkout available; set "
                    "HARNESS_DOMAIN_PACKS_CHECKOUT or pass --domain-root"
                ]
            )
        resolver = DomainResolver(domain_root, source.get("ref", ""))
        selections, conflicts, missing, fallbacks = resolve_domains(
            envelope, resolver, source.get("registry", ""), overlay
        )
        if resolver.errors:
            return fail_input(
                [f"pinned Domain revision: {error}" for error in resolver.errors]
            )
        plan["missing_inputs"].extend(missing)
        if not plan["missing_inputs"] and not conflicts and not selections:
            fallbacks.append(
                f"No active enabled Domain capability matches task_type "
                f"'{envelope.get('task_type')}'; execute model-native under the selected "
                "Kernel workflow, approvals, permissions, constraints, and evidence requirements."
            )
        if conflicts:
            plan["conflicts"] = conflicts
        else:
            plan["selections"] = selections
        plan["fallbacks"] = sorted(set(fallbacks))

    plan["execution_mode"] = (
        "domain_augmented" if plan["selections"] else "model_native"
    )

    plan["assessment"] = derive_assessment(envelope, len(plan["selections"]))
    plan["scope_fingerprint"] = scope_fingerprint(
        envelope, workflow, plan["selections"], plan["fallbacks"]
    )
    if not plan["missing_inputs"] and not plan["conflicts"]:
        plan["approval_gates"] = build_gates(
            envelope, workflow, plan["assessment"], plan["scope_fingerprint"]
        )

    plan["status"] = derive_status(plan)

    if args.decisions is not None:
        if plan["status"] != "needs_approval":
            return fail_input(
                [
                    f"decisions record provided but plan status is "
                    f"'{plan['status']}'; decisions apply only to needs_approval plans"
                ]
            )
        decisions = load_json(args.decisions, "decisions record", errors)
        if errors:
            return fail_input(errors)
        decision_errors: list[str] = []
        if not apply_decisions(plan, decisions, decision_errors):
            return fail_input(decision_errors)
        plan["status"] = derive_status(plan)

    rendered = json.dumps(plan, indent=2, ensure_ascii=False) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

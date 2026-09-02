#!/usr/bin/env python3
"""Validate routing documents against schemas and fail-closed state invariants."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema_validation import validate_instance


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


def apply_schema(document: dict, schema: dict, label: str, errors: list[str]) -> None:
    for error in validate_instance(document, schema):
        errors.append(f"{label}: {error}")


def validate_plan_state(plan: dict, errors: list[str]) -> None:
    status = plan.get("status")
    selections = plan.get("selections")
    approval_gates = plan.get("approval_gates")
    conflicts = plan.get("conflicts")
    missing_inputs = plan.get("missing_inputs")
    execution_mode = plan.get("execution_mode")
    execution_plan = plan.get("execution_plan")
    fallbacks = plan.get("fallbacks")
    if not all(
        isinstance(value, list)
        for value in (selections, approval_gates, conflicts, missing_inputs, fallbacks)
    ):
        return
    if not isinstance(execution_plan, dict):
        return

    gate_statuses = [
        gate.get("status") for gate in approval_gates if isinstance(gate, dict)
    ]
    pending = "pending" in gate_statuses
    rejected = "rejected" in gate_statuses

    if execution_mode == "domain_augmented" and not selections:
        errors.append("routing plan: domain_augmented mode requires a Domain selection")
    if execution_mode == "model_native" and selections:
        errors.append("routing plan: model_native mode cannot contain Domain selections")
    plan_required = execution_plan.get("required") is True
    plan_status = execution_plan.get("status")
    artifact = execution_plan.get("artifact")
    plan_digest = execution_plan.get("sha256")
    presentation = execution_plan.get("presentation_evidence")
    domain_ids = execution_plan.get("domain_ids")
    selected_domain_ids = sorted(
        selection.get("domain_id")
        for selection in selections
        if isinstance(selection, dict) and isinstance(selection.get("domain_id"), str)
    )
    if plan_required:
        if execution_mode != "domain_augmented":
            errors.append("routing plan: a required Domain execution plan requires domain_augmented mode")
        if domain_ids != selected_domain_ids:
            errors.append("routing plan: Domain execution plan must cover every selected Domain")
        if plan_status == "missing" and any(value is not None for value in (artifact, plan_digest)):
            errors.append("routing plan: missing Domain execution plan cannot declare an artifact or digest")
        if plan_status in {"draft", "presented"} and (not artifact or not plan_digest):
            errors.append("routing plan: draft or presented Domain execution plan requires an artifact and digest")
        if plan_status == "draft" and presentation:
            errors.append("routing plan: draft Domain execution plan cannot contain presentation evidence")
        if plan_status == "presented" and not presentation:
            errors.append("routing plan: presented Domain execution plan requires presentation evidence")
    elif plan_status != "not-required" or any(
        value not in (None, []) for value in (artifact, plan_digest, domain_ids, presentation)
    ):
        errors.append("routing plan: a non-required Domain execution plan must be empty and not-required")
    if (
        execution_mode == "model_native"
        and status not in {"needs_input", "unroutable"}
        and not fallbacks
    ):
        errors.append("routing plan: model_native mode requires an explicit fallback reason")

    if status == "routed":
        if pending or rejected or conflicts or missing_inputs:
            errors.append(
                "routing plan: routed status requires every gate approved and no conflicts or missing inputs"
            )
    elif status == "needs_approval":
        if not pending:
            errors.append("routing plan: needs_approval status requires a pending approval gate")
        if rejected or conflicts or missing_inputs:
            errors.append(
                "routing plan: needs_approval status cannot contain rejected gates, conflicts, or missing inputs"
            )
    elif status == "approval_rejected":
        if not rejected:
            errors.append("routing plan: approval_rejected status requires a rejected gate")
        if conflicts or missing_inputs:
            errors.append(
                "routing plan: approval_rejected status cannot contain conflicts or missing inputs"
            )
    elif status == "needs_input":
        if not missing_inputs:
            errors.append("routing plan: needs_input status requires a missing input")
        if approval_gates or conflicts:
            errors.append(
                "routing plan: needs_input status cannot contain approval gates or conflicts"
            )
    elif status == "unroutable":
        if selections or approval_gates or missing_inputs:
            errors.append(
                "routing plan: unroutable status cannot contain selections, approval gates, or missing inputs"
            )
        if not conflicts:
            errors.append("routing plan: unroutable status requires a conflict or reason")

    gate_ids = [
        gate.get("gate_id")
        for gate in approval_gates
        if isinstance(gate, dict) and isinstance(gate.get("gate_id"), str)
    ]
    if len(gate_ids) != len(set(gate_ids)):
        errors.append("routing plan: approval gate IDs must be unique")
    for gate in approval_gates:
        if not isinstance(gate, dict):
            continue
        if gate.get("scope_fingerprint") != plan.get("scope_fingerprint"):
            errors.append(
                "routing plan: every approval gate must bind to the current scope fingerprint"
            )
        if gate.get("status") in {"approved", "rejected"} and not gate.get("evidence"):
            errors.append(
                "routing plan: approved or rejected gates require decision evidence"
            )
        if (
            gate.get("kind") == "implementation"
            and gate.get("status") in {"approved", "rejected"}
            and plan_required
            and plan_status != "presented"
        ):
            errors.append(
                "routing plan: a Domain implementation decision requires the current "
                "execution plan to be presented"
            )


def validate_workflow_registry(registry: dict, errors: list[str]) -> None:
    workflows = registry.get("workflows")
    if not isinstance(workflows, list):
        return
    workflow_ids = [
        workflow.get("id")
        for workflow in workflows
        if isinstance(workflow, dict) and isinstance(workflow.get("id"), str)
    ]
    if len(workflow_ids) != len(set(workflow_ids)):
        errors.append("task workflow registry: workflow IDs must be unique")
    task_classes: list[str] = []
    for workflow in workflows:
        if isinstance(workflow, dict) and isinstance(workflow.get("task_classes"), list):
            task_classes.extend(
                item for item in workflow["task_classes"] if isinstance(item, str)
            )
    if len(task_classes) != len(set(task_classes)):
        errors.append(
            "task workflow registry: each task class must resolve to exactly one workflow"
        )


def validate_workflow_selection(
    envelope: dict, plan: dict, registry: dict, errors: list[str]
) -> None:
    selection = plan.get("workflow_selection")
    workflows = registry.get("workflows")
    if not isinstance(selection, dict) or not isinstance(workflows, list):
        return
    matching = [
        workflow
        for workflow in workflows
        if isinstance(workflow, dict)
        and workflow.get("id") == selection.get("workflow_id")
        and workflow.get("version") == selection.get("version")
    ]
    if len(matching) != 1:
        errors.append(
            "routing plan: workflow selection must resolve to exactly one registered ID and version"
        )
        return
    task_classes = matching[0].get("task_classes", [])
    if envelope.get("task_class") not in task_classes:
        errors.append(
            "routing plan: selected workflow must declare the Task Envelope task class"
        )
    approval_policy = matching[0].get("approval_policy")
    assessment = plan.get("assessment")
    risk_level = assessment.get("risk_level") if isinstance(assessment, dict) else None
    approval_gates = plan.get("approval_gates")
    selections = plan.get("selections")
    requires_approval = approval_policy == "always-before-implementation" or risk_level in {
        "G1",
        "G2",
        "G3",
    }
    has_implementation_gate = isinstance(approval_gates, list) and any(
        isinstance(gate, dict) and gate.get("kind") == "implementation"
        for gate in approval_gates
    )
    if (
        requires_approval
        and isinstance(approval_gates, list)
        and not has_implementation_gate
    ):
        errors.append(
            "routing plan: selected workflow and risk require an implementation approval gate"
        )
    execution_plan = plan.get("execution_plan")
    if (
        requires_approval
        and envelope.get("operation") != "inspect"
        and plan.get("execution_mode") == "domain_augmented"
        and isinstance(execution_plan, dict)
        and execution_plan.get("required") is not True
    ):
        errors.append(
            "routing plan: Domain-augmented mutating work requires a Domain execution plan"
        )


def validate_skill_bindings(plan: dict, errors: list[str]) -> None:
    selections = plan.get("selections")
    if not isinstance(selections, list):
        return
    for selection_index, selection in enumerate(selections):
        if not isinstance(selection, dict):
            continue
        capabilities = selection.get("capability_ids")
        skills = selection.get("skills")
        if not isinstance(capabilities, list) or not isinstance(skills, list):
            continue
        for skill_index, skill in enumerate(skills):
            if not isinstance(skill, dict):
                continue
            if skill.get("capability_id") not in capabilities:
                errors.append(
                    "routing plan: "
                    f"selections[{selection_index}].skills[{skill_index}] must bind to a selected capability"
                )


def validate_overlay(overlay: dict, errors: list[str]) -> None:
    domains = overlay.get("domains")
    if not isinstance(domains, list):
        return
    domain_ids = [
        domain.get("id")
        for domain in domains
        if isinstance(domain, dict) and isinstance(domain.get("id"), str)
    ]
    if len(domain_ids) != len(set(domain_ids)):
        errors.append("project overlay: Domain IDs must be unique")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    documents = {
        "source configuration": (
            load_object(root / "config" / "domain-pack-sources.json", errors),
            load_object(root / "schemas" / "domain-pack-source.schema.json", errors),
        ),
        "task envelope": (
            load_object(root / "examples" / "task-envelope.json", errors),
            load_object(root / "schemas" / "task-envelope.schema.json", errors),
        ),
        "task workflow registry": (
            load_object(root / "config" / "task-workflows.json", errors),
            load_object(root / "schemas" / "task-workflow-registry.schema.json", errors),
        ),
        "routing plan": (
            load_object(root / "examples" / "routing-plan.json", errors),
            load_object(root / "schemas" / "routing-plan.schema.json", errors),
        ),
        "project overlay": (
            load_object(root / "examples" / "project-domain-overlay.json", errors),
            load_object(root / "schemas" / "project-domain-overlay.schema.json", errors),
        ),
    }
    for label, (document, schema) in documents.items():
        apply_schema(document, schema, label, errors)

    config = documents["source configuration"][0]
    envelope = documents["task envelope"][0]
    workflow_registry = documents["task workflow registry"][0]
    plan = documents["routing plan"][0]
    overlay = documents["project overlay"][0]
    sources = config.get("sources", [])
    if isinstance(sources, list):
        source_ids = [
            source.get("id") for source in sources if isinstance(source, dict)
        ]
        if len(source_ids) != len(set(source_ids)):
            errors.append("source configuration: source IDs must be unique")

    if plan.get("task_id") != envelope.get("task_id"):
        errors.append("routing plan: task_id must match the Task Envelope")
    validate_plan_state(plan, errors)
    validate_workflow_registry(workflow_registry, errors)
    validate_workflow_selection(envelope, plan, workflow_registry, errors)
    validate_skill_bindings(plan, errors)
    validate_overlay(overlay, errors)

    plan_source = plan.get("source")
    if isinstance(plan_source, dict) and isinstance(sources, list):
        matching = [
            source
            for source in sources
            if isinstance(source, dict)
            and source.get("id") == plan_source.get("source_id")
        ]
        if len(matching) != 1:
            errors.append("routing plan: source_id must resolve to exactly one configured source")
        else:
            configured = matching[0]
            for plan_key, source_key in (
                ("repository", "repository"),
                ("revision", "ref"),
                ("registry", "registry"),
            ):
                if plan_source.get(plan_key) != configured.get(source_key):
                    errors.append(
                        f"routing plan: source {plan_key} must match configured {source_key}"
                    )
    return errors


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Routing contract validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

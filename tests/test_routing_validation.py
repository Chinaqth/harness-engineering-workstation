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

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_repository_examples_are_valid(self) -> None:
        self.assertEqual(MODULE.validate(self.root), [])

    def test_routed_plan_requires_selection(self) -> None:
        path = self.root / "examples" / "routing-plan.json"
        plan = json.loads(path.read_text(encoding="utf-8"))
        plan["status"] = "routed"
        plan["conflicts"] = []
        path.write_text(json.dumps(plan), encoding="utf-8")
        self.assertTrue(
            any("requires at least one selection" in error for error in MODULE.validate(self.root))
        )

    def test_plan_must_reference_same_task(self) -> None:
        path = self.root / "examples" / "routing-plan.json"
        plan = json.loads(path.read_text(encoding="utf-8"))
        plan["task_id"] = "other-task"
        path.write_text(json.dumps(plan), encoding="utf-8")
        self.assertTrue(any("must match" in error for error in MODULE.validate(self.root)))


if __name__ == "__main__":
    unittest.main()

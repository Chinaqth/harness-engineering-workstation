from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("init_change", ROOT / "scripts" / "init_change.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class InitChangeTests(unittest.TestCase):
    def test_creates_record_in_explicit_non_git_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "plain-project"
            project.mkdir()
            destination = MODULE.create_change(ROOT, project, "20260809-example")
            self.assertEqual(destination, project / "changes" / "20260809-example")
            self.assertFalse((project / ".git").exists())
            self.assertTrue((destination / "requirements.md").is_file())
            self.assertIn("变更需求", (destination / "requirements.md").read_text(encoding="utf-8"))

    def test_rejects_implicit_or_invalid_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            with self.assertRaises(ValueError):
                MODULE.create_change(ROOT, project, "bad id")

    def test_refuses_to_overwrite_existing_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            MODULE.create_change(ROOT, project, "20260809-example")
            with self.assertRaises(ValueError):
                MODULE.create_change(ROOT, project, "20260809-example")


if __name__ == "__main__":
    unittest.main()

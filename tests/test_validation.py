from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


validate_change = load_script("validate_change", "validate_change.py")
knowledge_garden = load_script("knowledge_garden", "knowledge-garden.py")


class AcceptanceValidationTests(unittest.TestCase):
    def test_valid_done_record_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "acceptance.json"
            path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "change_id": "sample",
                        "risk": "G2",
                        "status": "done",
                        "criteria": [
                            {
                                "id": "AC-01",
                                "description": "An observable result.",
                                "status": "passing",
                                "evidence": ["tests: passed"],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(validate_change.validate_acceptance(path, "sample", "G2"), [])

    def test_done_record_rejects_pending_criterion(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "acceptance.json"
            path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "change_id": "sample",
                        "risk": "G2",
                        "status": "done",
                        "criteria": [
                            {
                                "id": "AC-01",
                                "description": "An observable result.",
                                "status": "pending",
                                "evidence": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            errors = validate_change.validate_acceptance(path, "sample", "G2")
            self.assertTrue(any("done change cannot contain" in error for error in errors))


class KnowledgeGardenTests(unittest.TestCase):
    def test_broken_relative_link_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "index.md").write_text("[Missing](missing.md)\n", encoding="utf-8")
            errors = knowledge_garden.broken_links(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("broken local link", errors[0])

    def test_done_change_is_not_subject_to_freshness_check(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            change = root / "changes" / "sample"
            change.mkdir(parents=True)
            (change / "requirements.md").write_text(
                "- Status: done\n- Review-By: 2020-01-01\n",
                encoding="utf-8",
            )
            self.assertEqual(
                knowledge_garden.stale_changes(root, knowledge_garden.dt.date(2026, 8, 28)),
                [],
            )


if __name__ == "__main__":
    unittest.main()

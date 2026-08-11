import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from schema_validation import validate_instance


class ProjectHarnessBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(
            (ROOT / "schemas" / "project-harness-bridge.schema.json").read_text(
                encoding="utf-8"
            )
        )
    def assert_valid(self, value):
        self.assertEqual(validate_instance(value, self.schema), [])

    def assert_invalid(self, value):
        self.assertNotEqual(validate_instance(value, self.schema), [])

    def test_accepts_exact_minimal_bridge(self):
        self.assert_valid({"contract_code": "harness-engineering", "enabled": True})
        self.assert_valid({"contract_code": "harness-engineering", "enabled": False})

    def test_rejects_contract_mismatch_and_non_boolean_enablement(self):
        self.assert_invalid({"contract_code": "Harness-Engineering", "enabled": True})
        self.assert_invalid({"contract_code": "harness-engineering", "enabled": "true"})

    def test_rejects_missing_or_additional_fields(self):
        self.assert_invalid({"enabled": True})
        self.assert_invalid(
            {
                "contract_code": "harness-engineering",
                "enabled": True,
                "mode": "full",
            }
        )


if __name__ == "__main__":
    unittest.main()

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_manifests.py"
SPEC = importlib.util.spec_from_file_location("validate_manifests", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

SHA = "a" * 64


def panel_fixture():
    models = []
    for index, name in enumerate(("a", "b", "c", "d", "e"), start=1):
        models.append(
            {
                "slot": f"P{index}",
                "provider": name,
                "model_id": "model",
            }
        )
    return {"models": models}


def completion_fixture():
    components = {
        name: {
            "status": "COMPLETE",
            "expected": 1,
            "completed": 1,
            "terminal": 1,
            "incomplete": 0,
            "content_sha256": SHA,
        }
        for name in MODULE.COMPONENTS
    }
    return {
        "overall_status": "COMPLETE",
        "components": components,
        "run_incomplete": 0,
        "namespace_hashes": {
            protocol: {
                "primary": SHA,
                "audit": SHA,
                "repeat": SHA,
                "sensitivity": None,
            }
            for protocol in ("DRRL", "ERL")
        },
    }


class ManifestInvariantTests(unittest.TestCase):
    def test_panel_accepts_unique_sorted_slots(self):
        self.assertEqual(MODULE.validate_panel(panel_fixture()), [])

    def test_panel_rejects_duplicate_or_misordered_slots(self):
        duplicate = panel_fixture()
        duplicate["models"][1]["slot"] = "P1"
        self.assertTrue(MODULE.validate_panel(duplicate))
        misordered = panel_fixture()
        misordered["models"][0]["provider"] = "z"
        self.assertTrue(MODULE.validate_panel(misordered))

    def test_completion_accepts_consistent_complete_manifest(self):
        self.assertEqual(MODULE.validate_completion(completion_fixture()), [])

    def test_completion_rejects_false_complete_manifest(self):
        payload = completion_fixture()
        component = next(iter(MODULE.COMPONENTS))
        payload["components"][component]["completed"] = 0
        payload["run_incomplete"] = 1
        errors = MODULE.validate_completion(payload)
        self.assertGreaterEqual(len(errors), 2)

    def test_protocol_lock_requires_all_roles(self):
        valid = {
            "files": [
                {"path": role, "role": role} for role in MODULE.REQUIRED_FILE_ROLES
            ],
            "stage0_excluded": True,
        }
        self.assertEqual(MODULE.validate_protocol_lock(valid), [])
        invalid = copy.deepcopy(valid)
        invalid["files"].pop()
        self.assertTrue(MODULE.validate_protocol_lock(invalid))


if __name__ == "__main__":
    unittest.main()

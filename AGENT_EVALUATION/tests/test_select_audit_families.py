import importlib.util
import sys
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "select_audit_families.py"
REPO = ROOT.parent
REGISTRY = (
    REPO / "evidence_maps/CANONICAL_FAMILY_REGISTRY.csv"
)
ALIAS_MAP = REPO / "evidence_maps/ALIAS_VERSION_MAP.csv"

SPEC = importlib.util.spec_from_file_location("select_audit_families", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = MODULE.build_selection(REGISTRY, ALIAS_MAP)

    def test_expected_sizes(self):
        self.assertEqual(self.result["eligible_family_count"], 98)
        self.assertEqual(len(self.result["stage0"]), 8)
        self.assertEqual(len(self.result["audit32"]), 32)
        self.assertEqual(len(self.result["repeat16"]), 16)
        self.assertEqual(len(self.result["primary_assignments"]), 98)

    def test_stratum_quotas(self):
        stage0 = Counter(
            (row["cluster"], row["eligibility_status"]) for row in self.result["stage0"]
        )
        audit = Counter(
            (row["cluster"], row["eligibility_status"])
            for row in self.result["audit32"]
        )
        repeat = Counter(
            (row["cluster"], row["eligibility_status"])
            for row in self.result["repeat16"]
        )
        for cluster in MODULE.CLUSTERS:
            for status in MODULE.STATUSES:
                self.assertEqual(stage0[(cluster, status)], 1)
                self.assertEqual(audit[(cluster, status)], 4)
                self.assertEqual(repeat[(cluster, status)], 2)

    def test_complex_quota_and_repeat_subset(self):
        self.assertGreaterEqual(
            sum(row["complex_lineage"] for row in self.result["audit32"]), 8
        )
        audit_keys = {row["family_key"] for row in self.result["audit32"]}
        repeat_keys = {row["family_key"] for row in self.result["repeat16"]}
        self.assertTrue(repeat_keys <= audit_keys)

    def test_stage0_is_excluded_from_formal_audit(self):
        stage0_keys = {row["family_key"] for row in self.result["stage0"]}
        audit_keys = {row["family_key"] for row in self.result["audit32"]}
        self.assertTrue(stage0_keys.isdisjoint(audit_keys))

    def test_offsets_and_primary_pairs(self):
        offsets = Counter(
            row["primary_pipeline"]["audit_offset"] for row in self.result["audit32"]
        )
        self.assertEqual(offsets, Counter({1: 8, 2: 8, 3: 8, 4: 8}))
        for assignment in self.result["primary_assignments"].values():
            self.assertNotEqual(assignment["retriever"], assignment["verifier"])
        pairs = Counter(
            (assignment["retriever"], assignment["verifier"])
            for assignment in self.result["primary_assignments"].values()
        )
        retrievers = Counter(
            assignment["retriever"]
            for assignment in self.result["primary_assignments"].values()
        )
        verifiers = Counter(
            assignment["verifier"]
            for assignment in self.result["primary_assignments"].values()
        )
        self.assertEqual(len(pairs), 20)
        self.assertLessEqual(max(pairs.values()) - min(pairs.values()), 1)
        self.assertLessEqual(max(retrievers.values()) - min(retrievers.values()), 1)
        self.assertLessEqual(max(verifiers.values()) - min(verifiers.values()), 1)

    def test_is_deterministic(self):
        again = MODULE.build_selection(REGISTRY, ALIAS_MAP)
        self.assertEqual(self.result, again)


if __name__ == "__main__":
    unittest.main()

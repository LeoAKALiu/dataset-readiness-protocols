import json
import re
import unittest
from copy import deepcopy
from pathlib import Path
from urllib.parse import unquote

from jsonschema import Draft202012Validator


AGENT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = AGENT_ROOT.parent
SHA = "a" * 64


def load_schema(name):
    return json.loads((AGENT_ROOT / "schemas" / name).read_text(encoding="utf-8"))


def valid_panel():
    return {
        "panel_id": "panel-1",
        "pi_agent": {
            "version_or_commit": "1.0.0",
            "config_sha256": SHA,
            "adapter_manifest_sha256": SHA,
        },
        "tool_registry_sha256": SHA,
        "prompt_manifest_sha256": SHA,
        "models": [
            {
                "slot": f"P{index}",
                "provider": provider,
                "model_id": "model",
                "display_name": provider,
                "route_id": None,
                "invocation_mode": "oauth",
                "adapter_version": "1.0.0",
                "account_tier": None,
                "exposed_parameters": {},
                "provider_managed_parameters": ["temperature", "seed"],
            }
            for index, provider in enumerate(("a", "b", "c", "d", "e"), start=1)
        ],
        "created_at": "2026-08-19T00:00:00Z",
    }


def valid_completion():
    component = {
        "status": "COMPLETE",
        "expected": 1,
        "completed": 1,
        "terminal": 1,
        "incomplete": 0,
        "content_sha256": SHA,
    }
    return {
        "protocol_lock_id": "lock-1",
        "panel_id": "panel-1",
        "run_id": "run-1",
        "overall_status": "COMPLETE",
        "components": {
            name: deepcopy(component)
            for name in (
                "DRRL_PRIMARY_COMPLETE",
                "ERL_ELIGIBILITY_COMPLETE",
                "ERL_PRIMARY_COMPLETE",
                "DRRL_AGENT_AUDIT_COMPLETE",
                "ERL_AGENT_AUDIT_COMPLETE",
                "DRRL_REPEAT_AUDIT_COMPLETE",
                "ERL_REPEAT_AUDIT_COMPLETE",
                "HUMAN_REFERENCE_COMPLETE",
                "ANALYSIS_COMPLETE",
            )
        },
        "namespace_hashes": {
            protocol: {
                "primary": SHA,
                "audit": SHA,
                "repeat": SHA,
                "sensitivity": None,
            }
            for protocol in ("DRRL", "ERL")
        },
        "unresolved_after_review": 0,
        "run_incomplete": 0,
        "input_sha256": SHA,
        "output_sha256": SHA,
        "code_sha256": SHA,
        "environment_sha256": SHA,
        "generated_at": "2026-08-19T00:00:00Z",
    }


def valid_evidence_packet():
    return {
        "packet_id": "packet-1",
        "protocol_lock_id": "lock-1",
        "run_id": "run-1",
        "replicate_id": "replicate-1",
        "namespace": "primary",
        "evaluation_unit": {
            "family_key": "family-1",
            "release_key": "release-1",
            "evaluation_unit_id": "unit-1",
            "cluster": "A",
        },
        "protocol": "DRRL",
        "field_id": "A1",
        "role": "RETRIEVER",
        "model_slot": "P1",
        "raw_value": "value",
        "normalized_value": "value",
        "unit": None,
        "statistical_object": None,
        "applicability": "APPLICABLE",
        "sources": [
            {
                "url": "https://example.org/source",
                "normalized_url": "https://example.org/source",
                "accessed_at": "2026-08-19T00:00:00Z",
                "source_type": "official_dataset_page",
                "locator": "metadata table",
                "excerpt": "value",
                "content_sha256": SHA,
                "http_status": 200,
                "cache_ref": "cache/source.html",
            }
        ],
        "evidence_quality": "Q2",
        "authority_scope": ["artifact_contents"],
        "proposal_origin": "PROPOSED_BY_RETRIEVER",
        "comparison_result": "NOT_RUN",
        "verification_state": "ACCEPTED",
        "terminal_reason": None,
        "parent_packet_ids": [],
        "created_at": "2026-08-19T00:00:00Z",
    }


def valid_prompt_manifest():
    names = (
        "common_system_contract",
        "protocol_field_contract",
        "cluster_dictionary_adapter",
        "role_adapter",
    )
    return {
        "prompt_manifest_id": "prompt-1",
        "render_order": list(names),
        "components": [
            {
                "name": name,
                "path": f"prompts/{name}.md",
                "version": "1.0.0",
                "sha256": SHA,
            }
            for name in names
        ],
        "rendered_prompt_path": "rendered/prompt-1.txt",
        "rendered_prompt_sha256": SHA,
        "role_output_schema_sha256": SHA,
        "created_at": "2026-08-19T00:00:00Z",
    }


class RepositoryContractTests(unittest.TestCase):
    def test_all_json_schemas_parse(self):
        schemas = sorted((AGENT_ROOT / "schemas").glob("*.json"))
        self.assertGreaterEqual(len(schemas), 5)
        for schema in schemas:
            with self.subTest(schema=schema.name):
                payload = json.loads(schema.read_text(encoding="utf-8"))
                self.assertEqual(
                    payload["$schema"],
                    "https://json-schema.org/draft/2020-12/schema",
                )
                Draft202012Validator.check_schema(payload)

    def test_panel_schema_requires_each_slot_once(self):
        validator = Draft202012Validator(load_schema("panel-manifest.schema.json"))
        payload = valid_panel()
        self.assertEqual(list(validator.iter_errors(payload)), [])
        payload["models"][1]["slot"] = "P1"
        self.assertTrue(list(validator.iter_errors(payload)))

    def test_completion_schema_rejects_false_overall_complete(self):
        validator = Draft202012Validator(load_schema("completion-manifest.schema.json"))
        payload = valid_completion()
        self.assertEqual(list(validator.iter_errors(payload)), [])
        payload["components"]["ANALYSIS_COMPLETE"]["status"] = "IN_PROGRESS"
        self.assertTrue(list(validator.iter_errors(payload)))

    def test_evidence_schema_rejects_q0_accepted_packet(self):
        validator = Draft202012Validator(load_schema("evidence-packet.schema.json"))
        payload = valid_evidence_packet()
        self.assertEqual(list(validator.iter_errors(payload)), [])
        payload["evidence_quality"] = "Q0"
        payload["sources"] = []
        self.assertTrue(list(validator.iter_errors(payload)))

    def test_protocol_lock_schema_requires_every_file_role(self):
        schema = load_schema("protocol-lock.schema.json")
        validator = Draft202012Validator(schema)
        roles = (
            "protocol",
            "dictionary",
            "prompt",
            "schema",
            "normalizer",
            "metric_runner",
            "rule_engine",
            "analysis_plan",
            "completion_spec",
        )
        payload = {
            "protocol_lock_id": "lock-1",
            "repository_commit": "a" * 40,
            "registry_sha256": SHA,
            "alias_map_sha256": SHA,
            "panel_manifest_sha256": SHA,
            "selection_manifest_sha256": SHA,
            "files": [
                {"path": f"{role}.json", "sha256": SHA, "role": role} for role in roles
            ],
            "stage0_excluded": True,
            "created_at": "2026-08-19T00:00:00Z",
        }
        self.assertEqual(list(validator.iter_errors(payload)), [])
        payload["files"].pop()
        self.assertTrue(list(validator.iter_errors(payload)))

    def test_prompt_manifest_requires_four_distinct_components_and_render(self):
        validator = Draft202012Validator(load_schema("prompt-manifest.schema.json"))
        payload = valid_prompt_manifest()
        self.assertEqual(list(validator.iter_errors(payload)), [])
        payload["components"][1]["name"] = "common_system_contract"
        self.assertTrue(list(validator.iter_errors(payload)))

    def test_local_markdown_links_resolve(self):
        markdown_files = [
            REPO_ROOT / "README.md",
            REPO_ROOT / "DRRL/DRRL_EVALUATION_PROTOCOL.md",
            REPO_ROOT / "ERL/ERL_EVALUATION_PROTOCOL.md",
            *sorted(AGENT_ROOT.glob("*.md")),
        ]
        missing = []
        for markdown in markdown_files:
            content = markdown.read_text(encoding="utf-8")
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", content):
                if (
                    "://" in target
                    or target.startswith("#")
                    or target.startswith("mailto:")
                ):
                    continue
                local_target = unquote(target.split("#", 1)[0])
                if not (markdown.parent / local_target).resolve().exists():
                    missing.append((str(markdown), target))
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Validate semantic invariants not expressible cleanly in JSON Schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SLOTS = ("P1", "P2", "P3", "P4", "P5")
REQUIRED_FILE_ROLES = {
    "protocol",
    "dictionary",
    "prompt",
    "schema",
    "normalizer",
    "metric_runner",
    "rule_engine",
    "analysis_plan",
    "completion_spec",
}
COMPONENTS = {
    "DRRL_PRIMARY_COMPLETE",
    "ERL_ELIGIBILITY_COMPLETE",
    "ERL_PRIMARY_COMPLETE",
    "DRRL_AGENT_AUDIT_COMPLETE",
    "ERL_AGENT_AUDIT_COMPLETE",
    "DRRL_REPEAT_AUDIT_COMPLETE",
    "ERL_REPEAT_AUDIT_COMPLETE",
    "HUMAN_REFERENCE_COMPLETE",
    "ANALYSIS_COMPLETE",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_panel(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    models = payload.get("models", [])
    slots = [model.get("slot") for model in models]
    if sorted(slots) != sorted(SLOTS):
        errors.append("panel must contain each slot P1-P5 exactly once")
    canonical = sorted(
        models,
        key=lambda model: (
            str(model.get("provider", "")).casefold(),
            str(model.get("model_id", "")).casefold(),
        ),
    )
    expected_slots = list(SLOTS)
    observed_slots = [model.get("slot") for model in canonical]
    if observed_slots != expected_slots:
        errors.append(
            "panel slots must follow normalized provider/model_id dictionary order"
        )
    return errors


def validate_protocol_lock(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    files = payload.get("files", [])
    roles = {item.get("role") for item in files}
    missing_roles = sorted(REQUIRED_FILE_ROLES - roles)
    if missing_roles:
        errors.append(f"protocol lock missing file roles: {missing_roles}")
    paths = [item.get("path") for item in files]
    if len(paths) != len(set(paths)):
        errors.append("protocol lock contains duplicate file paths")
    if payload.get("stage0_excluded") is not True:
        errors.append("protocol lock must exclude Stage-0 outputs")
    return errors


def validate_completion(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    components = payload.get("components", {})
    if set(components) != COMPONENTS:
        errors.append("completion manifest must contain exactly seven component gates")
    for name, component in components.items():
        if component.get("status") != "COMPLETE":
            continue
        expected = component.get("expected")
        if not (expected == component.get("completed") == component.get("terminal")):
            errors.append(f"{name}: COMPLETE requires expected=completed=terminal")
        if component.get("incomplete") != 0:
            errors.append(f"{name}: COMPLETE requires incomplete=0")
        if not component.get("content_sha256"):
            errors.append(f"{name}: COMPLETE requires content_sha256")

    if payload.get("overall_status") == "COMPLETE":
        incomplete_components = [
            name
            for name, component in components.items()
            if component.get("status") != "COMPLETE"
        ]
        if incomplete_components:
            errors.append(
                "overall COMPLETE has incomplete components: "
                + ", ".join(sorted(incomplete_components))
            )
        if payload.get("run_incomplete") != 0:
            errors.append("overall COMPLETE requires run_incomplete=0")
        namespaces = payload.get("namespace_hashes", {})
        for protocol in ("DRRL", "ERL"):
            protocol_namespaces = namespaces.get(protocol, {})
            for namespace in ("primary", "audit", "repeat"):
                if not protocol_namespaces.get(namespace):
                    errors.append(
                        f"overall COMPLETE requires {protocol}/{namespace} "
                        "namespace hash"
                    )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel", type=Path)
    parser.add_argument("--protocol-lock", type=Path)
    parser.add_argument("--completion", type=Path)
    args = parser.parse_args()
    requested = [args.panel, args.protocol_lock, args.completion]
    if not any(requested):
        parser.error("provide at least one manifest path")

    errors: list[str] = []
    if args.panel:
        errors.extend(
            f"panel: {error}" for error in validate_panel(load_json(args.panel))
        )
    if args.protocol_lock:
        errors.extend(
            f"protocol-lock: {error}"
            for error in validate_protocol_lock(load_json(args.protocol_lock))
        )
    if args.completion:
        errors.extend(
            f"completion: {error}"
            for error in validate_completion(load_json(args.completion))
        )
    if errors:
        raise SystemExit("\n".join(errors))
    print("manifest invariants: OK")


if __name__ == "__main__":
    main()

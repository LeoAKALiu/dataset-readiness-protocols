#!/usr/bin/env python3
"""Deterministically select Stage-0, audit-32, and repeat-16 families.

This script also creates a balanced primary retriever/verifier allocation. It
does not select release/task sentinels; those must be frozen in the protocol
lock using the documented sentinel precedence rules.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Iterable


CLUSTERS = ("A", "B", "C", "D")
STATUSES = ("include", "provisional")
SLOTS = ("P1", "P2", "P3", "P4", "P5")
COMPLEX_TOKENS = ("derivative", "composite", "expanded", "subset")
SELECTION_DOMAIN = "drrl-erl-agent-selection-v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def load_registry(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    eligible = [
        row
        for row in rows
        if row["cluster"] in CLUSTERS and row["eligibility_status"] in STATUSES
    ]
    keys = [row["family_key"] for row in eligible]
    if len(keys) != len(set(keys)):
        raise ValueError("eligible registry contains duplicate family_key values")
    return eligible


def load_complex_families(path: Path) -> set[str]:
    separate_counts: Counter[str] = Counter()
    relations: dict[str, list[str]] = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            key = row["family_key"]
            if row["separate_evaluation_unit"].strip().lower() == "yes":
                separate_counts[key] += 1
            relations[key].append(row["relation_to_family"].lower())
    complex_keys = {key for key, count in separate_counts.items() if count >= 2}
    complex_keys.update(
        key
        for key, values in relations.items()
        if any(token in value for value in values for token in COMPLEX_TOKENS)
    )
    return complex_keys


def rank_row(
    registry_sha: str,
    lock_label: str,
    selection: str,
    row: dict[str, str],
) -> str:
    return digest(
        registry_sha,
        lock_label,
        selection,
        row["cluster"],
        row["eligibility_status"],
        row["family_key"],
    )


def grouped_selection(
    rows: list[dict[str, str]],
    registry_sha: str,
    lock_label: str,
    selection: str,
    per_stratum: int,
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for cluster in CLUSTERS:
        for status in STATUSES:
            group = [
                row
                for row in rows
                if row["cluster"] == cluster and row["eligibility_status"] == status
            ]
            if len(group) < per_stratum:
                raise ValueError(
                    f"stratum {cluster}/{status} has {len(group)} rows; "
                    f"requires {per_stratum}"
                )
            group.sort(
                key=lambda row: rank_row(registry_sha, lock_label, selection, row)
            )
            selected.extend(group[:per_stratum])
    return selected


def enforce_complex_quota(
    selected: list[dict[str, str]],
    population: list[dict[str, str]],
    complex_keys: set[str],
    quota: int,
    registry_sha: str,
    lock_label: str,
) -> list[dict[str, str]]:
    result = list(selected)
    while sum(row["family_key"] in complex_keys for row in result) < quota:
        selected_keys = {row["family_key"] for row in result}
        candidates = [
            row
            for row in population
            if row["family_key"] in complex_keys
            and row["family_key"] not in selected_keys
            and any(
                chosen["cluster"] == row["cluster"]
                and chosen["eligibility_status"] == row["eligibility_status"]
                and chosen["family_key"] not in complex_keys
                for chosen in result
            )
        ]
        if not candidates:
            raise ValueError(f"cannot satisfy complex-family quota {quota}")
        candidates.sort(
            key=lambda row: rank_row(registry_sha, lock_label, "audit32_complex", row)
        )
        incoming = candidates[0]
        replaceable = [
            row
            for row in result
            if row["cluster"] == incoming["cluster"]
            and row["eligibility_status"] == incoming["eligibility_status"]
            and row["family_key"] not in complex_keys
        ]
        outgoing = max(
            replaceable,
            key=lambda row: rank_row(registry_sha, lock_label, "audit32", row),
        )
        result[result.index(outgoing)] = incoming
    return result


def assign_audit_offsets(
    audit_rows: list[dict[str, str]], registry_sha: str, lock_label: str
) -> dict[str, int]:
    offsets: dict[str, int] = {}
    pattern = (1, 2, 3, 4, 1, 2, 3, 4)
    for cluster in CLUSTERS:
        group = [row for row in audit_rows if row["cluster"] == cluster]
        if len(group) != 8:
            raise ValueError(f"audit cluster {cluster} must contain 8 families")
        group.sort(
            key=lambda row: rank_row(registry_sha, lock_label, "audit_offset", row)
        )
        for row, offset in zip(group, pattern, strict=True):
            offsets[row["family_key"]] = offset
    return offsets


def interleaved_population(
    rows: list[dict[str, str]], registry_sha: str, lock_label: str
) -> Iterable[dict[str, str]]:
    for cluster in CLUSTERS:
        queues: dict[str, deque[dict[str, str]]] = {}
        for status in STATUSES:
            group = [
                row
                for row in rows
                if row["cluster"] == cluster and row["eligibility_status"] == status
            ]
            group.sort(
                key=lambda row: rank_row(registry_sha, lock_label, "primary_order", row)
            )
            queues[status] = deque(group)
        while any(queues.values()):
            for status in STATUSES:
                if queues[status]:
                    yield queues[status].popleft()


def assign_primary_pairs(
    rows: list[dict[str, str]],
    audit_offsets: dict[str, int],
    registry_sha: str,
    lock_label: str,
) -> dict[str, dict[str, object]]:
    all_pairs = [(i, j) for i in range(5) for j in range(5) if i != j]
    base, extra = divmod(len(rows), len(all_pairs))
    pair_targets: Counter[tuple[int, int]] = Counter({pair: base for pair in all_pairs})
    extra_retrievers: Counter[int] = Counter()
    extra_verifiers: Counter[int] = Counter()
    extra_pairs: set[tuple[int, int]] = set()
    while len(extra_pairs) < extra:
        candidates = [pair for pair in all_pairs if pair not in extra_pairs]

        def extra_cost(pair: tuple[int, int]) -> tuple[object, ...]:
            i, j = pair
            return (
                extra_retrievers[i],
                extra_verifiers[j],
                digest(
                    registry_sha,
                    lock_label,
                    "pair_target_extra",
                    str(i),
                    str(j),
                ),
            )

        chosen_extra = min(candidates, key=extra_cost)
        extra_pairs.add(chosen_extra)
        extra_retrievers[chosen_extra[0]] += 1
        extra_verifiers[chosen_extra[1]] += 1
        pair_targets[chosen_extra] += 1

    global_pairs: Counter[tuple[int, int]] = Counter()
    cluster_pairs: Counter[tuple[str, int, int]] = Counter()
    stratum_pairs: Counter[tuple[str, str, int, int]] = Counter()
    global_retrievers: Counter[int] = Counter()
    global_verifiers: Counter[int] = Counter()
    stratum_retrievers: Counter[tuple[str, str, int]] = Counter()
    stratum_verifiers: Counter[tuple[str, str, int]] = Counter()
    assignments: dict[str, dict[str, object]] = {}

    audit_rows = [row for row in rows if row["family_key"] in audit_offsets]
    audit_rows.sort(
        key=lambda row: rank_row(registry_sha, lock_label, "primary_audit_order", row)
    )
    non_audit_rows = [
        row
        for row in interleaved_population(rows, registry_sha, lock_label)
        if row["family_key"] not in audit_offsets
    ]

    for row in [*audit_rows, *non_audit_rows]:
        cluster = row["cluster"]
        status = row["eligibility_status"]
        offset = audit_offsets.get(row["family_key"])
        allowed = (
            [(i, (i + offset) % 5) for i in range(5)]
            if offset is not None
            else all_pairs
        )
        candidates = [
            pair for pair in allowed if global_pairs[pair] < pair_targets[pair]
        ]
        if not candidates:
            raise ValueError(
                f"no remaining primary-pair capacity for {row['family_key']}"
            )

        def cost(pair: tuple[int, int]) -> tuple[object, ...]:
            i, j = pair
            return (
                global_pairs[(i, j)] / pair_targets[(i, j)],
                global_retrievers[i],
                global_verifiers[j],
                cluster_pairs[(cluster, i, j)],
                stratum_pairs[(cluster, status, i, j)],
                stratum_retrievers[(cluster, status, i)],
                stratum_verifiers[(cluster, status, j)],
                digest(
                    registry_sha,
                    lock_label,
                    "primary_pair_tie",
                    row["family_key"],
                    str(i),
                    str(j),
                ),
            )

        chosen = min(candidates, key=cost)
        i, j = chosen
        global_pairs[chosen] += 1
        cluster_pairs[(cluster, i, j)] += 1
        stratum_pairs[(cluster, status, i, j)] += 1
        global_retrievers[i] += 1
        global_verifiers[j] += 1
        stratum_retrievers[(cluster, status, i)] += 1
        stratum_verifiers[(cluster, status, j)] += 1
        assignments[row["family_key"]] = {
            "retriever": SLOTS[i],
            "verifier": SLOTS[j],
            "audit_offset": offset,
        }
    if global_pairs != pair_targets:
        raise AssertionError("primary-pair allocation did not fill exact targets")
    return assignments


def compact_row(
    row: dict[str, str],
    complex_keys: set[str],
    primary_assignments: dict[str, dict[str, object]],
) -> dict[str, object]:
    return {
        "family_key": row["family_key"],
        "canonical_name": row["canonical_name"],
        "cluster": row["cluster"],
        "eligibility_status": row["eligibility_status"],
        "complex_lineage": row["family_key"] in complex_keys,
        "primary_pipeline": primary_assignments[row["family_key"]],
    }


def build_selection(registry_path: Path, alias_map_path: Path) -> dict[str, object]:
    registry_sha = file_sha256(registry_path)
    alias_sha = file_sha256(alias_map_path)
    selection_seed = digest(registry_sha, alias_sha, SELECTION_DOMAIN)
    lock_label = selection_seed
    rows = load_registry(registry_path)
    complex_keys = load_complex_families(alias_map_path)

    stage0 = grouped_selection(rows, registry_sha, lock_label, "stage0", per_stratum=1)
    stage0_keys = {row["family_key"] for row in stage0}
    audit_population = [row for row in rows if row["family_key"] not in stage0_keys]
    audit = grouped_selection(
        audit_population, registry_sha, lock_label, "audit32", per_stratum=4
    )
    audit = enforce_complex_quota(
        audit,
        audit_population,
        complex_keys,
        quota=8,
        registry_sha=registry_sha,
        lock_label=lock_label,
    )
    audit_offsets = assign_audit_offsets(audit, registry_sha, lock_label)
    primary_assignments = assign_primary_pairs(
        rows, audit_offsets, registry_sha, lock_label
    )

    audit_keys = {row["family_key"] for row in audit}
    repeat_population = [row for row in rows if row["family_key"] in audit_keys]
    repeat16 = grouped_selection(
        repeat_population,
        registry_sha,
        lock_label,
        "repeat16",
        per_stratum=2,
    )

    sort_key = lambda row: (  # noqa: E731 - compact deterministic serializer
        row["cluster"],
        row["eligibility_status"],
        row["family_key"],
    )
    return {
        "selection_algorithm": "sha256-stratified-v1",
        "selection_domain": SELECTION_DOMAIN,
        "selection_seed": selection_seed,
        "registry_sha256": registry_sha,
        "alias_map_sha256": alias_sha,
        "eligible_family_count": len(rows),
        "complex_family_rule": {
            "minimum_separate_units": 2,
            "relation_tokens": list(COMPLEX_TOKENS),
            "audit_minimum": 8,
        },
        "stage0": [
            compact_row(row, complex_keys, primary_assignments)
            for row in sorted(stage0, key=sort_key)
        ],
        "audit32": [
            compact_row(row, complex_keys, primary_assignments)
            for row in sorted(audit, key=sort_key)
        ],
        "repeat16": [
            compact_row(row, complex_keys, primary_assignments)
            for row in sorted(repeat16, key=sort_key)
        ],
        "primary_assignments": {
            key: primary_assignments[key] for key in sorted(primary_assignments)
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--alias-map", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_selection(args.registry, args.alias_map)
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the ISM mapping schema and prove every public check is accounted for."""

from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOCK = ROOT / "mapping/provenance.lock.yaml"


def key(check: dict[str, str]) -> tuple[str, str]:
    return check["engine"], check.get("rule_id") or check["policy"]


def kyverno_inventory(repo: Path) -> set[tuple[str, str]]:
    inventory = set()
    for path in repo.glob("policies/**/*.yaml"):
        if path.name == "kyverno-test.yaml":
            continue
        for document in yaml.safe_load_all(path.read_text()):
            if isinstance(document, dict) and document.get("kind") == "ClusterPolicy":
                inventory.add(("kyverno", document["metadata"]["name"]))
    return inventory


def kubescape_inventory(repo: Path) -> set[tuple[str, str]]:
    inventory = set()
    for path in repo.glob("rules/*/rule.metadata.json"):
        inventory.add(("kubescape", json.loads(path.read_text())["name"]))
    return inventory


def expected_ids(data: dict) -> dict[tuple[str, str], list[str]]:
    expected: dict[tuple[str, str], set[str]] = defaultdict(set)
    for control in data["controls"]:
        for check in control["checks"]:
            expected[key(check)].add(control["ism_id"])
    for check in data["unmapped"]:
        expected.setdefault(key(check), set())
    return {check: sorted(ids) for check, ids in expected.items()}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    if actual != expected:
        raise SystemExit(f"{label} checksum differs: want {expected}, got {actual}")


def validate_provenance(data: dict, lock: dict, regolibrary: Path | None) -> None:
    upstream_lock = lock["sources"]["kubescape_regolibrary"]
    kubescape_checks = [
        check
        for control in data["controls"]
        for check in control["checks"]
        if check["engine"] == "kubescape"
    ] + [check for check in data["unmapped"] if check["engine"] == "kubescape"]

    errors = []
    seen = set()
    for check in kubescape_checks:
        identity = key(check)
        if identity in seen:
            continue
        seen.add(identity)
        provenance = check.get("provenance")
        if not provenance:
            errors.append(f"{identity[1]} has no provenance decision")
            continue
        upstream = provenance.get("upstream")
        if provenance["disposition"] == "adapt" and not upstream:
            errors.append(f"{identity[1]} is {provenance['disposition']} but has no upstream source")
            continue
        if provenance["disposition"] == "custom" and upstream:
            errors.append(f"{identity[1]} is custom but declares an upstream source")
            continue
        if not upstream:
            continue
        if upstream["repository"] != upstream_lock["repository"] or upstream["ref"] != upstream_lock["ref"]:
            errors.append(f"{identity[1]} does not use the locked Kubescape source")
            continue
        if regolibrary:
            control_files = list(regolibrary.glob(f"controls/{upstream['control_id']}-*.json"))
            rule_files = [
                path
                for path in regolibrary.glob("rules/*/rule.metadata.json")
                if json.loads(path.read_text()).get("name") == upstream["rule_name"]
            ]
            if len(control_files) != 1:
                errors.append(f"{identity[1]} cannot resolve upstream control {upstream['control_id']}")
            elif upstream["rule_name"] not in json.loads(control_files[0].read_text()).get("rulesNames", []):
                errors.append(f"{identity[1]} upstream control does not include rule {upstream['rule_name']}")
            if len(rule_files) != 1:
                errors.append(f"{identity[1]} cannot resolve upstream rule {upstream['rule_name']}")
    if errors:
        raise SystemExit("invalid Kubescape provenance:\n" + "\n".join(errors))


def profile_ids(profile: dict) -> list[str]:
    return sorted(
        value.upper()
        for imported in profile["profile"]["imports"]
        for included in imported.get("include-controls", [])
        for value in included.get("with-ids", [])
    )


def catalog_controls(value: object) -> dict[str, dict]:
    controls = {}
    if isinstance(value, dict):
        control_id = value.get("id", "")
        if control_id.startswith("ism-"):
            controls[control_id.upper()] = value
        for child in value.values():
            controls.update(catalog_controls(child))
    elif isinstance(value, list):
        for child in value:
            controls.update(catalog_controls(child))
    return controls


def statement(control: dict) -> str | None:
    return next((part.get("prose") for part in control.get("parts", []) if part.get("name") == "statement"), None)


def validate_authorities(
    data: dict,
    lock: dict,
    catalog_path: Path | None,
    profile_path: Path | None,
    controls_path: Path | None,
) -> None:
    locked_ids = lock["profiles"]["e8_ml2"]["controls"]
    if locked_ids != sorted(set(locked_ids)) or len(locked_ids) != 87:
        raise SystemExit("locked E8 ML2 profile must contain 87 unique ISM IDs in sorted order")

    sources = lock["sources"]
    if catalog_path:
        validate_hash(catalog_path, sources["asd_ism_catalog"]["sha256"], "ASD ISM catalog")
        catalog = catalog_controls(json.loads(catalog_path.read_text()))
        errors = []
        for control in data["controls"]:
            upstream = catalog.get(control["ism_id"])
            if not upstream:
                errors.append(f"{control['ism_id']} is absent from the ASD catalog")
            elif statement(upstream) != control["title"]:
                errors.append(f"{control['ism_id']} title differs from the ASD statement")
        if errors:
            raise SystemExit("ASD catalog mismatch:\n" + "\n".join(errors))

    if profile_path:
        validate_hash(profile_path, sources["asd_e8_ml2_profile"]["sha256"], "ASD E8 ML2 profile")
        actual_ids = profile_ids(json.loads(profile_path.read_text()))
        if actual_ids != locked_ids:
            raise SystemExit("locked E8 ML2 control IDs differ from the supplied ASD profile")

    if controls_path:
        validate_hash(controls_path, sources["kubescape_control_inventory"]["sha256"], "Kubescape control inventory")


def validate_embedded_ids(data: dict, framework_repo: Path | None) -> None:
    expected = expected_ids(data)
    mismatches = []
    for path in ROOT.glob("policies/**/*.yaml"):
        if path.name == "kyverno-test.yaml":
            continue
        for document in yaml.safe_load_all(path.read_text()):
            if not isinstance(document, dict) or document.get("kind") != "ClusterPolicy":
                continue
            name = document["metadata"]["name"]
            raw = document["metadata"].get("annotations", {}).get("latticework.systems/ism-controls")
            try:
                actual = json.loads(raw)
            except (TypeError, json.JSONDecodeError):
                actual = None
            if actual != expected[("kyverno", name)]:
                mismatches.append(f"{path}:{name}={actual!r}")

    if framework_repo:
        for path in framework_repo.glob("rules/*/rule.metadata.json"):
            metadata = json.loads(path.read_text())
            actual = metadata.get("attributes", {}).get("ismControls")
            if actual != expected[("kubescape", metadata["name"])]:
                mismatches.append(f"{path}:{metadata['name']}={actual!r}")

    if mismatches:
        raise SystemExit("embedded ISM metadata differs from mapping:\n" + "\n".join(mismatches))


def format_keys(values: set[tuple[str, str]]) -> str:
    return ", ".join(f"{engine}:{name}" for engine, name in sorted(values))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", type=Path, default=ROOT / "mapping/ism-mapping.yaml")
    parser.add_argument("--schema", type=Path, default=ROOT / "mapping/schema/ism-mapping.schema.json")
    parser.add_argument("--provenance-lock", type=Path, default=DEFAULT_LOCK)
    parser.add_argument("--framework-repo", type=Path)
    parser.add_argument("--asd-catalog", type=Path)
    parser.add_argument("--e8-profile", type=Path)
    parser.add_argument("--kubescape-controls", type=Path)
    parser.add_argument("--regolibrary", type=Path)
    args = parser.parse_args()

    data = yaml.safe_load(args.mapping.read_text())
    schema = json.loads(args.schema.read_text())
    lock = yaml.safe_load(args.provenance_lock.read_text())
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda error: list(error.path))
    if errors:
        raise SystemExit("\n".join(f"schema: {'/'.join(map(str, error.path))}: {error.message}" for error in errors))

    ids = [control["ism_id"] for control in data["controls"]]
    if ids != sorted(ids) or len(ids) != len(set(ids)):
        raise SystemExit("controls must have unique ISM IDs in sorted order")

    if args.regolibrary and not args.regolibrary.is_dir():
        raise SystemExit(f"Kubescape regolibrary not found: {args.regolibrary}")
    validate_provenance(data, lock, args.regolibrary)
    validate_authorities(data, lock, args.asd_catalog, args.e8_profile, args.kubescape_controls)

    mapped = {key(check) for control in data["controls"] for check in control["checks"]}
    unmapped = {key(check) for check in data["unmapped"]}
    overlap = mapped & unmapped
    if overlap:
        raise SystemExit(f"checks cannot be both mapped and unmapped: {format_keys(overlap)}")

    inventory = kyverno_inventory(ROOT)
    engines = {"kyverno"}
    if args.framework_repo:
        if not args.framework_repo.is_dir():
            raise SystemExit(f"framework repository not found: {args.framework_repo}")
        inventory |= kubescape_inventory(args.framework_repo)
        engines.add("kubescape")

    expected_inventory = {check for check in mapped | unmapped if check[0] in engines}
    missing = inventory - expected_inventory
    stale = expected_inventory - inventory
    if missing:
        raise SystemExit(f"orphan checks: {format_keys(missing)}")
    if stale:
        raise SystemExit(f"unknown checks in mapping: {format_keys(stale)}")

    validate_embedded_ids(data, args.framework_repo)

    profile_ids = set(lock["profiles"]["e8_ml2"]["controls"])
    profile_total = len(profile_ids)
    profile_mapped = len(profile_ids & set(ids))
    print(
        f"valid: {len(ids)} detector-backed ISM controls; {profile_mapped} of {profile_total} in the locked E8 ML2 profile, "
        f"{len(mapped)} mapped checks, {len(unmapped)} explicitly unmapped checks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

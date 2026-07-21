#!/usr/bin/env python3
"""Generate stable compatibility views from the canonical ISM mapping."""

from __future__ import annotations

import argparse
from collections import defaultdict
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "mapping/ism-mapping.yaml"
PROVENANCE_LOCK = ROOT / "mapping/provenance.lock.yaml"
DEFAULT_OUTPUT = ROOT / "mapping/views/e8.yaml"
DEFAULT_KUBESCAPE_OUTPUT = ROOT / "mapping/views/kubescape.json"
STRATEGIES = {
    "application-control": ("E8-01", "Application control"),
    "patch-applications": ("E8-02", "Patch applications"),
    "configure-microsoft-office-macro-settings": ("E8-03", "Configure Microsoft Office macro settings"),
    "user-application-hardening": ("E8-04", "User application hardening"),
    "restrict-admin-privileges": ("E8-05", "Restrict administrative privileges"),
    "patch-operating-systems": ("E8-06", "Patch operating systems"),
    "multi-factor-authentication": ("E8-07", "Multi-factor authentication"),
    "regular-backups": ("E8-08", "Regular backups"),
}


def check_key(check: dict[str, str]) -> tuple[str, str]:
    return check["engine"], check.get("rule_id") or check["policy"]


def render(source: Path = SOURCE, provenance_lock: Path = PROVENANCE_LOCK) -> str:
    data = yaml.safe_load(source.read_text())
    lock = yaml.safe_load(provenance_lock.read_text())
    controls_by_strategy: dict[str, list[str]] = defaultdict(list)
    checks: dict[tuple[str, str], dict[str, object]] = {}

    for control in data["controls"]:
        e8_view = control["views"]["e8"]
        if not e8_view:
            continue
        strategy = e8_view["strategy"]
        controls_by_strategy[strategy].append(control["ism_id"])
        for check in control["checks"]:
            key = check_key(check)
            item = checks.setdefault(key, {**{k: v for k, v in check.items() if k != "coverage"}, "ism_ids": [], "coverage": check["coverage"]})
            item["ism_ids"].append(control["ism_id"])
            if check["coverage"] == "partial":
                item["coverage"] = "partial"

    strategies = []
    for slug, (strategy_id, name) in STRATEGIES.items():
        ids = sorted(controls_by_strategy.get(slug, []))
        strategies.append({"id": strategy_id, "name": name, "ismControls": [value.removeprefix("ISM-") for value in ids]})

    profile_controls = lock["profiles"]["e8_ml2"]["controls"]
    detector_backed = sorted(set(profile_controls) & {control["ism_id"] for control in data["controls"]})
    view = {
        "schema_version": data["schema_version"],
        "source": {"canonical": "../ism-mapping.yaml", "ism_release": data["ism_release"], "generated": True},
        "profile_coverage": {
            "profile": "ASD Essential Eight Maturity Level 2",
            "source": "../provenance.lock.yaml",
            "total_controls": len(profile_controls),
            "detector_backed_controls": detector_backed,
            "without_detector_mapping": sorted(set(profile_controls) - set(detector_backed)),
        },
        "strategies": strategies,
        "checks": [checks[key] for key in sorted(checks)],
        "unmapped": sorted(data["unmapped"], key=check_key),
    }
    return yaml.safe_dump(view, sort_keys=False, allow_unicode=True)


def render_kubescape(source: Path = SOURCE) -> str:
    data = yaml.safe_load(source.read_text())
    checks: dict[str, dict[str, object]] = {}
    for control in data["controls"]:
        for check in control["checks"]:
            if check["engine"] != "kubescape":
                continue
            item = checks.setdefault(
                check["rule_id"],
                {
                    "rule_id": check["rule_id"],
                    "provenance": check["provenance"],
                    "ism_controls": [],
                },
            )
            item["ism_controls"].append(
                {
                    "ism_id": control["ism_id"],
                    "title": control["title"],
                    "coverage": check["coverage"],
                    "evidence_note": control["evidence_note"],
                }
            )

    view = {
        "schema_version": data["schema_version"],
        "source": {
            "canonical": "../ism-mapping.yaml",
            "ism_release": data["ism_release"],
            "generated": True,
            "provenance_lock": "../provenance.lock.yaml",
        },
        "checks": [checks[name] for name in sorted(checks)],
        "excluded_unmapped_rules": [
            {"rule_id": check["rule_id"], "reason": check["reason"]}
            for check in data["unmapped"]
            if check["engine"] == "kubescape"
        ],
    }
    return json.dumps(view, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--provenance-lock", type=Path, default=PROVENANCE_LOCK)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--kubescape-output", type=Path, default=DEFAULT_KUBESCAPE_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = render(args.source, args.provenance_lock)
    kubescape_generated = render_kubescape(args.source)
    if args.check:
        if not args.output.exists() or args.output.read_text() != generated:
            raise SystemExit(f"{args.output} is stale; run scripts/generate_views.py")
        if not args.kubescape_output.exists() or args.kubescape_output.read_text() != kubescape_generated:
            raise SystemExit(f"{args.kubescape_output} is stale; run scripts/generate_views.py")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(generated)
    args.kubescape_output.write_text(kubescape_generated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

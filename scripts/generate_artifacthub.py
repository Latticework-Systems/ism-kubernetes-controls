#!/usr/bin/env python3
"""Generate Artifact Hub packages for the deployable Kyverno policy families.

Artifact Hub indexes a directory tree: each package is one directory holding an
`artifacthub-pkg.yml` alongside the manifests it installs. This script projects
`policies/<family>/policy.yaml` into that layout under `artifacthub/`, keeping
only the Kyverno objects. Install the Velero, CronJob and ConfigMap objects
from the source tree instead; they need site-specific configuration first.

Descriptions and readmes come from `mapping/ism-mapping.yaml`, so the ISM
controls, coverage and evidence boundaries a package lists stay tied to the
canonical mapping. Pin each package version and creation date in PACKAGES
below, and bump the version by hand when you change a policy: Artifact Hub
requires a monotonic semver per package.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "mapping/ism-mapping.yaml"
POLICIES = ROOT / "policies"
DEFAULT_OUTPUT = ROOT / "artifacthub"

REPO_URL = "https://github.com/Latticework-Systems/ism-kubernetes-controls"
RAW_URL = "https://raw.githubusercontent.com/Latticework-Systems/ism-kubernetes-controls/main"
KUBERNETES_VERSION = "1.27"
KYVERNO_VERSION = "1.13.0"

# family -> package metadata. Bump version by hand when the family's policies
# change. createdAt is the first publication date; leave it alone.
PACKAGES = {
    "application-control": {
        "version": "0.1.0",
        "createdAt": "2026-08-28T00:00:00Z",
        "displayName": "ISM Application Control",
        "summary": (
            "Restricts workloads to images from an approved registry list, blocks mutable "
            "'latest' tags, and blocks privileged containers and the SYS_ADMIN capability."
        ),
        "extra": (
            "The approved registry list is read at admission time from the "
            "`ism-approved-registries` ConfigMap. The package leaves that ConfigMap to "
            "you. Create it in the `kyverno` namespace before enforcing. See "
            f"{REPO_URL}/blob/main/policies/application-control/policy.yaml."
        ),
    },
    "backups": {
        "version": "0.1.0",
        "createdAt": "2026-08-28T00:00:00Z",
        "displayName": "ISM Regular Backups",
        "summary": (
            "Requires production PersistentVolumeClaims to declare an explicit backup "
            "disposition label, so unlabelled storage cannot reach production unnoticed."
        ),
        "extra": (
            "This package ships the admission policy alone. The Velero Schedules, etcd "
            "backup reference and monthly restoration-test CronJob that produce the rest "
            "of the backup evidence live in the source repository at "
            f"{REPO_URL}/tree/main/policies/backups."
        ),
    },
    "patch-applications": {
        "version": "0.1.0",
        "createdAt": "2026-08-28T00:00:00Z",
        "displayName": "ISM Patch Applications",
        "summary": (
            "Requires images to carry a build-date annotation and a passing vulnerability "
            "scan result, and gates internet-facing workloads on image age."
        ),
        "extra": (
            "Your build pipeline stamps the annotations these policies read. A pass "
            "shows the pipeline ran. It says nothing about whether the scanner was "
            "right or whether anyone fixed what it found."
        ),
    },
    "patch-operating-systems": {
        "version": "0.1.0",
        "createdAt": "2026-08-28T00:00:00Z",
        "displayName": "ISM Patch Operating Systems",
        "summary": (
            "Requires workloads to declare their base image and blocks base images whose "
            "distribution has reached end of life."
        ),
        "extra": (
            "The policy carries the end-of-life list. Review it as distributions "
            "reach end of support."
        ),
    },
    "privileged-access": {
        "version": "0.1.0",
        "createdAt": "2026-08-28T00:00:00Z",
        "displayName": "ISM Restrict Administrative Privileges",
        "summary": (
            "Disables default ServiceAccount token automount, requires production "
            "workloads to run under a dedicated ServiceAccount, blocks legacy "
            "ServiceAccount token Secrets, and blocks new cluster-admin bindings."
        ),
        "extra": (
            "One policy in this family mutates ServiceAccounts. Review "
            "`ism-privileged-access-mutate-default-sa` against your workloads before "
            "moving it out of Audit."
        ),
    },
    "workload-hardening": {
        "version": "0.1.0",
        "createdAt": "2026-08-28T00:00:00Z",
        "displayName": "ISM Workload Hardening",
        "summary": (
            "Requires a hardened container security context, blocks host namespace "
            "sharing and hostPath volumes, and requires a read-only root filesystem."
        ),
        "extra": (
            "The hostPath policy applies to production namespaces only. Scope out "
            "platform components that need hostPath by namespace label."
        ),
    },
}

class Literal(str):
    """A string emitted as a YAML block literal, so markdown stays reviewable."""


def _represent_literal(dumper: yaml.Dumper, data: Literal):
    return dumper.represent_scalar("tag:yaml.org,2002:str", str(data), style="|")


yaml.SafeDumper.add_representer(Literal, _represent_literal)


BASE_KEYWORDS = [
    "kyverno",
    "ism",
    "irap",
    "asd",
    "australian-government",
    "compliance",
    "evidence",
    "essential-eight",
]


def load_documents(path: Path) -> list[dict]:
    return [document for document in yaml.safe_load_all(path.read_text()) if document]


def cluster_policies(documents: list[dict]) -> list[dict]:
    return [document for document in documents if document.get("kind") == "ClusterPolicy"]


def controls_for(mapping: dict, policy_names: set[str]) -> list[dict]:
    """Canonical ISM controls evidenced by the given Kyverno policy names."""
    matched = []
    for control in mapping["controls"]:
        checks = [
            check
            for check in control["checks"]
            if check["engine"] == "kyverno" and check["policy"] in policy_names
        ]
        if checks:
            matched.append(
                {
                    "ism_id": control["ism_id"],
                    "title": control["title"],
                    "coverage": "partial"
                    if any(check["coverage"] == "partial" for check in checks)
                    else "full",
                    "evidence_note": " ".join(control["evidence_note"].split()),
                }
            )
    return sorted(matched, key=lambda control: control["ism_id"])


def render_readme(meta: dict, policies: list[dict], controls: list[dict]) -> str:
    lines = [
        f"# {meta['displayName']}",
        "",
        meta["summary"],
        "",
        "## ISM controls evidenced",
        "",
        "| Control | Coverage | Title |",
        "| --- | --- | --- |",
    ]
    for control in controls:
        lines.append(f"| {control['ism_id']} | {control['coverage']} | {control['title']} |")
    lines += [
        "",
        "## Evidence boundary",
        "",
        "Each mapping below is partial evidence. A PolicyReport shows what the cluster",
        "admitted. It does not discharge an ISM control, and it is not an assessment.",
        "",
    ]
    for control in controls:
        lines.append(f"- **{control['ism_id']}**: {control['evidence_note']}")
    lines += [
        "",
        "## Policies in this package",
        "",
    ]
    for policy in policies:
        annotations = policy["metadata"].get("annotations", {})
        title = annotations.get("policies.kyverno.io/title", policy["metadata"]["name"])
        severity = annotations.get("policies.kyverno.io/severity", "unspecified")
        lines.append(f"- `{policy['metadata']['name']}`: {title} (severity: {severity})")
    lines += [
        "",
        "## Notes",
        "",
        meta["extra"],
        "",
        "The canonical mapping, its ASD OSCAL provenance and the Kyverno test suite are",
        f"maintained at {REPO_URL}.",
        "",
    ]
    return Literal("\n".join(lines))


def render_package(family: str, meta: dict, policies: list[dict], controls: list[dict]) -> str:
    subjects = sorted(
        {
            policy["metadata"].get("annotations", {}).get("policies.kyverno.io/subject", "Pod")
            for policy in policies
        }
    )
    control_ids = ", ".join(control["ism_id"] for control in controls)
    package = {
        "name": f"ism-{family}",
        "version": meta["version"],
        "displayName": meta["displayName"],
        "createdAt": meta["createdAt"],
        "description": (
            f"{meta['summary']} Provides partial Kubernetes evidence for Australian "
            f"Government ISM controls {control_ids}."
        ),
        "license": "Apache-2.0",
        "homeURL": REPO_URL,
        "install": Literal(
            "```shell\n"
            f"kubectl apply -f {RAW_URL}/artifacthub/ism-{family}/ism-{family}.yaml\n"
            "```\n"
            "\n"
            "Policies install in Audit mode. Review the resulting PolicyReports for your\n"
            "workloads before switching any policy to Enforce.\n"
        ),
        "keywords": BASE_KEYWORDS + [family],
        "links": [
            {"name": "Source", "url": f"{REPO_URL}/tree/main/policies/{family}"},
            {"name": "Canonical ISM mapping", "url": f"{REPO_URL}/blob/main/mapping/ism-mapping.yaml"},
        ],
        "provider": {"name": "Latticework Systems"},
        "readme": render_readme(meta, policies, controls),
        "annotations": {
            "kyverno/category": "ASD ISM",
            "kyverno/kubernetesVersion": KUBERNETES_VERSION,
            "kyverno/subject": ", ".join(subjects),
            "kyverno/version": KYVERNO_VERSION,
        },
    }
    return yaml.safe_dump(package, sort_keys=False, allow_unicode=True, width=100)


def render(mapping_path: Path = MAPPING) -> dict[str, str]:
    """Return the full generated tree as {relative path: content}."""
    mapping = yaml.safe_load(mapping_path.read_text())
    tree: dict[str, str] = {}
    for family, meta in PACKAGES.items():
        source = POLICIES / family / "policy.yaml"
        policies = cluster_policies(load_documents(source))
        if not policies:
            raise SystemExit(f"{source} contains no ClusterPolicy objects")
        names = {policy["metadata"]["name"] for policy in policies}
        controls = controls_for(mapping, names)
        if not controls:
            raise SystemExit(f"no ISM controls in {mapping_path} reference policies from {family}")
        directory = f"ism-{family}"
        tree[f"{directory}/ism-{family}.yaml"] = yaml.safe_dump_all(
            policies, sort_keys=False, allow_unicode=True, width=100, explicit_start=True
        )
        tree[f"{directory}/artifacthub-pkg.yml"] = render_package(family, meta, policies, controls)
    return tree


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mapping", type=Path, default=MAPPING)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    tree = render(args.mapping)
    if args.check:
        for relative, content in sorted(tree.items()):
            target = args.output / relative
            if not target.exists() or target.read_text() != content:
                raise SystemExit(f"{target} is stale; run scripts/generate_artifacthub.py")
        return 0
    for relative, content in sorted(tree.items()):
        target = args.output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

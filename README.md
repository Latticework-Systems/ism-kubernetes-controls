# ISM Kubernetes Controls

Open, machine-readable mappings and Kyverno policies for Kubernetes-observable parts of the Australian Signals Directorate Information Security Manual (ISM).

This repository is the source of truth for the relationship between ISM controls and Kubernetes checks. It does not perform an assessment, produce a client report or provide certification.

## What this repo is for

This repo does two things, and you can use either or both:

1. **Reference mapping.** [`mapping/ism-mapping.yaml`](./mapping/ism-mapping.yaml) is the canonical, machine-readable statement of which ISM controls have Kubernetes-observable evidence, what that evidence is, and its exact boundary.
2. **Deployable Kyverno policies.** [`policies/`](./policies/) contains real `ClusterPolicy` manifests you can apply to your own cluster today to start collecting that evidence.

### Quick start

```bash
kubectl apply -k .
kubectl get policyreport,clusterpolicyreport -A
```

This applies the first-wave bundle (`application-control`, `workload-hardening`, `privileged-access`) in `Audit` mode — nothing is blocked, you only get `PolicyReport`/`ClusterPolicyReport` findings to review. See [Kyverno policy families](#kyverno-policy-families) below for the full policy set, and switch specific policies to `Enforce` only once you've reviewed the reports for your workloads.

## What is here

- [`mapping/ism-mapping.yaml`](./mapping/ism-mapping.yaml) — the hand-maintained canonical mapping, including evidence boundaries and pinned Kubescape provenance.
- [`mapping/views/kubescape.json`](./mapping/views/kubescape.json) — generated input for the companion `ism-kubescape-framework` repository.
- [`mapping/views/e8.yaml`](./mapping/views/e8.yaml) — a generated Essential Eight ML2 compatibility view. Essential Eight is not the repository's primary model.
- [`policies/`](./policies/) — ISM-aligned Kyverno policies that can audit or enforce selected Kubernetes settings.
- [`mapping/provenance.lock.yaml`](./mapping/provenance.lock.yaml) — pinned ASD OSCAL and upstream Kubescape sources.

The current mapping contains 21 detector-backed ISM controls. Seventeen of those occur in ASD's 87-control Essential Eight ML2 OSCAL profile. The remaining four are full-ISM workload and network controls:

- ISM-1182 — network traffic is limited to business-required flows.
- ISM-1246 — server applications are hardened using ASD and vendor guidance.
- ISM-1416 — inbound and outbound connections are restricted to approved applications and services.
- ISM-1604 — shared software isolation mechanisms are hardened.

All mappings are partial evidence unless explicitly stated otherwise. For example, a NetworkPolicy finding can show whether a workload is selected by ingress and egress policy; it cannot prove that the policy matches business need or that the cluster network plugin enforces it.

## How the repositories fit together

`ism-kubernetes-controls` defines the meaning: ISM control, Kubernetes check, provenance and evidence boundary.

`ism-kubescape-framework` consumes the generated Kubescape view and implements the read-only Rego scan rules. It should not invent independent ISM mappings.

Latticework Posture can consume scan and PolicyReport output to provide reporting and workflow. Remediate can turn reviewed findings into GitOps changes. Golden Templates provide reusable, hardened workload implementations. Those products are deliberately outside this public mapping repository.

## Kyverno policy families

| Policy family | Kubernetes evidence | Mapped ISM controls |
|---|---|---|
| [`application-control`](./policies/application-control/) | Approved registries, immutable version selection and privileged-container restrictions | ISM-1490, ISM-1657, ISM-1871 |
| [`patch-applications`](./policies/patch-applications/) | Declared build date and vulnerability-scan state at admission | ISM-1690, ISM-1693, ISM-1698, ISM-1700, ISM-1808, ISM-1876 |
| [`workload-hardening`](./policies/workload-hardening/) | Security context, host isolation and read-only root filesystem | ISM-1246, ISM-1604 |
| [`privileged-access`](./policies/privileged-access/) | Dedicated service accounts, legacy tokens and cluster-admin bindings | ISM-0445, ISM-1685, ISM-1883 |
| [`patch-operating-systems`](./policies/patch-operating-systems/) | Declared base-image support state | ISM-1501, ISM-1694, ISM-1695, ISM-1877 |
| [`backups`](./policies/backups/) | Declared backup coverage for production PVCs | ISM-1511 |

19 ISM controls have Kyverno evidence, implemented across 17 `ClusterPolicy` objects (some families cover more than one control per policy). The remaining 2 mapped controls (ISM-1182, ISM-1416) are Kubescape-only network checks with no Kyverno equivalent — see [`ism-kubescape-framework`](https://github.com/Latticework-Systems/ism-kubescape-framework).

The root [`kustomization.yaml`](./kustomization.yaml) (applied above in Quick start) is a brownfield-friendly first wave covering `application-control`, `workload-hardening` and `privileged-access` in `Audit` mode, and it omits the default-service-account mutation.

The other three families (`patch-applications`, `patch-operating-systems`, `backups`) are not in the first-wave bundle because they depend on annotations or labels your CI/CD or backup tooling must populate first (see each family's directory for details). Add them to your own `kustomization.yaml` once those annotations are in place.

## Validate locally

```bash
python3 -m pip install -r requirements-dev.txt
make mapping-check
make validate
```

`make validate` downloads the pinned Kyverno CLI release with a pinned SHA-256 checksum, renders the first-wave bundle and runs the guarded test target. The guard treats detailed `Want ..., got ...` rows as failures even if Kyverno exits successfully.

For a provenance review against the exact authority files named in [`mapping/provenance.lock.yaml`](./mapping/provenance.lock.yaml):

```bash
python3 scripts/validate_mapping.py \
  --framework-repo ../ism-kubescape-framework \
  --asd-catalog /path/to/ISM_catalog.json \
  --e8-profile /path/to/ISM_E8_ML2-baseline_profile.json \
  --kubescape-controls /path/to/kubescape-controls.json \
  --regolibrary /path/to/regolibrary
```

## Scope and assurance boundary

Kubernetes can provide useful technical evidence for only part of the ISM. These checks do not establish governance, assessor judgement, endpoint configuration, identity-provider configuration, patch release dates, scanner cadence, backup completion or formal compliance.

Use the exact `evidence_note` attached to each mapping when presenting a result. A passing check means only that the scanned object satisfied that detector at that time.

Apache-2.0 licensed. Report security issues using [`SECURITY.md`](./SECURITY.md).

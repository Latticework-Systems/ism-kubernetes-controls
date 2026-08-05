# ISM Kubernetes Controls

Machine-readable mappings and Kyverno policies for Kubernetes-observable parts of the Australian Signals Directorate Information Security Manual (ISM).

This repository defines the relationship between ISM controls and Kubernetes checks. Assessment, reporting and certification sit outside its scope.

## What this repo is for

Use either part on its own:

1. **Reference mapping.** [`mapping/ism-mapping.yaml`](./mapping/ism-mapping.yaml) is the canonical, machine-readable statement of which ISM controls have Kubernetes-observable evidence, what that evidence is, and its exact boundary.
2. **Deployable Kyverno policies.** [`policies/`](./policies/) contains `ClusterPolicy` manifests that collect that evidence from your cluster.

### Quick start

The root Kustomize bundle creates ten `ClusterPolicy` resources and an approved-registry `ConfigMap` in the `kyverno` namespace. It covers application control, workload hardening and privileged access. The overlay sets the validation policies to `Audit` mode and removes the default-service-account mutation policy.

Prerequisites:

- A Kubernetes cluster and `kubectl` configured for the intended context.
- [Kyverno installed](https://kyverno.io/docs/installation/installation/) and running, including its [reports controller](https://kyverno.io/docs/introduction/how-kyverno-works/).
- Permission to create cluster-scoped `ClusterPolicy` resources and a `ConfigMap` in the `kyverno` namespace.

Read the root [`kustomization.yaml`](./kustomization.yaml) and the three source manifests for [application control](./policies/application-control/policy.yaml), [workload hardening](./policies/workload-hardening/policy.yaml) and [privileged access](./policies/privileged-access/policy.yaml). The preview command below shows the final resources after Kustomize applies the Audit patches.

```bash
# Confirm the target cluster.
kubectl config current-context

# Preview the exact resources. This makes no cluster changes.
kubectl apply --dry-run=client -k . -o yaml

# Compare the bundle with objects in the cluster. Exit 1 means it found differences.
kubectl diff -k .

# Apply the same Audit-mode bundle.
kubectl apply -k .

# Review the findings produced by Kyverno.
kubectl get policyreport,clusterpolicyreport -A
```

The bundled registry allowlist contains example values. Review and replace them in [`policies/application-control/policy.yaml`](./policies/application-control/policy.yaml) before relying on its findings. See [Kyverno policy families](#kyverno-policy-families) for the full policy set. Change a policy to `Enforce` after you review its reports against your workloads.

For a brownfield cluster, policies with other names remain in place and keep their existing behaviour. `kubectl apply` can change resources that share a name with this bundle, including `kyverno/ism-approved-registries`, so inspect `kubectl diff` before applying. Eight policies scan existing matching resources and populate reports. The legacy-token and cluster-admin-binding policies use `background: false`; they evaluate admission requests and skip existing objects. Audit mode leaves requests unblocked by this bundle. Existing `Enforce` and mutation policies keep their effects. Overlapping policies can report the same workload under different policy names.

## What is here

- [`mapping/ism-mapping.yaml`](./mapping/ism-mapping.yaml): the hand-maintained canonical mapping, including evidence boundaries and pinned Kubescape provenance.
- [`mapping/views/kubescape.json`](./mapping/views/kubescape.json): generated input for the companion `ism-kubescape-framework` repository.
- [`mapping/views/e8.yaml`](./mapping/views/e8.yaml): a generated Essential Eight ML2 compatibility view. ISM remains the primary model.
- [`policies/`](./policies/): ISM-aligned Kyverno policies that can audit or enforce selected Kubernetes settings.
- [`mapping/provenance.lock.yaml`](./mapping/provenance.lock.yaml): pinned ASD OSCAL and upstream Kubescape sources.

The current mapping contains 21 detector-backed ISM controls. Seventeen of those occur in ASD's 87-control Essential Eight ML2 OSCAL profile. The remaining four are full-ISM workload and network controls:

- ISM-1182: network traffic is limited to business-required flows.
- ISM-1246: server applications are hardened using ASD and vendor guidance.
- ISM-1416: inbound and outbound connections are restricted to approved applications and services.
- ISM-1604: shared software isolation mechanisms are hardened.

Each mapping states its evidence boundary. For example, a NetworkPolicy finding can show whether ingress and egress policies select a workload. An assessor must establish that the policy matches business need and that the cluster network plugin enforces it.

## How the repositories fit together

`ism-kubernetes-controls` defines the meaning: ISM control, Kubernetes check, provenance and evidence boundary.

`ism-kubescape-framework` consumes the generated Kubescape view and implements the read-only Rego scan rules. It should not invent independent ISM mappings.

Latticework Posture consumes scan and PolicyReport output for reporting and workflow. Remediate turns reviewed findings into GitOps changes. Golden Templates provide hardened workload implementations. Each product has its own repository.

## Kyverno policy families

| Policy family | Kubernetes evidence | Mapped ISM controls |
|---|---|---|
| [`application-control`](./policies/application-control/) | Approved registries, immutable version selection and privileged-container restrictions | ISM-1490, ISM-1657, ISM-1871 |
| [`patch-applications`](./policies/patch-applications/) | Declared build date and vulnerability-scan state at admission | ISM-1690, ISM-1693, ISM-1698, ISM-1700, ISM-1808, ISM-1876 |
| [`workload-hardening`](./policies/workload-hardening/) | Security context, host isolation and read-only root filesystem | ISM-1246, ISM-1604 |
| [`privileged-access`](./policies/privileged-access/) | Dedicated service accounts, legacy tokens and cluster-admin bindings | ISM-0445, ISM-1685, ISM-1883 |
| [`patch-operating-systems`](./policies/patch-operating-systems/) | Declared base-image support state | ISM-1501, ISM-1694, ISM-1695, ISM-1877 |
| [`backups`](./policies/backups/) | Declared backup coverage for production PVCs | ISM-1511 |

Seventeen `ClusterPolicy` objects provide evidence for 19 ISM controls. Some policies cover more than one control. The remaining two mapped controls, ISM-1182 and ISM-1416, use Kubescape network checks with no Kyverno equivalent. See [`ism-kubescape-framework`](https://github.com/Latticework-Systems/ism-kubescape-framework).

The root [`kustomization.yaml`](./kustomization.yaml) (applied above in Quick start) is a brownfield-friendly first wave covering `application-control`, `workload-hardening` and `privileged-access` in `Audit` mode, and it omits the default-service-account mutation.

The first wave omits `patch-applications`, `patch-operating-systems` and `backups`. Those families depend on annotations or labels supplied by CI/CD or backup tooling. Add them to your Kustomize configuration after that metadata exists.

## Scope and assurance boundary

Kubernetes provides technical evidence for part of the ISM. These checks cannot establish governance, assessor judgement, endpoint configuration, identity-provider configuration, patch release dates, scanner cadence, backup completion or formal compliance.

Use the exact `evidence_note` attached to each mapping when presenting a result. A passing check means only that the scanned object satisfied that detector at that time.

See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for local validation, provenance review and Kubescape mapping releases.

Licensed under Apache-2.0. Report security issues using [`SECURITY.md`](./SECURITY.md).

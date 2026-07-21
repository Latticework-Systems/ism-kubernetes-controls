# ISM Kubernetes controls quickstart

This installs the first Kyverno policy wave in `Audit` mode and exports raw results for downstream review.

## Prerequisites

- A supported Kubernetes cluster and `kubectl` access able to install `ClusterPolicy` resources.
- Kyverno installed through your normal Helm or GitOps process.
- Approved registry and namespace labels configured from [`templates/`](./templates/).

## Validate the public policy tree

```bash
python3 -m pip install -r requirements-dev.txt
make validate
```

The target renders the root kustomization and runs the guarded Kyverno tests. It does not connect to a cluster.

## Apply the first wave

```bash
kubectl apply -f docs/templates/approved-registries-configmap.yaml
kubectl apply -f docs/templates/namespace-labels.yaml
kubectl apply -k .
```

The root bundle patches validation policies to `Audit`, so it reports without blocking workloads. Review platform namespaces and findings before selectively changing a policy to `Enforce`.

## Export raw evidence

```bash
kubectl get policyreports -A -o yaml > policyreports.yaml
kubectl get clusterpolicyreports -o yaml > clusterpolicyreports.yaml
```

The companion `ism-kubescape-framework` can produce a second, read-only view of resources already present in the cluster or a manifest set. Kyverno and Kubescape intentionally overlap on some settings: Kyverno observes admission, while Kubescape observes current state.

Pass those raw files to Posture or another downstream workflow. This repository does not classify findings, manage exceptions, render HTML, or make an assessment conclusion.

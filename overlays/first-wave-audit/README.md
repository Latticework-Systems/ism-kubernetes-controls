# First-wave Audit rollout

The repo root `kustomization.yaml` renders the first-wave Audit bundle:

- Application control: ISM-1490, ISM-1657 and ISM-1871
- Workload hardening: ISM-1246 and ISM-1604
- Privileged access: ISM-0445, ISM-1685 and ISM-1883

All validate policies are patched to `Audit`. The default service account
mutation policy is excluded so the first pass observes the cluster without
changing workloads or service accounts.

Use from the repository root:

```bash
kubectl apply -k .
```

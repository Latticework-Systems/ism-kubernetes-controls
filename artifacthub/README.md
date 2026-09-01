# Artifact Hub packages

Generated. Do not edit by hand — run `make artifacthub-generate`.

Artifact Hub indexes a directory tree in which each package is one directory
holding an `artifacthub-pkg.yml` beside the manifests it installs.
[`scripts/generate_artifacthub.py`](../scripts/generate_artifacthub.py) projects
each `policies/<family>/policy.yaml` into that layout, keeping only the Kyverno
objects. Package descriptions, the ISM control tables and the evidence
boundaries are derived from [`mapping/ism-mapping.yaml`](../mapping/ism-mapping.yaml),
so a published package can never claim coverage the canonical mapping does not
support. CI fails if this directory is stale.

The Velero Schedules, etcd backup reference and restoration-test CronJob in
`policies/backups/` are deliberately excluded: Artifact Hub packages of kind
"Kyverno policies" are expected to contain policies, and those objects need
site-specific configuration before they mean anything.

## Publishing

`artifacthub-repo.yml` in this directory carries the setup steps. Point the
repository at the `artifacthub` path of this repo on `main`.

## Changing a policy

1. Edit `policies/<family>/policy.yaml` as usual and keep the Kyverno tests green.
2. Bump that family's `version` in the `PACKAGES` table in
   `scripts/generate_artifacthub.py`. Artifact Hub requires a monotonically
   increasing semver per package and treats each version as immutable.
   Leave `createdAt` alone; it is the first publication date.
3. Run `make artifacthub-generate` and commit the result.

# Artifact Hub packages

Generated. Do not edit by hand; run `make artifacthub-generate`.

Artifact Hub indexes a directory tree in which each package is one directory
holding an `artifacthub-pkg.yml` beside the manifests it installs.
[`scripts/generate_artifacthub.py`](../scripts/generate_artifacthub.py) projects
each `policies/<family>/policy.yaml` into that layout, keeping only the Kyverno
objects. Descriptions, ISM control tables and evidence boundaries come from
[`mapping/ism-mapping.yaml`](../mapping/ism-mapping.yaml), so the packages list
only the coverage that mapping supports.

Run `make artifacthub-check` to catch a stale tree. Nothing in CI calls it yet.

The Velero Schedules, etcd backup reference and restoration-test CronJob in
`policies/backups/` stay out of the packages. Artifact Hub expects a package of
kind "Kyverno policies" to contain policies, and those three objects need
site-specific configuration before they mean anything.

## Publishing

This repository is registered on Artifact Hub as kind "Kyverno policies",
pointing at the `artifacthub` path on `main`. `artifacthub-repo.yml` holds the
repository ID that claims it.

## Changing a policy

1. Edit `policies/<family>/policy.yaml` and keep the Kyverno tests green.
2. Bump that family's `version` in the `PACKAGES` table in
   `scripts/generate_artifacthub.py`. Artifact Hub wants a monotonic semver per
   package and treats each published version as immutable. Leave `createdAt`
   alone; it records the first publication.
3. Run `make artifacthub-generate` and commit the result.

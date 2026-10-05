# Contributing

Contributions that improve mapping accuracy, policy behaviour, fixtures, or evidence boundaries are welcome.

## Install the commit hooks

The hooks scan staged changes for secrets with Gitleaks and block provider assessment packs, spreadsheets, PDFs and anything under `.private/` or `docs/private/`:

```bash
python3 -m pip install pre-commit
pre-commit install
```

CI also runs TruffleHog on every push and pull request.

## Validate changes locally

Install the development dependencies, then run both validation targets:

```bash
python3 -m pip install -r requirements-dev.txt
make mapping-check
make validate
```

`make mapping-check` validates the canonical mapping and checks its generated views without downloading sources. `make validate` downloads the checksum-pinned Kyverno CLI, renders the first-wave Audit bundle and runs every policy test. Its guard fails detailed `Want ..., got ...` mismatches even when Kyverno returns a successful exit code.

If a mapping change affects the companion Kubescape framework, run:

```bash
python3 scripts/validate_mapping.py --framework-repo /path/to/ism-kubescape-framework
```

Changes to Kubescape provenance must resolve against the upstream revision in [`mapping/provenance.lock.yaml`](./mapping/provenance.lock.yaml). Download the authority files listed there, then run:

```bash
python3 scripts/validate_mapping.py \
  --asd-catalog /path/to/ISM_catalog.json \
  --e8-profile /path/to/ISM_E8_ML2-baseline_profile.json \
  --kubescape-controls /path/to/kubescape-controls.json \
  --regolibrary /path/to/regolibrary
```

Relationships in [`mapping/upstream/kubescape-regolibrary.yaml`](./mapping/upstream/kubescape-regolibrary.yaml) use existing regolibrary controls at the separate `kubescape_regolibrary_framework` ref in the lock. To check them against that revision, add `--regolibrary-framework /path/to/regolibrary-at-that-ref`. `make mapping-check` regenerates `mapping/views/regolibrary-ism.json`, the `frameworks/ism.json` contributed upstream, and fails if it is stale.

## Pull requests

Before opening a pull request:

1. Do not commit cluster evidence, credentials, kubeconfigs, local paths, private endpoints, or customer information.
2. State the evidence boundary for any compliance-related claim; these controls do not provide certification.

## Publish the Kubescape mapping

Merging a pull request that changes `mapping/views/kubescape.json` or `mapping/views/regolibrary-ism.json` publishes a release. The [merge workflow](./.github/workflows/auto-release.yaml) validates the mapping and tags `main` with the next version, using the `RELEASE_DEPLOY_KEY` deploy key. The tag starts the [release workflow](./.github/workflows/release-mapping.yaml). Label the pull request to choose the version:

| Label | Release |
| --- | --- |
| none | patch, for example `v0.3.0` to `v0.3.1` |
| `release:minor` | minor, for example `v0.3.0` to `v0.4.0` |
| `release:major` | major, for example `v0.3.0` to `v1.0.0` |
| `release:skip` | no release |

Tags are immutable, so choose the label before merging. To release by hand instead, tag the head of `main` and push the tag:

```bash
git tag -a vX.Y.Z -m vX.Y.Z
git push origin vX.Y.Z
```

The release workflow validates the generated views and publishes `kubescape.json` and `regolibrary-ism.json` with their SHA-256 checksums. Enable [immutable releases](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes) before publishing the first tag so GitHub locks the tag and assets and produces the attestation used by `ism-kubescape-framework`.

The companion [`ism-kubescape-framework`](https://github.com/Latticework-Systems/ism-kubescape-framework) verifies and imports a release with:

```bash
make update-mapping CONTROLS_VERSION=vX.Y.Z
```

Report suspected vulnerabilities privately as described in [SECURITY.md](./SECURITY.md).

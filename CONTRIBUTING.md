# Contributing

Contributions that improve mapping accuracy, policy behaviour, fixtures, or evidence boundaries are welcome.

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

## Pull requests

Before opening a pull request:

1. Do not commit cluster evidence, credentials, kubeconfigs, local paths, private endpoints, or customer information.
2. State the evidence boundary for any compliance-related claim; these controls do not provide certification.

## Publish the Kubescape mapping

Maintainers publish a mapping after review and a green `main` build. Create a `v*` tag from `main` and push it:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

The [release workflow](./.github/workflows/release-mapping.yaml) validates the generated view and publishes `kubescape.json` with its SHA-256 checksum. Enable [immutable releases](https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/establish-provenance-and-integrity/prevent-release-changes) before publishing the first tag so GitHub locks the tag and assets and produces the attestation used by `ism-kubescape-framework`.

The companion [`ism-kubescape-framework`](https://github.com/Latticework-Systems/ism-kubescape-framework) verifies and imports a release with:

```bash
make update-mapping CONTROLS_VERSION=vX.Y.Z
```

Report suspected vulnerabilities privately as described in [SECURITY.md](./SECURITY.md).

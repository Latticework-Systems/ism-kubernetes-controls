# Contributing

Contributions that improve mapping accuracy, policy behaviour, fixtures, or evidence boundaries are welcome.

Before opening a pull request:

1. Run `make mapping-check` after changing mapping data.
2. Run `make validate` after changing policies or fixtures.
3. Do not commit cluster evidence, credentials, kubeconfigs, local paths, private endpoints, or customer information.
4. State the evidence boundary for any compliance-related claim; these controls do not provide certification.

If a mapping change also affects the companion Kubescape framework, run:

```bash
python3 scripts/validate_mapping.py --framework-repo /path/to/ism-kubescape-framework
```

Changes to Kubescape provenance must also resolve against the locked upstream revision. Download the official artifacts named in `mapping/provenance.lock.yaml`, then run:

```bash
python3 scripts/validate_mapping.py \
  --asd-catalog /path/to/ISM_catalog.json \
  --e8-profile /path/to/ISM_E8_ML2-baseline_profile.json \
  --kubescape-controls /path/to/kubescape-controls.json \
  --regolibrary /path/to/regolibrary
```

The ordinary `make mapping-check` remains offline and performs no download.

Report suspected vulnerabilities privately as described in [SECURITY.md](./SECURITY.md).

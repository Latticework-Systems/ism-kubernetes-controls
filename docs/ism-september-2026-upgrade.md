# September 2026 ISM upgrade

The canonical mapping targets September 2026, using ASD's [OSCAL v2026.09.4 release](https://www.cyber.gov.au/ism/oscal/v2026.09.4). The catalog and Essential Eight ML2 profile are pinned by URL, version and SHA-256 in [`mapping/provenance.lock.yaml`](../mapping/provenance.lock.yaml). ASD's [September change summary](https://www.cyber.gov.au/sites/default/files/2026-08/ISM%20September%202026%20changes%20%28September%202026%29.pdf) explains the release changes; the OSCAL catalog supplies the exact statements used in the mapping.

## Authority comparison

The June `v2026.06.18` catalog contains 1,101 ISM controls; September contains 1,143. There are 44 additions and two removals: ISM-0521 is rescinded and ISM-1448 is merged into ISM-1372. Neither removed control had a detector mapping here.

All 21 previously mapped control IDs remain in the catalog. Two statements changed: ISM-0445 explicitly refers to privileged **human** users, and ISM-1883 removes the reference to services and updates its duties wording. ISM-0445, ISM-1685 and ISM-1883 now belong to **Guidelines for system access**. The other mapped statements and chapters match September without edits.

The Essential Eight ML2 profile still contains the same 87 IDs. Detector coverage changes from 17 to 16 of those IDs because the service-account checks no longer claim ISM-0445. The mapping now contains 23 detector-backed ISM controls, including three new September controls outside the ML2 profile: ISM-2128, ISM-2141 and ISM-2143. All coverage remains partial.

## Privileged-access review and reuse

Existing Kyverno policy logic and fixtures are retained. The following relationships were reviewed against the September catalog and the local policy's actual scope.

| Detector | September relationship | Evidence boundary |
| --- | --- | --- |
| `ism-privileged-access-mutate-default-sa` | Moves from ISM-0445 to ISM-2143 | Disables token automount on default ServiceAccounts when the mutation is installed; it does not prove unique credentials. The root Audit bundle omits this mutation. |
| `ism-privileged-access-require-dedicated-sa` | Moves from ISM-0445 / ISM-1883 to ISM-2143 | Production Pods must use a non-default ServiceAccount. Multiple workloads can still use the same non-default account or share other credentials. |
| `ism-privileged-access-block-legacy-sa-tokens` | Retains ISM-1685 and adds ISM-2141 | Checks new and updated legacy token Secrets. It does not scan existing Secrets or prove projected tokens, short lifetimes or dynamic application credentials. |
| `ism-privileged-access-block-cluster-admin-binding` | Retains ISM-1883 | Restricts new and updated cluster-admin bindings, including human subjects; authorised online-service access still needs external evidence. |
| `ism-no-cluster-admin-binding` / `ism-no-wildcard-permissions` | Retain partial ISM-1883 support with its revised statement | Observe permission breadth. They do not establish which human accounts require access to online services. |
| `ism-minimise-clusterrolebindings` | Becomes explicitly unmapped | Counts cluster-wide service-account bindings and does not evaluate human account access. It is excluded from the generated Kubescape mapping. |

The local detectors keep their existing locked `regolibrary` revision and implementations. The regolibrary framework relationships described below use a separate ref. Catalog text and profile membership are verified against ASD; the applicability relationships are local, bounded interpretations, not ASD endorsements or assessments.

## Kernel-mode code

ISM-2128 limits the ability to install, load or modify kernel-mode code to privileged users who need it. `ism-no-privileged-containers` provides partial evidence: a privileged container holds every capability, including `CAP_SYS_MODULE`. The rule does not detect a container that adds `SYS_MODULE` on its own. `ism-drop-all-capabilities` is not mapped to ISM-2128 in this release. Neither rule assesses node access or driver signing.

## Kubescape regolibrary framework

[`mapping/upstream/kubescape-regolibrary.yaml`](../mapping/upstream/kubescape-regolibrary.yaml) records the relationships between 15 existing regolibrary controls and ISM controls, for the `ISM` framework contributed to [kubescape/regolibrary](https://github.com/kubescape/regolibrary/issues/803). Each entry names the related local checks, explains any difference in rule behaviour, and states the evidence boundary for the upstream rule. `scripts/generate_views.py` renders [`mapping/views/regolibrary-ism.json`](../mapping/views/regolibrary-ism.json), and the release workflow publishes it with a SHA-256 checksum.

These relationships use upstream controls at the `kubescape_regolibrary_framework` ref in the provenance lock, `9e768319`. The local detectors keep their `01f57dec` provenance. `validate_mapping.py` requires every ISM ID to exist in the canonical mapping and every related check to be known. With `--regolibrary-framework`, it also requires each control to resolve, with the recorded name, at the locked ref. Relationships that differ from the local mapping are deliberate:

- C-0046 → ISM-2128: the upstream rule rejects added capabilities on the `insecureCapabilities` list, whose default includes `SYS_MODULE`.
- C-0189 → ISM-2143: it checks the same default service-account properties as the Kyverno policies mapped to ISM-2143.
- C-0210 replaces C-0055 for seccomp, because C-0055 now accepts any profile, including `Unconfined`.

## Coverage census

[`mapping/coverage.yaml`](../mapping/coverage.yaml) moves to September 2026. Twenty-two census titles take ASD's revised wording, mostly the "human users" and "security controls" amendments. ISM-0445 moves from `automated` to `external-api` with an identity-provider collector, because its detectors now support ISM-2143. ISM-2128, ISM-2141 and ISM-2143 join the census as `automated` rows, so the census now covers 134 controls and its `automated` rows still equal the 23 detector-backed controls. The other September additions are not yet reviewed into the census.

## New requirements needing additional evidence

Only ISM-2128, ISM-2141 and ISM-2143 gain partial mappings through existing checks. The other 41 additions have no detector mapping in this repository. Requirements particularly relevant to Kubernetes deployments include:

| Controls | Evidence needed beyond current checks |
| --- | --- |
| ISM-2142, ISM-2144, ISM-2146 | Central management, incident-driven changes and revocation of application or workload static credentials. Kubernetes Secret presence alone does not establish these properties. |
| ISM-2151, ISM-2152 | Enforced backup immutability, backup infrastructure segregation and separate administrative authentication. A PVC backup label establishes none of these. |
| ISM-2154, ISM-2155 | Approved dependency pins in source and reproducible builds with independent verification. Image tag selection, image digest pinning in deployment manifests (Kubescape C-0306) or declared build age is insufficient. |
| ISM-2160 | Effective isolation of equipment management interfaces on a dedicated management network. Workload NetworkPolicy selection alone is insufficient. |
| ISM-2133–ISM-2135, ISM-2156–ISM-2159 | AI agent identities and registers, minimum permissions, task-scoped authorisation, untrusted input handling and tool invocation logs. Generic service-account and RBAC checks do not establish these application properties. |

These gaps remain outside the generated scanner controls until an appropriate detector and evidence boundary are implemented and reviewed.

## Change set and validation

The change set covers the canonical mapping and provenance lock, privileged-access policy annotations and messages, generated E8 and Kubescape views, the privileged-access Artifact Hub package, and the README. The privileged-access package advances to `0.1.1`; its original creation date is retained. Admission and mutation rules, the first-wave bundle and policy fixtures retain their behaviour.

Validate with the repository's development dependencies installed:

```bash
make mapping-check
make artifacthub-check
make validate
python3 scripts/validate_mapping.py \
  --asd-catalog .tools/ism/2026.09.4/ISM_catalog.json \
  --e8-profile .tools/ism/2026.09.4/ISM_E8_ML2-baseline_profile.json
```

Download the two authority files using the URLs in the provenance lock before the last command. It verifies their checksums, every mapped statement and the ML2 ID list. Compare each `ism_topic` with the control's top-level catalog chapter as well. Generate both views into two temporary destinations and compare them to verify deterministic output.

Validation on 5 October 2026 passed: mapping and Artifact Hub freshness checks, authority checks for all 23 mapped statements and the 87 profile IDs, all 23 chapter references, deterministic view generation, and all 81 Kyverno tests. The rendered first-wave bundle still contains ten Audit policies and excludes the default-service-account mutation. These are local checks; they do not establish runtime deployment or compliance.

## Downstream handoff

Publish a reviewed, validated mapping tag through the existing release workflow before the companion `ism-kubescape-framework` imports it with `make update-mapping CONTROLS_VERSION=vX.Y.Z`. That import must regenerate control metadata, add ISM-2128 to `ism-no-privileged-containers` and omit `ism-minimise-clusterrolebindings` from the ISM framework. The regolibrary pull request should cite the `regolibrary-ism.json` asset from the same release. Previously published releases retain their June mapping.

This repository update supplies mapping metadata and bounded technical evidence. Runtime deployment, new detector implementation and companion-repository adoption are separate work.

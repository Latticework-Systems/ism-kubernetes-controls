# Kubescape framework implementation contract

This is the review gate for generating the companion `ism-kubescape-framework` from the canonical ISM mapping.

## Inputs

- `mapping/ism-mapping.yaml` for ISM relationships and evidence boundaries.
- `mapping/provenance.lock.yaml` for pinned ASD and Kubescape source revisions.
- Kubescape `regolibrary` at the locked commit.
- Public fixtures only. No kubeconfig, cluster result, customer data, local path, or private endpoint is an input.

## Output

- One deterministic Kubescape framework named `ism-kubernetes`.
- Only detector-backed controls are included. Assessment-only and out-of-scope controls must not become pass-through or always-pass scanner controls.
- Every rule is a standalone local implementation. Upstream rules are provenance exemplars, not runtime or release dependencies.
- Adapted and custom rules retain their public fixtures and state which upstream behaviour was adopted or why no exemplar fit.
- Framework results remain raw evidence. Scoring, assessment conclusions, exceptions, HTML, and remediation decisions belong downstream.

## Current implementation slice

1. Generate framework control metadata from the canonical mapping instead of hand-maintaining embedded ISM ID lists.
2. Cover the mapped application-control, RBAC, workload-hardening and network-policy checks.
3. Keep every detector standalone and record whether its behaviour adapts a pinned upstream exemplar or is custom.
4. Add pass, fail and missing-field parity fixtures for every detector.
5. Keep `ism-no-wildcard-permissions` custom while C-0187 points at the wrong semantic rule.

## Acceptance criteria

- Generation is offline, deterministic, and produces no diff on a second run.
- Every generated detector has at least one pass and one fail fixture, including explicit false, missing, empty, and null cases where the input permits them.
- The generated framework includes no control without an approved detector reference.
- The mapping validator resolves every adapted exemplar against the locked `regolibrary` revision.
- Kubescape returns the expected detailed result for every fixture; the test gate does not trust a summary count alone.
- Public-tree disclosure and secret scans pass before repository creation.

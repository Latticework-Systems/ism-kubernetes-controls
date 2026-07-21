# Repository boundaries

The repositories stay separate because the mapping is useful beyond any one scanner.

| Repository | Responsibility | Does not own |
|---|---|---|
| `ism-kubernetes-controls` | ISM-to-Kubernetes applicability, evidence boundaries, detector references, and preventive Kyverno policies | Scan orchestration, scoring, report UI, remediation workflow |
| `ism-kubescape-framework` | A Kubescape-specific framework generated from the mapping and implemented as standalone adapted or custom detectors; emits raw scan evidence | The canonical ISM mapping, assessment conclusions, report UI |
| Latticework Posture | Ingests raw evidence, presents current posture, and supports assessment workflow | Admission enforcement or workload deployment |
| Latticework Remediate | Turns accepted gaps into reviewed remediation work | The authoritative ISM mapping or evidence collection |
| Golden templates | Reusable, tested deployment implementations used during remediation | Assessment or scan interpretation |

Kyverno and Kubescape can evaluate some of the same Kubernetes properties, but at different points in the lifecycle. Kyverno can reject or report a resource at admission. Kubescape observes resources already present in a cluster or manifest set. Sharing the mapping and detector provenance prevents those two implementations from silently making different compliance claims.

A future Falco adapter can remain separate in the same way. Falco runtime events would cite the relevant ISM controls and evidence boundary from this repository without putting Falco-specific rules into the Kubescape framework.

Upstream Kubescape, NSA, CIS, and MITRE rules are exemplars. They inform provenance and parity tests, but generated Latticework controls do not import them at runtime. This keeps the update trigger tied to ISM or an intentional local rule review rather than upstream framework drift.

The mapping is authoritative only for the Kubernetes evidence relationship. ASD's published ISM OSCAL catalog remains authoritative for the control text, and an assessor remains responsible for conclusions beyond the declared evidence boundary.

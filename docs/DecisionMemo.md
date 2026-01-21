# Decision Memo: Risk-Based Pre-Harm Safety System

## Decision

Adopt a **staged, risk-based safety funnel with human-in-the-loop oversight** to support early detection and proportionate intervention for emerging safety risks, rather than relying on fully automated enforcement or purely reactive moderation workflows.

This decision establishes a system where AI-assisted components surface and prioritize risk indicators, while humans retain final authority over all intervention decisions.

---

## Context

The platform operates in environments where safety risks evolve rapidly, particularly in live and youth-adjacent contexts. Existing moderation approaches are primarily optimized for post-violation enforcement, which limits their effectiveness in preventing escalation of ambiguous or emerging risks.

At the same time, safety decisions carry high stakes for users, creators, and the platform. Errors—especially false positives or opaque automated actions—can erode trust, introduce bias, and create regulatory risk. Any system designed to intervene earlier must therefore balance speed, accuracy, and governance.

---

## Rationale

This approach was selected based on the following considerations:

- **Ambiguity and novelty are inherent to emerging risks**  
  Early-stage harmful behaviors often do not map cleanly to existing policy categories, making binary classification insufficient.

- **Context matters more than isolated signals**  
  Risk assessment requires aggregation of behavioral, temporal, and contextual information that single-model or rule-based approaches struggle to capture reliably.

- **Human accountability is non-negotiable in safety-critical decisions**  
  Intervention decisions must remain explainable, auditable, and reviewable, particularly where youth safety or irreversible actions are involved.

- **Proportionate intervention reduces downstream harm**  
  Surfacing risks earlier enables lower-severity, reversible actions that can prevent escalation and reduce reliance on punitive enforcement.

A staged funnel allows the system to surface weak but meaningful signals, escalate confidence gradually, and route only the most concerning cases to human review or stronger intervention paths.

---

## Alternatives Considered

### 1. Fully Automated Enforcement
**Description:**  
Automated systems directly determine and execute enforcement actions based on detected signals.

**Rejected because:**
- High risk of false positives, particularly for novel or context-dependent behaviors
- Limited explainability and auditability
- Increased potential for user and creator harm
- Elevated regulatory and reputational risk

---

### 2. Purely Manual Review
**Description:**  
Human moderators review all safety cases without algorithmic prioritization or signal aggregation.

**Rejected because:**
- Does not scale to platform volume
- Introduces significant latency, especially in live contexts
- Increases moderator cognitive load and burnout
- Misses early intervention windows where harm could be prevented

---

### 3. Single-Model Risk Scoring
**Description:**  
A single model produces a unified risk score used to drive intervention decisions.

**Rejected because:**
- Insufficient handling of contextual nuance and evolving behaviors
- Encourages over-reliance on opaque outputs
- Difficult to govern and explain in high-stakes scenarios
- Poor fit for graduated, reversible intervention strategies

---

## Risks and Mitigations

### Risk: Over-Intervention
**Concern:**  
Early detection systems may act on weak or ambiguous signals, leading to unnecessary disruption.

**Mitigations:**
- Use confidence-weighted risk tiers rather than binary decisions
- Favor low-severity, reversible actions at early stages
- Require human confirmation for irreversible interventions

---

### Risk: Bias Amplification
**Concern:**  
Risk signals may disproportionately impact certain communities, creator styles, or regions.

**Mitigations:**
- Evaluate outcomes at the system level, not just individual signals
- Monitor for disproportionate impact across demographics and regions
- Incorporate policy and moderator feedback into ongoing calibration

---

### Risk: Moderator Overload
**Concern:**  
Additional surfaced cases could increase workload without improving outcomes.

**Mitigations:**
- Prioritize cases based on escalation velocity and potential impact
- Batch and rank surfaced cases to improve queue efficiency
- Continuously monitor throughput and cognitive load indicators

---

## Open Risks

The following risks remain and are expected to be addressed through phased rollout, monitoring, and iteration rather than upfront specification:

- **Adversarial adaptation:**  
  Creators may evolve behaviors to evade detection, reducing signal effectiveness over time.

- **Policy drift across regions:**  
  Differences in cultural context and regulatory requirements may complicate consistent calibration.

- **Signal decay and model drift:**  
  Over time, signals may lose relevance or introduce unintended effects if not actively reviewed.

---

## Conclusion

This decision reflects a deliberate tradeoff: prioritizing governance, proportionality, and human accountability over speed or automation. A staged, risk-based, human-in-the-loop system provides the flexibility needed to address emerging risks while maintaining trust, explainability, and regulatory alignment.

This approach is expected to evolve through controlled rollout, cross-functional review, and continuous learning.

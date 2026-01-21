# Glossary

This glossary defines key terms, metrics, and concepts used throughout the Early Risk Detection & Intervention System documentation. Definitions are intended to clarify meaning and scope rather than prescribe implementation details.

---

## Core Concepts

### Risk Indicator
An observable signal or pattern suggesting an increased likelihood of harmful outcomes.  
Risk indicators are **not determinations of wrongdoing**, intent, or policy violations.

Examples include contextual patterns, behavioral changes, or emerging trends evaluated over time.

---

### Pre-Harm
A design framing focused on identifying and addressing **early-stage risk signals** before clear policy violations or severe harm occur.

Pre-harm systems prioritize **early, proportionate intervention** rather than reactive enforcement.

---

### Human-in-the-Loop (HITL)
A system design approach in which humans retain final decision-making authority over interventions.

Automated components may surface signals or provide decision support, but **humans approve, modify, or reject all actions**, particularly irreversible ones.

---

### Proportionate Intervention
An intervention strategy in which the **severity of action matches the assessed level of risk**, favoring low-severity and reversible actions whenever possible.

Proportionality aims to reduce harm while minimizing unnecessary disruption to users and creators.

---

### Reversible Intervention
An action that can be undone or adjusted if risk subsides or additional context becomes available.

Examples include prompts, temporary limitations, or monitoring rather than permanent enforcement.

---

## System Concepts

### Staged Safety Funnel
A multi-step system that progressively aggregates signals, enriches context, assigns confidence-weighted risk tiers, and routes cases to appropriate intervention paths.

This design avoids binary decisions and supports gradual escalation.

---

### Signal Ingestion
The collection of lightweight, observable signals from content, behavior, and context.

Signal ingestion prioritizes **aggregation and metadata** over invasive or granular inspection.

---

### Context Enrichment
The process of augmenting raw signals with historical, behavioral, and trend-level context to reduce ambiguity and improve interpretation.

Context enrichment helps distinguish isolated events from meaningful patterns.

---

### Risk Tier
A confidence-weighted categorization (e.g., low, medium, high) representing the system’s assessment of potential risk.

Risk tiers are **not enforcement decisions** and do not directly trigger punishment.

---

### Confidence-Weighted
A design principle in which system outputs reflect varying levels of certainty rather than binary outcomes.

Confidence weighting supports abstention, gradual escalation, and human judgment under uncertainty.

---

## Metrics and Evaluation

### Time-to-Detection (TTD)
The elapsed time between the first appearance of meaningful risk indicators and human review.

TTD is used to evaluate whether the system surfaces risk earlier than post-violation moderation pipelines.

---

### Risk Score Velocity
The rate at which assessed risk increases over time.

Velocity emphasizes **change and escalation patterns** rather than static signal strength.

---

### Prioritization Accuracy
The degree to which surfaced cases align with moderator-assessed risk severity and urgency.

This metric evaluates queue ordering and decision support quality rather than model correctness.

---

### Harm Exposure
The duration and severity of user exposure to potentially harmful situations.

Harm exposure is evaluated downstream of intervention to assess preventative effectiveness.

---

### False Positive
A case in which an intervention occurs despite the absence of meaningful risk.

False positives are evaluated at the **system level** and considered alongside proportionality and reversibility.

---

### Appeal and Reversal Rate
The frequency with which users or creators successfully challenge or reverse interventions.

These rates are used as guardrail metrics to monitor over-intervention and trust impact.

---

### Disproportionate Impact
Differences in outcomes or intervention rates across user groups, regions, or content categories that cannot be explained by risk patterns alone.

Disproportionate impact is monitored to identify potential bias or unfairness.

---

## Governance and Operations

### Auditability
The ability to reconstruct and review how and why a case was surfaced, escalated, or acted upon.

Auditability includes access to signal sources, confidence levels, and human decision logs.

---

### Explainability
The ability to communicate system behavior and decisions to internal stakeholders in a clear and understandable manner.

Explainability is prioritized over model complexity in safety-critical contexts.

---

### Policy-Aligned
A design constraint requiring that system behavior adheres to existing platform policies and governance processes.

Policy-aligned systems do not independently define or modify enforcement rules.

---

### Adversarial Adaptation
Deliberate or incidental changes in user behavior intended to evade detection or exploit system thresholds.

Adversarial adaptation is expected over time and addressed through monitoring and iteration.

---

### Abstention
A system behavior in which no automated action is taken due to low confidence or conflicting signals.

Abstention favors human review or no action over forced decisions.

---

## Explicit Exclusions

The following are **out of scope** for this system and documentation:

- Intent inference or psychological diagnosis  
- Automated enforcement or punishment  
- Mental health assessment  
- Individual-level profiling beyond observable risk indicators  
- Real-time autonomous policy optimization  

---

## Notes

Glossary definitions may evolve as system design and governance considerations mature.  
All terms are intended to support shared understanding across product, engineering, operations, policy, and program management stakeholders.

# Early Risk Detection & Intervention System for LIVE + youth-adjacent media (Design Exercise)

## Repository Scope

This repository is intended as a design exercise for an **AI-assisted, human-in-the-loop safety system** focused on **LIVE features and youth-adjacent media**, where irreversible user impact and regulatory considerations necessitate conservative intervention and human oversight.

Related technical work exploring **fully automated Trust & Safety reasoning**, including prompt engineering, evaluation workflows, and model-side guardrails for LLMs, is maintained separately and intentionally scoped to non-user-facing contexts.

## Overview
This repository explores a risk-based, AI-assisted safety system designed to surface early warning signals and support proportionate intervention **before harm occurs** using a human-in-the-loop approach, particularly in high-risk contexts such as live interactions and youth (teens) exposure.

Traditional content moderation systems tend to focus on post-violation enforcement. While this might be effective at scale, this approach is often too slow for fast-evolving behaviors with ambiguous emerging risks. At the same time, overly aggressive automation risks false positives, creator harm, and loss of user trust.

This approach is informed by research on proactive moderation, which shows that moderators already implement early preventive strategies. Algorithmic support is most effective when it augments existing workflows rather replacing them. Prior works also highlights that proactive interventions can produce unfair or harmful outcomes when context is ignored, particulary in fast-evolving or adversarial environments. This reinforces the need for conservative deployment and sustained human review (human-in-the-loop). To address ambiguity and uncertainty, the system must prioritize **confidence-weighted signals and escalations**, drawing on research that supports selective intervention and abstention in high-stakes decision-making settings.

This project proposes a staged safety funnel that prioritizes **early detection, human-in-the-loop decision-making, and graduated interventions**, while maintaining an auditable, explainable, and policy-aligned position.

---

## What This Project Is
- A **product and systems design exercise**
- A **risk-based safety funnel**, not a single classifier
- A framework for **early detection and escalation**, not enforcement
- An exploration of how AI can **support** human judgment in safety-critical workflows

## What This Project Is Not
- A production-ready moderation system  
- A fully automated enforcement solution  
- A tool that infers user intent or diagnoses mental health  
- A replica of any real platform’s internal systems  

All data used in this repository is **synthetic and illustrative**.

---

## Problem Statement
Large-scale media and entertainment platforms are proactively recruiting talent to detect and respond to emerging safety risks early, with and without the application of AI, especially when harmful behaviors evolve faster than static rules and enforcement systems.

This challenge is particularly pronounced in 'Live' products and youth-adjacent contexts, where:
- Harm can escalate rapidly
- Signals are ambiguous
- Over-intervention can cause unintended damage

This project examines how a **risk-based AI-assisted funnel** can detect early indicators, enable timely human review processes, and support proportionate intervention before harm becomes widespread.

---

## System Concept (High-Level)
The proposed system follows a staged funnel:

1. **Lightweight Risk Signals**  
   Early indicators from content, behavior, and context, including **AI-assisted signal extraction** from text, audio, visual, and behavioral metadata.

2. **Context Enrichment**  
   Historical patterns, audience composition, and trend signals **augmented by machine learning models** to surface correlations and emerging patterns.

3. **Risk Tier Assignment**  
   Confidence-weighted risk categorization (not binary decisions), informed by aggregated signals rather than direct enforcement logic

4. **Intervention Routing**  
   Graduated actions such as friction, prompts, or human review, based on risk tier and confidence thresholds.

5. **Human-in-the-Loop Review**  
   Moderators retain final decision authority, with AI outputs presented as decision support rather than recommendations.

6. **Feedback Loop**  
   Enforcement outcomes inform future thresholds and signals, enabling **iterative models and rule refinement**.

Detailed operational workflows, escalation logic, and moderator action paths are documented in the PRD.md and illustrated in the system diagrams located in the diagrams folder.
---

## Why Pre-Harm Framing
This system focuses on **risk of harmful outcomes**, not intent prediction. It avoids diagnosing users or making irreversible decisions automatically. The goal is to intervene earlier, with lighter-touch actions, and escalate only when confidence increases.

---

## Key Design Principles
- **Human accountability over automation**
- **Confidence-weighted signals, not binary labels**
- **Early, proportionate intervention**
- **Auditability and explainability**
- **Policy-aligned guardrails**

---

## How to Navigate This Repository

This repository is organized to reflect how a Safety PM would reason about system design rather than production implementation.

Recommended reading order:
1. **README.md** – Problem framing and system overview
2. **/docs/PRD.md** – Product requirements and scope
3. **/docs/DecisionMemo.md** – Key tradeoffs and design rationale
4. **/diagrams/** – Visual system and workflow diagrams
5. **/prototype/** – Lightweight simulation demonstrating decision flow

The prototype is intentionally minimal and exists to illustrate system behavior, not model performance or production readiness.

---

## Repository Structure

ai-assisted-safety-intervention/
├── README.md
├── docs/
│ ├── PRD.md
│ ├── DecisionMemo.md
│ ├── EthicsAndSafety.md
│ └── Glossary.md
├── diagrams/
│ ├── 01_safety_funnel_overview.png
│ ├── 02_risk_signal_taxonomy.png
│ ├── 03_trend_discovery_graph.png
│ └── 04_human_in_loop_workflow.png
├── prototype/
│ ├── README.md
│ ├── simulate_sessions.py
│ ├── risk_scoring.py
│ ├── routing_logic.py
│ └── sample_output/
├── data/
│ ├── synthetic_sessions.json
│ └── synthetic_signals.json
└── LICENSE

---

## Status
This is an evolving design exercise and will be updated as assumptions, tradeoffs, and safety considerations are refined.

---

## Selected References (Academic)

This project is informed by prior work on proactive moderation, human-in-the-loop system design, uncertainty-aware decision support, and adversarial evasion in moderation settings.

### Proactive moderation and early risk detection
- Schluger et al., “Proactive Moderation of Online Discussions: Existing Practices and the Potential for Algorithmic Support” (2022). :contentReference[oaicite:0]{index=0}  
- Warner et al., “A critical reflection on the use of toxicity detection algorithms within proactive moderation systems” (2025). :contentReference[oaicite:1]{index=1}  
- Ollagnier et al., “Challenges and Advances in Predicting Online Antisocial Behavior” (systematic review, includes early harm detection and proactive moderation support) (2025). :contentReference[oaicite:2]{index=2}  

### Human-in-the-loop moderation and oversight
- Link et al., “A Human-is-the-Loop Approach for Semi-Automated Content Moderation” (2016). :contentReference[oaicite:3]{index=3}  
- Gómez-Carmona et al., “Human-in-the-loop machine learning: Reconceptualizing the users’ role…” (2024). :contentReference[oaicite:4]{index=4}  
- Crootof, “Humans in the Loop” (legal and governance perspective relevant to platform moderation oversight) (2023). :contentReference[oaicite:5]{index=5}  

### Uncertainty and abstention (decision support, not automation)
- Hasan et al., “Survey on Leveraging Uncertainty Estimation Towards Trustworthy Deep Neural Networks: Reject Option / Selective Classification” (2023). :contentReference[oaicite:6]{index=6}  
- Jiang Xin et al., “Selective Prediction and Error Regularization for Natural Language Processing” (2021). :contentReference[oaicite:7]{index=7}  
- Gawlikowski et al., “A Survey on Uncertainty Estimation in Deep Learning” (ACM Computing Surveys) (2021). :contentReference[oaicite:8]{index=8}  

### Adversarial and evasion considerations in moderation
- “Tri-modal Adversarial Attacks on Short Videos for Content Moderation” (introduces SVMA dataset and multimodal evasion framing) (2025). :contentReference[oaicite:9]{index=9}  
- Conti et al., “Captcha-based attacks in online social media” (discusses obfuscation techniques fooling automatic content moderators) (2023). :contentReference[oaicite:10]{index=10}  
- Kumbam et al., “Exploiting Explainability to Design Adversarial Attacks…” (ICWSM, hate-speech detection context) (2025). :contentReference[oaicite:11]{index=11}  

---

## Use of AI Tools

Large language models (GPT 5.2, Claude AI, Gemini) were used as **assistive tools** during the drafting and research phases of this project, including:
- Structuring early outlines and documentation drafts
- Summarizing publicly available academic literature
- Editing document writing for clarity and consistency
- Generating synthetic datasets

All system design decisions, tradeoffs, and final content reflect independent judgment.  
No proprietary data, platform-specific materials, or internal policies were used.

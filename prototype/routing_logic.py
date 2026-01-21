#!/usr/bin/env python3
"""
routing_logic.py

Maps a RiskOutput into a routing decision aligned with the PRD:
- graduated, reversible actions
- explicit human-in-the-loop for high-risk or low-confidence cases
- avoids irreversible enforcement in the prototype

Important:
- This is a portfolio prototype. Routing rules are illustrative and intentionally conservative.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
from risk_scoring import RiskOutput


@dataclass(frozen=True)
class RoutingDecision:
    suggested_action_tier: str   # none | prompt | friction | limit | human_review
    human_review_required: bool
    rationale: str
    reversible: bool
    requires_policy_signoff: bool


def route_case(risk: RiskOutput, inputs: Dict[str, Any]) -> RoutingDecision:
    """
    Convert (risk tier, confidence band, abstention) into an action tier.

    Key idea:
    - If confidence is low and risk is non-trivial, prefer human review.
    - Prefer reversible actions early (prompt/friction) before stronger actions (limit).
    """
    # Default: no action
    suggested = "none"
    human_review_required = False
    reversible = True
    requires_policy_signoff = False

    # Optional context knobs (kept minimal)
    content_format = inputs.get("content_format", "unknown")
    aud_u18 = inputs.get("aud_u18_share", None)
    youth_heavy = (aud_u18 is not None and aud_u18 >= 0.35 and content_format == "live")

    # Abstain under uncertainty
    if risk.abstain_flag:
        return RoutingDecision(
            suggested_action_tier="human_review",
            human_review_required=True,
            reversible=True,
            requires_policy_signoff=False,
            rationale="Low confidence with non-trivial risk → abstain from automated action and route to human review."
        )

    # Route by tier + confidence
    if risk.risk_tier == "low":
        suggested = "none"
        human_review_required = False
        reversible = True
        rationale = "Low risk tier → no intervention."
    elif risk.risk_tier == "med":
        # medium risk: friction by default, review if youth-heavy + medium confidence
        if youth_heavy and risk.confidence_band != "low":
            suggested = "human_review"
            human_review_required = True
            reversible = True
            rationale = "Medium risk + youth-heavy context → route to human review."
        else:
            suggested = "friction"
            human_review_required = False
            reversible = True
            rationale = "Medium risk → apply reversible friction to reduce escalation likelihood."
    else:  # high
        if risk.confidence_band == "high":
            suggested = "limit"
            human_review_required = False
            reversible = True  # still reversible in prototype
            requires_policy_signoff = True
            rationale = "High risk + high confidence → apply stronger (still reversible) limitation."
        else:
            suggested = "human_review"
            human_review_required = True
            reversible = True
            rationale = "High risk but not high confidence → route to human review."

    return RoutingDecision(
        suggested_action_tier=suggested,
        human_review_required=human_review_required,
        reversible=reversible,
        requires_policy_signoff=requires_policy_signoff,
        rationale=rationale,
    )

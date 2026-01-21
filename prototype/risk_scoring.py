#!/usr/bin/env python3
"""
risk_scoring.py

A lightweight, explainable risk scoring module for the portfolio prototype.

Important:
- This is NOT a production model.
- It demonstrates the *system behavior* described in the PRD:
  - confidence-weighted risk tiers
  - abstention under uncertainty
  - separation of signal extraction vs intervention decision-making

Design choices:
- Uses a simple weighted blend of synthetic signal scores and context proxies.
- Emits both:
  - risk_score: float in [0,1]
  - risk_tier: low/med/high
  - confidence_band: low/med/high
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import math


@dataclass(frozen=True)
class RiskOutput:
    risk_score: float
    risk_tier: str
    confidence_band: str
    abstain_flag: bool
    # components for auditability / explanation
    component_text: float
    component_audio: float
    component_visual: float
    component_behavior: float
    component_cross_age: float
    component_novelty: float
    completeness_penalty: float
    agreement_score: float


def _bounded(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


def _std(values: list[float]) -> float:
    if not values:
        return 0.0
    m = sum(values) / len(values)
    var = sum((v - m) ** 2 for v in values) / len(values)
    return math.sqrt(var)


def compute_risk_and_confidence(inputs: Dict[str, Any]) -> RiskOutput:
    """
    Compute a simple risk score and confidence band based on:
    - synthetic multi-signal scores (text/audio/visual/behavior/novelty)
    - cross-age interaction proxy
    - data completeness (e.g., missing audience mix)

    inputs expects fields defined in simulate_sessions._session_to_inputs.
    """

    # weights: keep stable and readable
    w = {
        "text": 0.22,
        "audio": 0.10,
        "visual": 0.18,
        "behavior": 0.28,
        "cross_age": 0.12,
        "novelty": 0.10,
    }

    text = float(inputs["text_signal"])
    audio = float(inputs["audio_signal"])
    visual = float(inputs["visual_signal"])
    behavior = float(inputs["behavior_signal"])
    novelty = float(inputs["novelty_score"])
    cross_age = float(inputs["cross_age_interaction_rate"])

    # completeness penalty: missing audience shares or region reduces confidence
    completeness_penalty = 0.0
    aud_u18 = inputs.get("aud_u18_share", None)
    if aud_u18 is None:
        completeness_penalty += 0.18
    if inputs.get("creator_region", None) in (None, "", "unknown"):
        completeness_penalty += 0.05

    # if audience is missing, cross-age component is less reliable
    cross_age_component = cross_age * (0.7 if aud_u18 is None else 1.0)

    comp_text = w["text"] * text
    comp_audio = w["audio"] * audio
    comp_visual = w["visual"] * visual
    comp_behavior = w["behavior"] * behavior
    comp_cross_age = w["cross_age"] * cross_age_component
    comp_novelty = w["novelty"] * novelty

    risk_score = _bounded(comp_text + comp_audio + comp_visual + comp_behavior + comp_cross_age + comp_novelty)

    # agreement: if signals disagree strongly, reduce confidence
    sigs = [text, audio, visual, behavior, novelty, cross_age_component]
    agreement_score = _bounded(1.0 - _std(sigs))  # higher is better

    # confidence combines agreement + completeness
    conf_raw = _bounded(0.55 * agreement_score + 0.45 * (1.0 - completeness_penalty))
    if conf_raw >= 0.72:
        confidence_band = "high"
    elif conf_raw >= 0.52:
        confidence_band = "med"
    else:
        confidence_band = "low"

    # tiering: conservative cutoffs; avoid over-escalating
    if risk_score >= 0.68:
        risk_tier = "high"
    elif risk_score >= 0.40:
        risk_tier = "med"
    else:
        risk_tier = "low"

    # abstain: medium/high risk but low confidence → prefer review over automated intervention
    abstain_flag = (risk_tier in ("med", "high") and confidence_band == "low")

    return RiskOutput(
        risk_score=risk_score,
        risk_tier=risk_tier,
        confidence_band=confidence_band,
        abstain_flag=abstain_flag,
        component_text=comp_text,
        component_audio=comp_audio,
        component_visual=comp_visual,
        component_behavior=comp_behavior,
        component_cross_age=comp_cross_age,
        component_novelty=comp_novelty,
        completeness_penalty=completeness_penalty,
        agreement_score=agreement_score,
    )

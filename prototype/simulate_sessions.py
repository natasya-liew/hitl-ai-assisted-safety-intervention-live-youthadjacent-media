#!/usr/bin/env python3
"""
simulate_sessions.py

Creates a small synthetic run from the canonical dataset files in ../data (or a user-provided path),
computes risk + routing, and writes a sample output JSON for demo purposes.

This script is intentionally lightweight: it demonstrates the *decision flow* described in the PRD
(signals → risk tiering → routing → HITL placeholder → outcomes), not model performance.

Usage:
  python simulate_sessions.py --sessions ../synthetic_sessions.csv --events ../synthetic_events.csv --out sample_output/risk_routing_example.json
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd

from risk_scoring import compute_risk_and_confidence, RiskOutput
from routing_logic import route_case, RoutingDecision


def _load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return pd.read_csv(path)


def _select_demo_sessions(
    sessions_df: pd.DataFrame,
    n: int = 12,
) -> pd.DataFrame:
    """
    Pick a small set of sessions that are interesting for demos:
    - include a mix of platforms and formats
    - include some abstention cases
    - include some low/med/high risk
    """
    # Basic candidates
    live_df = sessions_df[sessions_df["content_format"] == "live"]
    sv_df = sessions_df[sessions_df["content_format"] == "short_video"]

    # Prefer cases with diverse tiers
    def pick_by_tier(df: pd.DataFrame, tier: str, k: int) -> pd.DataFrame:
        sub = df[df["risk_tier"] == tier]
        return sub.sample(min(k, len(sub)), random_state=42) if len(sub) else df.sample(min(k, len(df)), random_state=42)

    picks = []
    if len(live_df):
        picks.append(pick_by_tier(live_df, "high", 3))
        picks.append(pick_by_tier(live_df, "med", 3))
        picks.append(pick_by_tier(live_df, "low", 2))
    if len(sv_df):
        picks.append(pick_by_tier(sv_df, "high", 1))
        picks.append(pick_by_tier(sv_df, "med", 2))
        picks.append(pick_by_tier(sv_df, "low", 1))

    demo = pd.concat(picks, ignore_index=True).drop_duplicates(subset=["session_id"])

    # If not enough, fill randomly
    if len(demo) < n:
        remaining = sessions_df[~sessions_df["session_id"].isin(demo["session_id"])]
        if len(remaining):
            demo = pd.concat([demo, remaining.sample(min(n - len(demo), len(remaining)), random_state=42)], ignore_index=True)

    return demo.head(n)


def _session_to_inputs(row: pd.Series) -> Dict[str, Any]:
    """
    Convert a sessions row to the inputs expected by the scoring function.
    Keep this explicit and readable.
    """
    return {
        "platform": row["platform"],
        "content_format": row["content_format"],
        "creator_age_band": row["creator_age_band"],
        "creator_region": row.get("creator_region", None),
        "account_tenure_days": int(row["account_tenure_days"]),
        "category": row["category"],
        # audience shares can be NaN in pandas
        "aud_u18_share": None if pd.isna(row.get("aud_u18_share")) else float(row["aud_u18_share"]),
        "aud_18_24_share": None if pd.isna(row.get("aud_18_24_share")) else float(row["aud_18_24_share"]),
        "aud_25_plus_share": None if pd.isna(row.get("aud_25_plus_share")) else float(row["aud_25_plus_share"]),
        "aud_unknown_share": None if pd.isna(row.get("aud_unknown_share")) else float(row["aud_unknown_share"]),
        "viewer_peak": int(row["viewer_peak"]),
        "join_rate_per_min": None if pd.isna(row.get("join_rate_per_min")) else float(row["join_rate_per_min"]),
        "exit_rate_per_min": None if pd.isna(row.get("exit_rate_per_min")) else float(row["exit_rate_per_min"]),
        "comment_rate_per_min": float(row["comment_rate_per_min"]),
        "cross_age_interaction_rate": float(row["cross_age_interaction_rate"]),
        "text_signal": float(row["text_signal"]),
        "audio_signal": float(row["audio_signal"]),
        "visual_signal": float(row["visual_signal"]),
        "behavior_signal": float(row["behavior_signal"]),
        "novelty_score": float(row["novelty_score"]),
        "trend_cluster_id": row["trend_cluster_id"],
        # optional: observed reports count
        "raw_report_count": int(row.get("raw_report_count", 0)),
    }


def _attach_recent_events(
    session_id: str,
    events_df: pd.DataFrame,
    max_rows: int = 6,
) -> List[Dict[str, Any]]:
    """
    Attach a few event slices for narrative.
    For LIVE, grab last few minutes; for short video, grab the single slice.
    """
    sub = events_df[events_df["session_id"] == session_id].sort_values("minute_index")
    if len(sub) == 0:
        return []
    # last max_rows
    tail = sub.tail(max_rows)
    # convert to plain JSON-friendly dicts with NaNs -> None
    out = []
    for _, r in tail.iterrows():
        d = r.to_dict()
        for k, v in list(d.items()):
            if pd.isna(v):
                d[k] = None
        out.append(d)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sessions", type=str, default="../data/synthetic_sessions.csv", help="Path to synthetic_sessions.csv")
    ap.add_argument("--events", type=str, default="../data/synthetic_events.csv", help="Path to synthetic_events.csv")
    ap.add_argument("--out", type=str, default="sample_output/risk_routing_example.json", help="Output JSON path")
    ap.add_argument("--n", type=int, default=12, help="Number of sessions to include in the demo output")
    args = ap.parse_args()

    sessions_df = _load_csv(Path(args.sessions))
    events_df = _load_csv(Path(args.events))

    demo_df = _select_demo_sessions(sessions_df, n=args.n)

    demo_cases: List[Dict[str, Any]] = []
    for _, row in demo_df.iterrows():
        session_id = str(row["session_id"])
        inputs = _session_to_inputs(row)

        risk_out: RiskOutput = compute_risk_and_confidence(inputs)
        routing: RoutingDecision = route_case(risk_out, inputs)

        demo_cases.append({
            "session_id": session_id,
            "platform": inputs["platform"],
            "content_format": inputs["content_format"],
            "category": inputs["category"],
            "inputs_snapshot": {
                # include a small subset for readability
                "creator_age_band": inputs["creator_age_band"],
                "creator_region": inputs["creator_region"],
                "aud_u18_share": inputs["aud_u18_share"],
                "viewer_peak": inputs["viewer_peak"],
                "cross_age_interaction_rate": inputs["cross_age_interaction_rate"],
                "signals": {
                    "text": inputs["text_signal"],
                    "audio": inputs["audio_signal"],
                    "visual": inputs["visual_signal"],
                    "behavior": inputs["behavior_signal"],
                    "novelty": inputs["novelty_score"],
                },
            },
            "risk_output": asdict(risk_out),
            "routing_decision": asdict(routing),
            "recent_event_slices": _attach_recent_events(session_id, events_df),
            "notes": "Synthetic example for portfolio demonstration. Not a production system."
        })

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_payload = {
        "generated_by": "simulate_sessions.py",
        "record_count": len(demo_cases),
        "cases": demo_cases
    }

    out_path.write_text(json.dumps(out_payload, indent=2), encoding="utf-8")
    print(f"Wrote demo output: {out_path.resolve()}")


if __name__ == "__main__":
    main()

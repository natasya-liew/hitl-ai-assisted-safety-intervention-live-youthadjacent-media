# Schema (Synthetic)

This document defines the schemas for the synthetic datasets used in this repository. It is intended to clarify field meanings, types, allowed values, nullability, and lightweight validation expectations.

The datasets are platform-agnostic and designed to resemble common patterns seen in short-form and live products across major media platforms.

---

## Files

- `synthetic_sessions.csv` / `synthetic_sessions.json`  
  One record per session (LIVE or short-form). Contains coarse creator metadata, session metadata, aggregated audience composition, synthetic multi-signal scores, risk outputs, routing/HITL fields, and downstream outcome proxies.

- `synthetic_events.csv` / `synthetic_events.json`  
  Time-sliced events per session. LIVE sessions include up to 15 minute-level slices. Short-form videos include one slice (`minute_index = 0`).

---

## Identifier formats (validation)

- `session_id`: `sess_000001` (regex: `^sess_\d{6}$`)
- `creator_account_id`: `acct_000001` (regex: `^acct_\d{6}$`)
- `trend_cluster_id`: `trend_01` (regex: `^trend_\d{2}$`)

---

## Enumerations

- `platform`: `tiktok | instagram | facebook | youtube`
- `content_format`: `live | short_video`
- `creator_age_band`: `u18 | 18_24 | 25_plus | unknown`
- `creator_region`: `NA | EU | LATAM | APAC | MEA` (nullable)
- `category`: `general | gaming | beauty | fitness | music | news | education | comedy | lifestyle | sports`
- `confidence_band`: `low | med | high`
- `risk_tier`: `low | med | high`
- `suggested_action_tier`: `none | prompt | friction | limit | human_review`
- `final_action_taken`: `none | prompt | friction | limit | human_review`
- `moderator_decision`: `approve | override | no_action | unknown`
- `event_flag` (events file): `report_spike | audience_shift | null`

---

## Shared numeric ranges (validation)

### Scores and rates
- Signal scores: `text_signal`, `audio_signal`, `visual_signal`, `behavior_signal`, `novelty_score` are floats in **[0, 1]**
- `risk_score` is a float in **[0, 1]**
- `cross_age_interaction_rate` is a float in **[0, 1]**
- `risk_velocity` is a float (typically small magnitude; may be negative or positive)

### Audience shares
- `aud_u18_share`, `aud_18_24_share`, `aud_25_plus_share`, `aud_unknown_share` are floats in **[0, 1]** or null
- When all four audience shares are present, they **typically sum to ~1.0** (small drift may occur due to rounding)

---

## Schema: `synthetic_sessions.*`

### Columns

| Field | Type | Nullable | Description |
|---|---:|:---:|---|
| session_id | string | No | Unique session identifier |
| platform | enum | No | Platform label for cross-platform applicability |
| content_format | enum | No | `live` or `short_video` |
| creator_account_id | string | No | Synthetic creator identifier |
| creator_age_band | enum | No | Coarse age band |
| creator_region | enum | Yes | Coarse region (nullable for "unknown") |
| account_tenure_days | int | No | Synthetic account age (days) |
| start_time_local | string (ISO-8601) | No | Local timestamp for session start |
| duration_sec | int | No | Session duration in seconds |
| category | enum | No | High-level content category |
| aud_u18_share | float | Yes | Audience share under 18 (aggregated) |
| aud_18_24_share | float | Yes | Audience share 18–24 (aggregated) |
| aud_25_plus_share | float | Yes | Audience share 25+ (aggregated) |
| aud_unknown_share | float | Yes | Audience share unknown (aggregated) |
| viewer_peak | int | No | Peak viewers (LIVE) or views proxy (short-form) |
| join_rate_per_min | float | Yes | Join rate (LIVE); null for short-form |
| exit_rate_per_min | float | Yes | Exit rate (LIVE); null for short-form |
| comment_rate_per_min | float | No | Comment rate proxy per minute |
| cross_age_interaction_rate | float | No | Aggregate cross-age interaction proxy |
| text_signal | float | No | Synthetic text-based signal score |
| audio_signal | float | No | Synthetic audio-based signal score |
| visual_signal | float | No | Synthetic visual-based signal score |
| behavior_signal | float | No | Synthetic behavioral signal score |
| novelty_score | float | No | Synthetic novelty / emerging trend score |
| trend_cluster_id | string | No | Synthetic trend cluster identifier |
| risk_score | float | No | Aggregated risk score |
| risk_velocity | float | No | Approximate change in risk over time (LIVE) |
| confidence_band | enum | No | Confidence band for risk assessment |
| risk_tier | enum | No | Low/medium/high risk tier |
| abstain_flag | bool | No | If true, system prefers review due to low confidence |
| suggested_action_tier | enum | No | Suggested intervention tier pre-review |
| human_review_required | bool | No | Whether the system routes to human review |
| moderator_decision | enum | No | Moderator outcome (or `unknown` if no review) |
| final_action_taken | enum | No | Final action applied after review/routing |
| raw_report_count | int | No | Synthetic count of reports during session |
| downstream_harm_report_count | int | No | Synthetic downstream reports proxy |
| policy_violation_downstream | bool | No | Synthetic downstream violation proxy |
| appeal_or_reversal | bool | No | Synthetic appeal/reversal proxy |
| driver_age_risk | bool | No | Synthetic driver flag: age-related risk present |
| driver_boundary_escalation | bool | No | Synthetic driver flag: boundary escalation present |
| driver_contextual_vulnerability | bool | No | Synthetic driver flag: contextual vulnerability present |
| driver_emerging_trend | bool | No | Synthetic driver flag: emerging trend present |

### Notes
- Audience share fields may be fully null to simulate privacy/telemetry gaps.
- `moderator_decision` remains `unknown` when no human review occurs.
- Driver fields are included to support debugging and explanation in the prototype; they are not intended as real-world features.

---

## Schema: `synthetic_events.*`

### Columns

| Field | Type | Nullable | Description |
|---|---:|:---:|---|
| session_id | string | No | Foreign key to sessions |
| minute_index | int | No | Minute slice index (0-based). Short-form uses 0 |
| viewer_count | int | No | Viewer count at this slice (LIVE) or views proxy |
| join_rate_per_min | float | Yes | Join rate at minute slice (LIVE). Null for short-form |
| comment_rate_per_min | float | Yes | Comment rate at minute slice |
| aud_u18_share | float | Yes | Audience share under 18 at slice |
| aud_18_24_share | float | Yes | Audience share 18–24 at slice |
| aud_25_plus_share | float | Yes | Audience share 25+ at slice |
| aud_unknown_share | float | Yes | Audience unknown share at slice |
| text_signal | float | No | Text signal at slice |
| audio_signal | float | No | Audio signal at slice |
| visual_signal | float | No | Visual signal at slice |
| behavior_signal | float | No | Behavior signal at slice |
| novelty_score | float | No | Novelty score at slice |
| risk_score | float | No | Risk score at slice |
| event_flag | enum | Yes | Optional event marker (`report_spike`, `audience_shift`) |

### Notes
- LIVE sessions include multiple slices (up to 15) to model escalation and velocity.
- Some slices may include an `event_flag` to support edge-case demonstrations.

---

## Recommended integrity checks (lightweight)

These checks are intentionally minimal and are meant for prototype robustness rather than data engineering completeness:

1. **ID format validation** for `session_id` and `creator_account_id`.
2. **Enum validation** for categorical fields.
3. **Range validation** for scores in [0, 1].
4. **Audience shares**: if any share is non-null, either:
   - all four shares are present and sum to ~1.0, **or**
   - shares are intentionally partial (documented as an edge-case).
5. **Short-form join/exit rates** should be null.

---

## Data generation disclaimer

All fields are synthetic. Any resemblance to real users or sessions is coincidental. The dataset is designed for demonstrating the design patterns described in the PRD (confidence-weighted risk tiers, HITL routing, reversible interventions, and auditability) rather than for training production models.

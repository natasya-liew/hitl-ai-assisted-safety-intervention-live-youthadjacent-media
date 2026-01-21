# Data Package (Synthetic)

This folder contains **fully synthetic** data designed to demonstrate the end-to-end behavior of the Early Risk Detection & Intervention System (signals → risk tiering → routing → HITL decisions → outcomes).

No real users, creators, or platform data is included. Values are simulated to resemble common patterns seen in short-form and live products across major platforms (e.g., TikTok, Instagram, YouTube, Facebook) while remaining platform-agnostic.

## Files

- `synthetic_sessions.csv` / `synthetic_sessions.json`  
  One row (or object) per session. Includes creator metadata (coarse), session metadata, aggregated audience composition, synthetic multi-signal scores, risk outputs, routing outcomes, and downstream outcome proxies.

- `synthetic_events.csv` / `synthetic_events.json`  
  Time-sliced events for sessions. Live sessions include up to 15 minute-level slices to support demonstrating escalation and risk velocity. Short videos include a single slice.

## Data realism approach

The dataset is "clean core + realistic edge cases":
- **80–90%** of rows are complete and consistent (for clarity and reproducibility).
- **10–20%** of rows include realistic operational issues such as:
  - Missing audience composition (privacy/telemetry gaps)
  - Missing coarse region (unknown)
  - Delayed signal spikes in live sessions
  - Conflicting signals (e.g., text high but behavior low)
  - Report spikes that may or may not correspond to downstream violations

## Nullability and validation

### Identifiers
- `session_id` format: `sess_000001` (regex: `^sess_\d{6}$`)
- `creator_account_id` format: `acct_000001` (regex: `^acct_\d{6}$`)

### Enumerations
- `platform`: `tiktok | instagram | facebook | youtube`
- `content_format`: `live | short_video`
- `risk_tier`: `low | med | high`
- `confidence_band`: `low | med | high`
- `suggested_action_tier` / `final_action_taken`: `none | prompt | friction | limit | human_review`

### Nullable fields
- Audience shares (`aud_*_share`) may be null (unknown or unavailable).
- For `short_video`, `join_rate_per_min` and `exit_rate_per_min` may be null.

### Ranges
- Signal scores (`*_signal`, `novelty_score`, `risk_score`, `cross_age_interaction_rate`) are in `[0, 1]`.
- Audience shares are in `[0, 1]` and typically sum to ~1.0 when present.

## Notes on interpretation

- Signal fields represent **synthetic model outputs**, not raw content.
- `abstain_flag=true` indicates the system preferred human review due to low confidence.
- `policy_violation_downstream` and `downstream_harm_report_count` are synthetic outcome proxies used for demonstration only.

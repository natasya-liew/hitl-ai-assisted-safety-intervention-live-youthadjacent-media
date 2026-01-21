# Edge-Case Scenarios (Synthetic)

These scenarios are intentionally represented in ~10–20% of the synthetic dataset to demonstrate real-world constraints and the system’s behavior under uncertainty.

1. **Missing audience composition**
   - `aud_*_share` is null (or partially null) due to privacy or telemetry gaps.
   - Expected behavior: confidence decreases; system may abstain or escalate to review.

2. **Missing region**
   - `creator_region` is null.
   - Expected behavior: reduced confidence; conservative routing when risk is elevated.

3. **Delayed signal spike (LIVE)**
   - Early slices show low signals; a spike appears mid-session.
   - Expected behavior: risk velocity increases; routing escalates based on change over time.

4. **Conflicting signals**
   - Example: `text_signal` high while `behavior_signal` low (or vice versa).
   - Expected behavior: confidence decreases; system favors abstention or human review.

5. **Report spike without downstream violation**
   - `event_flag=report_spike` occurs but `policy_violation_downstream=false`.
   - Expected behavior: avoid punitive bias; rely on multi-signal context.

6. **Audience shift toward youth**
   - `event_flag=audience_shift` and `aud_u18_share` increases sharply.
   - Expected behavior: age-related risk indicators increase; conservative routing.

7. **High novelty, low other signals**
   - `novelty_score` is high but other signals are low.
   - Expected behavior: track as emerging trend candidate; do not over-intervene.

8. **High engagement volatility**
   - Large changes in `viewer_count`, `join_rate_per_min`, or `comment_rate_per_min`.
   - Expected behavior: treat as contextual signal; rely on combined indicators.

9. **Low-risk session with strong intervention (false positive proxy)**
   - Low `risk_score` but `final_action_taken` is `friction` or `limit`, increasing `appeal_or_reversal`.
   - Expected behavior: monitor guardrails; refine thresholds and review cues.

10. **Medium/high risk + low confidence (abstention case)**
   - `risk_tier=med` or `high` with `confidence_band=low`.
   - Expected behavior: `abstain_flag=true`, route to human review.

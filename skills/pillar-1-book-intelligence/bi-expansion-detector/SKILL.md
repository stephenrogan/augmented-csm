---
name: bi-expansion-detector
description: Identifies accounts showing signals of readiness for expansion including upsell, cross-sell, and seat or licence growth. Surfaces opportunity with evidence so humans can time the commercial conversation. Use when asked to find expansion opportunities, identify upsell candidates, detect cross-sell signals, analyse licence utilisation for growth, build an expansion pipeline, score accounts for commercial readiness, or when any workflow needs to know which accounts are ripe for growth. Also triggers for questions about expansion scoring, revenue growth signals, or commercial opportunity identification.
license: MIT
metadata:
  version: "1.0.0"
  pillar: book-intelligence
  category: detection-layer
---

# Expansion Signal Detector

Identifies accounts ready for expansion and surfaces opportunity with evidence. Part of the Book Intelligence detection layer -- feeds directly into the Commercial Motion pillar (Pillar 5) where humans own the timing, framing, and execution of expansion conversations.

This is a **detection and surfacing** skill. It identifies expansion signals and scores opportunity. It never initiates commercial conversations, sends pricing, or makes offers. The boundary between Book Intelligence and Commercial Motion is absolute here.

## When to Run

- **Scheduled**: Weekly scan across all accounts
- **Triggered**: When Usage Pattern Monitor flags breakout growth or when licence utilisation exceeds threshold
- **On-demand**: When a human requests an expansion assessment for a specific account

## Core Execution Logic

### Step 1: Apply Health Filter

**Critical rule**: Do not surface expansion signals on unhealthy accounts.

Filter out any account with:
- Health Score Engine composite below 70
- Any active risk signal from the Risk Signal Detector
- Known open support escalation (P1 or P2)

Rationale: Asking an unhealthy customer to buy more is tone-deaf and damages trust. Fix the health first, then pursue expansion.

### Step 2: Evaluate Expansion Signals

For each account that passes the health filter, check the following signals:

**Licence Utilisation Signal**
- Trigger: Active users / purchased seats > 80% sustained for 30+ days
- Strength: High (direct demand signal)
- Expansion type: Seat growth
- Evidence: Current utilisation rate, trend, days above threshold

**Feature-Gating Signal**
- Trigger: Users attempt to access features above current product tier 3+ times in 30 days
- Strength: High (demonstrated demand for higher-tier capabilities)
- Expansion type: Tier upgrade
- Evidence: Features attempted, frequency, user roles attempting access

**Usage Breadth Growth**
- Trigger: New teams or departments begin adopting within the last 60 days (detected via new user clusters or new use-case patterns)
- Strength: Medium-High (organic spread indicates internal advocacy)
- Expansion type: Seat growth or cross-sell
- Evidence: New user count, department/team identifiers if available, usage patterns

**Usage Depth Growth**
- Trigger: Power user metrics exceed segment 90th percentile
- Strength: Medium (indicates deep value realisation among active users)
- Expansion type: Tier upgrade (power users often need advanced features)
- Evidence: Specific metrics exceeding threshold, user count at power-user level

**Contract Maturity**
- Trigger: Account past initial adoption phase (6+ months on contract) with stable or growing usage
- Strength: Low (enabling condition, not a signal on its own)
- Expansion type: Any
- Evidence: Contract age, usage trend classification

### Step 3: Score Opportunity

For each account with one or more expansion signals:

1. Sum the signal strength scores (High=3, Medium-High=2.5, Medium=2, Low=1)
2. Apply a multiplier based on current health (health 70-80: 0.8x, 81-90: 1.0x, 91-100: 1.2x)
3. Classify expansion type based on the dominant signal (licence utilisation points to seat growth, feature-gating points to tier upgrade, breadth growth points to cross-sell)

If historical conversion data is available (signal-to-closed-expansion), use it to calibrate scores. See `references/conversion-calibration.md`. Default to the scoring above until calibration data is available.

### Step 4: Estimate Timing Window

Based on the signal pattern:
- Licence utilisation >90%: Immediate opportunity (customer is likely already feeling the constraint)
- Feature-gating hits accelerating: 30-60 day window (customer is exploring but has not made a decision)
- Breadth growth in early stages: 60-90 day window (let the organic adoption mature before approaching commercially)
- Depth growth only: 90+ day window (deepen the relationship before introducing commercial conversation)

### Step 5: Generate Opportunity Brief

```json
{
  "account_id": "string",
  "account_name": "string",
  "current_arr": 42000,
  "health_score": 84,
  "opportunity_score": 7.2,
  "expansion_type": "seat_growth",
  "timing_window": "immediate",
  "signals": [
    {
      "signal": "licence_utilisation",
      "strength": "high",
      "evidence": "Utilisation at 93% for 45 consecutive days. 3 users sharing credentials (detected via concurrent session patterns)",
      "first_detected": "2026-01-25"
    },
    {
      "signal": "usage_breadth_growth",
      "strength": "medium_high",
      "evidence": "12 new users from Marketing department onboarded organically in last 40 days",
      "first_detected": "2026-02-01"
    }
  ],
  "recommended_approach": "Customer is capacity-constrained and expanding organically. Seat growth conversation is natural. Lead with the new Marketing team adoption as evidence of broadening value.",
  "handoff_to": "csm_commercial_review"
}
```

### Step 6: Suppress and Deduplicate

- Do not re-surface an expansion signal that has already been acknowledged by the CSM
- If an expansion opportunity has been pursued and the customer declined, suppress for 90 days unless a new signal type appears
- If an account's health drops below 70 after an expansion signal is surfaced, withdraw the signal and notify the CSM

## Output Format

**Expansion opportunity queue (weekly):**
- Ranked list of accounts with expansion signals, ordered by opportunity score
- Each entry includes: account name, ARR, health score, expansion type, timing window, signal evidence, recommended approach

**Monthly expansion pipeline report:**
- New opportunities surfaced this month
- Opportunities converted to active commercial conversations
- Revenue from signal-sourced expansions (requires feedback loop from Commercial Motion pillar)
- Signal-to-conversion rate by signal type

## Handoff to Human

| Condition | Routing | Urgency |
|-----------|---------|---------|
| Licence utilisation >90% sustained | Direct alert to CSM | This week |
| Feature-gating acceleration | Weekly expansion digest | Next review cycle |
| Breadth growth (new teams) | Weekly expansion digest | Next review cycle |
| Multiple signals clustering | Direct alert to CSM | This week |

The human decides: pursue now, nurture first, or park. The human owns the timing, the framing, and the commercial conversation. See `references/human-decision-guide.md`.

## Confidence and Limitations

- **Medium confidence** overall. Signal detection is reliable; conversion probability estimation requires historical calibration
- **High confidence** for licence utilisation (direct demand signal with minimal ambiguity)
- **Medium confidence** for feature-gating and breadth growth (strong indicators but not guarantees of commercial readiness)
- **Low confidence** for timing estimates without historical conversion data. Default to conservative timing
- Cannot detect expansion readiness that exists only in relationship context (e.g., customer mentions budget availability in a call but usage data shows nothing unusual)
- The health filter is deliberately conservative. Some accounts below 70 health may still be expansion candidates if the health issue is isolated. The human can override

## Dependencies

**Required:**
- `bi-health-score` (health filter and health multiplier)
- `bi-usage-monitor` (breakout growth, usage depth/breadth signals)
- CRM licence/contract data (utilisation calculation, contract age)
- Product analytics (feature-gating events, user clustering)

**Optional:**
- `bi-risk-detector` (to suppress expansion on accounts with active risk)
- Product tier configuration (for feature-gating signal mapping)
- Historical expansion data (for conversion calibration)

**Downstream consumers:**
- Commercial Motion pillar (Pillar 5) -- the primary consumer
- `bi-account-brief` (active expansion signals for account context)
- Leadership reporting (expansion pipeline)

## References

- `references/conversion-calibration.md` -- How to calibrate opportunity scores with historical data
- `references/human-decision-guide.md` -- How CSMs should evaluate and act on expansion signals

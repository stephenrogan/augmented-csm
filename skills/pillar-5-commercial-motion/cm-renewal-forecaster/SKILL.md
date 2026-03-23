---
name: cm-renewal-forecaster
description: Forecasts renewal outcomes across the portfolio by combining health data, engagement signals, usage trends, and historical patterns into probability-weighted projections. Produces renewal pipeline reports for CS leadership, CRO, and CFO audiences. Use when asked to forecast renewals, predict churn probability, build a retention forecast, assess portfolio renewal risk, project NRR, or when leadership needs forward-looking retention data. Also triggers for questions about renewal probability, churn forecasting, NRR projection, retention pipeline, or revenue risk assessment.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: commercial-motion
  category: commercial-ops
---

# Renewal Forecaster

Produces probability-weighted renewal forecasts by combining health signals, usage data, engagement patterns, and historical outcomes. Part of the Commercial Motion pillar.

This is an **analytical and reporting** skill. It produces forecasts and projections. It does not make retention decisions or set strategy -- those are human calls informed by the forecast.

## When to Run

- **Scheduled**: Weekly forecast refresh for all accounts renewing in next 180 days
- **On-demand**: When leadership requests a forecast update
- **Triggered**: When a significant risk or health signal changes on an account within the renewal window

## Core Execution Logic

### Step 1: Identify Renewal Cohort

Pull all accounts with renewal dates in the next 180 days. For each, assemble:
- Current health score and trend (from bi-health-score)
- Risk signal count and severity (from bi-risk-detector)
- Usage trend classification (from bi-usage-monitor)
- Engagement pattern (from ra-engagement-tracker)
- Renewal risk classification (from lo-renewal-manager: On Track / Watch / At Risk / Critical)
- Expansion signals (from bi-expansion-detector -- renewals with expansion opportunity are a different conversation)
- Contract details (ARR, term, auto-renewal clause, notice period)

### Step 2: Assign Renewal Probability

**Default probability model** (use until historical calibration data is available):

| Risk Classification | Base Probability | Positive Adjustments | Negative Adjustments |
|--------------------|-----------------|---------------------|---------------------|
| On Track | 95% | +2% if health >85 and stable for 90+ days | -5% if any single risk signal present; -10% if engagement declining |
| Watch | 75% | +10% if active save play showing health improvement | -10% per additional risk signal; -5% if usage declining; -15% if competitive signal |
| At Risk | 45% | +15% if executive engaged and customer responding to intervention | -10% if competitive signal; -15% if champion departed; -10% if timeline <60 days with no progress |
| Critical | 15% | +20% if customer explicitly willing to negotiate (not silent) | -10% if timeline <30 days; -15% if customer stated intent to leave |

**Probability bounds**: Floor at 5% (even "certain" churns occasionally reverse). Cap at 98% (even "certain" renewals occasionally surprise).

**Calibration**: After 12 months of data, replace the default model with historically-calibrated probabilities. See `references/probability-calibration.md`.

### Step 3: Compute Portfolio Forecast

Aggregate individual account probabilities into portfolio-level projections:

| Metric | Computation |
|--------|------------|
| Expected retained ARR | Sum of (account ARR * renewal probability) for all renewing accounts |
| Expected churn ARR | Sum of (account ARR * (1 - renewal probability)) |
| Expected expansion ARR | Sum of (expansion opportunity value * expansion probability) for accounts with both renewal and expansion |
| Forecast NRR | (Expected retained ARR + Expected expansion ARR) / Total renewing ARR |
| Optimistic scenario (80% CI) | Assume all Watch accounts renew, At Risk accounts at 60%, Critical at 25% |
| Pessimistic scenario (80% CI) | Assume Watch accounts at 60%, At Risk at 30%, Critical at 5% |
| Most likely scenario | Use the computed probabilities as-is |

### Step 4: Identify Actionable Accounts

Flag accounts where intervention could meaningfully change the forecast:

| Category | Criteria | Why Actionable |
|----------|----------|---------------|
| Saveable At Risk | At Risk, renewal >60 days away, no competitive signal, root cause is addressable | Enough time and a path to resolution exists |
| Critical but engaged | Critical, customer is still communicating and willing to discuss | Window is closing but customer has not fully disengaged |
| Watch trending down | Watch, health declining for 2+ consecutive periods | Currently probable renewal, but trajectory suggests it may become At Risk without intervention |
| Expansion at renewal | On Track with active expansion signal and renewal in next 90 days | Opportunity to convert a renewal into a growth event |

### Step 5: Generate Forecast Report

```json
{
  "forecast_date": "2026-03-10",
  "horizon": "next_180_days",
  "portfolio": {
    "renewing_accounts": 42,
    "renewing_arr": 3200000
  },
  "forecast": {
    "most_likely": {
      "retained_arr": 2880000,
      "churn_arr": 320000,
      "expansion_arr": 180000,
      "nrr": 0.956
    },
    "optimistic": { "nrr": 0.982 },
    "pessimistic": { "nrr": 0.921 }
  },
  "by_classification": {
    "on_track": { "count": 28, "arr": 2100000, "avg_probability": 0.94 },
    "watch": { "count": 8, "arr": 680000, "avg_probability": 0.72 },
    "at_risk": { "count": 4, "arr": 340000, "avg_probability": 0.41 },
    "critical": { "count": 2, "arr": 80000, "avg_probability": 0.13 }
  },
  "actionable_accounts": [
    {
      "account": "Acme Corp",
      "arr": 85000,
      "renewal_date": "2026-05-15",
      "days_remaining": 66,
      "classification": "at_risk",
      "probability": 0.45,
      "category": "saveable_at_risk",
      "top_risk": "Champion departed February, usage declining since",
      "intervention_opportunity": "New VP Engineering hired last week -- window to establish relationship before renewal window",
      "csm": "Jane Doe"
    }
  ],
  "period_over_period": {
    "nrr_change_vs_last_week": -0.003,
    "accounts_worsened": 2,
    "accounts_improved": 1,
    "new_at_risk": 1
  }
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Forecast review | Full forecast with scenarios and actionable accounts | Whether the probabilities match their qualitative intelligence. CSM managers override individual account probabilities based on relationship context |
| Resource allocation | Actionable accounts ranked by save potential and ARR | Which accounts to invest save effort in, given limited CSM capacity |
| Executive communication | Forecast with confidence intervals | How to present the forecast to the CRO/CFO -- which scenario to emphasise, what narrative to frame around the numbers |
| Expansion timing | Accounts with both renewal and expansion signals | Whether to pursue expansion at renewal (efficient) or separate the conversations (less risky) |

## Confidence and Limitations

- **High confidence** for timeline tracking and milestone computation -- deterministic calendar logic
- **Medium confidence** for probability estimation using the default model -- health and signal data are strong predictive inputs, but the model has not been calibrated against your specific portfolio's churn patterns until you have 12 months of data
- **Medium confidence** for portfolio aggregation -- individual account probabilities may be off, but errors tend to cancel out at the portfolio level (some pessimistic, some optimistic). The aggregate forecast is more reliable than any individual account prediction
- **Low confidence** for accounts with limited data history (<6 months) or accounts where the risk is purely relationship-based with no data signal
- Probability estimates should be treated as directional, not precise. "75% renewal probability" means "more likely than not with moderate risk," not a guarantee
- The forecast does not account for portfolio-level events (pricing changes, product launches, market shifts) that may move multiple renewals simultaneously. The human must factor these in
- The optimistic/pessimistic scenarios are bounded estimates, not worst-case/best-case. True worst case (major product failure, market crash) is outside the model

## Dependencies

**Required:**
- lo-renewal-manager (renewal classifications, timeline data)
- bi-health-score (health data for probability computation)
- CRM API (contract data, ARR, renewal dates)

**Strongly recommended:**
- bi-risk-detector (risk signal count and severity)
- bi-usage-monitor (usage trend for trajectory assessment)
- bi-expansion-detector (expansion signals for combined renewal-expansion opportunities)
- ra-engagement-tracker (engagement pattern for probability adjustment)

**Downstream consumers:**
- CS leadership (weekly forecast review)
- CRO/CFO (monthly/quarterly revenue planning)
- Board reporting (quarterly NRR projection)
- ic-cross-func-prep (pipeline review materials)

## References

- `references/probability-calibration.md` -- Historical calibration methodology, minimum data requirements, and model validation process

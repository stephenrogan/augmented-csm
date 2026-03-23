# Human Decision Guide: Renewal Forecast Review

## Your Role

The Renewal Forecaster produces probability-weighted renewal predictions based on health, engagement, commercial signals, and historical patterns. Your job is to validate the forecast against your relationship knowledge, adjust where the model is wrong, and decide what actions each renewal requires. The model sees data. You see the customer.

## When You Will See This

Forecast outputs are generated:

1. **Weekly** -- full portfolio forecast refresh for all accounts renewing in the next 180 days
2. **On leadership request** -- ad hoc forecast updates for pipeline reviews or board reporting
3. **On signal change** -- when a significant risk or health event changes the outlook for an account within the renewal window

## Decision Framework

### 1. Validate the probability

- Does the model's confidence match your gut? When they diverge, investigate why. Sometimes you know something the data doesn't -- a verbal commitment, an internal champion pushing for renewal. Sometimes the data has spotted something you've missed -- a usage decline you haven't noticed, a support pattern you've normalised.
- Check the key drivers. If the probability is low, which signals are pulling it down? Are they current or stale? A risk signal from 60 days ago that has since been resolved should not still be dragging the forecast.
- Compare to the customer's stated intent. Have they said anything about renewal plans? Verbal signals often lead data signals by 30-60 days. If the customer has told you they are renewing, the model should reflect that -- override if it doesn't.

### 2. Classify each renewal

| Category | Probability Range | Your Action |
|----------|------------------|-------------|
| **Locked** | 90%+ | Light touch -- confirm timeline, prepare paperwork, look for expansion opportunity |
| **Expected** | 70-89% | Standard process -- QBR if due, value reinforcement, stakeholder check |
| **At risk** | 40-69% | Active intervention -- identify the blocker, build a save plan, engage leadership if needed |
| **Unlikely** | Below 40% | Triage decision -- is this saveable? If yes, full escalation. If no, begin transition planning and protect remaining revenue |

### 3. Adjust the forecast

Log your override with reasoning. This creates the feedback loop that improves the model over time:
- "Adjusted from 65% to 85% -- spoke with CTO yesterday, confirmed budget allocated and renewal approved internally"
- "Adjusted from 80% to 50% -- champion departed last week, no replacement identified, remaining contacts are disengaged"

Your overrides are not corrections of the model -- they are additions of information the model cannot access. Both the model's view and your view have value.

## Special Handling

### The 70% trap

Accounts forecast at 70-80% are the most dangerous segment of your portfolio. High enough that they don't trigger intervention protocols. Low enough that they're not actually safe. Apply more scrutiny to this range than any other. For every account in this band, ask: what specific evidence supports this being above 50%? If you cannot name it, the account is at risk and the forecast is generous.

### Multi-year renewals

The forecast model may not account for multi-year contract dynamics -- auto-renewal clauses, price escalation terms, minimum commitment thresholds, or early termination windows. Review the contract terms directly for any renewal with ARR above your threshold. A forecast is only as good as its understanding of the commercial structure.

### Portfolio-level accuracy

Individual forecasts can be wrong. Portfolio-level forecasts should be accurate. If your aggregate forecast consistently over-predicts (you forecast 85% portfolio renewal and achieve 78%), the model or your overrides are systematically biased. Review your override patterns quarterly and calibrate.

### Forecast as a leadership communication tool

Your manager and their leadership will use this forecast to plan revenue, budget, and headcount. A forecast that is wrong in either direction is damaging. Over-optimistic forecasts cause surprise misses. Over-pessimistic forecasts cause unnecessary panic and intervention. Aim for accuracy, not comfort.

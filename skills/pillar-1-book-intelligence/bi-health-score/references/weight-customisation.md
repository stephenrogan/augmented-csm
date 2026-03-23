# Weight Customisation Guide

The default health score formula applies a fixed weighting across all accounts:

```
Composite = (Usage * 0.35) + (Engagement * 0.25) + (Support * 0.20) + (Sentiment * 0.10) + (Commercial * 0.10)
```

This default works for most B2B SaaS mid-market motions. It should be customised when the business model, segment, or go-to-market motion means a different signal mix better predicts retention.

## When to Customise

Customise weights when you observe a persistent disconnect between health scores and actual outcomes. Specifically:

- **Accounts churning with healthy scores**: The score is missing the signals that matter. The components being weighted down are likely the ones that predict churn in your context.
- **Accounts renewing with unhealthy scores**: The score is over-weighting signals that do not predict churn for this segment. Reduce those component weights.
- **A specific segment consistently scores higher/lower than outcomes justify**: The default weights do not fit that segment's retention drivers.

Do **not** customise weights reactively based on a single account outcome. Wait for a pattern across 10+ accounts before adjusting.

## Recommended Weight Profiles by Motion

### High-Touch Enterprise

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Usage | 0.25 | Still important but enterprise usage patterns are lumpy and seasonal |
| Engagement | 0.35 | Executive and multi-stakeholder engagement is the strongest retention signal |
| Support | 0.15 | Enterprise accounts tolerate more support friction when relationships are strong |
| Sentiment | 0.15 | NPS/CSAT from enterprise sponsors carries high predictive weight |
| Commercial | 0.10 | Unchanged |

### Product-Led Growth (PLG)

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Usage | 0.45 | Usage IS the relationship in PLG; decline predicts churn directly |
| Engagement | 0.10 | Low-touch model means engagement signals are sparse and less meaningful |
| Support | 0.20 | Unchanged |
| Sentiment | 0.10 | Unchanged |
| Commercial | 0.15 | Licence utilisation and expansion signals are strong in PLG |

### Scaled / Digital-Touch SMB

| Component | Weight | Rationale |
|-----------|--------|-----------|
| Usage | 0.40 | Primary signal in absence of relationship depth |
| Engagement | 0.15 | Measured via digital engagement (portal, email opens), not meetings |
| Support | 0.25 | Support experience disproportionately affects SMB retention |
| Sentiment | 0.10 | Unchanged |
| Commercial | 0.10 | Unchanged |

## How to Validate a Custom Weight Profile

1. Pull the last 12 months of churn and renewal data for the target segment
2. For each churned account: compute what the health score would have been at T-90 (90 days before churn) using the proposed weights
3. For each renewed account: compute the same
4. Measure the separation: do churned accounts score meaningfully lower than renewed accounts at T-90?
5. Compare to the default weights: does the custom profile produce better separation?
6. If yes, adopt. If marginal, keep the default -- simplicity has value.

## Weight Change Process

1. Propose new weights with rationale and validation data
2. VP/Director of CS approves (weights directly affect which accounts surface as at-risk)
3. CS Ops implements in the Health Score Engine configuration
4. Run both old and new weights in parallel for 30 days to confirm no unexpected effects
5. Cut over to new weights
6. Review again at next quarterly benchmark refresh

## Constraints

- No component may be weighted below 0.05 (5%). Every signal matters at some level; zero-weighting a component hides real risk.
- All weights must sum to 1.00.
- Weight changes apply at the segment level, not per-account. If a single account needs special treatment, that is a human judgment call, not a system configuration.

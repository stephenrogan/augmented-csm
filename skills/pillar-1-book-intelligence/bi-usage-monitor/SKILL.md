---
name: bi-usage-monitor
description: Tracks product usage patterns at the account level, detects meaningful behaviour changes, and classifies trends against segment benchmarks. Use when asked to monitor usage, detect usage declines, track adoption trends, identify usage anomalies, flag accounts with dropping engagement, analyse product stickiness, compare account usage to peers, or when any workflow needs current usage trend data for an account. Also triggers for questions about DAU/MAU ratios, feature adoption rates, session depth, or usage benchmarking.
license: MIT
metadata:
  version: "1.0.0"
  pillar: book-intelligence
  category: foundation-layer
---

# Usage Pattern Monitor

Tracks product usage at the account level, detects meaningful changes in behaviour, and classifies trend direction against segment benchmarks. Part of the Book Intelligence foundation layer -- feeds data into the Health Score Engine, Risk Signal Detector, and Expansion Signal Detector.

This is a **detection and surfacing** skill. It observes, computes, and alerts. It never contacts customers or initiates any external action.

## When to Run

- **Scheduled**: Daily for all accounts. Generates alerts only when a meaningful pattern change is detected -- not on every run
- **On-demand**: When a human or downstream skill requests current usage profile for a specific account
- **Triggered**: When product analytics reports a significant event (e.g., usage spike or feature-gating hit)

## Core Execution Logic

### Step 1: Pull Current Period Usage Data

For each account, pull the following from the product analytics platform:

| Metric | Definition | Granularity |
|--------|-----------|-------------|
| Active Users | Unique users with at least one session | Daily, Weekly, Monthly |
| Feature Adoption Breadth | Count of distinct features used / total available features | Weekly |
| Session Depth | Average actions per session | Daily |
| Key Workflow Completions | Core use-case workflows completed successfully | Daily |
| API Call Volume | Total API calls (if applicable) | Daily |
| Licence Utilisation | Active users / purchased seats | Weekly |

### Step 2: Compare to Account Baseline

For each metric, compute the account's own 90-day rolling average as the baseline. This captures the account's normal behaviour, independent of segment benchmarks.

Calculate the delta: `current_period_value - 90_day_rolling_average`

Express as a percentage change: `(delta / 90_day_rolling_average) * 100`

### Step 3: Compare to Segment Benchmark

Pull segment benchmarks from the shared benchmark dataset (see `references/usage-benchmarks.md`). Segment is defined by tier, company size band, and contract age cohort.

For each metric, classify the account's position relative to the segment:
- **Above 75th percentile**: Strong adopter
- **Between median and 75th**: Healthy adopter
- **Between 25th and median**: Below-average adopter
- **Below 25th percentile**: Underperforming

### Step 4: Classify Trend Direction

For each metric, classify the trend based on the account's own baseline:

| Classification | Criteria |
|---------------|----------|
| Growing | >10% above 90-day rolling average for current period |
| Stable | Within +/-10% of 90-day rolling average |
| Declining | >10% below 90-day rolling average for current period |

### Step 5: Detect Pattern Types

Scan for these specific patterns, which carry different urgency and interpretation:

**Gradual Decline**
- Definition: 3+ consecutive declining measurement periods (daily or weekly depending on metric)
- Significance: Sustained disengagement. Not a blip -- something structural has changed
- Alert urgency: High

**Sudden Drop**
- Definition: >25% single-period decline from prior period
- Significance: An event happened -- product issue, stakeholder change, competitive displacement, or data error
- Alert urgency: Critical (verify data integrity first)

**Adoption Plateau**
- Definition: Usage stable but below segment median for 60+ consecutive days
- Significance: The account has settled into underutilisation. They are using the product but not realising full value
- Alert urgency: Medium (feeds into Product Adoption pillar)

**Breakout Growth**
- Definition: >30% above 90-day baseline sustained for 2+ measurement periods
- Significance: Expansion signal. New use case, new team onboarding, or champion-driven adoption push
- Alert urgency: Low (opportunity, not risk). Route to Expansion Signal Detector

**Seasonal Pattern**
- Definition: Usage pattern correlates with a known seasonal cycle (e.g., Q4 dip in certain industries)
- Significance: Not a risk signal -- suppress alert if pattern matches historical seasonal data
- Handling: Compare to same period prior year if data is available. See `references/seasonal-patterns.md`

### Step 6: Correlate with Known Events

For declining patterns, check for correlating events:
- Support tickets opened in the same window (product issues)
- Stakeholder changes in CRM (champion departure)
- Product releases or changes (new version causing friction)
- Known outages or incidents

Present correlations as hypotheses, not conclusions. The human interprets causation.

### Step 7: Generate Output

Produce a per-account usage profile and, if a pattern is detected, an alert.

## Output Format

**Per-account usage profile:**
```json
{
  "account_id": "string",
  "period": "2026-03-10",
  "metrics": {
    "dau_mau_ratio": { "value": 0.42, "baseline_90d": 0.38, "delta_pct": 10.5, "segment_position": "above_median", "trend": "growing" },
    "feature_adoption_breadth": { "value": 0.65, "baseline_90d": 0.61, "delta_pct": 6.6, "segment_position": "above_75th", "trend": "stable" },
    "session_depth": { "value": 12.3, "baseline_90d": 14.1, "delta_pct": -12.8, "segment_position": "below_median", "trend": "declining" },
    "key_workflow_completions": { "value": 847, "baseline_90d": 820, "delta_pct": 3.3, "segment_position": "above_median", "trend": "stable" },
    "licence_utilisation": { "value": 0.78, "baseline_90d": 0.72, "delta_pct": 8.3, "segment_position": "above_median", "trend": "growing" }
  },
  "patterns_detected": [],
  "overall_usage_trend": "stable"
}
```

**Pattern alert (generated only when a pattern is detected):**
```json
{
  "account_id": "string",
  "alert_type": "gradual_decline",
  "severity": "high",
  "evidence": {
    "metric": "session_depth",
    "current_value": 12.3,
    "baseline_90d": 14.1,
    "consecutive_declining_periods": 4,
    "segment_position": "below_median"
  },
  "correlations": [
    { "type": "support_ticket", "detail": "P2 ticket opened 12 days ago re: performance issues" }
  ],
  "suggested_investigation": "Session depth declining for 4 consecutive weeks. Possible product performance issue -- correlates with open P2 ticket. Verify with customer whether performance is impacting usage."
}
```

**Portfolio usage report (weekly):**
- Accounts by overall usage trend: growing / stable / declining / insufficient data
- Top 5 largest usage declines with pattern classification
- Top 5 largest usage increases (expansion signals)
- Accounts with adoption plateaus (below median, stable for 60+ days)

## Handoff to Human

| Condition | Action | Urgency |
|-----------|--------|---------|
| Sudden drop (>25% single period) | Alert CSM with data integrity note -- verify before acting | Immediate |
| Gradual decline (3+ periods) | Surface to CSM with correlation hypotheses | Same day |
| Adoption plateau (60+ days below median) | Flag for adoption review -- route to Product Adoption pillar | Weekly digest |
| Breakout growth (>30% sustained) | Surface to CSM as expansion signal -- route to Expansion Detector | Weekly digest |

See `references/human-decision-guide.md` for interpretation framework.

## Confidence and Limitations

- **High confidence** for pattern detection given clean data with 90+ days of history
- **Medium confidence** for causal correlation (why usage changed). Agent presents correlations as hypotheses, never conclusions
- **Low confidence** for accounts with <30 days of history -- insufficient baseline. Flag as "new account, limited usage history"
- Cannot distinguish intentional usage reduction (customer rightsizing) from disengagement
- Seasonal patterns require at least 1 year of historical data to detect reliably

## Dependencies

**Required:**
- Product analytics API (Mixpanel, Amplitude, Pendo, or data warehouse)
- Segment benchmark dataset (shared with Health Score Engine)
- Account metadata from CRM (tier, size band, contract age)

**Downstream consumers:**
- `bi-health-score` (usage component input)
- `bi-risk-detector` (pattern alerts as risk signals)
- `bi-expansion-detector` (breakout growth as expansion signal)
- `bi-account-brief` (usage profile for account context)

## References

- `references/usage-benchmarks.md` -- Metric definitions and benchmark thresholds by segment
- `references/seasonal-patterns.md` -- Known seasonal patterns and suppression logic
- `references/human-decision-guide.md` -- How CSMs should interpret usage alerts

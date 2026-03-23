---
name: bi-segment-trends
description: Analyses portfolio-level trends across customer segments to identify systemic patterns affecting multiple accounts. Use when asked to analyse portfolio health by segment, identify cohort-level churn patterns, compare retention across tiers or industries, build portfolio health reports, detect systemic issues across the book, assess segment-level risk, or when leadership needs a strategic view of CS performance beyond individual accounts. Also triggers for questions about cohort analysis, segment benchmarking, portfolio-level NRR drivers, or CS capacity planning inputs.
license: MIT
metadata:
  version: "1.0.0"
  pillar: book-intelligence
  category: intelligence-layer
---

# Segment Trend Analyser

Analyses portfolio-level trends across defined segments to identify systemic patterns. Part of the Book Intelligence intelligence layer -- synthesises data from all foundation and detection skills into strategic insights for CS leadership.

This is an **analytical and reporting** skill. It identifies patterns, generates hypotheses, and produces reports. It does not make strategic decisions or implement changes. Those are human (typically VP/Director level) decisions.

## When to Run

- **Scheduled**: Weekly or bi-weekly, depending on portfolio size
- **On-demand**: When leadership requests portfolio analysis, during QBR preparation, or when a systemic issue is suspected
- **Triggered**: When Risk Signal Detector flags a spike in risk signals concentrated in a specific segment

## Core Execution Logic

### Step 1: Define Segments

Group all accounts by each segmentation dimension. Standard dimensions:

| Dimension | Values |
|-----------|--------|
| Tier | Enterprise, Mid-Market, SMB |
| Industry | As defined in CRM (typically 8-15 categories) |
| Company Size Band | Small (1-50), Medium (51-200), Large (201-1000), Enterprise (1000+) |
| Contract Age Cohort | New (0-6mo), Established (7-18mo), Mature (19-36mo), Tenured (36+mo) |
| Region | As defined in CRM |
| Onboarding Cohort | By quarter of contract start (Q1-2025, Q2-2025, etc.) |

Each account can be analysed across multiple dimensions simultaneously.

### Step 2: Compute Segment-Level Metrics

For each segment, compute:

| Metric | Source | Computation |
|--------|--------|-------------|
| Median health score | Health Score Engine | Median of all composite scores in segment |
| Health score distribution | Health Score Engine | % of accounts in each health band (Critical/At Risk/Healthy/Strong) |
| Usage trend distribution | Usage Pattern Monitor | % of accounts classified as growing/stable/declining |
| Risk signal density | Risk Signal Detector | Total active risk signals / number of accounts in segment |
| Expansion signal density | Expansion Signal Detector | Total active expansion signals / number of accounts in segment |
| Churn rate (trailing 12mo) | CRM churn data | Accounts churned / total accounts at period start |
| NRR (trailing 12mo) | CRM revenue data | (Starting ARR - churn + expansion) / Starting ARR |

### Step 3: Compute Period-over-Period Changes

For each metric in each segment:
1. Compare current period to prior period (week-over-week for weekly runs, month-over-month for monthly)
2. Compute absolute change and percentage change
3. Flag segments where any metric changes by more than the portfolio-average change rate

### Step 4: Identify Outlier Segments

A segment is an outlier when its metrics diverge significantly from the portfolio average:

| Outlier Type | Detection Criteria |
|-------------|-------------------|
| Health declining faster than portfolio | Segment median health decline > 1.5x portfolio median decline |
| Risk concentration | Segment risk signal density > 2x portfolio average |
| Expansion underperformance | Segment expansion signal density < 0.5x portfolio average |
| Churn spike | Segment trailing-90-day churn rate > 1.5x segment's trailing-12-month average |
| Cohort divergence | An onboarding cohort shows health/usage metrics >15% below the prior cohort at the same contract age |

### Step 5: Generate Hypotheses

For each outlier segment, correlate with known events and generate a hypothesis:

**Example hypotheses:**
- "Mid-market accounts onboarded in Q3-2025 show 18% lower feature adoption than Q2-2025 cohort at the same contract age. Hypothesis: onboarding process change introduced in July 2025 may be less effective"
- "Enterprise accounts in Financial Services show risk signal density 2.4x portfolio average. Hypothesis: regulatory change in January 2026 shifted customer priorities away from our product's core use case"
- "SMB accounts in the 7-18 month cohort have 22% higher churn rate than the same cohort 12 months ago. Hypothesis: pricing increase in Q1-2025 is creating renewal friction for accounts reaching first renewal"

Hypotheses are directional, not causal. They are starting points for human investigation, not conclusions.

### Step 6: Generate Report

Produce a structured portfolio segment report with drill-down capability.

## Output Format

**Portfolio Segment Report:**

```json
{
  "report_date": "2026-03-10",
  "portfolio_summary": {
    "total_accounts": 342,
    "total_arr": 28500000,
    "median_health": 74,
    "health_trend": "stable",
    "risk_signal_density": 0.82,
    "expansion_signal_density": 0.34
  },
  "segments": [
    {
      "dimension": "tier",
      "value": "mid-market",
      "account_count": 156,
      "arr": 12400000,
      "median_health": 71,
      "health_trend": "declining",
      "health_distribution": { "critical": 5, "at_risk": 28, "healthy": 89, "strong": 34 },
      "usage_trend_distribution": { "growing": 22, "stable": 98, "declining": 36 },
      "risk_density": 1.14,
      "expansion_density": 0.29,
      "period_change": {
        "median_health": -3,
        "risk_density": "+0.21",
        "note": "Health declining faster than portfolio average"
      },
      "outlier": true,
      "hypothesis": "Mid-market health decline concentrated in accounts with <12 months tenure. Possible onboarding quality gap."
    }
  ],
  "outlier_alerts": [
    {
      "segment": "mid-market / 7-18mo tenure",
      "alert_type": "health_declining_faster_than_portfolio",
      "evidence": "Median health dropped 6 points in 4 weeks vs. portfolio drop of 2 points",
      "hypothesis": "Recent onboarding cohort underperforming. Investigate onboarding process changes."
    }
  ]
}
```

## Handoff to Human

This skill surfaces to VP/Director-level CS leadership, not individual CSMs.

| Output | Audience | Urgency |
|--------|----------|---------|
| Outlier segment alerts | VP/Director of CS | Within current reporting cycle |
| Cohort divergence alerts | VP/Director of CS + CS Ops | Same week (may indicate systemic process issue) |
| Churn spike alerts | VP/Director of CS + CRO/CFO | Same day if spike is material to NRR forecast |
| Regular segment report | CS leadership team | Weekly/bi-weekly digest |

The human validates hypotheses, investigates root causes, and decides on portfolio-level interventions (process changes, resource reallocation, segment-specific strategies).

## Confidence and Limitations

- **Medium confidence** for statistical trends at sufficient portfolio size (20+ accounts per segment)
- **Low confidence** for segments with <20 accounts -- flag as "small sample, interpret with caution"
- Hypotheses are directional, not causal. Multiple hypotheses may explain the same trend
- Cannot account for external market factors not captured in internal data
- Seasonal patterns at the segment level require 12+ months of data

## Dependencies

**Required:**
- `bi-health-score` (all account health records)
- `bi-usage-monitor` (all account usage profiles)
- `bi-risk-detector` (aggregate risk signals)
- `bi-expansion-detector` (aggregate expansion signals)
- CRM segmentation data (tier, industry, size, region, contract dates)
- CRM churn and revenue data (for trailing churn rate and NRR)

**Downstream consumers:**
- CS leadership reporting
- CS strategy and capacity planning
- Board/investor reporting (NRR trends by segment)

## References

- `references/statistical-methods.md` -- Methods for outlier detection and significance testing
- `references/report-templates.md` -- Formatted report templates for leadership consumption

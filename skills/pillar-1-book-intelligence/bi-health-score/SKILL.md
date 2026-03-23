---
name: bi-health-score
description: Computes and maintains composite health scores for customer accounts by aggregating product usage, support engagement, stakeholder activity, and sentiment signals. Use when asked to calculate health scores, assess account health, monitor portfolio health, identify at-risk accounts, build health scoring models, set up health monitoring, or when any downstream CS workflow needs current account health data. Also triggers for questions about customer health, account risk, portfolio risk, health trends, health dashboards, or NRR forecasting that depends on health inputs.
license: MIT
metadata:
  version: "1.0.0"
  pillar: book-intelligence
  category: foundation-layer
---

# Health Score Engine

The foundational skill for the Book Intelligence pillar of the CSM Agent Twin. Every other Book Intelligence skill depends on the health score this skill produces. If this skill is unreliable, every downstream skill degrades.

## What This Skill Does

Computes a composite health score (0-100) for every account in a CSM's book by pulling data from multiple sources, normalising against segment benchmarks, and producing a weighted index with component-level breakdown and trend analysis.

This is a **detection and surfacing** skill. It computes, classifies, and writes data. It never contacts customers, sends emails, or initiates any external action.

## When to Run

- **Scheduled**: Daily for high-touch/enterprise accounts, weekly for scaled/SMB
- **On-demand**: When any human or downstream skill requests current health for a specific account
- **Triggered**: When a data source reports a significant change (support escalation, usage spike/drop, NPS response)

## Core Execution Logic

### Step 1: Pull Latest Data from Source Systems

Gather current-period data from each input source. If a source is unavailable or stale (>7 days for usage, >30 days for sentiment), flag the staleness explicitly in the output rather than computing from incomplete data.

**Required data sources:**

| Source | Data Points | Refresh Cadence |
|--------|------------|-----------------|
| Product Analytics | DAU/WAU/MAU, feature adoption rates, session depth, API call volume, key workflow completions | Daily |
| Support Platform | Ticket volume, severity distribution, resolution time, CSAT per ticket, open P1/P2 count | Daily |
| CRM | Contact engagement (emails, meetings, calls), last touch per stakeholder, activity log | Daily |
| Survey Tool | NPS responses, CSAT scores, qualitative feedback flags | As received |
| Billing/Contract | ARR, contract end date, payment history, licence utilisation | Weekly |

### Step 2: Normalise Each Signal

Convert raw metrics to a 0-100 scale using **segment-specific benchmarks**. Segment is defined by the account's tier, company size band, and contract age cohort.

For each metric:
1. Pull the segment benchmark (median, 25th percentile, 75th percentile) from `references/segment-benchmarks.md`
2. Map the account's raw value to 0-100 where: 0 = segment bottom 5%, 50 = segment median, 100 = segment top 5%
3. Use linear interpolation between benchmark points
4. Cap at 0 and 100 -- do not extrapolate beyond bounds

### Step 3: Compute Weighted Composite

Apply the default weighting formula:

```
Composite = (Usage * 0.35) + (Engagement * 0.25) + (Support * 0.20) + (Sentiment * 0.10) + (Commercial * 0.10)
```

**Component definitions:**
- **Usage (35%)**: Blended score from DAU/WAU trend, feature adoption breadth, session depth, key workflow completion rate
- **Engagement (25%)**: Blended score from stakeholder touch frequency, meeting attendance rate, email response rate, portal login frequency
- **Support (20%)**: Inverse-weighted -- high ticket volume and severity lower the score. Factors: ticket volume vs. segment norm, P1/P2 ratio, average resolution time, CSAT trend
- **Sentiment (10%)**: Latest NPS score normalised to segment, CSAT trend, qualitative feedback flags (positive/negative)
- **Commercial (10%)**: Licence utilisation rate, payment history (on-time vs. late), days to renewal proximity factor

If a component has no data (e.g., no NPS response in 90 days), redistribute its weight proportionally across the remaining components and flag the gap.

See `references/weight-customisation.md` for guidance on adjusting weights by segment or business model.

### Step 4: Calculate Trend Vectors

For each component and the composite:
1. Compute 7-day, 30-day, and 90-day rolling averages
2. Compare current value to each rolling average
3. Classify trend: **Improving** (current > 30-day avg by >5 points), **Stable** (within 5 points), **Declining** (current < 30-day avg by >5 points)
4. Flag **rapid decline**: composite drops >10 points in 7 days

### Step 5: Flag Risk Drivers

For each account:
- Flag any single component scoring below the segment 25th percentile
- Identify the specific metric(s) dragging the component down
- Label each flag with the component name and the driver metric (e.g., "Support: P1 ticket volume 3x segment median")

### Step 6: Write to CRM

Write the following to the CRM health object per account:
- Composite score (0-100)
- Component scores (5 values, 0-100 each)
- Trend direction per component (improving/stable/declining)
- Risk driver flags (array of strings)
- Data freshness flags (array of stale sources, if any)
- Last computed timestamp

## Output Format

**Per-account health record:**
```json
{
  "account_id": "string",
  "composite_score": 72,
  "trend": "declining",
  "components": {
    "usage": { "score": 81, "trend": "stable" },
    "engagement": { "score": 65, "trend": "declining" },
    "support": { "score": 58, "trend": "declining" },
    "sentiment": { "score": 80, "trend": "stable" },
    "commercial": { "score": 75, "trend": "improving" }
  },
  "risk_drivers": [
    "Support: P1 ticket volume 3x segment median",
    "Engagement: No executive contact in 74 days"
  ],
  "data_freshness": {
    "stale_sources": [],
    "last_computed": "2026-03-10T08:00:00Z"
  }
}
```

**Weekly portfolio summary:**
- Distribution histogram: accounts by health band (0-40 Critical, 41-65 At Risk, 66-80 Healthy, 81-100 Strong)
- Week-over-week movers: accounts that changed band
- Top 5 largest score declines with driver breakdown

## Handoff to Human

This skill surfaces data to humans. It does not make decisions. Handoff triggers:

| Condition | Action | Urgency |
|-----------|--------|---------|
| Composite drops below 65 | Surface to CSM with full component breakdown | Same day |
| Any component below segment 25th percentile | Flag in daily digest with specific driver | Next business day |
| Composite declines >10 points in 7 days | Alert CSM immediately with trend evidence | Immediate |
| Data staleness on >1 source for >14 days | Alert CS Ops to investigate integration | Within 48 hours |

**What the human does with this:** Interprets the score in relationship context, decides whether to investigate or act, prioritises against other accounts. The score is an input to judgment, not a substitute for it.

## Confidence and Limitations

- **High confidence** when all data sources are fresh and the account has 90+ days of history
- **Medium confidence** for accounts <90 days old (limited baseline) -- flag as "early-stage, limited history"
- **Low confidence** when any source is stale >7 days -- flag explicitly, do not present score as reliable
- The score measures observable signals. It cannot detect risks that only exist in relationship context (e.g., a champion who is privately disengaged but still attending meetings)
- Component weights are defaults. They should be reviewed quarterly and adjusted per segment. See `references/weight-customisation.md`

## Dependencies

**Required integrations:**
- CRM with API access (Salesforce, HubSpot, or Gainsight) for contact/activity data and health object writes
- Product analytics platform for usage data
- Support platform for ticket data
- Survey/NPS tool for sentiment data

**Required reference data:**
- Segment benchmark dataset (see `references/segment-benchmarks.md`) -- must be maintained and updated quarterly
- Account segmentation classification in CRM (tier, company size band, contract age cohort)

**Downstream consumers:**
- `bi-usage-monitor` (reads usage component)
- `bi-risk-detector` (reads composite + components + trends)
- `bi-expansion-detector` (reads composite for health filter)
- `bi-account-brief` (reads full health record)
- `bi-segment-trends` (reads all account health records for portfolio analysis)

## Common Issues

**Score seems wrong for a specific account:**
Check data freshness first. If all sources are fresh, check segment classification -- an account miscategorised into the wrong size band will benchmark incorrectly.

**Scores cluster too tightly (all accounts 60-80):**
Benchmark data may be stale or segment definitions too broad. Tighten segmentation or refresh benchmarks.

**Component weight feels wrong for a segment:**
See `references/weight-customisation.md`. High-touch enterprise accounts may need higher Engagement weight; PLG accounts may need higher Usage weight.

## References

- `references/segment-benchmarks.md` -- Benchmark definitions and update procedures
- `references/weight-customisation.md` -- Guidance on adjusting component weights by segment
- `references/integration-patterns.md` -- API patterns for each supported data source

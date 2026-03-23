---
name: cc-report-generator
description: Produces weekly, monthly, and quarterly reports for CSMs, managers, and leadership by aggregating data from all pillar skills into formatted, distributable reports. Adapts content, detail, and emphasis by audience. Use when asked to generate a CS report, build a weekly summary, create a portfolio report, produce a dashboard update, compile metrics for leadership, or when any recurring reporting need should be automated. Also triggers for questions about CS reporting, metrics compilation, dashboard data generation, performance summaries, or NRR reporting.
license: MIT
metadata:
  version: "1.0.0"
  pillar: communication-content
  category: data-ops
---

# Report Generator

Produces recurring and ad-hoc reports by aggregating data from all pillar skills into formatted, audience-appropriate documents. Part of the Communication & Content Production pillar.

This is a **data aggregation and formatting** skill. It pulls from across the skill suite and structures for specific audiences. The data speaks; humans add narrative, strategic context, and forward-looking commentary.

## When to Run

- **Scheduled**: Weekly CSM reports (Monday morning), monthly manager reports (first business day), quarterly leadership reports (within 5 business days of quarter close)
- **On-demand**: When a specific report is requested for a non-recurring purpose
- **Triggered**: When a significant event occurs that warrants an out-of-cycle report (e.g., major churn event, portfolio-level health shift)

## Core Execution Logic

### Step 1: Determine Report Type and Audience

| Report | Audience | Cadence | Focus | Length |
|--------|----------|---------|-------|--------|
| CSM Weekly | Individual CSM | Weekly | Their portfolio: health, priorities, risk, expansion, overdue items | 1 page |
| Manager Monthly | Team lead | Monthly | Team performance: aggregate health, renewal pipeline, process metrics, per-CSM breakdown | 2-3 pages |
| Leadership Quarterly | VP CS, CRO, CFO | Quarterly | NRR, churn analysis, expansion, segment trends, strategic outlook | 3-5 pages |
| Board Summary | Board / investors | Quarterly | Financial retention metrics, strategic narrative (human-written), forward outlook | 1 page |
| Ad-hoc | Varies | As needed | Specific topic deep-dive: segment analysis, churn cohort, expansion pipeline | Varies |

### Step 2: Pull and Aggregate Data by Report Type

**CSM Weekly Report data sources:**

| Data Element | Source | Metric |
|-------------|--------|--------|
| Portfolio health | bi-health-score | Distribution by band, week-over-week changes, top movers |
| This week's priorities | lo-check-in-scheduler + lo-sla-monitor | Upcoming touchpoints, overdue commitments, due items |
| Risk queue | bi-risk-detector | Prioritised risk accounts with top risk driver |
| Expansion signals | bi-expansion-detector | Active signals with estimated value |
| Renewal pipeline | lo-renewal-manager | Renewals in next 90 days by classification |
| Engagement compliance | ra-engagement-tracker | Touchpoints completed vs. expected, gap accounts |
| Action items | lo-sla-monitor | Commitments due this week, overdue items |

**Manager Monthly Report data sources:**

| Data Element | Source | Metric |
|-------------|--------|--------|
| Team portfolio health | bi-health-score (aggregated) | Health distribution across the team, per-CSM breakdown |
| Renewal forecast | cm-renewal-forecaster | NRR projection, confidence interval, period-over-period trend |
| Churn and expansion | CRM + bi-expansion-detector | ARR lost, ARR expanded, net change, trailing 30 days |
| Process metrics | lo-check-in-scheduler + lo-sla-monitor | Touchpoint cadence compliance, QBR completion rate, SLA adherence |
| Escalation summary | ic-escalation-router | Active escalations, resolution time, stall rate |
| Capacity | CRM + bi-health-score | Accounts per CSM, health distribution per CSM, workload indicators |
| Engagement health | ra-engagement-tracker | Team-level engagement metrics, gap accounts per CSM |

**Leadership Quarterly Report data sources:**

| Data Element | Source | Metric |
|-------------|--------|--------|
| NRR | cm-renewal-forecaster + CRM | Trailing 12 months, current quarter, by segment |
| Churn analysis | CRM + churn post-mortems | Churn rate, root cause distribution, preventable vs. non-preventable |
| Expansion | CRM + bi-expansion-detector | Expansion revenue, pipeline, conversion rate |
| Health trajectory | bi-health-score | Portfolio-wide health trend, segment-level trends |
| Segment analysis | bi-segment-trends | Outlier segments, emerging patterns |
| Process maturity | All operational skills | Automation rate, process execution rate, human override patterns |
| Strategic recommendations | CSM leadership input (human-written) | Forward-looking priorities and resource needs |

### Step 3: Compute Period-Over-Period Changes

Every report includes trend context, not just current state:

| Report Level | Comparison Period | Key Trend Metrics |
|-------------|------------------|------------------|
| CSM Weekly | This week vs. last week | Health movers, new risks, new expansion signals, compliance change |
| Manager Monthly | This month vs. last month | NRR trend, churn trend, process compliance trend, team capacity |
| Leadership Quarterly | This quarter vs. last quarter, and vs. same quarter last year | NRR trajectory, churn rate direction, expansion growth rate |

Flag significant changes: any metric that moved >10% period-over-period gets highlighted with a direction indicator and the primary driver.

### Step 4: Format for Audience

**Formatting principles:**

| Audience | Wants | Does Not Want |
|----------|-------|--------------|
| Individual CSM | Specific accounts, actionable priorities, what is due this week | Portfolio-level financials, strategic commentary |
| Team manager | Per-CSM performance, team trends, resource needs, coaching opportunities | Individual account details (unless discussing a specific escalation) |
| VP CS / CRO | Revenue metrics, pipeline health, strategic risks, resource decisions | Operational details, individual CSM performance |
| CFO | NRR, cost of retention, CS as a P&L line item | Process metrics, engagement data, account-level detail |
| Board | One-page summary: NRR, retention rate, strategic outlook | Anything that requires CS domain knowledge to interpret |

### Step 5: Generate Report

```json
{
  "report_id": "rpt-2026-weekly-jane-doe-w11",
  "report_type": "csm_weekly",
  "audience": "Jane Doe (CSM)",
  "period": "Week of 2026-03-10",
  "generated": "2026-03-10T07:00:00Z",
  "portfolio_summary": {
    "total_accounts": 42,
    "health_distribution": { "strong": 12, "healthy": 22, "at_risk": 6, "critical": 2 },
    "vs_last_week": { "strong": "+1", "healthy": "0", "at_risk": "-1", "critical": "0" },
    "avg_health_score": 72,
    "avg_health_trend": "stable"
  },
  "this_week_priorities": {
    "touchpoints_due": 8,
    "overdue_items": 2,
    "commitments_due": 5,
    "qbrs_this_week": 1,
    "renewals_next_30_days": 2
  },
  "risk_queue": [
    {
      "account": "Acme Corp",
      "arr": 85000,
      "health": 58,
      "top_risk": "Champion departed, usage declining",
      "renewal_days": 67,
      "recommended_action": "Engage replacement stakeholder this week"
    }
  ],
  "expansion_signals": [
    {
      "account": "Delta Corp",
      "signal": "Licence utilisation 93% for 30 days",
      "estimated_value": 15000,
      "status": "CSM to assess timing"
    }
  ],
  "engagement_compliance": {
    "touchpoints_expected_last_week": 10,
    "touchpoints_completed": 9,
    "compliance_rate": 0.90,
    "gap_accounts": ["Beta Inc -- 28 days since last touch"]
  },
  "period_highlights": [
    "Acme Corp moved from Watch to At Risk (champion departure)",
    "Gamma Corp completed onboarding ahead of schedule",
    "Delta Corp expansion signal surfaced (licence utilisation ceiling)"
  ]
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| CSM Weekly review | Portfolio data, priorities, risk queue | How to allocate time this week. The report ranks; the CSM decides |
| Manager Monthly narrative | Team data, trends, per-CSM breakdown | The story behind the numbers. "NRR down 0.3%" needs human context: is this a trend or a blip? What should leadership know? |
| Leadership Quarterly strategy | Full portfolio data, segment trends, churn analysis | Strategic recommendations, resource requests, forward-looking priorities. The data is the evidence; leadership provides the strategy |
| Board Summary framing | Financial metrics, trend data | How to position the quarter. What to highlight, what to contextualise, what narrative to provide |

## Confidence and Limitations

- **High confidence** for data aggregation and formatting -- pulling and computing from defined sources is deterministic
- **High confidence** for period-over-period comparisons -- mathematical computation with defined comparison windows
- **Medium confidence** for report emphasis -- the skill highlights statistically significant changes, but the human may want different emphasis based on strategic priorities or audience expectations
- **Low confidence** for narrative context. The numbers do not explain themselves. "NRR declined 0.3%" is a fact; "NRR declined because of two unexpected churns in the enterprise segment, both triggered by competitive displacement" is insight. The human provides insight
- Report quality depends entirely on upstream data quality. If cc-crm-updater is not running, if bi-health-score has stale data, or if activity logging is incomplete, the report reflects those gaps. Garbage in, garbage out
- Cannot generate strategic recommendations or forward-looking commentary -- that is the most valuable section of any leadership report, and it requires human judgment
- Cannot assess whether a metric matters to a specific audience at a specific time. Standard report templates include the default metrics, but the CSM or manager may need to adjust emphasis based on what leadership is focused on this quarter

## Dependencies

**Required:**
- All Book Intelligence skills (primary data sources for health, risk, usage, expansion)
- CRM API (account data, contract data, activity data)

**Strongly recommended:**
- All Lifecycle Orchestration skills (operational metrics for process compliance reporting)
- cm-renewal-forecaster (renewal and NRR projection for pipeline reports)
- ic-escalation-router (escalation metrics for operational reporting)
- ra-engagement-tracker (engagement metrics for CSM and team reports)
- bi-segment-trends (segment analysis for leadership reporting)

**Downstream consumers:**
- Individual CSMs (weekly portfolio management)
- CS managers (monthly team performance and coaching)
- CS leadership (quarterly strategic planning and resource allocation)
- CRO / CFO (quarterly revenue planning and retention strategy)
- Board reporting (quarterly NRR and strategic metrics)

## References

- `references/report-templates.md` -- Detailed templates for each report type with section definitions and formatting guidelines

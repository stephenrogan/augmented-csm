---
name: pa-value-reporter
description: Measures and reports on value delivered to customers including time-to-value tracking, ROI evidence assembly, outcome metrics, and value narratives for QBRs and renewal conversations. Use when asked to measure customer ROI, track time-to-value, build a value report, create an ROI case, quantify outcomes for a customer, or when any workflow needs evidence of value delivered. Also triggers for questions about customer outcomes, value realisation, ROI measurement, business impact quantification, or proving the investment is worth it.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: product-adoption
  category: value-measurement
---

# Value Reporter

Measures and reports on value delivered to customers. Tracks time-to-value, assembles ROI evidence, and produces value narratives for customer-facing and internal use. Part of the Product Adoption & Value Realisation pillar.

This is a **measurement and evidence assembly** skill. It quantifies what the product has delivered. It does not define what value means to the customer (that is a consultative conversation) or fabricate outcomes the data does not support.

## When to Run

- **Triggered**: By cc-qbr-deck-builder (for QBR value slides), by lo-renewal-manager (for renewal value narrative)
- **On-demand**: When a CSM needs value evidence for a customer conversation
- **Scheduled**: Monthly value snapshot update for all accounts

## Core Execution Logic

### Step 1: Determine Value Framework

Value metrics fall into two tiers:

**Universal metrics** (applicable to all accounts, computed automatically):
- Active users and growth trajectory
- Workflow completions (core use-case executions)
- Time saved (estimated from automation metrics)
- Feature adoption breadth (from pa-adoption-tracker)

**Custom metrics** (account-specific, defined during onboarding or QBR):
- Specific KPIs the customer identified as success criteria
- Business outcomes tied to their stated goals
- Metrics from their success plan (from lo-milestone-tracker)

If no custom metrics are defined, use universal metrics with segment benchmarks for context. Custom metrics always take priority because they represent what the customer actually cares about.

### Step 2: Compute Value Evidence

For each metric type, apply the appropriate computation:

| Metric | Computation | Data Source | Confidence |
|--------|------------|-------------|-----------|
| Time saved | Automated workflow completions * estimated manual time per workflow | Product analytics + manual time estimate from feature catalogue | Medium -- estimate depends on assumed manual time |
| Productivity gain | Workflow completions per user: current vs. baseline period | Product analytics | High -- direct measurement |
| Adoption ROI | Features adopted * utilisation rate, compared to pricing | pa-adoption-tracker + contract data | Medium -- value-per-feature is estimated |
| Custom KPI | Current value vs. baseline established at onboarding | Product analytics + CRM (baseline) | High if baseline is well-defined; Low if baseline was not captured |
| Cost avoidance | What the customer would have spent on headcount/tools to achieve the same output manually | Industry benchmarks + customer input | Low -- highly estimated. Use only if customer has validated the methodology |

### Step 3: Generate Time-to-Value Report

For accounts in early lifecycle or approaching renewal:

| Milestone | Definition | How Measured | Benchmark |
|-----------|-----------|-------------|-----------|
| Activation | First meaningful product use (not just login) | First key workflow completion | Segment median from pa-benchmark-engine |
| Habit formation | Sustained regular usage by the team | 4 consecutive weeks of >50% user activity | Segment median |
| Value realisation | First measurable business outcome | Custom KPI meets or exceeds baseline target, or universal metric reaches significant threshold | Segment median |

Track actual days vs. benchmark at each milestone. Accounts that reach value faster than segment peers are strong retention and expansion candidates.

### Step 4: Build Value Narrative

Assemble the evidence into a structured narrative:

**Headline metric**: The single most compelling number. Choose based on:
1. The metric the customer cares about most (from success plan or stated goals)
2. The metric with the strongest improvement
3. The metric that is easiest to understand without context

**Supporting evidence**: 2-3 additional metrics that reinforce the headline.

**Benchmark context**: How this compares to segment peers (from pa-benchmark-engine). Frame as validation: "Your outcomes are in the top quartile for companies your size."

**Trend**: Value trajectory over time. Is the customer getting more value each quarter, or has value plateaued?

**Forward look**: What additional value is available if adoption deepens. This bridges the value report into the adoption and expansion conversation.

### Step 5: Format for Context

Adapt the output based on consumption context:

| Context | Emphasis | Length |
|---------|----------|--------|
| QBR slide | Headline metric + supporting chart + peer comparison | 1-2 slides |
| Renewal conversation | Cumulative value over contract period, ROI calculation, forward projection | 1 page |
| Executive summary | Headline metric + one sentence on trend | 3-4 sentences |
| Internal business case | Full evidence package with methodology notes | 1 page |
| Expansion conversation | Value delivered + untapped value available with expanded product/seats | 1 page |

## Output Format

```json
{
  "account_id": "string",
  "report_period": "Q1-2026",
  "value_framework": "custom",
  "headline": {
    "metric": "Estimated hours saved through automated workflows",
    "value": 340,
    "period": "Q1-2026",
    "trend": "increasing",
    "vs_prior_period": "+22%"
  },
  "supporting_metrics": [
    {
      "metric": "Automated workflow completions",
      "value": 2847,
      "vs_prior_period": "+22%",
      "vs_segment_median": "+38%"
    },
    {
      "metric": "Active feature count",
      "value": 18,
      "vs_available": 24,
      "adoption_rate": 0.75
    },
    {
      "metric": "Active user ratio",
      "value": 0.78,
      "trend": "growing"
    }
  ],
  "time_to_value": {
    "activation_days": 8,
    "habit_formation_days": 28,
    "value_realisation_days": 52,
    "segment_benchmark": { "activation": 12, "habit_formation": 35, "value_realisation": 60 },
    "position": "faster_than_72_percent_of_peers"
  },
  "custom_kpis": [
    {
      "kpi": "Manual reporting time per week",
      "baseline": "12 hours",
      "current": "4 hours",
      "improvement": "67% reduction",
      "source": "Customer-confirmed in Q4 QBR"
    }
  ],
  "narrative": {
    "headline_sentence": "Your team saved an estimated 340 hours this quarter through automated workflows -- up 22% from last quarter.",
    "benchmark_sentence": "You are realising value faster than 72% of similar companies.",
    "forward_look": "With Advanced Reporting adoption (currently untouched), your analytics team could save an additional 4-6 hours per week."
  },
  "customer_safe": true,
  "methodology_notes": "Time saved estimate uses 7.2 minutes per workflow as the manual baseline, derived from industry average for this workflow type. Customer has not independently validated this estimate."
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Value framework selection | Universal metrics computed; custom KPI status | Whether to use universal metrics, custom KPIs, or both. Whether to invest in defining custom KPIs if none exist |
| Credibility check | Full evidence with methodology notes | Whether the numbers are credible enough to present. If the customer will challenge the methodology, the CSM adjusts or adds caveats |
| Narrative framing | Headline, supporting evidence, benchmark context | How to frame for this specific customer and conversation. The data is objective; the story is human |
| Sharing decision | Customer-safe flag, methodology notes | What to share, what to keep internal, and how to present uncertainty in estimates |
| Forward look positioning | Available untapped value from adoption gaps | Whether to frame the forward look as consultative (helping them get more value) or commercial (justifying expansion) |

## Confidence and Limitations

- **High confidence** for usage-based metrics (workflow completions, feature adoption counts, active users) -- direct measurement from product analytics
- **Medium confidence** for estimated value metrics (hours saved, productivity gain). These use assumptions about manual time equivalents that may not match the customer's reality. Always label as "estimated" and include the methodology
- **Low confidence** for business outcome attribution (revenue influenced, cost avoided). Correlation between product usage and business outcomes requires customer confirmation, not just data inference. Never present inferred outcomes as measured fact
- **Low confidence** for cost avoidance calculations. These are the most commonly challenged value metrics. Use only when the customer has validated the methodology or when presenting as a range rather than a precise number
- Time-to-value benchmarks require sufficient historical data across cohorts. New products or new segments may lack reliable benchmarks
- Custom KPIs are the most meaningful value metrics but require upfront investment to define baselines. If the baseline was not captured during onboarding, retroactive value measurement is unreliable
- Never inflate. A credible conservative number is more powerful than an impressive number the customer will challenge. If they push back on your value claim, you lose credibility on everything else in the conversation

## Dependencies

**Required:**
- Product analytics API (usage data, workflow completions)
- CRM API (contract data for ROI calculation, custom KPIs from success plans)

**Strongly recommended:**
- pa-adoption-tracker (feature adoption data for breadth metrics)
- pa-benchmark-engine (peer comparison for value context)
- lo-milestone-tracker (success plan milestones and baselines)

**Downstream consumers:**
- cc-qbr-deck-builder (value slides for QBR presentations)
- lo-renewal-manager (value narrative for renewal preparation)
- cm-commercial-case-builder (value evidence for expansion proposals)
- bi-health-score (value metrics inform commercial component)

## References

- `references/value-methodology.md` -- Estimation methods, confidence ratings, and customer validation process

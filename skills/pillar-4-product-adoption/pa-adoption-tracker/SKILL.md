---
name: pa-adoption-tracker
description: Tracks feature-level adoption within accounts, identifies underutilised capabilities, and generates adoption gap analysis. Maps used vs. available features to surface where customers are leaving value on the table. Use when asked to track feature adoption, analyse product usage depth, identify underutilised features, build adoption plans, measure feature penetration, or when any workflow needs to understand what a customer is and is not using. Also triggers for questions about feature adoption rates, usage gaps, product stickiness, or adoption health.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: product-adoption
  category: adoption-engine
---

# Adoption Tracker

Tracks feature-level product adoption within accounts. Maps used vs. available features, identifies underutilisation, and generates gap analysis to feed adoption planning. Part of the Product Adoption & Value Realisation pillar.

This is a **measurement and analysis** skill. It tells you what the customer is using and what they are not. It does not diagnose why adoption has stalled (that is often organisational, not technical -- a human judgment) or build the adoption strategy (that is consultative work).

## When to Run

- **Scheduled**: Weekly feature adoption scan across all accounts
- **On-demand**: When a CSM requests adoption analysis for a specific account
- **Triggered**: By lo-qbr-orchestrator (to populate QBR adoption slides), by bi-usage-monitor (when usage plateau is detected)

## Core Execution Logic

### Step 1: Map Feature Universe

For each account, determine the total available feature set:
1. Pull product tier from CRM contract data
2. Map tier to feature catalogue (see `references/feature-catalogue.md`)
3. Apply any account-specific entitlements (add-ons, beta features, custom modules)
4. Result: the complete list of features this customer has access to, categorised by feature group

### Step 2: Track Feature Usage

For each available feature, query product analytics for:

| Metric | Definition | Measurement Period |
|--------|-----------|-------------------|
| Ever used | Has any user at this account ever used this feature | All time |
| Active users | Number of distinct users who used the feature | Last 30 days |
| Usage frequency | How often the feature is used per active user | Last 30 days |
| Last used date | Most recent usage of the feature by any user | Timestamp |
| Trend | Usage direction compared to 90-day baseline | Current vs. 90-day avg |

### Step 3: Classify Adoption Status

For each feature, classify based on usage depth:

| Status | Criteria | What It Means |
|--------|----------|--------------|
| Core adopted | Used by >50% of active users, weekly or more frequently | Feature is embedded in the team's workflow. Switching cost is high |
| Partially adopted | Used by 10-50% of users, or used monthly or less | Feature is known but not habitual. Adoption can deepen or fade |
| Explored | Used by <10% of users, or used fewer than 3 times total | Someone tried it. It did not stick. Investigate why |
| Abandoned | Previously used (>5 uses historical) but no usage in 60+ days | Feature was adopted then dropped. This is a stronger signal than "never used" -- something changed |
| Untouched | Never used by any user | Customer may not know it exists, may not need it, or may face a barrier to adopting it |

### Step 4: Generate Gap Analysis

For each untouched, explored, or abandoned feature:

1. **Relevance check**: Is this feature relevant to the customer's stated use case? Cross-reference with:
   - Customer goals from CRM or success plan
   - Segment-typical feature usage (from pa-benchmark-engine -- what do similar customers use?)
   - Feature group (if they use other features in the same group, the gap feature is likely relevant)

2. **Benchmark comparison**: What percentage of segment peers use this feature?
   - >70% of peers use it: High relevance gap -- customer is missing something most peers find valuable
   - 40-70% of peers use it: Moderate relevance -- worth exploring but not urgent
   - <40% of peers use it: Low relevance -- feature may be niche or segment-inappropriate

3. **Value assessment**: What does this feature enable?
   - Pull from feature catalogue: expected value, typical use cases, time savings estimate
   - Flag features that directly address the customer's stated goals but remain unused

### Step 5: Prioritise Adoption Recommendations

Rank gaps by:
1. Direct alignment with customer goals (highest priority -- they said they want this outcome and a feature exists to deliver it)
2. High peer adoption rate with low customer adoption (the market has validated this feature)
3. Abandoned features (something caused the customer to stop using it -- investigate before recommending re-adoption)
4. Adjacent features (features in the same group as features they already use heavily)

For each recommended gap to address, include:
- Feature name and description
- Why it matters for this customer
- Peer adoption rate
- Suggested enablement approach (self-serve resource, demo, training session)
- Expected impact if adopted

## Output Format

**Per-account adoption profile:**
```json
{
  "account_id": "string",
  "product_tier": "professional",
  "scan_date": "2026-03-10",
  "features_available": 24,
  "adoption_summary": {
    "core_adopted": 12,
    "partially_adopted": 5,
    "explored": 3,
    "abandoned": 1,
    "untouched": 3
  },
  "adoption_score": 0.71,
  "adoption_trend": "stable",
  "top_gaps": [
    {
      "feature": "Advanced Reporting",
      "feature_group": "Analytics",
      "status": "untouched",
      "segment_adoption_rate": 0.78,
      "relevance": "high",
      "goal_alignment": "Customer goal: reduce manual reporting time. This feature automates executive report generation",
      "value_estimate": "4-6 hours per week saved for the analytics team",
      "recommended_approach": "Live demo in next check-in -- feature is complex enough to warrant guided introduction",
      "priority": 1
    },
    {
      "feature": "Workflow Automation Rules",
      "feature_group": "Automation",
      "status": "abandoned",
      "last_used": "2025-11-15",
      "segment_adoption_rate": 0.65,
      "relevance": "high",
      "goal_alignment": "Customer previously used this. Abandonment coincides with their admin leaving in November",
      "value_estimate": "Eliminates 3 manual steps per workflow execution",
      "recommended_approach": "Investigate abandonment cause with current admin. May need re-training after personnel change",
      "priority": 2
    }
  ],
  "portfolio_position": {
    "vs_segment_median": "above",
    "percentile": 68,
    "trend": "stable"
  }
}
```

**Portfolio adoption report (weekly):**
```json
{
  "report_date": "2026-03-10",
  "portfolio_summary": {
    "total_accounts": 42,
    "avg_adoption_score": 0.64,
    "accounts_above_median": 24,
    "accounts_below_25th": 6,
    "features_most_underutilised": [
      { "feature": "Advanced Reporting", "untouched_accounts": 18, "segment_adoption_rate": 0.78 }
    ]
  },
  "movers": {
    "adoption_improved": [{ "account": "Acme Corp", "score_change": "+0.08", "features_newly_adopted": 2 }],
    "adoption_declined": [{ "account": "Beta Inc", "score_change": "-0.05", "features_abandoned": 1 }]
  }
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Gap prioritisation | Ranked gaps with relevance, peer data, and value estimate | Which gaps to address first based on customer relationship context and conversation timing |
| Abandonment investigation | Feature name, abandonment date, correlated events | Whether to investigate with the customer, and how to frame it |
| Adoption plan creation | Gap analysis, enablement resources, peer benchmarks | The actual adoption plan -- milestones, timeline, how to position it with the customer |
| Enablement approach | Self-serve vs. guided recommendation per gap | Whether the customer needs a demo, a training session, or just a link |
| Product feedback | Adoption gaps that persist despite enablement | Whether to escalate to product as a UX or capability issue |

## Confidence and Limitations

- **High confidence** for feature usage tracking -- binary data (used/not used) from product analytics is objective
- **High confidence** for adoption status classification -- the thresholds are definitive given clean data
- **Medium confidence** for relevance assessment -- peer adoption rates are a good proxy but the customer's specific context may make a feature irrelevant despite high peer usage
- **Medium confidence** for abandoned feature detection -- the 60-day threshold is a sensible default but some features are legitimately seasonal or project-based
- **Low confidence** for root cause of non-adoption. The skill can tell you what is not being used. It cannot tell you why. Possible causes: the customer does not know the feature exists (awareness), they tried it and it did not work for them (product friction), their org is not ready for it (change management), or the feature is genuinely not relevant (false gap). The CSM diagnoses the cause
- Feature catalogue must be maintained as the product evolves. A stale catalogue produces inaccurate gap analysis -- features that were added or removed will be miscounted
- Usage data granularity matters. If product analytics tracks feature-level events, this skill is precise. If it only tracks page views or module-level access, the adoption picture is blurrier

## Dependencies

**Required:**
- Product analytics API (feature-level usage data per account per user)
- Product tier configuration and feature catalogue (see `references/feature-catalogue.md`)
- CRM API (customer goals, success plan data, segment classification)

**Strongly recommended:**
- pa-benchmark-engine (for peer adoption rates)
- pa-enablement-orchestrator (for routing adoption recommendations to enablement resources)
- bi-usage-monitor (for trend context)
- lo-milestone-tracker (for adoption milestone integration)

**Downstream consumers:**
- bi-health-score (adoption data feeds the usage component)
- cc-qbr-deck-builder (adoption data populates QBR slides)
- bi-expansion-detector (deep adoption is an expansion signal)
- pa-value-reporter (adoption breadth is a value metric)

## References

- `references/feature-catalogue.md` -- Feature definitions, tier mapping, categorisation, and maintenance process

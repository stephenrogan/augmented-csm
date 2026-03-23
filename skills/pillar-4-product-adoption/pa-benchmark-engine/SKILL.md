---
name: pa-benchmark-engine
description: Benchmarks account adoption metrics against segment peers to show customers where they stand relative to similar companies. Produces comparison data for QBRs, adoption conversations, and value narratives. Use when asked to benchmark a customer against peers, create adoption comparisons, show how an account compares to similar companies, build segment comparison data, or when any customer-facing conversation needs peer benchmarking context. Also triggers for questions about peer comparison, industry benchmarks, best-in-class adoption metrics, or competitive positioning within a segment.
license: MIT
metadata:
  version: "1.0.0"
  pillar: product-adoption
  category: adoption-engine
---

# Benchmark Engine

Benchmarks account-level adoption metrics against segment peers. Produces customer-safe comparison data that shows where the account stands relative to similar companies. Part of the Product Adoption & Value Realisation pillar.

This is a **comparison and reporting** skill. It computes how an account measures against its cohort. It does not advise on what to do about the comparison -- that is consultative work the CSM leads.

## When to Run

- **Triggered**: By cc-qbr-deck-builder (for QBR benchmark slides), by pa-adoption-tracker (for gap analysis context)
- **On-demand**: When a CSM needs benchmark data for a customer conversation
- **Scheduled**: Monthly benchmark refresh across all accounts

## Core Execution Logic

### Step 1: Identify Benchmark Cohort

Match the account to its segment cohort using the same segmentation as bi-health-score:
- Product tier (determines feature universe)
- Company size band (determines expected usage intensity)
- Industry (if sufficient data -- minimum 20 accounts per industry cohort)
- Contract age cohort (normalises for maturity -- a 3-month account should not be compared to a 3-year account)

If the precise cohort has fewer than 20 accounts, fall back to the next broader segment (e.g., drop industry, then drop contract age). Flag the fallback in the output.

### Step 2: Compute Benchmark Metrics

For each metric, compute the cohort distribution and the account's position within it:

| Metric | Definition | Why It Matters for Benchmarking |
|--------|-----------|-------------------------------|
| Feature adoption breadth | Features used / features available | Shows whether the customer is using what they are paying for |
| Active user ratio | Active users (30-day) / purchased seats | Shows whether the team has embraced the product |
| Key workflow completions | Core use-case workflows per month | Shows whether the product is delivering its primary value |
| Session depth | Average actions per session | Shows engagement quality -- shallow sessions suggest low value extraction |
| Time to first value | Days from contract start to first key workflow | Shows onboarding effectiveness (for newer accounts) |
| Feature adoption velocity | New features adopted per quarter | Shows whether the customer is expanding their usage over time |

For each metric, compute:
- Account value (current period)
- Cohort 25th percentile
- Cohort median (50th percentile)
- Cohort 75th percentile
- Account percentile rank within the cohort

### Step 3: Classify Position

| Position | Criteria | Customer-Safe Language |
|----------|----------|----------------------|
| Top quartile | Above 75th percentile | "Your team is among the highest-performing users of [product] in your segment" |
| Above average | Between median and 75th | "Your team is ahead of most similar companies on this metric" |
| Average | Within 10% of median | "Your team is in line with similar companies" |
| Below average | Between 25th and median | "There is an opportunity to increase value -- similar companies achieve more on this metric" |
| Bottom quartile | Below 25th percentile | "This is an area where your team could gain significant value with focused attention" |

Never use "bottom quartile" or "underperforming" in customer-facing language. Frame gaps as opportunities, not deficiencies.

### Step 4: Generate Comparison Views

Produce three comparison formats:

**Snapshot**: Current position across all metrics (for QBR slides)
**Trend**: Position change over the last 3-4 quarters (for progress narrative)
**Gap analysis**: Where the account trails peers most, ordered by potential impact (for adoption planning)

### Step 5: Generate Suggested Framing

For each metric, produce a one-sentence framing the CSM can use in conversation:
- Leading metrics: "Your team's [metric] is in the top quartile -- that is driving the outcomes you are seeing in [related outcome]"
- Lagging metrics: "Similar companies typically achieve [benchmark value] on [metric] -- your team is at [current value], which suggests there is room to drive more value from [related feature]"

These are suggestions for the CSM to adapt, not scripts to read verbatim.

## Output Format

```json
{
  "account_id": "string",
  "benchmark_date": "2026-03-10",
  "cohort": {
    "definition": "mid-market / medium / established",
    "cohort_size": 48,
    "fallback_applied": false
  },
  "metrics": [
    {
      "metric": "feature_adoption_breadth",
      "account_value": 0.65,
      "cohort_p25": 0.42,
      "cohort_median": 0.58,
      "cohort_p75": 0.72,
      "percentile_rank": 68,
      "position": "above_average",
      "trend_4q": "improving",
      "customer_framing": "Your team uses more features than most similar companies -- 65% breadth vs. 58% median. This depth of adoption is a strong indicator of value realisation."
    },
    {
      "metric": "active_user_ratio",
      "account_value": 0.62,
      "cohort_p25": 0.55,
      "cohort_median": 0.71,
      "cohort_p75": 0.84,
      "percentile_rank": 34,
      "position": "below_average",
      "trend_4q": "stable",
      "customer_framing": "Similar companies at your tier typically have 71% of their licensed users active. Your team is at 62% -- there is an opportunity to drive more value by expanding adoption across the team."
    }
  ],
  "summary": {
    "leading_metrics": ["feature_adoption_breadth", "key_workflow_completions"],
    "lagging_metrics": ["active_user_ratio"],
    "overall_position": "above_average",
    "key_opportunity": "Active user ratio is the primary gap. If addressed, it would move the account from above average to top quartile overall."
  },
  "customer_safe": true
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Which benchmarks to share | Full comparison data with customer-safe framing | Which metrics to highlight -- not all comparisons are motivating. The CSM picks what fits the conversation |
| How to frame underperformance | Opportunity language, peer data, suggested framing | The exact words and tone. Some customers respond to competitive framing ("your peers do better"); others find it condescending |
| Whether the cohort is right | Cohort definition and size | The customer may not see themselves as comparable to the segment. The CSM may need to adjust ("compared to companies your size in SaaS" vs. "compared to companies in financial services") |
| Gap prioritisation | Lagging metrics ranked by potential impact | Which gaps to address based on customer priorities and timing |

## Confidence and Limitations

- **High confidence** for percentile computation given sufficient cohort size (20+ accounts) -- the math is deterministic
- **Medium confidence** for cohort matching -- segmentation accuracy directly affects benchmark relevance. An account miscategorised into the wrong tier or size band produces misleading comparisons
- **Medium confidence** for suggested framing -- the language is appropriate for the metric position but may not fit the relationship tone or conversation context
- **Low confidence** for small cohorts (<20 accounts). Results are noisy and may mislead. Always flag small cohort size in the output
- Benchmarks are descriptive, not prescriptive. Being below median is not inherently bad if the customer's use case requires less intensive usage (e.g., a customer using the product for a narrow, specialised purpose may have low breadth scores but high depth on the features they use)
- Cannot benchmark on dimensions not tracked in product analytics (relationship quality, strategic alignment, internal satisfaction)
- Customer-facing benchmarks must be anonymised. Never expose individual account data. Never name specific peer companies. Present as "companies similar to yours"
- Benchmark data reflects the cohort's current state, which is not necessarily "good." If the entire segment underutilises a feature, the median is low. An account at the median is "average for the segment" but may still be underperforming against what is possible

## Dependencies

**Required:**
- Product analytics API (feature-level usage data across all accounts for cohort computation)
- Segment benchmark dataset (shared infrastructure with bi-health-score)
- CRM segmentation data (tier, company size, industry, contract age)

**Strongly recommended:**
- pa-adoption-tracker (for feature-level detail per account)
- bi-health-score (for health context -- do not benchmark unhealthy accounts without noting the health context)

**Downstream consumers:**
- cc-qbr-deck-builder (benchmark slides for customer presentations)
- pa-adoption-tracker (peer adoption rates for gap analysis)
- pa-value-reporter (benchmark context for value narrative)
- bi-expansion-detector (high benchmark position as expansion readiness signal)

## References

- `references/benchmark-methodology.md` -- Cohort definition, percentile computation, refresh cadence, and customer-safe output rules

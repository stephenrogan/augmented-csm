---
name: pa-feedback-aggregator
description: Aggregates product feedback from support tickets, call transcripts, surveys, and CSM notes, then clusters into themes for the product team. Produces weighted reports showing which issues affect the most customers and the most revenue. Use when asked to collect customer feedback, aggregate feature requests, theme product feedback, build a voice-of-customer report, identify common product gaps, or when any workflow needs structured feedback data for the product team. Also triggers for questions about customer feedback analysis, feature request patterns, product improvement priorities, or voice of customer reporting.
license: MIT
metadata:
  version: "1.0.0"
  pillar: product-adoption
  category: feedback-loop
---

# Feedback Aggregator

Collects product feedback from multiple sources, clusters it into themes, and produces structured reports for the product team. Part of the Product Adoption & Value Realisation pillar.

This is a **collection and analysis** skill. It aggregates and themes feedback. It does not prioritise product roadmap decisions (that is product management) or advocate for specific customers (that is the CSM's job using this data as evidence).

## When to Run

- **Continuous**: Scans incoming support tickets and call transcripts for feedback signals
- **Scheduled**: Monthly aggregation and theming report
- **On-demand**: When a CSM or product manager requests feedback analysis on a specific topic or feature area

## Core Execution Logic

### Step 1: Collect Feedback from All Sources

| Source | Collection Method | Signal Type | Confidence |
|--------|------------------|-------------|-----------|
| Support tickets | Scan for feature request tags, "wish," "would be great if," "need to be able to" language | Direct product feedback | High -- customer explicitly stating a need |
| Call transcripts | Extract product discussion segments, feature questions, frustration language, workaround descriptions | Conversational feedback | Medium -- context matters, may be speculative |
| NPS/CSAT surveys | Extract free-text responses mentioning product capabilities | Sentiment-linked feedback | High -- customer volunteered the feedback |
| CSM notes | Scan CRM notes for product-related observations and customer quotes | Relationship-context feedback | Medium -- filtered through CSM interpretation |
| Feature request log | Pull from formal feature request system if one exists | Formal requests | High -- explicitly logged |
| Community forum | Extract posts discussing product capabilities or gaps (from ca-community-monitor if available) | Peer-validated feedback | Medium -- may represent vocal minority |

### Step 2: Normalise and Deduplicate

For each feedback item captured:
1. **Normalise language**: "need better reporting" and "reporting is too basic" and "we need custom dashboards" may all be the same theme. Group by intent, not by exact phrasing
2. **Deduplicate per account**: Multiple tickets from the same account about the same issue count as one feedback item with severity weight, not multiple independent requests. This prevents a single noisy customer from dominating the analysis
3. **Tag metadata**: For each item, record:
   - Account ID, ARR, segment
   - Source (ticket/call/survey/note/formal request)
   - Date captured
   - Sentiment (request vs. frustrated complaint vs. blocking issue)
   - Contact role (end user, admin, champion, executive -- executive feedback carries different weight)

### Step 3: Cluster into Themes

Group feedback into a two-level taxonomy:

**Level 1 -- Category:**
| Category | Definition |
|----------|-----------|
| Feature gap | A capability the product does not have that customers want |
| Feature improvement | An existing feature that needs enhancement |
| UX/usability | The feature exists but is too difficult or unintuitive to use |
| Performance | Speed, reliability, scale, uptime issues |
| Integration | Connections to other tools, API capabilities, data import/export |
| Documentation | Missing or outdated help content, unclear guidance |

**Level 2 -- Specific theme within category:**
Each category contains specific themes (e.g., within "Feature gap": "Custom reporting dashboards," "Advanced permission controls," "Mobile app"). Themes emerge from the clustering -- do not force feedback into predetermined themes.

### Step 4: Rank Themes by Impact

For each theme, compute:

| Weight Factor | Computation | Why It Matters |
|--------------|-------------|---------------|
| Breadth | Number of unique accounts with this feedback | Wide impact vs. single-customer issue |
| Revenue weight | Sum of ARR across requesting accounts | Financial materiality |
| Health correlation | % of accounts with this feedback that also have declining health scores | Retention impact |
| Churn correlation | % of accounts that churned in the last 12 months that had this feedback before churning | Predictive churn signal |
| Sentiment intensity | % of feedback items tagged as "blocking issue" or "frustrated complaint" vs. "request" | Urgency signal |

**Composite impact score** = (Breadth * 0.25) + (Revenue weight normalised * 0.25) + (Health correlation * 0.20) + (Churn correlation * 0.20) + (Sentiment intensity * 0.10)

### Step 5: Generate Reports

**Monthly Product Feedback Report:**
For the product team, CS leadership, and cross-functional review.

```json
{
  "report_period": "February 2026",
  "total_feedback_items": 142,
  "unique_accounts": 38,
  "new_themes_this_month": 3,
  "top_themes": [
    {
      "theme": "Custom reporting dashboards",
      "category": "feature_gap",
      "impact_score": 8.4,
      "accounts": 12,
      "total_arr": 890000,
      "sentiment_breakdown": { "request": 7, "frustrated": 4, "blocking": 1 },
      "health_correlation": "3 of 12 accounts also have declining health scores",
      "churn_correlation": "2 accounts that churned in the last 12 months had this feedback",
      "representative_feedback": "Our analytics team exports data to build reports manually. It takes 4 hours a week. If we could build custom dashboards inside the platform, that time goes away.",
      "roadmap_status": "Planned -- Q3 2026",
      "summary": "12 accounts across mid-market and enterprise requesting customisable reporting. Correlated with adoption plateaus in the analytics feature set. Planned for Q3 -- product team should consider accelerating given the churn correlation."
    }
  ],
  "trending": [
    { "theme": "API rate limit increases", "direction": "up", "new_accounts_this_month": 4 }
  ],
  "resolved_this_month": [
    { "theme": "Bulk import performance", "resolution": "Performance improvement shipped in v3.2", "accounts_affected": 8 }
  ]
}
```

**Per-account feedback view:**
For CSMs preparing for QBRs or renewal conversations.

```json
{
  "account_id": "string",
  "active_feedback_items": 3,
  "themes": [
    { "theme": "Custom reporting", "status": "planned_q3", "first_raised": "2025-09-15", "times_raised": 4 }
  ],
  "resolved_items": 2
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Theme validation | Clustered themes with evidence | Whether the clustering is correct -- did the agent merge things that are distinct, or split things that belong together? |
| Impact assessment | Composite scores with component breakdown | Whether the weighting reflects the business reality. A theme with low breadth but one account threatening to churn may deserve higher priority than the score suggests |
| Product advocacy | Ranked themes with evidence and roadmap status | How to present this to the product team. The CSM uses the data to advocate; the data alone does not set priorities |
| Customer communication | Per-account feedback view with roadmap status | How and when to communicate roadmap updates to customers who raised the feedback |

## Confidence and Limitations

- **High confidence** for feedback collection and counting -- aggregating tickets and requests is deterministic
- **High confidence** for deduplication per account -- same account, same topic, same item
- **Medium confidence** for theme clustering -- NLP-based grouping may merge distinct issues or split related ones. Human review of the top 10 themes each month is recommended before presenting to the product team
- **Medium confidence** for impact scoring -- the weighting formula is a sensible default but should be calibrated against actual churn data over time
- **Low confidence** for churn correlation -- correlation is not causation. A churned account that mentioned a feature gap may have churned for an unrelated reason. Present as "correlated with" not "caused by"
- Feedback from vocal customers may be overrepresented even after deduplication. One account raising 15 tickets on the same issue counts as one feedback item, but the intensity signal may still skew perception. The breadth metric (unique accounts) is the most reliable measure of true demand
- Cannot assess the feasibility or cost of building a requested feature -- that is product management territory
- Qualitative feedback (verbatims from calls and surveys) requires NLP that may miss nuance, sarcasm, or cultural context. High-impact themes should be verified against the raw source material

## Dependencies

**Required:**
- Support platform API (ticket content, tags, metadata)
- CRM API (account data for ARR weighting and contact role identification)

**Strongly recommended:**
- Call transcript integration (Gong, Chorus) for conversational feedback
- Survey/NPS tool for sentiment-linked feedback
- bi-health-score (for health correlation analysis)
- ic-feature-request-tracker (for roadmap status linkage)

**Downstream consumers:**
- Product team (primary consumer -- monthly report for roadmap input)
- ic-cross-func-prep (CS-product sync materials)
- cc-qbr-deck-builder (per-account feedback view for QBR context)
- CS leadership (feedback-correlated churn data for strategic planning)

## References

- `references/feedback-taxonomy.md` -- Category definitions, clustering methodology, and deduplication rules

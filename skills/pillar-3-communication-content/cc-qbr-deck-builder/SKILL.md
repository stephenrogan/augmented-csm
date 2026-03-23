---
name: cc-qbr-deck-builder
description: Generates data-populated QBR presentation decks by pulling usage metrics, health data, support history, value evidence, and adoption analytics into a structured slide format by segment. Produces a deck the CSM customises with strategic narrative and recommendations. Use when asked to build a QBR deck, prepare business review slides, generate a customer presentation with data, populate a QBR template, or when lo-qbr-orchestrator triggers content preparation. Also triggers for questions about QBR content, business review presentations, customer-facing data decks, or quarterly review materials.
license: MIT
metadata:
  version: "1.0.0"
  pillar: communication-content
  category: content-engine
---

# QBR Deck Builder

Generates data-populated QBR decks by assembling usage metrics, health trends, support data, value evidence, and adoption analytics into a structured presentation. Part of the Communication & Content Production pillar.

This is a **content assembly and generation** skill. It produces a data-rich deck that the CSM customises with narrative, strategic recommendations, and relationship-aware framing. The agent builds the evidence; the human tells the story.

## When to Run

- **Triggered**: By lo-qbr-orchestrator at T-7 before a scheduled QBR
- **On-demand**: When a CSM requests a QBR deck for a specific account

## Core Execution Logic

### Step 1: Pull Data from All Sources

Gather the complete data picture for the account:

| Data Category | Source Skill | Specific Metrics Pulled |
|-------------|-------------|----------------------|
| Usage and adoption | bi-usage-monitor, pa-adoption-tracker | DAU/MAU, feature adoption breadth, key workflow completions, trend direction, period-over-period change |
| Health | bi-health-score | Composite score, component breakdown, trajectory over last 2+ quarters |
| Value delivered | pa-value-reporter | Headline metric, supporting evidence, time-to-value benchmarks, customer-defined KPI progress |
| Benchmarks | pa-benchmark-engine | Account position vs. segment peers across key metrics |
| Support | Support platform | Ticket volume, resolution time, CSAT, open issues, escalation history |
| Milestones | lo-milestone-tracker | Success plan progress, milestones completed, milestones overdue |
| Engagement | ra-engagement-tracker | Touchpoint history, stakeholder engagement health |
| Contract | CRM | ARR, renewal date, product tier, contract terms |
| Feature requests | ic-feature-request-tracker | Open requests with roadmap status, resolved requests since last QBR |

**Data freshness check**: All data must be within 7 days of the QBR date. Flag any data source that is stale. A QBR deck with outdated data undermines credibility.

### Step 2: Select Deck Template by Segment

| Segment | Slide Count | Structure | Audience Expectation |
|---------|------------|-----------|---------------------|
| Enterprise | 10-15 slides | Formal structure with executive summary, detailed data slides, strategic recommendations, and discussion time | Decision-makers expect data depth, benchmarking, and forward-looking strategy |
| Mid-Market | 8-10 slides | Balanced structure with usage review, value highlights, support summary, and looking ahead | Operators expect actionable insights and clear next steps |
| SMB | 5-6 slides (or email format) | Condensed with usage snapshot, value highlights, tips, and action items | Busy leaders expect brevity and immediate takeaways |

### Step 3: Populate Slides by Template

**Enterprise QBR deck:**

| Slide | Content | Data Source | CSM Input Required |
|-------|---------|------------|-------------------|
| 1. Title and agenda | Meeting details, attendees, agenda items | Calendar, CRM | CSM may adjust agenda based on conversation goals |
| 2. Executive summary | 3-5 bullet headline: health trajectory, value headline, key milestone, primary discussion topic | bi-health-score, pa-value-reporter | CSM writes the "so what" framing |
| 3. Relationship overview | Key events since last QBR, milestones achieved, stakeholder changes | lo-milestone-tracker, ra-stakeholder-mapper | CSM adds context on relationship dynamics |
| 4-5. Usage and adoption | Usage trend charts, feature adoption breadth, peer comparison | bi-usage-monitor, pa-adoption-tracker, pa-benchmark-engine | CSM highlights what matters to this customer |
| 6. Value delivered | Headline metric, supporting evidence, ROI calculation | pa-value-reporter | CSM validates methodology and framing |
| 7. Support summary | Ticket volume, resolution time, CSAT, open issues | Support platform | CSM adds context on any sensitive support history |
| 8. Product roadmap | Relevant upcoming features, feature request status updates | ic-feature-request-tracker, product roadmap | CSM selects which roadmap items to highlight |
| 9. Strategic recommendations | **PLACEHOLDER -- CSM writes this slide** | N/A | This is the most valuable slide. The agent cannot write it because it requires judgment about the account's future direction |
| 10. Discussion | Open floor for customer priorities and questions | N/A | CSM prepares discussion questions based on relationship context |
| 11. Action items | Captured during the meeting (populated post-QBR) | N/A | CSM captures live |

**Mid-Market QBR deck** follows the same logic with slides 3 and 8 consolidated and lighter data depth.

**SMB QBR** compresses to: usage snapshot, value highlights, 2-3 tips/recommendations, and action items.

### Step 4: Generate Comparison Views

For every data slide, produce comparison context:

| Comparison Type | What It Shows | Where Used |
|----------------|-------------|-----------|
| Period-over-period | This quarter vs. last quarter | Every data slide -- shows trajectory |
| Benchmark | Account vs. segment peers (from pa-benchmark-engine) | Usage and adoption slides -- shows relative position |
| Plan vs. actual | Success plan milestones: target vs. actual dates | Milestone slide -- shows accountability |
| Year-over-year | Same quarter last year (if data available) | Value slide -- shows long-term trend |

### Step 5: Apply Quality Gates

Before delivering the deck:

| Gate | Check | Fail Action |
|------|-------|------------|
| Data freshness | All data within 7 days of QBR date | Flag stale sources. Pull fresh data if possible |
| Data accuracy | Spot-check 3 key numbers against CRM source | If discrepancy found, investigate before delivering |
| Customer-safe | No internal terminology (risk scores, internal notes, CSM assessments) visible | Strip all internal-only data. This is a customer-facing deck |
| Completeness | All template slides populated (except CSM-input slides) | Flag any slide with missing data. Provide the slide with a "data unavailable" note rather than omitting it |
| Readability | Charts are labelled, numbers are formatted, slide titles are descriptive (not just "Usage") | Reformat any chart that requires explanation to understand |
| Strategic slides | CSM-input slides are clearly marked as placeholders | The agent should never fill in the strategic recommendation slide with generic advice |

## Output Format

```json
{
  "account_id": "string",
  "qbr_date": "2026-04-15",
  "deck_format": "enterprise",
  "slides_generated": 11,
  "slides_requiring_csm_input": 3,
  "data_freshness": {
    "all_current": true,
    "stale_sources": [],
    "oldest_data_point": "2026-04-09"
  },
  "content_summary": {
    "health": { "score": 74, "trend": "improving", "vs_last_qbr": "+6" },
    "usage": { "dau_mau": 0.42, "feature_breadth": 0.65, "trend": "growing" },
    "value": { "headline": "340 hours saved this quarter", "vs_prior_quarter": "+22%" },
    "support": { "tickets": 12, "avg_resolution_hours": 4.2, "csat": 4.6 },
    "benchmark_position": "Above average across key metrics. Top quartile in workflow completions"
  },
  "csm_action_required": [
    "Write strategic recommendations (slide 9)",
    "Review and customise executive summary framing (slide 2)",
    "Prepare discussion questions based on relationship context (slide 10)"
  ],
  "delivery_status": "draft_ready_for_csm_review"
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Strategic recommendations | Full data package, trend context, adoption gaps | What to recommend for the next quarter. This is the slide that demonstrates the CSM's value as a strategic partner, not just a data presenter |
| Narrative framing | Data slides with comparison views | How to tell the story. The same data can be framed as "strong performance" or "room for improvement" depending on what the CSM wants the customer to focus on |
| Slide selection | Full deck template | Which slides to keep, which to cut, which to reorder. Not every QBR needs every slide. A 45-minute QBR with 15 slides means 3 minutes per slide -- too fast for depth |
| Data emphasis | All metrics with peer comparisons | Which metrics to highlight. Lead with strengths to build confidence, then address gaps constructively |
| Sensitivity review | Customer-safe check applied | Whether any data point, while factually accurate, should be excluded because of customer sensitivity (e.g., a metric that declined due to a customer-side error) |

## Confidence and Limitations

- **High confidence** for data population -- pulling metrics and formatting into slides is deterministic
- **High confidence** for period-over-period computation -- mathematical comparison with defined windows
- **Medium confidence** for chart selection and emphasis -- the skill highlights statistically significant changes, but the CSM may want different emphasis based on conversation strategy
- **Medium confidence** for benchmark context -- peer comparison is factual, but whether a specific benchmark motivates or discourages this customer depends on their competitive mindset
- **Low confidence** for narrative framing -- the skill generates factual summaries, not persuasive narratives. The CSM adds the story. A QBR deck without narrative is a data dump, not a business review
- Cannot generate the strategic recommendation slides. These require judgment about the account's future direction, relationship dynamics, and what the customer is ready to hear. This is the CSM's highest-value contribution to the QBR
- Cannot determine which slides the customer will care about most. An executive may want to skip straight to the financial summary; a technical lead may want to deep-dive into usage. The CSM adjusts the presentation flow based on the room

## Dependencies

**Required:**
- bi-health-score (health data for trajectory slides)
- bi-usage-monitor (usage data for adoption slides)
- pa-value-reporter (value evidence for ROI slides)
- CRM API (contract data, account context)

**Strongly recommended:**
- pa-adoption-tracker (feature-level adoption for depth)
- pa-benchmark-engine (peer comparison data)
- lo-milestone-tracker (success plan progress)
- Support platform (support summary data)
- ic-feature-request-tracker (roadmap update status)
- ra-engagement-tracker (engagement context for relationship slides)

**Downstream consumers:**
- CSM (deck review and customisation -- the most important consumer. The deck is a tool for the CSM, not the final product)
- lo-qbr-orchestrator (deck delivery as part of the QBR lifecycle workflow)
- CRM (QBR activity record with deck link)
- pa-value-reporter (QBR is a validation point for value metrics -- customer reaction feeds back)

## References

- `references/deck-guidelines.md` -- Slide design principles, data visualisation standards, and customer-safe content rules

---
name: pa-knowledge-base-curator
description: Keeps customer-facing help content aligned with product changes, identifies content gaps from support ticket patterns, surfaces relevant resources to customers based on adoption profiles, and measures documentation effectiveness through ticket deflection. Use when asked to audit help content, identify knowledge base gaps, recommend documentation improvements, match customers to relevant help articles, track documentation quality, or when support ticket patterns suggest missing or outdated documentation. Also triggers for questions about help centre management, documentation quality, self-serve content strategy, support deflection through better documentation, or content gap analysis.
license: MIT
metadata:
  version: "1.0.0"
  pillar: product-adoption
  category: enablement-engine
---

# Knowledge Base Curator

Maintains alignment between product capabilities and customer-facing documentation. Identifies content gaps from support patterns, detects stale content after product changes, and surfaces relevant resources to customers proactively. Part of the Product Adoption & Value Realisation pillar.

This is a **monitoring and recommendation** skill. It identifies where documentation is missing, outdated, or underperforming. It does not write the documentation (that is content team or enablement work) -- it tells you what needs writing, what needs updating, and estimates the impact of fixing it.

## When to Run

- **Triggered**: After product releases (scan for help articles that reference changed features)
- **Scheduled**: Weekly support ticket pattern analysis for content gap detection
- **On-demand**: When a CSM requests relevant resources for a specific customer based on their adoption profile

## Core Execution Logic

### Step 1: Identify Content Gaps from Support Patterns

Analyse support ticket data for signals that documentation is missing or inadequate:

| Signal | Detection Criteria | Confidence | Estimated Gap Impact |
|--------|-------------------|-----------|---------------------|
| Recurring question cluster | 5+ tickets from different accounts on the same topic in 30 days | High | High -- same question being asked repeatedly means the answer is not findable |
| "How do I" language | Tickets phrased as procedural questions ("How do I set up...", "Where can I find...") | High | High -- these are documentation-solvable questions |
| High-traffic article followed by ticket | Article viewed and then a ticket created within 30 minutes by the same user | High | High -- the article exists but does not answer the question |
| Search-with-no-result | Help centre search queries that return zero matches (if analytics available) | Medium | Medium -- demand exists for content that does not |
| New feature tickets | Spike in tickets about a feature within 30 days of its release, with no corresponding help article | High | High -- documentation was not created alongside the release |
| Workaround descriptions | Tickets where the CSM or support agent describes a workaround for something that should be documented | Medium | Medium -- the knowledge exists internally but is not published |

For each gap identified, compute:
- **Estimated ticket deflection**: Based on the number of tickets this gap generated in the last 30 days, how many could have been prevented with documentation?
- **Revenue weight**: Total ARR of accounts that submitted tickets on this topic
- **Effort estimate**: How complex would the documentation be? (Simple FAQ, step-by-step guide, or comprehensive tutorial)

### Step 2: Audit Content Freshness After Product Releases

After each product release:

1. Map changed features to existing help articles using feature names, keywords, and product area tags
2. For each affected article, classify the impact:

| Impact | Criteria | Priority |
|--------|----------|----------|
| Breaking | Article references UI, workflow, or feature that has been removed or fundamentally changed | Critical -- article will actively mislead readers |
| Outdated | Article is factually correct but references old UI or does not cover new capabilities | High -- article is incomplete |
| Minor | Article is mostly correct but could mention a new option or improvement | Low -- update when convenient |
| Unaffected | Article covers content that was not changed in this release | None -- no action needed |

3. Prioritise updates by: (a) article monthly traffic, (b) impact severity, (c) gap creation (does the outdated article create a new content gap?)

### Step 3: Surface Resources to Customers

Based on a customer's adoption profile from pa-adoption-tracker:

1. For features they are using: surface advanced tips, best practices, and power-user guides
2. For features they are not using but should be (relevant untouched features): surface introductory guides and tutorials
3. Personalise the recommendation by segment and use case:
   - Enterprise customers get comprehensive documentation
   - SMB customers get quick-start guides and video walkthroughs
4. Deliver through pa-enablement-orchestrator (integrated enablement plan) or directly to the CSM for inclusion in a touchpoint

### Step 4: Measure Documentation Effectiveness

Track whether content is actually solving problems:

| Metric | Computation | What It Tells You |
|--------|------------|------------------|
| View-to-ticket ratio | Tickets created within 30 min of article view / total article views | Whether the article answers the question (lower is better) |
| Search satisfaction | Searches that result in an article click (not a "no results" or immediate bounce) | Whether content is findable |
| Content gap ticket volume | Total tickets in the last 30 days that match identified gaps | The cost of not having the content |
| Post-publication deflection | Ticket volume on a topic before vs. after documentation was published | Whether the new content actually reduced tickets |
| Staleness rate | Percentage of articles not reviewed since the last 2 product releases | How much of the knowledge base is at risk of being outdated |

### Step 5: Generate Reports

**Weekly content gap report:**

```json
{
  "report_date": "2026-03-10",
  "gaps_identified": [
    {
      "topic": "Custom API authentication for SSO environments",
      "evidence": "12 tickets from 8 accounts in 30 days. All procedural 'how do I' questions",
      "current_article": "none",
      "estimated_ticket_deflection_monthly": 10,
      "arr_of_affected_accounts": 420000,
      "recommended_content_type": "Step-by-step guide with screenshots",
      "estimated_creation_effort": "2-3 hours",
      "priority": "high"
    },
    {
      "topic": "Bulk import performance with large datasets",
      "evidence": "6 tickets from 5 accounts. Current article covers basic import but not performance optimisation for large files",
      "current_article": "KB-2025-0089",
      "article_monthly_views": 180,
      "view_to_ticket_ratio": 0.033,
      "recommended_action": "Expand existing article with performance section",
      "estimated_effort": "1 hour",
      "priority": "medium"
    }
  ],
  "stale_articles": [
    {
      "article_id": "KB-2024-0142",
      "title": "Setting up dashboard widgets",
      "last_updated": "2025-06-15",
      "product_changes_since": 2,
      "impact": "outdated",
      "monthly_views": 340,
      "priority": "high"
    }
  ],
  "content_health_summary": {
    "total_articles": 142,
    "current": 98,
    "needs_update": 31,
    "outdated_critical": 4,
    "staleness_rate": 0.25,
    "avg_view_to_ticket_ratio": 0.018,
    "estimated_monthly_deflectable_tickets": 28
  }
}
```

**Per-customer resource recommendations (for CSM or pa-enablement-orchestrator):**

```json
{
  "account_id": "string",
  "recommendations": [
    {
      "feature": "Advanced Reporting",
      "adoption_status": "untouched",
      "segment_adoption_rate": 0.78,
      "resources": [
        { "title": "Getting Started with Custom Reports", "type": "tutorial", "url": "https://...", "duration": "5 min read" },
        { "title": "Custom Report Templates Gallery", "type": "reference", "url": "https://...", "duration": "browse" }
      ],
      "suggested_framing": "Your team has access to custom reporting -- this 5-minute guide covers the basics. Most teams at your tier use this to cut manual reporting time"
    }
  ]
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Gap prioritisation | Ranked gaps with ticket volume, ARR weight, and effort estimates | Which gaps to address first, given content team capacity. The skill ranks by impact; the content team may have capacity constraints |
| Content creation | Gap specification with evidence and content type recommendation | The actual content. Writing help articles is human work -- the skill defines what is needed, not how to write it |
| Customer resource delivery | Per-customer recommendations with framing suggestions | Whether and how to share resources with specific customers. The CSM knows whether sending a help article will be helpful or patronising |
| Stale content triage | Stale articles ranked by traffic and severity | Whether to update, archive, or redirect each stale article. Some outdated articles are still useful with a minor edit; others should be retired |

## Confidence and Limitations

- **High confidence** for content staleness detection -- comparing article dates to product release dates is deterministic
- **High confidence** for recurring question detection -- ticket clustering on the same topic is a strong gap signal
- **Medium confidence** for content gap identification -- support ticket pattern analysis is robust but may surface noise from one-off issues that are not representative of broader demand
- **Medium confidence** for ticket deflection estimates -- based on historical ticket volume, not a guarantee that documentation will eliminate all related tickets. Some tickets will persist because the customer prefers human interaction or has a variant not covered by the article
- **Low confidence** for content quality assessment -- the skill can detect that an article exists and measure its view-to-ticket ratio, but it cannot assess whether the article is well-written, clearly structured, or genuinely helpful. High traffic with a low view-to-ticket ratio is a good proxy, but not definitive
- Search-with-no-result analysis requires help centre search analytics integration. Not all platforms provide this. Without it, the skill loses one of its gap detection signals
- Cannot write or update documentation. This is a measurement and recommendation skill. Execution requires a content team or enablement resource

## Dependencies

**Required:**
- Support platform API (ticket data, content, and patterns)
- Help centre or knowledge base platform (article catalogue, view counts, search analytics if available)

**Strongly recommended:**
- Product release tracking (for staleness detection after releases)
- pa-adoption-tracker (customer adoption profiles for resource matching)
- pa-enablement-orchestrator (for routing resource recommendations into enablement plans)

**Downstream consumers:**
- Content team (primary consumer -- gap reports drive content creation priorities)
- pa-enablement-orchestrator (resource recommendations feed enablement plans)
- CSMs (per-customer resource recommendations for touchpoints)
- CS leadership (content health metrics for resource allocation decisions)

## References

- `references/content-audit-process.md` -- Post-release audit process, quarterly full audit, and gap report methodology

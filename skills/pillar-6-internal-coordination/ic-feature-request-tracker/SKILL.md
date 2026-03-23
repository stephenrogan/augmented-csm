---
name: ic-feature-request-tracker
description: Logs customer feature requests from calls, tickets, and emails, links them to the product roadmap, tracks their status, and surfaces updates to CSMs when requested features ship or are declined. Use when asked to log a feature request, track product requests, link customer needs to the roadmap, monitor when a requested feature is available, or when any customer interaction surfaces a product enhancement need. Also triggers for questions about feature request management, roadmap tracking, customer-requested product changes, or product backlog from the CS perspective.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: internal-coordination
  category: coordination-engine
---

# Feature Request Tracker

Logs feature requests, links to the product roadmap, tracks status changes, and notifies CSMs when requested features ship. Part of the Internal Coordination pillar.

This is a **logging and tracking** skill. It maintains the record and surfaces updates. The CSM decides what to request, how to prioritise for their customer, and when to communicate roadmap updates.

## When to Run

- **Triggered**: When cc-call-summariser or pa-feedback-aggregator identifies a feature request
- **On-demand**: When a CSM manually logs a request
- **Scheduled**: Weekly roadmap status check to detect shipped or declined features

## Core Execution Logic

### Step 1: Capture the Request

For each feature request, capture:

| Field | Source | Required |
|-------|--------|----------|
| Account ID | CRM | Yes |
| Contact who raised it | Call notes, ticket, or CSM input | Yes |
| Contact role | CRM contact record | Yes -- executive requests carry different weight |
| Description | Customer's own words where possible | Yes |
| Business impact | Why they need it -- what problem it solves for their business | Yes -- this is what makes a request actionable for product |
| Customer priority | Critical (blocking), important (significant pain), nice-to-have (improvement) | Yes |
| Source | Call, support ticket, email, QBR, community forum | Yes |
| Date logged | Timestamp | Auto |
| Current workaround | How the customer is handling this without the feature | If known -- shows urgency |

### Step 2: Link to Roadmap

Check the product roadmap or feature tracking system for matches:

| Match Type | Criteria | Action |
|-----------|----------|--------|
| Exact match | Feature is planned or in development that directly addresses the request | Link the request to the roadmap item. Inherit timeline and status |
| Partial match | Related feature is planned that may partially address the need | Link with a note explaining what is and is not covered |
| No match | Request is new to the product team | Log as unlinked. Include in the next pa-feedback-aggregator report for product review |

### Step 3: Track Status

Each request follows a lifecycle:

| Status | Definition | CSM Notification |
|--------|-----------|-----------------|
| Logged | Request captured, not yet reviewed by product | None (acknowledge to customer that it is logged) |
| Acknowledged | Product team has seen and accepted the request into the backlog | Optional -- CSM decides whether to tell the customer |
| Planned | Feature is on the roadmap with estimated timeline | Alert CSM: "[Feature] planned for [timeline]" |
| In development | Feature is actively being built | Alert CSM: "[Feature] in development, expected [date]" |
| Shipped | Feature is live and available on the customer's tier | Alert CSM: "[Feature] is live. Here are the release notes. Consider reaching out to [contacts who requested it]" |
| Declined | Product team decided not to build (with rationale) | Alert CSM with rationale: "[Feature] will not be built because [reason]. Suggested alternative: [if any]" |
| Workaround available | The need can be addressed with existing capabilities | Alert CSM with documentation: "This can be achieved using [existing feature]. Here is how: [link]" |

### Step 4: Maintain Request Registry

A searchable registry of all feature requests with:
- Request count by theme (how many unique accounts have asked for this)
- ARR weight (total ARR of accounts requesting this feature)
- Status (linked to roadmap item status)
- Average age (how long requests have been open)
- Churn correlation (did any accounts that churned have this as an open request)

This data feeds pa-feedback-aggregator for the monthly product feedback report.

### Step 5: Generate Outputs

**Per-account request view (for QBR or renewal prep):**
```json
{
  "account_id": "string",
  "active_requests": [
    {
      "id": "FR-2026-0089",
      "description": "Custom reporting dashboards with drag-and-drop configuration",
      "business_impact": "Analytics team spends 4 hours per week building reports manually",
      "customer_priority": "critical",
      "status": "planned",
      "roadmap_item": "ROAD-2026-Q3-014",
      "estimated_availability": "Q3 2026",
      "first_raised": "2025-09-15",
      "times_raised": 4,
      "days_open": 176
    }
  ],
  "resolved_requests": [
    {
      "id": "FR-2025-0312",
      "description": "Bulk user import from CSV",
      "status": "shipped",
      "shipped_date": "2026-01-15",
      "customer_notified": true
    }
  ],
  "summary": "3 active requests (1 critical, 1 important, 1 nice-to-have). 2 resolved in last 6 months."
}
```

**Product team summary (feeds pa-feedback-aggregator):**
```json
{
  "total_open_requests": 87,
  "unique_themes": 34,
  "top_requested": [
    {
      "theme": "Custom reporting dashboards",
      "unique_accounts": 12,
      "total_arr": 890000,
      "avg_days_open": 142,
      "status": "planned_q3",
      "churn_correlation": "2 churned accounts had this as an open request"
    }
  ],
  "recently_shipped": [
    { "feature": "Bulk user import", "shipped": "2026-01-15", "accounts_requesting": 8 }
  ]
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Request prioritisation | Request details, customer priority, business impact | How strongly to advocate for this request in product discussions. Not all critical requests from one customer are critical for the portfolio |
| Customer communication on status | Status update, roadmap timeline, alternatives | How and when to communicate. "Planned for Q3" can be shared as-is, but "Declined" requires careful framing |
| Workaround delivery | Existing feature documentation that addresses the need | Whether the workaround is genuinely adequate for this customer or whether the request stands |
| Shipped feature follow-up | Release notes, customer contacts who requested | Whether to reach out proactively, include in the next QBR, or let the customer discover it |

## Confidence and Limitations

- **High confidence** for logging and status tracking -- structured data management with defined lifecycle states
- **High confidence** for shipped feature notification -- product releases are definitive events
- **Medium confidence** for roadmap matching -- keyword and topic matching may produce false positives (partial match that does not actually address the need) or miss valid matches (different terminology for the same concept)
- **Low confidence** for predicting when a feature will ship. Roadmap timelines change frequently. The skill reflects the current roadmap state, which is a snapshot, not a commitment
- Cannot influence product prioritisation. The skill informs through data (request volume, ARR weight, churn correlation). The CSM advocates through relationship and judgment in product discussions
- Cannot assess whether a declined feature request will cause the customer to churn. That assessment requires understanding the customer's alternatives, their emotional investment in the request, and the overall relationship health

## Dependencies

**Required:**
- CRM or feature request system (request storage and lifecycle tracking)
- Product roadmap integration (for matching and status tracking)

**Strongly recommended:**
- cc-call-summariser (automated request capture from calls)
- pa-feedback-aggregator (themes and impact analysis for product reporting)
- Support platform (for ticket-sourced requests)

**Downstream consumers:**
- pa-feedback-aggregator (feeds the monthly product feedback report)
- cc-qbr-deck-builder (per-account request view for QBR context)
- lo-renewal-manager (open critical requests as renewal risk factor)

## References

- `references/request-lifecycle.md` -- Full lifecycle definitions, matching criteria, and notification templates

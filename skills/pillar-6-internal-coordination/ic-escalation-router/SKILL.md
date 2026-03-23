---
name: ic-escalation-router
description: Routes customer escalations to the appropriate internal team with structured documentation, severity classification, and tracking. Ensures escalations reach the right people with full context and tracks through to resolution. Use when asked to escalate an account issue, route a customer problem to engineering or product, create an escalation ticket, manage the escalation process, or when any customer issue needs internal team involvement beyond the CSM. Also triggers for questions about escalation management, internal routing, cross-functional issue resolution, or escalation tracking.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: internal-coordination
  category: coordination-engine
---

# Escalation Router

Routes escalations to the right internal team with structured briefs, tracks resolution, and ensures nothing falls through the cracks. Part of the Internal Coordination pillar.

This is a **routing, documentation, and tracking** skill. It ensures the right people see the right information at the right time. The CSM decides what to escalate and at what severity; this skill handles the mechanics of getting it there and following through.

## When to Run

- **Triggered**: When CSM initiates an escalation (sets escalation flag in CRM or requests escalation)
- **On-demand**: When routing needs to be determined for a new issue
- **Continuous**: Monitors active escalations for stalls and SLA breaches

## Core Execution Logic

### Step 1: Classify the Escalation

Determine the category, severity, and routing target:

| Category | Routes To | Typical Trigger | Response SLA |
|----------|----------|-----------------|-------------|
| Product defect (bug) | Engineering via support platform | P1/P2 ticket not resolved within SLA | 4 hours acknowledge, 24-72 hours resolution depending on severity |
| Feature gap (blocking) | Product management | Customer blocked by missing capability, affecting retention | 48 hours acknowledge, 2 weeks decision on approach |
| Service failure | CS leadership + support leadership | SLA breach, repeated failures, relationship damage | 4 hours acknowledge, 24 hours remediation plan |
| Commercial dispute | CS leadership + finance | Billing issue, contract disagreement, pricing complaint | 48 hours acknowledge, 1 week resolution |
| Relationship at risk | CS leadership | Champion departure, competitive threat, strategic account declining | 24 hours acknowledge, CSM + manager strategy session within 48 hours |
| Executive intervention | CRO or CEO office | Strategic account, board-level relationship, existential churn risk | Same day acknowledge, executive response within 48 hours |

### Step 2: Generate Escalation Brief

Invoke cc-internal-brief-writer with escalation context. Every brief follows this structure:

**Headline** (one line): What is happening, to which customer, and what is at stake.
Example: "API latency issue affecting Acme Corp -- P1 open 12 days, EUR 85k ARR, renewal in 67 days"

**Customer impact** (2-3 sentences): How this affects the customer's business. Not just "they are unhappy" but "their analytics team cannot run reports, costing them an estimated 4 hours per week in manual workarounds."

**Timeline** (chronological):
- When the issue started
- Each escalation step taken, with date and outcome
- Current status

**Resolution attempts** (what has been tried):
- Every prior attempt to resolve, with the outcome of each
- This prevents the receiving team from re-trying approaches that have already failed

**Specific ask** (what you need):
- Not "please help" but "we need engineering to investigate the API latency on this account's instance and provide a fix or timeline by [date]"
- Include the definition of "resolved" from the customer's perspective

**Customer communication status**:
- What the customer has been told
- What they expect (specific timeline, specific outcome)
- Their current sentiment (patient, frustrated, threatening churn)

**Commercial context** (when relevant):
- ARR, renewal date, expansion pipeline
- Financial impact of losing this account

### Step 3: Route and Confirm Receipt

1. Send the brief to the identified team via the configured channel (Slack for urgent, email for standard, ticketing system for trackable)
2. Log the escalation with: ID, timestamp, category, severity, routing target, brief content
3. Start the acknowledgement clock (4 hours for critical, 24 hours for standard)
4. If no acknowledgement within the SLA: automatically re-route with escalation to the team's manager and a note that the initial routing was not acknowledged

### Step 4: Track Resolution

Monitor the escalation lifecycle:

| Status | Definition | Trigger for Next Status |
|--------|-----------|----------------------|
| Routed | Brief sent to receiving team | Acknowledgement received |
| Acknowledged | Receiving team confirms receipt and assigns owner | Work begins |
| In progress | Active work on resolution | Resolution delivered or status update due |
| Stalled | No progress for 48 hours (critical) or 5 business days (standard) | Re-escalation flag to CSM + manager |
| Resolved | Receiving team confirms fix/response delivered | CSM confirms customer is satisfied |
| Closed | CSM confirms resolution is complete from the customer's perspective | Escalation archived |

Status update cadence:
- Critical escalations: daily update to CSM, automatic stall detection at 48 hours
- Standard escalations: update every 3 business days, stall detection at 5 business days

### Step 5: Generate Escalation Report

Weekly summary for CS leadership:

```json
{
  "report_date": "2026-03-10",
  "active_escalations": 7,
  "new_this_week": 3,
  "resolved_this_week": 2,
  "stalled": 1,
  "average_resolution_time_days": 4.2,
  "escalations": [
    {
      "id": "ESC-2026-0342",
      "account": "Acme Corp",
      "category": "product_defect",
      "severity": "critical",
      "status": "in_progress",
      "days_open": 5,
      "owner": "Mike Ross (Eng Lead)",
      "arr_at_risk": 85000,
      "customer_sentiment": "frustrated_but_patient",
      "next_update_due": "2026-03-11"
    }
  ],
  "trends": {
    "most_common_category": "product_defect",
    "avg_time_to_acknowledge": "3.1 hours",
    "stall_rate": "14%"
  }
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Escalation initiation | Account context, issue details | Whether to escalate, at what severity, and how urgently. Not every issue warrants escalation |
| Severity classification | Suggested severity with rationale | Whether the suggested severity is correct. The CSM may override based on relationship context |
| Re-escalation | Stall notification with timeline and history | Whether to push harder, accept the timeline, or find an alternative path |
| Customer communication | Escalation status updates | What to tell the customer and when. Managing expectations during an escalation is pure human skill |
| Resolution confirmation | Receiving team's "resolved" status | Whether the resolution actually addresses the customer's need from their perspective |

## Confidence and Limitations

- **High confidence** for routing logic and brief generation -- structured classification and documentation with defined rules
- **High confidence** for status tracking and stall detection -- timestamp-based monitoring with defined thresholds
- **Medium confidence** for severity classification -- the skill classifies based on defined criteria (ticket severity, ARR, renewal proximity), but the CSM may assess severity differently based on relationship context or cumulative frustration
- **Low confidence** for resolution timeline estimation -- how quickly an internal team resolves an issue depends on their capacity, competing priorities, and technical complexity. The SLAs are targets, not guarantees
- Cannot guarantee that the receiving team will act within the expected timeframe
- Cannot assess whether escalation is the right approach vs. a direct conversation, a workaround, or accepting the limitation
- Cannot navigate internal politics -- if the receiving team is resistant or under-resourced, the CSM must advocate through relationship and influence, not routing mechanics

## Dependencies

**Required:**
- CRM API (escalation tracking, account context)
- Internal messaging (Slack or email for routing)
- cc-internal-brief-writer (brief generation)

**Strongly recommended:**
- bi-account-brief (full account context for briefs)
- lo-sla-monitor (for SLA breach-triggered escalations)
- Support platform (for ticket-linked escalations)

**Downstream consumers:**
- ic-cross-func-prep (escalation committee materials)
- ic-internal-notifier (escalation status notifications)
- cc-report-generator (weekly escalation summary)

## References

- `references/routing-rules.md` -- Complete routing table, acknowledgement SLAs, and re-escalation protocols

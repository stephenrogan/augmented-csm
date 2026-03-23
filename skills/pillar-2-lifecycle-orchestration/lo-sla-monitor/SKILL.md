---
name: lo-sla-monitor
description: Tracks commitments, SLAs, and promises made to customers across all touchpoints. Surfaces upcoming deadlines, flags breaches, and maintains an accountability record. Use when asked to track customer commitments, monitor SLA compliance, manage action items from calls and meetings, ensure follow-through on promises, build an accountability system for CS, or when any workflow needs to know what has been committed to a customer and whether it has been delivered. Also triggers for questions about commitment tracking, follow-up management, promise fulfilment, or accountability monitoring.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: lifecycle-orchestration
  category: workflow-engine
---

# SLA Monitor

Tracks commitments and SLAs made to customers -- from formal contractual obligations to informal promises made in calls and emails. Surfaces upcoming deadlines, flags breaches before they happen, and maintains an accountability record. Part of the Lifecycle Orchestration pillar.

This is a **tracking and alerting** skill. It monitors commitments against deadlines and surfaces deviations. It does not make commitments, renegotiate deadlines, or communicate with customers about breaches. Those are human decisions.

## When to Run

- **Continuous**: Monitors all active commitments against their deadlines
- **Triggered**: When a new commitment is logged (manually by CSM or extracted from call transcripts/meeting notes)
- **On-demand**: When a CSM requests the commitment status for a specific account

## Commitment Types

| Type | Source | Example | Tracking Method |
|------|--------|---------|----------------|
| Contractual SLA | Contract terms | 99.9% uptime, 4-hour P1 response time | Automated from support/platform data |
| Feature commitment | Sales or CS conversation | "Feature X will be available by Q2" | Manual logging, tracked against product roadmap |
| Action item | Call or meeting | "I will send you the benchmark report by Friday" | Manual logging by CSM or extracted from call transcripts |
| Response commitment | Email or ticket | "I will get back to you within 24 hours" | Automated from email/ticket timestamps |
| Escalation commitment | Escalation process | "Engineering will have a fix within 5 business days" | Manual logging, tracked against internal team |

## Core Execution Logic

### Step 1: Capture Commitments

Commitments enter the system through three channels:

**Automated capture:**
- Support ticket SLAs (response time, resolution time) from support platform
- Contractual SLAs from contract terms in CRM
- Action items extracted from call transcripts (if NLP extraction is available)

**Semi-automated capture:**
- Post-call summary parsing: when the CSM generates a call summary, the skill identifies action items with owners and deadlines
- Email parsing: detect commitment language ("I will," "we will," "by [date]") in outbound CSM emails

**Manual capture:**
- CSM logs a commitment directly (account, description, owner, deadline)

### Step 2: Track Against Deadlines

For each active commitment:
1. Calculate days remaining to deadline
2. Classify status:

| Status | Criteria |
|--------|----------|
| On track | Deadline >3 days away, no indicators of delay |
| Due soon | Deadline within 3 business days |
| At risk | Deadline within 1 business day and no evidence of completion |
| Overdue | Past deadline, not marked as complete |
| Completed | Owner confirms delivery or automated detection confirms fulfilment |

### Step 3: Alert on Upcoming Deadlines

| Alert | When | To Whom |
|-------|------|---------|
| Reminder | 3 business days before deadline | Commitment owner (CSM or internal team) |
| Urgent | 1 business day before deadline, if not yet complete | Commitment owner + CSM (if owner is not the CSM) |
| Breach | Deadline passes without completion | CSM + manager. Include commitment details, customer, and elapsed time |

### Step 4: Maintain Accountability Record

For each account, maintain a running record of all commitments:
- Total commitments made (trailing 90 days)
- Completion rate (% delivered on time)
- Average time to fulfil
- Most common breach type (if any)
- Overdue items (currently open)

This record feeds into QBR preparation, renewal assessment, and escalation context.

## Output Format

**Active commitment record (per account):**
```json
{
  "account_id": "string",
  "active_commitments": [
    {
      "id": "commit-001",
      "description": "Send benchmark report comparing account usage to segment peers",
      "owner": "Jane Doe (CSM)",
      "created": "2026-03-07",
      "deadline": "2026-03-14",
      "status": "on_track",
      "source": "QBR call on 2026-03-07",
      "days_remaining": 4
    },
    {
      "id": "commit-002",
      "description": "Engineering fix for API latency issue",
      "owner": "Engineering (via escalation)",
      "created": "2026-02-28",
      "deadline": "2026-03-10",
      "status": "at_risk",
      "source": "Escalation TICKET-4521",
      "days_remaining": 0
    }
  ],
  "accountability_summary": {
    "commitments_90d": 12,
    "completed_on_time": 10,
    "completion_rate": 0.83,
    "currently_overdue": 0,
    "currently_at_risk": 1
  }
}
```

**CSM commitment dashboard (weekly):**
```json
{
  "csm": "Jane Doe",
  "week_of": "2026-03-10",
  "due_this_week": 4,
  "at_risk": 1,
  "overdue": 0,
  "completion_rate_30d": 0.91,
  "accounts_with_overdue_items": [],
  "top_priority": {
    "account": "Acme Corp",
    "commitment": "Engineering fix for API latency",
    "deadline": "2026-03-10",
    "status": "at_risk"
  }
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| At-risk commitment (approaching deadline) | Commitment details, owner, customer context | Whether to push the owner, renegotiate the deadline with the customer, or escalate |
| Breached commitment | Breach details, customer impact, communication history | How to communicate the breach to the customer, what remediation to offer |
| Pattern of breaches on an account | Accountability record, breach history | Whether there is a systemic issue (over-promising, under-resourced, product gap) |
| Internal team not delivering | Commitment details, internal owner, days overdue | Whether to escalate internally, adjust the commitment, or find an alternative |

## Confidence and Limitations

- **High confidence** for deadline tracking and alerting -- deterministic calendar logic
- **Medium confidence** for automated commitment capture from call transcripts and emails -- NLP extraction may miss or misinterpret commitments
- **Low confidence** for commitments that were made verbally and never logged -- the system can only track what it knows about
- Cannot assess whether a completed commitment was delivered to the customer's satisfaction (only that it was delivered)
- Cannot prioritise between competing commitments when resources are limited -- that is a human judgment call

## Dependencies

**Required:**
- CRM API (commitment logging, account context)
- Calendar or task management integration (deadline tracking)

**Strongly recommended:**
- Support platform (for SLA tracking on tickets)
- Call transcript integration (for automated commitment extraction)
- Email integration (for commitment language detection)
- `bi-account-brief` (for customer context when a breach occurs)

## References

- `references/commitment-capture.md` -- Patterns for extracting commitments from different sources

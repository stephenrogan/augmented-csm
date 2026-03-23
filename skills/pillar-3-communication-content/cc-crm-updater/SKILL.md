---
name: cc-crm-updater
description: Automatically logs activities, updates CRM fields, and maintains data accuracy across the CRM by syncing information from email, calendar, call transcripts, and product analytics. Detects and flags data inconsistencies, stale records, and missing fields. Use when asked to update CRM records, auto-log activities, sync account data, maintain CRM hygiene, or automate CRM field updates. Also triggers for questions about CRM accuracy, activity logging automation, data sync between systems, CRM data quality, or field reconciliation.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: communication-content
  category: data-ops
---

# CRM Updater

Maintains CRM accuracy by automatically logging activities, updating fields, and syncing data from connected systems. The unglamorous but essential data hygiene layer that every other skill depends on -- health scores, engagement tracking, renewal forecasting, and reporting are all only as good as the CRM data underneath them.

This is a **data operations** skill. It writes structured data to the CRM. It does not make judgment calls about what data means -- it ensures the data is there, accurate, and current.

## When to Run

- **Continuous**: Syncs activities as they occur (email sent, call completed, ticket resolved, meeting held)
- **Scheduled**: Daily reconciliation pass to catch missed updates, flag inconsistencies, and report on data health
- **On-demand**: When a CSM requests a data refresh for a specific account

## Core Execution Logic

### Step 1: Auto-Log Activities from Connected Systems

As events occur across connected systems, log them to the CRM activity record:

| Source | Events Logged | Fields Written | Deduplication |
|--------|-------------|---------------|---------------|
| Email integration | Emails sent/received to customer contacts | Date, type (email), participants, subject, direction (inbound/outbound), thread ID | Match on thread ID + timestamp to prevent duplicates from sync delays |
| Calendar integration | Meetings held (completed only) | Date, type (meeting), attendees, duration, outcome placeholder | Match on calendar event ID |
| Calendar integration | Meetings cancelled or no-showed | Date, type (meeting_cancelled/no_show), attendees | Separate event type -- valuable signal |
| Call platform | Calls completed | Date, type (call), participants, duration, summary (from cc-call-summariser if available) | Match on platform call ID |
| Support platform | Tickets opened, escalated, resolved | Ticket ID, severity, status change, timestamp, CSAT (if collected) | Match on ticket ID + status |
| Product analytics | Key usage events (login, milestone, feature activation) | Event type, timestamp, user | Write weekly summary rather than individual events to avoid CRM bloat |

**Filtering rules**: Not everything should be logged. Automated marketing emails, system notifications, auto-replies, and background API calls are excluded. Only human-meaningful interactions create CRM activity records.

### Step 2: Update Account-Level Fields

Keep CRM fields current from upstream skill computations:

| Field | Source Skill | Update Frequency | Write Behaviour |
|-------|-------------|-----------------|-----------------|
| Health score | bi-health-score | Per computation cadence (daily or weekly) | Overwrite with latest score. Preserve score history for trend analysis |
| Health band | bi-health-score | On band change | Overwrite. Log the band change as an event |
| Lifecycle stage | lo-onboarding-orchestrator, lo-milestone-tracker | On stage transition | Overwrite on confirmed transitions only. Never regress without CSM approval |
| Last touch date | Activity log (most recent of any channel) | Continuous | Overwrite with most recent activity timestamp |
| Last touch channel | Activity log | Continuous | Overwrite with the channel of the most recent activity |
| Usage summary | bi-usage-monitor | Weekly | Snapshot of key usage metrics (DAU, feature count, session depth) |
| Active risk signals | bi-risk-detector | On signal change | Write current active signals. Clear resolved signals |
| Renewal date and status | Contract data | On change | Overwrite from contract source. Flag conflicts with CSM-entered dates |
| Primary contact / champion | ra-stakeholder-mapper | On classification change | Update with current champion. Log changes as events |
| Expansion signals | bi-expansion-detector | On signal change | Write active signals for pipeline visibility |

### Step 3: Reconciliation and Hygiene (Daily Pass)

Every day, scan the CRM for data health issues:

| Check | Detection Criteria | Action | Priority |
|-------|-------------------|--------|----------|
| Activity gap | No activity logged for an account in 30+ days | Flag to CSM: "No recorded activity for [account] in [X] days. Verify engagement is happening through channels not connected to the system, or investigate lapsed engagement" | High -- may indicate a relationship gap or a logging issue |
| Empty required fields | Health score, primary contact, lifecycle stage, or renewal date is blank | Flag to CS Ops with specific field, account, and suggested resolution | Medium -- downstream skills cannot function without these fields |
| Lifecycle stage conflict | CRM says "Onboarding" but product analytics show mature usage (90+ days of active use) | Flag to CSM: "Lifecycle stage may be incorrect. Account shows mature usage but is still classified as Onboarding" | Low -- does not affect health score but misrepresents the account |
| Stale field | A field that should update regularly (health score, usage summary) has not been updated beyond its expected refresh cadence | Flag to CS Ops: "Data source may be disconnected. [Field] for [account] last updated [date]" | Medium -- indicates an integration issue |
| Duplicate contacts | Same email address appears on multiple contact records | Flag to CS Ops for merge decision | Low -- but causes confusion if not resolved |
| Contact-account mismatch | A contact's email domain does not match the account's domain | Flag to CS Ops: may be a legitimate secondary domain or a mislinked contact | Low |
| Health-activity discrepancy | Account has healthy engagement metrics but health score is declining (or vice versa) | Flag to CSM for investigation. The health score may be correct (another component is driving the decline) or may need recalibration | Medium |

### Step 4: Protect CSM-Entered Data

Critical principle: the agent never silently overwrites data that a CSM has manually entered.

| Scenario | Behaviour |
|----------|----------|
| Agent computes a field value that differs from CSM-entered value | Flag the conflict. Present both values. CSM decides which is correct |
| Agent detects an activity the CSM already logged | Skip the duplicate. Do not create a second record |
| Agent wants to change lifecycle stage backward (e.g., from Adoption to Onboarding) | Block the change. Flag for CSM review. Stage regression is almost always an error |
| CSM manually overrides a health score | Preserve the override. On next computation cycle, flag if the computed score differs significantly from the override |

### Step 5: Generate Data Health Report

Daily summary for CS Ops, weekly summary for CS leadership:

```json
{
  "report_date": "2026-03-10",
  "activity_logging": {
    "activities_logged_today": 47,
    "by_channel": { "email": 22, "meeting": 8, "call": 5, "support": 7, "product_event": 5 },
    "duplicates_skipped": 3,
    "logging_errors": 0
  },
  "field_updates": {
    "fields_updated_today": 23,
    "health_scores_written": 42,
    "lifecycle_stage_changes": 1,
    "conflicts_flagged": 2
  },
  "reconciliation": {
    "accounts_scanned": 142,
    "accounts_with_flags": 5,
    "flags": [
      {
        "account": "Beta Inc",
        "flag": "activity_gap",
        "detail": "No recorded activity in 35 days. Last touch: email on Feb 3",
        "recommended_action": "CSM review -- verify engagement status",
        "priority": "high"
      },
      {
        "account": "Gamma Corp",
        "flag": "lifecycle_stage_conflict",
        "detail": "Stage is 'Onboarding' but account has 8 months of active usage",
        "recommended_action": "CSM or CS Ops update lifecycle stage to 'Active'",
        "priority": "low"
      }
    ]
  },
  "data_health_score": {
    "overall": 0.94,
    "by_dimension": {
      "activity_completeness": 0.97,
      "field_freshness": 0.95,
      "required_field_coverage": 0.91,
      "contact_accuracy": 0.93
    }
  }
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Reconciliation flags | Specific flag with evidence and recommended action | Whether the flag is a real data issue or a false positive. An activity gap may be a logging issue (CSM engaged via phone, not logged) or a real engagement lapse |
| Data conflicts | Both values (agent-computed and CSM-entered) with context | Which value is correct. The CSM has context the agent cannot see |
| Duplicate contact resolution | Both records with metadata | Which record to keep, how to merge, and whether the duplicate is a data entry error or a legitimate second contact |
| Stage regression | Current stage, proposed change, evidence | Whether the lifecycle stage should actually move backward (rare but possible after a product reset or contract restructure) |

## Confidence and Limitations

- **High confidence** for activity logging from structured sources (email, calendar, support) -- deterministic data writes with defined deduplication logic
- **High confidence** for field updates from upstream skills -- the agent writes what the skill computed. If the computation is wrong, that is the upstream skill's issue, not the CRM updater's
- **Medium confidence** for reconciliation flag relevance -- the flags are based on defined rules, but not every flag requires action. An activity gap on an SMB account with a quarterly cadence is expected, not concerning
- **Low confidence** for conflict resolution between agent-computed and CSM-entered values. The agent cannot determine which is correct -- it can only flag the discrepancy. The CSM decides
- Cannot log activities that happen outside connected systems. In-person meetings, phone calls not through the platform, Slack conversations, WhatsApp messages -- none of these appear unless the CSM logs them manually. This is a fundamental coverage gap that the reconciliation pass cannot fill
- Cannot ensure CSMs log their own observations and notes. The skill automates what is system-observable. The richest CRM data -- the CSM's qualitative assessment, relationship read, and strategic notes -- still requires human input

## Dependencies

**Required:**
- CRM API (read/write access to account, contact, activity, and custom field objects)

**Strongly recommended:**
- Email integration (for email activity logging)
- Calendar integration (for meeting logging)
- Call platform (for call logging)
- Support platform (for ticket event logging)
- All Book Intelligence skills (for field update sources)
- Product analytics (for usage event summaries)

**Downstream consumers:**
- Every skill that reads from CRM -- this skill ensures the data they consume is accurate and current
- bi-health-score, bi-risk-detector, bi-usage-monitor (depend on CRM field freshness)
- ra-engagement-tracker (depends on activity log completeness)
- lo-renewal-manager (depends on contract field accuracy)
- CS Ops (reconciliation flags and data quality metrics)
- CSMs (stale data and conflict alerts)

## References

- `references/sync-rules.md` -- Activity logging rules, field update policies, deduplication logic, and conflict resolution procedures

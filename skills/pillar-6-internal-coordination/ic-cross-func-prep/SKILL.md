---
name: ic-cross-func-prep
description: Prepares materials for internal cross-functional meetings including account reviews, pipeline reviews, escalation committees, and CS-product syncs. Compiles relevant account data tailored to each meeting's audience and purpose. Use when asked to prepare for an internal meeting, build an account review deck, compile data for a pipeline review, create materials for a CS-product sync, or when any internal meeting needs structured account data. Also triggers for questions about internal meeting preparation, cross-functional review materials, team sync documentation, or pipeline review content.
license: MIT
metadata:
  version: "1.0.0"
  pillar: internal-coordination
  category: coordination-engine
---

# Cross-Functional Prep

Prepares materials for internal meetings by compiling relevant account data tailored to the meeting type and audience. Part of the Internal Coordination pillar.

This is a **data compilation and formatting** skill. It assembles the right data for the right audience in the right format. The CSM or manager adds narrative, priorities, political awareness, and strategic framing.

## When to Run

- **Triggered**: By calendar integration when a recurring internal meeting is approaching (24 hours before)
- **On-demand**: When a CSM or manager requests materials for a specific meeting
- **Scheduled**: Weekly for recurring meetings (manager 1:1s, pipeline reviews)

## Core Execution Logic

### Step 1: Identify Meeting Type and Audience

Determine from the calendar event or request:

| Meeting Type | Primary Audience | Data Focus | Typical Cadence |
|-------------|-----------------|-----------|-----------------|
| Manager 1:1 / account review | CSM + their manager | Portfolio health, specific accounts to discuss, open items, CSM metrics | Weekly |
| Pipeline / renewal review | CS leadership + CRO | Renewal forecast, at-risk accounts, expansion pipeline, churn post-mortems | Weekly or bi-weekly |
| CS-product sync | CS leadership + Product management | Feature request themes, adoption blockers, product-correlated churn, release impact | Bi-weekly or monthly |
| Escalation committee | Cross-functional leadership | Active escalations, blocked items, resource requests | Weekly |
| Quarterly business review (internal) | CS leadership + executive team | NRR, churn analysis, expansion, segment trends, strategic priorities | Quarterly |

### Step 2: Pull Data by Meeting Type

**Manager 1:1 / Account Review:**

| Data Element | Source | Purpose |
|-------------|--------|---------|
| Portfolio health distribution | bi-health-score | Overview of the CSM's book health |
| Top risk accounts (3-5) | bi-risk-detector | Accounts that need manager awareness |
| Expansion pipeline | bi-expansion-detector | Revenue opportunities in progress |
| Overdue items | lo-sla-monitor | Commitments at risk or breached |
| Touchpoint cadence compliance | lo-check-in-scheduler | Is the CSM maintaining expected cadence? |
| Milestone progress | lo-milestone-tracker | Are accounts on track against plans? |
| Action items from last 1:1 | CRM or meeting notes | Follow-through on prior commitments |
| CSM-selected accounts | CSM input | Specific accounts the CSM wants to discuss (with bi-account-brief for each) |

**Pipeline / Renewal Review:**

| Data Element | Source | Purpose |
|-------------|--------|---------|
| Renewal forecast | cm-renewal-forecaster | NRR projection with confidence intervals |
| At-risk accounts | bi-risk-detector + lo-renewal-manager | Accounts with renewal risk, sorted by ARR and urgency |
| Intervention status | CSM input + CRM | What is being done about at-risk accounts |
| Expansion pipeline | bi-expansion-detector + CRM opportunities | Active expansion deals with stage and probability |
| Recent churn | CRM | Accounts lost this period with root cause summary |
| Churn post-mortems | churn-post-mortem records | Lessons from recent losses |
| Period-over-period trend | cm-renewal-forecaster | Is the forecast improving or deteriorating? |

**CS-Product Sync:**

| Data Element | Source | Purpose |
|-------------|--------|---------|
| Top feature request themes | pa-feedback-aggregator | What customers are asking for, weighted by breadth and ARR |
| Adoption blockers | pa-adoption-tracker | Features that are widely available but poorly adopted -- may indicate product issues |
| Product-correlated churn | pa-feedback-aggregator + churn data | Features whose absence was cited in churn post-mortems |
| Upcoming release impact | Product roadmap | Which customers will be affected by upcoming changes, positively or negatively |
| Open feature requests by status | ic-feature-request-tracker | What has been acknowledged, planned, or declined |

**Escalation Committee:**

| Data Element | Source | Purpose |
|-------------|--------|---------|
| Active escalations | ic-escalation-router | All open escalations with status, age, and owner |
| Stalled escalations | ic-escalation-router | Escalations with no progress beyond SLA |
| Blocked escalations | ic-escalation-router + CSM input | Escalations that need cross-functional decision to unblock |
| Resource requests | CSM input | Cases where the CSM needs engineering, product, or executive time |
| Resolution rate | ic-escalation-router | Trend data on how quickly escalations are being resolved |

### Step 3: Format for Audience

**Formatting principles by audience:**

| Audience | Wants to See | Does Not Want to See |
|----------|-------------|---------------------|
| CSM manager | Specific accounts, CSM judgment, relationship context | Portfolio-level financials, board metrics |
| CRO/CFO | Revenue at risk, NRR trajectory, financial impact | Individual account details unless asked |
| Product team | Usage data, feature requests, adoption patterns | Revenue data, commercial context (unless relevant to prioritisation) |
| Cross-functional leadership | Escalation status, blockers, resource needs | Detailed account history, CSM-level metrics |
| Executive team | Portfolio trends, NRR, strategic outlook | Operational details, individual escalations |

### Step 4: Deliver 24 Hours Before

- Generate the materials package
- Deliver to the meeting organiser (or all attendees if configured)
- Include a one-line summary of what is new or changed since the last meeting of this type
- Flag any items that require a decision in the meeting (not just awareness)

### Step 5: Post-Meeting Action Capture

After the meeting (if CSM provides notes):
- Extract action items from meeting notes
- Route to lo-sla-monitor for commitment tracking
- Update CRM records as needed
- Set reminders for follow-up items

## Output Format

```json
{
  "meeting_id": "mtg-2026-weekly-pipeline-w10",
  "meeting_type": "pipeline_review",
  "date": "2026-03-11T10:00:00Z",
  "prepared_for": "CS Leadership + CRO",
  "generated": "2026-03-10T10:00:00Z",
  "materials": {
    "renewal_forecast": {
      "source": "cm-renewal-forecaster",
      "headline": "NRR forecast 95.6% for next 90 days. Down 0.3% from last week",
      "detail_included": true
    },
    "at_risk_accounts": {
      "source": "bi-risk-detector + lo-renewal-manager",
      "count": 4,
      "total_arr_at_risk": 340000,
      "accounts": [
        {
          "name": "Acme Corp",
          "arr": 85000,
          "renewal_days": 66,
          "classification": "at_risk",
          "top_risk": "Champion departed, usage declining",
          "intervention": "New stakeholder identified, outreach scheduled this week"
        }
      ]
    },
    "expansion_pipeline": {
      "source": "bi-expansion-detector + CRM",
      "count": 6,
      "total_pipeline_value": 180000,
      "new_this_week": 1
    },
    "churn_this_period": {
      "count": 0,
      "arr_lost": 0
    }
  },
  "decisions_needed": [
    "Acme Corp: approve executive engagement for at-risk renewal (CSM requesting VP-to-VP call)"
  ],
  "changed_since_last_meeting": [
    "Acme Corp moved from Watch to At Risk (champion departed)",
    "Delta Corp expansion signal surfaced ($45k opportunity)"
  ]
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Account selection | Top accounts by risk, expansion, or escalation | Which specific accounts to spend time on in the meeting -- not everything gets discussed |
| Narrative framing | Data summary with period-over-period changes | The story behind the numbers. "NRR is down 0.3%" needs human context: is this a trend or a blip? |
| Decision items | Flagged items requiring meeting decision | Whether to approve executive engagement, reallocate resources, change strategy |
| Political awareness | Data only -- no political context | What to raise vs. what to handle offline. Some topics are better addressed in a side conversation |
| Post-meeting actions | Extracted action items | Confirmation that the captured actions are accurate and appropriately assigned |

## Confidence and Limitations

- **High confidence** for data compilation -- pulling from defined sources with structured output is deterministic
- **High confidence** for meeting-type matching -- the rules for which data goes to which meeting are defined
- **Medium confidence** for "changed since last meeting" detection -- requires access to prior meeting's data state, which depends on data retention
- **Low confidence** for determining what matters most in each specific meeting. The data shows what has changed, but the meeting organiser knows what the audience cares about this week. A data change that is statistically significant may be operationally irrelevant, and vice versa
- Cannot prioritise which accounts to discuss -- that is the meeting organiser's judgment
- Cannot navigate internal dynamics -- knowing which topics to raise in a group setting vs. offline is pure human judgment
- Materials are prepared 24 hours before. Last-minute changes (account churning the day before a pipeline review) may not be captured. The CSM should add real-time context

## Dependencies

**Required:**
- Calendar integration (meeting detection and timing)
- CRM API (account data, ownership)
- bi-account-brief (account context for any account discussed in detail)

**Meeting-type specific:**
- Pipeline review: cm-renewal-forecaster, bi-risk-detector, bi-expansion-detector
- CS-product sync: pa-feedback-aggregator, pa-adoption-tracker, ic-feature-request-tracker
- Escalation committee: ic-escalation-router
- Manager 1:1: lo-check-in-scheduler, lo-sla-monitor, lo-milestone-tracker, bi-health-score

**Downstream consumers:**
- lo-sla-monitor (post-meeting action items)
- CRM (meeting record and outcomes)

## References

- `references/meeting-prep-templates.md` -- Detailed templates for each meeting type with formatting guidelines

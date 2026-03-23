---
name: lo-onboarding-orchestrator
description: Manages the customer onboarding workflow from sales handoff through first-value milestone. Sequences tasks, triggers communications, tracks completion, and flags delays. Use when asked to set up onboarding for a new customer, track onboarding progress, build onboarding workflows, automate onboarding sequences, manage customer go-live, monitor time-to-value, or when any new account needs to be moved through a structured activation process. Also triggers for questions about onboarding playbooks, kickoff coordination, or implementation tracking.
license: MIT
metadata:
  version: "1.0.0"
  pillar: lifecycle-orchestration
  category: workflow-engine
---

# Onboarding Orchestrator

Manages the end-to-end onboarding workflow for new customers. Sequences tasks, triggers milestone-based communications, tracks completion against timeline, and flags delays or blockers for human intervention. Part of the Lifecycle Orchestration pillar -- the highest-volume workflow in most CS organisations.

This is an **execution and tracking** skill. It runs the onboarding process -- scheduling tasks, sending templated communications, updating CRM fields, and monitoring progress. It hands off to the human at defined decision points: when the customer deviates from the expected path, when a blocker requires judgment, or when the kickoff call needs to be led.

## When to Run

- **Triggered**: When a new deal closes and the handoff from sales is initiated (CRM opportunity stage = Closed Won)
- **Continuous**: Once activated for an account, runs until the onboarding workflow reaches the "first-value milestone" or is manually closed
- **On-demand**: When a CSM requests onboarding status or needs to reset/restart an onboarding workflow

## Onboarding Workflow Structure

The onboarding workflow is a sequence of phases, each containing tasks with defined triggers, owners, and completion criteria. The skill executes AGENT tasks automatically and surfaces HUMAN tasks with context and deadlines.

### Phase 1: Handoff and Setup (Days 0-3)

| Task | Operator | Trigger | Completion Criteria |
|------|----------|---------|-------------------|
| Generate handoff brief from sales data | AGENT | Deal closes | Brief created with deal context, customer expectations, technical requirements, key contacts |
| Create onboarding project in CRM | AGENT | Deal closes | Project record created with all fields populated, timeline set |
| Send welcome email to primary contact | AGENT | Handoff brief approved by CSM | Email sent using segment-appropriate template with personalisation |
| Schedule kickoff call | AGENT | Welcome email sent | Calendar invite sent to customer contacts + CSM + relevant internal stakeholders |
| Prepare kickoff deck | AGENT | Kickoff call scheduled | Deck generated with account context, agenda, expected outcomes, timeline |
| Lead kickoff call | HUMAN | Call scheduled | CSM leads the call, sets expectations, confirms goals and timeline |

### Phase 2: Technical Activation (Days 3-14)

| Task | Operator | Trigger | Completion Criteria |
|------|----------|---------|-------------------|
| Provision account and configure environment | AGENT | Kickoff complete | Account provisioned per technical requirements from handoff brief |
| Send configuration guide to customer | AGENT | Environment provisioned | Guide sent with step-by-step instructions tailored to customer's use case |
| Track configuration completion | AGENT | Guide sent | Monitor product analytics for configuration milestones; flag if incomplete after 5 business days |
| Send check-in email at Day 7 | AGENT | Day 7 from kickoff | Templated check-in asking about configuration progress, offering help |
| Resolve configuration blockers | HUMAN | Blocker flagged by tracking or customer | CSM investigates and resolves -- may involve support, product, or direct guidance |

### Phase 3: Adoption and First Value (Days 14-45)

| Task | Operator | Trigger | Completion Criteria |
|------|----------|---------|-------------------|
| Track first use-case completion | AGENT | Configuration complete | Monitor product analytics for core workflow execution; flag if no activity after 7 days |
| Send adoption tips email sequence | AGENT | First login detected | 3-email sequence over 14 days: getting started, advanced tips, success stories |
| Schedule 30-day check-in call | AGENT | Day 25 from kickoff | Calendar invite to primary contact + CSM |
| Generate 30-day progress report | AGENT | Day 28 from kickoff | Report with usage metrics vs. onboarding plan, adoption milestones hit/missed |
| Lead 30-day review call | HUMAN | Call scheduled | CSM reviews progress, adjusts adoption plan, identifies expansion of scope |
| Declare first-value milestone | HUMAN | Evidence of value realisation | CSM confirms the customer has achieved their primary use case. Onboarding complete |

### Phase 4: Transition to Steady State (Days 45-60)

| Task | Operator | Trigger | Completion Criteria |
|------|----------|---------|-------------------|
| Update account lifecycle stage in CRM | AGENT | First-value declared | Stage changed from "Onboarding" to "Adopted" |
| Generate onboarding summary | AGENT | Stage change | Summary document: timeline, milestones, blockers encountered, CSM notes |
| Transition to steady-state check-in cadence | AGENT | Stage change | Onboarding cadence deactivated; steady-state cadence activated via lo-check-in-scheduler |
| Send onboarding completion email | AGENT | Stage change | Email to customer confirming successful onboarding, introducing ongoing support model |

See `references/onboarding-templates.md` for all email templates and deck formats referenced above.

## Delay Detection and Escalation

The skill monitors elapsed time at every task and flags delays:

| Delay Condition | Action |
|----------------|--------|
| Task not completed within expected timeframe + 2 business days | Internal flag to CSM: "Task [X] is overdue by [N] days" |
| Customer-dependent task stalled for 5+ business days | Automated nudge email to customer (configurable, can be disabled) |
| Phase not completed within expected timeframe + 5 business days | Escalation flag to CSM + manager: "Onboarding for [account] is behind schedule" |
| No product activity detected 10+ days post-kickoff | Alert CSM: "No usage detected -- investigate whether technical blocker exists" |

Delay detection is automated. Delay resolution is HUMAN -- the CSM decides whether to push, adjust the timeline, or escalate.

## Output Format

**Onboarding status record (per account):**
```json
{
  "account_id": "string",
  "onboarding_start": "2026-03-01",
  "current_phase": "phase_2_technical_activation",
  "days_in_onboarding": 10,
  "expected_completion": "2026-04-15",
  "tasks_completed": 8,
  "tasks_remaining": 7,
  "tasks_overdue": 1,
  "overdue_details": [
    { "task": "Configuration completion", "expected_by": "2026-03-08", "days_overdue": 2, "owner": "customer" }
  ],
  "next_agent_action": { "task": "Send Day 7 check-in email", "scheduled": "2026-03-08" },
  "next_human_action": { "task": "Resolve configuration blocker", "urgency": "this_week" },
  "health_indicators": {
    "product_activity_detected": true,
    "customer_responsive": true,
    "on_track": false,
    "risk_level": "low"
  }
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Kickoff call | Handoff brief, deck, customer expectations | How to frame the engagement, which goals to prioritise |
| Configuration blocker | Blocker details, days stalled, customer communications | Whether to troubleshoot directly, involve support, or adjust scope |
| 30-day review | Progress report, usage data, milestone status | Whether onboarding is on track, whether to adjust the plan |
| First-value declaration | Usage evidence, customer feedback, adoption metrics | Whether the customer has achieved sufficient value to transition to steady state |
| Onboarding at risk | Delay escalation data, customer engagement pattern | Whether to extend onboarding, escalate internally, or accept the pace |

## Confidence and Limitations

- **High confidence** for task sequencing, scheduling, and tracking -- these are deterministic workflows
- **Medium confidence** for delay detection -- the system knows tasks are late but not why
- Cannot assess whether the customer is satisfied with the onboarding experience (that requires human interaction)
- Cannot adapt the onboarding plan to customer-specific circumstances without human input (e.g., customer wants to skip Phase 2 because they have internal technical resources)
- Template communications work for standard onboarding. Complex enterprise onboarding may require fully custom communications written by the CSM

## Dependencies

**Required:**
- CRM API (deal data for handoff, project tracking, lifecycle stage management)
- Calendar integration (scheduling kickoff and check-in calls)
- Email integration (sending templated communications)
- Product analytics (tracking configuration completion, first usage, adoption milestones)

**Optional:**
- `lo-handoff-manager` (for generating the sales-to-CS handoff brief)
- `bi-health-score` (for onboarding health indicators)
- `lo-milestone-tracker` (for detailed milestone tracking beyond the onboarding scope)
- Document generation (for kickoff decks and progress reports)

## References

- `references/onboarding-templates.md` -- Email templates, deck structure, and report formats
- `references/segment-variations.md` -- How the onboarding workflow adapts by segment (enterprise vs. mid-market vs. SMB)

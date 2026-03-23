---
name: lo-milestone-tracker
description: Tracks customer progress against defined adoption and lifecycle milestones, flags blockers, and reports on time-to-milestone metrics. Use when asked to track customer milestones, monitor adoption progress, measure time-to-value, build success plans with measurable checkpoints, identify stalled accounts, report on adoption velocity, or when any workflow needs to know whether a customer is on track against their plan. Also triggers for questions about success planning, goal tracking, outcome measurement, or adoption milestones.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: lifecycle-orchestration
  category: workflow-engine
---

# Milestone Tracker

Tracks customer progress against defined adoption and lifecycle milestones. Flags blockers, measures time-to-milestone, and reports on adoption velocity. Operates across the full lifecycle, not just onboarding -- milestones exist from first login through mature expansion.

This is a **tracking and alerting** skill. It monitors progress against defined checkpoints and surfaces deviations. It does not define the milestones (that is a joint human exercise with the customer) or resolve blockers (that is human judgment).

## When to Run

- **Continuous**: Monitors all accounts with active milestone plans against product analytics and CRM data
- **Triggered**: When product analytics detects a milestone completion event or when an expected milestone date passes without completion
- **On-demand**: When a CSM requests milestone status for a specific account

## Milestone Framework

### Milestone Types

| Type | Definition | Example |
|------|-----------|---------|
| Activation | First meaningful use of the product | First workflow completed, first report generated |
| Adoption | Sustained use of core capabilities | 80% of team logging in weekly for 4 consecutive weeks |
| Depth | Advanced feature or use case adoption | Second use case live, API integration active |
| Outcome | Business result achieved through the product | 20% reduction in manual process time, measurable ROI |
| Expansion | Growth beyond initial scope | New department onboarded, tier upgrade, additional product |

### Milestone Plans

Each account can have a milestone plan -- a set of defined milestones with target dates and success criteria. Plans can be:
- **Template-based**: Generated from segment defaults (e.g., all mid-market accounts get the standard adoption plan)
- **Custom**: Defined collaboratively by the CSM and customer during onboarding or QBR

## Core Execution Logic

### Step 1: Define or Load Milestone Plan

For each account:
1. Check if a custom milestone plan exists in CRM
2. If yes: load the plan with milestones, target dates, and success criteria
3. If no: apply the segment-default template (see `references/milestone-templates.md`)
4. Each milestone has: name, type, target date, success criteria (measurable), detection method (how the system knows it happened)

### Step 2: Monitor Progress

For each active milestone:
1. Query the appropriate data source for the milestone's detection criteria
2. Classify status: **Completed** (criteria met), **On Track** (not yet due, progress visible), **At Risk** (due within 14 days, no progress), **Overdue** (past due date, criteria not met), **Blocked** (CSM has flagged a specific blocker)

Detection methods by milestone type:

| Detection Source | Milestones Detected |
|-----------------|-------------------|
| Product analytics | Activation (first use), Adoption (usage thresholds), Depth (feature usage) |
| CRM data | Expansion (opportunity stage), custom milestones logged by CSM |
| Customer confirmation | Outcome milestones (business results -- requires CSM to confirm with customer) |

### Step 3: Flag Deviations

| Condition | Action |
|-----------|--------|
| Milestone at risk (due in 14 days, no progress) | Alert CSM: "Milestone [X] is due in [N] days with no progress detected" |
| Milestone overdue (past due, not complete) | Alert CSM + include in overdue report: "Milestone [X] is [N] days overdue" |
| Milestone completed ahead of schedule | Log completion, notify CSM (positive signal -- may indicate readiness for acceleration) |
| No milestone progress across the entire plan for 30+ days | Alert CSM: "No milestone progress for [account] in 30 days -- investigate stall" |

### Step 4: Measure Time-to-Milestone

For completed milestones, track:
- Actual completion date vs. target date (ahead, on time, late)
- Time from prior milestone to this milestone (velocity)
- Comparison to segment benchmark (how fast vs. peers)

### Step 5: Generate Milestone Report

**Per-account milestone status:**
```json
{
  "account_id": "string",
  "plan_type": "custom",
  "milestones": [
    {
      "name": "Core workflow live",
      "type": "activation",
      "target_date": "2026-03-15",
      "status": "completed",
      "completed_date": "2026-03-10",
      "days_ahead": 5
    },
    {
      "name": "80% team adoption",
      "type": "adoption",
      "target_date": "2026-04-15",
      "status": "on_track",
      "progress_indicator": "62% of team active, trending up"
    },
    {
      "name": "ROI measurement",
      "type": "outcome",
      "target_date": "2026-06-15",
      "status": "not_started",
      "progress_indicator": "Requires customer input -- not yet requested"
    }
  ],
  "overall_velocity": "ahead_of_plan",
  "next_milestone_due": { "name": "80% team adoption", "due": "2026-04-15", "days_remaining": 36 }
}
```

**Portfolio milestone report (weekly):**
- Milestones completed this week (by account and type)
- Milestones overdue (by account, days overdue, blocker if known)
- Stalled accounts (no progress in 30+ days)
- Time-to-milestone benchmarks (average by type and segment)

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Milestone plan creation | Segment template, customer goals from onboarding | Which milestones to set, what timelines are realistic, how to define success criteria |
| At-risk milestone | Milestone details, progress data, last touchpoint | Whether to intervene proactively, adjust the timeline, or investigate the blocker |
| Overdue milestone | Overdue details, account health, engagement data | Whether to push the customer, adjust the plan, escalate, or accept the delay |
| Stalled account | 30-day stall, usage data, last CSM interaction | Root cause investigation -- is this disengagement, a priority shift, or a technical blocker? |
| Outcome milestone confirmation | Usage data, suggested outcomes | Whether the customer has actually achieved the business result (requires customer conversation) |

## Confidence and Limitations

- **High confidence** for activation and adoption milestones detected via product analytics -- measurable and objective
- **Medium confidence** for progress estimation on milestones not yet due (trending indicators)
- **Low confidence** for outcome milestones -- business results require customer confirmation, not just usage data
- Cannot detect blockers that exist outside observable data (e.g., customer's internal priority shifted, budget was reallocated)
- Template-based plans may not fit every account. Custom plans require CSM effort to define but produce more meaningful tracking

## Dependencies

**Required:**
- Product analytics (for activation and adoption milestone detection)
- CRM API (milestone plan storage, status tracking)

**Strongly recommended:**
- `lo-onboarding-orchestrator` (for onboarding milestone handoff)
- `bi-usage-monitor` (for progress indicators on usage-based milestones)
- `bi-health-score` (for health context on stalled accounts)

## References

- `references/milestone-templates.md` -- Segment-default milestone plan templates

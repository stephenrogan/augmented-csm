---
name: lo-check-in-scheduler
description: Schedules and triggers recurring customer touchpoint cadences based on lifecycle stage, segment, health status, and engagement history. Use when asked to set up check-in cadences, manage touchpoint schedules, automate customer outreach timing, build engagement rhythms, adjust call frequency based on account health, or when any account needs a structured recurring touchpoint schedule. Also triggers for questions about touchpoint cadence, engagement frequency, call scheduling automation, or proactive outreach timing.
license: MIT
metadata:
  version: "1.0.0"
  pillar: lifecycle-orchestration
  category: workflow-engine
---

# Check-In Scheduler

Manages the recurring touchpoint cadence for all accounts post-onboarding. Determines when each account should be contacted, what type of touchpoint is appropriate, schedules it, and tracks completion. Adapts cadence dynamically based on health status, lifecycle stage, and engagement patterns.

This is an **execution and scheduling** skill. It determines cadence, sends calendar invites, triggers pre-meeting preparation, and flags missed touchpoints. It does not determine what to discuss -- that is human judgment informed by other skills (Account Brief, Risk Detector, Expansion Detector).

## When to Run

- **Triggered**: When an account transitions from onboarding to steady state (lifecycle stage = "Adopted")
- **Continuous**: Runs perpetually for all active accounts, evaluating cadence rules and scheduling next touchpoints
- **On-demand**: When a CSM requests a cadence adjustment or a manual scheduling override

## Cadence Rules Engine

The cadence for each account is determined by a rules engine that evaluates multiple factors:

### Base Cadence by Segment

| Segment | Default Cadence | Touchpoint Type |
|---------|----------------|-----------------|
| Enterprise | Every 2 weeks | Call or meeting |
| Mid-Market | Monthly | Call or meeting |
| SMB (managed) | Quarterly | Call or email check-in |
| SMB (scaled) | No scheduled cadence -- event-triggered only | Automated email |

### Dynamic Adjustments

The base cadence is adjusted based on account conditions:

| Condition | Adjustment | Rationale |
|-----------|-----------|-----------|
| Health score < 65 | Increase frequency by 1 tier (e.g., monthly becomes bi-weekly) | At-risk accounts need more attention |
| Health score > 85 and stable | Decrease frequency by 1 tier (e.g., bi-weekly becomes monthly) | Strong accounts need less hand-holding |
| Active risk signal (severity 4+) | Override to weekly until signal resolves | Urgent situations need rapid touchpoint |
| Expansion signal active | Add a dedicated expansion touchpoint within 14 days | Opportunity needs timely commercial conversation |
| Renewal within 90 days | Increase frequency by 1 tier | Pre-renewal period requires closer engagement |
| Customer unresponsive (2+ missed/declined) | Pause scheduling, alert CSM | Do not keep scheduling into the void -- human decides approach |

### Cadence Tiers

| Tier | Frequency | Calendar Scheduling |
|------|-----------|-------------------|
| Weekly | Every 7 days | Fixed recurring invite |
| Bi-weekly | Every 14 days | Fixed recurring invite |
| Monthly | Every 30 days | Individual invites, flexible on exact date |
| Quarterly | Every 90 days | Individual invites, aligned to QBR cycle |
| Event-triggered | No fixed schedule | Triggered by specific conditions (health drop, milestone, etc.) |

## Core Execution Logic

### Step 1: Evaluate Cadence for Each Account

For each active account:
1. Determine base cadence from segment
2. Check dynamic adjustment conditions (health, risk, expansion, renewal proximity)
3. Apply the highest-priority adjustment (risk override > renewal increase > health adjustment > base)
4. Output: target cadence tier for this account

### Step 2: Schedule Next Touchpoint

1. Check when the last touchpoint occurred (from CRM activity log)
2. Calculate the next touchpoint date based on cadence tier
3. If a recurring invite exists and cadence has not changed: no action needed
4. If cadence has changed or no invite exists: propose a time slot based on CSM and customer calendar availability
5. Send calendar invite with standard agenda placeholder

### Step 3: Trigger Pre-Meeting Preparation

48 hours before a scheduled touchpoint:
1. Invoke `bi-account-brief` to generate a fresh account brief
2. Surface the brief to the CSM with the meeting context (pre-call format)
3. Flag any new signals that have emerged since the last touchpoint
4. If the touchpoint is a QBR, invoke `lo-qbr-orchestrator` instead

### Step 4: Track Completion

After the scheduled touchpoint time:
1. Check if the meeting occurred (calendar status: completed, cancelled, no-show)
2. If completed: log the touchpoint, reset the cadence timer
3. If cancelled by customer: log the cancellation, do not immediately reschedule (let the CSM decide)
4. If no-show: flag to CSM. If this is the 2nd consecutive no-show, trigger the "customer unresponsive" adjustment

### Step 5: Generate Cadence Report

Weekly summary for each CSM:
- Upcoming touchpoints this week (with account brief links)
- Overdue touchpoints (scheduled but not yet completed)
- Cadence changes (accounts that moved to a different tier this week, with reason)
- Unresponsive accounts (paused cadences awaiting CSM decision)

## Output Format

**Per-account cadence record:**
```json
{
  "account_id": "string",
  "current_cadence_tier": "monthly",
  "base_cadence": "monthly",
  "active_adjustments": ["renewal_within_90_days"],
  "adjusted_cadence": "bi-weekly",
  "last_touchpoint": "2026-02-15",
  "next_touchpoint": "2026-03-01",
  "next_touchpoint_type": "call",
  "prep_status": "brief_generated",
  "missed_consecutive": 0
}
```

**CSM weekly cadence report:**
```json
{
  "csm": "Jane Doe",
  "week_of": "2026-03-10",
  "scheduled_touchpoints": 12,
  "overdue_touchpoints": 1,
  "cadence_changes": [
    { "account": "Acme Corp", "from": "monthly", "to": "bi-weekly", "reason": "Renewal within 90 days" }
  ],
  "paused_accounts": [
    { "account": "Beta Inc", "reason": "2 consecutive no-shows", "paused_since": "2026-02-28" }
  ]
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Customer unresponsive (2+ missed) | Missed touchpoint history, health data, last communication | How to re-engage: different channel, different contact, escalation, or accept the pattern |
| Cadence override request | Current cadence, health data, recent signals | Whether to manually set a different cadence than the rules engine recommends |
| Touchpoint content and approach | Account brief, signals, last interaction summary | What to discuss, what to propose, how to frame the conversation |

## Confidence and Limitations

- **High confidence** for scheduling mechanics -- cadence rules are deterministic
- **Medium confidence** for dynamic adjustments -- the health-based rules are sensible defaults but may need tuning per portfolio
- Cannot determine the best time of day or day of week for a specific customer (uses calendar availability as proxy)
- Cannot assess whether a touchpoint was productive (only whether it occurred)
- The "customer unresponsive" threshold (2 missed) is a default. Some segments tolerate more missed touchpoints before it is meaningful

## Dependencies

**Required:**
- CRM API (activity logging, lifecycle stage, segment data)
- Calendar integration (scheduling, availability checking, completion tracking)
- `bi-health-score` (for health-based cadence adjustments)

**Strongly recommended:**
- `bi-risk-detector` (for risk-based cadence override)
- `bi-expansion-detector` (for expansion touchpoint injection)
- `bi-account-brief` (for pre-meeting preparation)
- `lo-qbr-orchestrator` (for QBR-specific preparation)

## References

- `references/cadence-rules.md` -- Full cadence rule definitions and customisation guidance

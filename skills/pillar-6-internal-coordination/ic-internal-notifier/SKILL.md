---
name: ic-internal-notifier
description: Sends automated status updates and notifications to internal stakeholders when account events occur. Keeps product, support, sales, and leadership informed without requiring the CSM to manually update each team. Use when asked to set up internal notifications, automate status updates, keep cross-functional teams informed about account changes, or when any account event should trigger an internal communication. Also triggers for questions about internal communication automation, cross-team updates, stakeholder notification, or event-driven alerting.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: internal-coordination
  category: coordination-engine
---

# Internal Notifier

Automates internal notifications when account events occur. Keeps cross-functional teams informed without CSM manual effort. Part of the Internal Coordination pillar.

This is an **event-driven notification** skill. It sends structured updates to defined recipients when specific triggers fire. It does not make decisions about what to communicate -- it executes a notification ruleset.

## When to Run

- **Event-driven**: Fires when a defined trigger condition is met (from any pillar skill)
- **Scheduled**: Daily digest of account status changes for configured recipients
- **On-demand**: When a CSM requests a manual notification to a specific internal audience

## Core Execution Logic

### Step 1: Monitor Event Streams

Listen for events from all pillar skills:

| Event Source | Events Monitored |
|-------------|-----------------|
| bi-health-score | Score drops below threshold, rapid decline, band change |
| bi-risk-detector | New risk signal, signal escalation, signal cluster |
| bi-expansion-detector | New expansion signal surfaced |
| bi-competitive-intel | Competitive signal detected |
| ra-stakeholder-change-detector | Champion departure, executive change, new hire |
| lo-renewal-manager | Renewal risk classification change |
| lo-sla-monitor | Commitment at risk of breach, commitment breached |
| lo-milestone-tracker | Milestone missed, milestone achieved ahead of schedule |
| lo-onboarding-orchestrator | Onboarding delay, onboarding complete |
| ic-escalation-router | Escalation status change, escalation stalled |
| Support platform | P1 ticket opened, ticket SLA breached |
| CRM | Account churned, account renewed, expansion closed |

### Step 2: Match Against Notification Rules

Each event maps to a notification rule that defines recipient, channel, urgency, and content:

| Event | Recipient | Channel | Urgency | Content Template |
|-------|-----------|---------|---------|-----------------|
| Health below 65 | CSM manager | Slack | Same day | "[Account] health dropped to [score] (was [prior]). Driver: [top risk driver]. CSM: [name]" |
| Health rapid decline (>10pts/7d) | CSM + manager | Slack | Immediate | "[Account] health declined [X] points in 7 days. Current: [score]. Investigate today" |
| Renewal reclassified to At Risk/Critical | CS leadership + CRO | Slack + email | Same day | "[Account] renewal now [classification]. ARR: [amount]. Days to renewal: [days]. Top risk: [factor]" |
| Champion departure | CSM + manager | Slack | Immediate | "Champion departure: [contact name] ([role]) at [account]. ARR: [amount]. Action needed: identify replacement" |
| Competitive signal | CSM + manager | Slack | Immediate | "Competitive signal at [account]: [signal type]. Evidence: [summary]. CSM to assess and respond" |
| P1 ticket opened | CSM | Slack | Immediate | "P1 ticket [ID] opened for [account]: [issue summary]" |
| Expansion signal | CSM + sales partner | Email | This week | "Expansion opportunity at [account]: [signal type]. Estimated value: [amount]. Review in weekly pipeline" |
| Commitment at risk | Commitment owner + CSM | Slack | Same day | "Commitment to [account] due in [days]: [description]. Owner: [name]" |
| Account churned | CS leadership + CRO | Email | Same day | "[Account] churned. ARR lost: [amount]. Primary cause: [reason]. Post-mortem to follow" |
| Account renewed | CS leadership | Email (digest) | Weekly | "[Account] renewed. ARR retained: [amount]. Expansion: [if any]" |
| Milestone missed | CSM | Slack | Same day | "[Account] milestone overdue: [milestone name] by [days] days" |
| Escalation stalled | CSM + manager | Slack | Same day | "Escalation [ID] for [account] stalled [days] days. Owner: [name]. No progress since [date]" |

### Step 3: Format and Deliver

**Slack notifications (immediate and same-day):**
- Maximum 4 lines
- First line: event type and account name (bold)
- Second line: key data point
- Third line: action or urgency indicator
- Fourth line: who should act

**Email notifications (weekly digest):**
- Subject: "CS Weekly Digest: [date range]"
- Body: grouped by category (renewals, health changes, expansions, escalations)
- Each item: one line with account, event, and status

**Formatting rules:**
- Never use passive voice in notifications ("Health dropped" not "Health was observed to have dropped")
- Always include the account name, the data point, and who should act
- Always include a link to the full account brief or the relevant CRM record if platform supports it

### Step 4: Deduplicate and Manage Fatigue

**Deduplication rules:**
- Same event, same account, within 24 hours: do not re-notify. Include in daily digest instead
- Related events on the same account (e.g., health decline + usage decline): consolidate into a single notification noting both signals
- Persistent conditions (health below 65 for multiple days): notify once on first detection, then include in daily digest only

**Suppression:**
- Recipients can mute specific notification types (managed in notification preferences)
- CSMs on PTO: hold non-critical notifications until they return; route critical notifications to their backup
- Weekends and holidays: batch all non-immediate notifications for delivery Monday morning

### Step 5: Log and Track

For each notification:
- Log: timestamp, event, recipient, channel, content
- Track: was it acknowledged? (For Slack: was it read? For email: was it opened? If platform supports this)
- Report: weekly notification volume per recipient, acknowledgement rate, most common event types

## Output Format

**Individual Slack notification:**
```
🔴 Risk Alert: Acme Corp
Health score dropped to 58 (was 72 last week). Primary driver: support ticket volume 3x segment average.
Action: CSM review recommended today.
Owner: Jane Doe
```

**Daily digest:**
```json
{
  "digest_date": "2026-03-10",
  "recipient": "jane.doe@company.com",
  "items": [
    { "account": "Acme Corp", "event": "health_below_65", "detail": "Score 58, declining. Driver: support", "urgency": "same_day" },
    { "account": "Beta Inc", "event": "milestone_missed", "detail": "Onboarding config 3 days overdue", "urgency": "this_week" },
    { "account": "Gamma Corp", "event": "expansion_signal", "detail": "Licence utilisation 91% for 30 days", "urgency": "this_week" }
  ],
  "summary": "1 urgent, 2 this week. 0 escalations pending."
}
```

**Weekly notification report (for CS Ops):**
```json
{
  "week_of": "2026-03-10",
  "total_notifications_sent": 47,
  "by_channel": { "slack_immediate": 12, "slack_same_day": 18, "email_digest": 17 },
  "by_event_type": { "health_alerts": 8, "risk_signals": 5, "milestones": 6, "escalations": 3, "renewals": 4, "other": 21 },
  "suppressed": 6,
  "acknowledgement_rate": 0.82,
  "busiest_recipient": "jane.doe (14 notifications)",
  "fatigue_risk": ["jane.doe -- 14 notifications this week, up from 8 last week"]
}
```

## Handoff to Human

This skill is fire-and-forget for the notification itself. Human decisions happen after delivery:
- CSM decides how to respond to each alert
- Manager decides whether to intervene or let the CSM handle it
- Leadership decides whether to redirect resources based on aggregate signals
- CS Ops tunes the notification rules based on the weekly report (too many? too few? wrong thresholds?)

## Confidence and Limitations

- **High confidence** for event detection and notification delivery -- rule-based triggers with structured output from verified data sources
- **High confidence** for deduplication -- timestamp-based logic with defined windows
- **Medium confidence** for notification relevance -- the rules define when to notify, but not every notification warrants action. Some are informational. The recipient must triage
- Cannot assess whether a notification was acted on (only whether it was delivered and, if platform supports, read)
- Notification fatigue is the primary risk. If a CSM receives 15+ notifications per day, they will start ignoring all of them. The weekly report tracks volume per recipient specifically to detect this
- Cannot route to the right person if CRM ownership data is stale (e.g., account reassigned but CRM not updated)
- Daily digest consolidation may delay awareness of related signals that individually are not urgent but collectively signal a pattern

## Dependencies

**Required:**
- Slack or email integration (notification delivery)
- Event streams from all pillar skills (notification sources)

**Strongly recommended:**
- All Book Intelligence skills (primary event sources)
- All Lifecycle Orchestration skills (workflow event sources)
- CRM API (account ownership for recipient routing)

**Downstream consumers:**
- CSMs, managers, and leadership (notification recipients)
- CS Ops (weekly notification report for rule tuning)

## References

- `references/notification-rules.md` -- Complete rule table, deduplication logic, suppression policies, and digest formatting

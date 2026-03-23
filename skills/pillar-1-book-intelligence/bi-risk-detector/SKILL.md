---
name: bi-risk-detector
description: Monitors a defined set of risk indicators across the customer portfolio and generates prioritised risk alerts. Combines leading indicators from usage and health data with event-based triggers like champion departure, support escalation, and missed meetings. Use when asked to identify at-risk accounts, build a risk queue, set up churn early warning, monitor renewal risk, create risk dashboards, prioritise CSM intervention, or when any workflow needs to know which accounts require immediate attention. Also triggers for churn prediction, risk scoring, and portfolio risk assessment.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: book-intelligence
  category: detection-layer
---

# Risk Signal Detector

Monitors risk indicators across the portfolio and generates prioritised alerts. Part of the Book Intelligence detection layer -- consumes data from the Health Score Engine and Usage Pattern Monitor, produces a ranked risk queue for human triage.

This is a **detection and prioritisation** skill. It identifies signals, scores severity, and ranks accounts for human attention. It never initiates customer contact, triggers save plays, or makes intervention decisions. Those are human territory.

## When to Run

- **Event-based triggers**: Near-real-time monitoring via webhooks or event streams for champion departure, P1 support tickets, declined meetings, competitive mentions
- **Metric-based triggers**: Scheduled cadence aligned with Health Score Engine (daily for high-touch, weekly for scaled)
- **On-demand**: When a human requests the current risk queue or risk assessment for a specific account

## Signal Registry

The risk signal registry defines every signal the detector monitors. Each signal has a type, a severity weight, a detection method, and evidence requirements.

### Metric-Based Signals

| Signal | Detection Source | Severity (1-5) | Evidence Required |
|--------|-----------------|-----------------|-------------------|
| Health score below 65 | Health Score Engine | 3 | Composite score, component breakdown |
| Health score rapid decline (>10pts/7d) | Health Score Engine | 4 | Score delta, timeline, component drivers |
| Usage gradual decline (3+ periods) | Usage Pattern Monitor | 3 | Metric, baseline, delta, duration |
| Usage sudden drop (>25% single period) | Usage Pattern Monitor | 4 | Metric, prior value, current value |
| Adoption plateau (60+ days below median) | Usage Pattern Monitor | 2 | Metric, segment position, duration |
| Support volume spike (>2x 90-day average) | Support platform | 3 | Ticket count, severity mix, topics |
| CSAT/NPS decline (below segment 25th) | Survey tool | 3 | Score, prior score, segment benchmark |

### Event-Based Signals

| Signal | Detection Source | Severity (1-5) | Evidence Required |
|--------|-----------------|-----------------|-------------------|
| Champion departure | CRM contact change, LinkedIn | 5 | Contact name, role, departure date |
| Executive sponsor change | CRM contact change | 4 | Old sponsor, new sponsor (if known) |
| Declined meetings (2+ in 30 days) | Calendar integration | 3 | Meeting dates, attendees, decline count |
| No-reply streak (3+ CSM emails unanswered) | Email/CRM activity | 3 | Email dates, subjects, days since last reply |
| P1 support escalation | Support platform | 4 | Ticket ID, issue summary, duration open |
| Competitor mention | Support tickets, call transcripts | 4 | Source, context, competitor named |
| Contract objection or delay | CRM opportunity stage | 3 | Opportunity ID, stage, days stalled |
| Payment overdue (>30 days) | Billing system | 3 | Invoice ID, amount, days overdue |

See `references/signal-registry.md` for the full registry with detection logic and tuning guidance.

## Core Execution Logic

### Step 1: Evaluate Incoming Signals

For each trigger (event or scheduled metric check):
1. Match the signal against the signal registry
2. Validate evidence requirements are met (do not alert on incomplete data)
3. Score severity using the registry weight

### Step 2: Check for Signal Clustering

Multiple signals on the same account within a 14-day window amplify severity:
- 2 signals: severity of the highest signal +1
- 3+ signals: severity of the highest signal +2
- Cap at 5

Clustering is the strongest predictor of near-term churn. A single declining metric is a watch item. Three signals converging on one account is urgent.

### Step 3: Apply Temporal Weighting

Signals carry more urgency when renewal is near:
- >180 days to renewal: no adjustment
- 90-180 days: severity +0.5
- 30-90 days: severity +1
- <30 days: severity +1.5 (round up)

### Step 4: Rank the Risk Queue

Produce a ranked list of all accounts with active risk signals, ordered by:
1. Adjusted severity score (highest first)
2. Days to renewal (soonest first, as tiebreaker)
3. ARR (highest first, as secondary tiebreaker)

### Step 5: Generate Alert Briefs

For each account in the risk queue, produce an alert brief:

```json
{
  "account_id": "string",
  "account_name": "string",
  "risk_score": 4.5,
  "arr": 85000,
  "days_to_renewal": 67,
  "health_score": 58,
  "active_signals": [
    {
      "signal": "Usage gradual decline",
      "severity": 3,
      "evidence": "Session depth declining 4 consecutive weeks, now 22% below 90-day baseline",
      "first_detected": "2026-02-15",
      "source": "bi-usage-monitor"
    },
    {
      "signal": "Champion departure",
      "severity": 5,
      "evidence": "Jane Smith (VP Product) left the company per LinkedIn update 2026-02-28",
      "first_detected": "2026-03-01",
      "source": "crm-contact-change"
    }
  ],
  "cluster_amplification": true,
  "temporal_adjustment": 1.0,
  "suggested_investigation": "Champion departure coincides with usage decline. New sponsor unknown. Priority: identify new stakeholder and assess relationship continuity before renewal window.",
  "handoff_urgency": "immediate"
}
```

### Step 6: Suppress Duplicates

Do not re-alert on the same signal unless:
- Severity escalates (e.g., gradual decline progresses to a 4th consecutive period)
- A new correlated signal appears on the same account
- 14 days have passed since the last alert with no human acknowledgement

### Step 7: Generate Daily Digest

Produce a daily summary for the CSM:
- New alerts since last digest
- Escalated alerts (existing signals that worsened)
- Resolved alerts (signal conditions no longer met)
- Portfolio risk trend (total risk signals this week vs. prior week)

## Handoff to Human

**Every risk alert surfaces to human for triage. The agent does not act on risk.**

| Signal Type | Routing | Urgency |
|-------------|---------|---------|
| Champion departure | Direct alert to CSM + notification to CS leadership | Immediate |
| Competitive displacement signal | Direct alert to CSM | Immediate |
| P1 support escalation | Direct alert to CSM | Same day |
| Health score rapid decline | Direct alert to CSM | Same day |
| Clustered signals (3+) | Direct alert to CSM + flag for manager review | Same day |
| Single metric-based signal | Daily digest | Next business day |
| Adoption plateau | Weekly digest | Weekly |

The human decides: investigate, escalate, trigger a save play, monitor, or dismiss. See `references/human-decision-guide.md`.

## Confidence and Limitations

- **High confidence** for signal detection (binary: the signal is present or it is not)
- **Medium confidence** for prioritisation (severity weights are defaults -- they need tuning per portfolio based on historical churn correlation)
- **Low confidence** for causal inference. The agent presents signals and correlations. It does not explain why the customer is at risk. That is human interpretation
- Cannot detect risks that exist only in relationship context (private dissatisfaction, internal political shifts, unvoiced budget concerns)
- Signal clustering amplification assumes signals are independent. If two signals share a root cause (e.g., a product outage causes both usage decline and support spike), the amplification may overstate severity

## Dependencies

**Required:**
- `bi-health-score` (composite and component scores, trends)
- `bi-usage-monitor` (pattern alerts)
- CRM API (contact changes, activity data, opportunity stages)
- Support platform API (ticket data, escalations)
- Calendar integration (meeting declines)

**Optional but high-value:**
- Email integration (no-reply streak detection)
- LinkedIn integration or stakeholder change detection service (champion departure)
- Call transcript integration (competitor mentions)
- Billing system (payment overdue signals)

**Downstream consumers:**
- `bi-account-brief` (active risk signals for account context)
- `bi-segment-trends` (aggregate risk by segment)
- Human triage queue

## References

- `references/signal-registry.md` -- Full signal definitions, detection logic, and tuning guidance
- `references/severity-calibration.md` -- How to adjust severity weights based on historical churn data
- `references/human-decision-guide.md` -- How CSMs should triage and respond to risk alerts

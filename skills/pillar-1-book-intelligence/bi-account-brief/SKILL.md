---
name: bi-account-brief
description: Compiles a comprehensive structured account snapshot by pulling from all available data sources. Gives the CSM full account context in under 60 seconds instead of 30-60 minutes of manual assembly. Use when asked to prepare for a customer call, build an account brief, generate a QBR prep summary, create an account snapshot, review an account before a meeting, assemble account context for an escalation, or when any human decision point across any pillar needs current account context. Also triggers for pre-call prep, account review, executive briefing preparation, or any request for a consolidated view of an account.
license: MIT
metadata:
  version: "1.0.0"
  pillar: book-intelligence
  category: intelligence-layer
---

# Account Briefing Generator

The most-used skill in the Book Intelligence pillar. Compiles a structured, comprehensive account snapshot from all available data sources. Designed to replace the 30-60 minutes a CSM spends manually assembling account context before a call, QBR, renewal conversation, or escalation.

This is a **data assembly** skill. It pulls, structures, and formats. No inference, no judgment, no action. The brief is an input to every human decision point across all pillars.

## When to Run

- **On-demand**: CSM requests a brief before a call, meeting, QBR, renewal conversation, or escalation
- **Auto-generated**: Triggers ahead of scheduled meetings when linked to calendar integration (generates brief 30 minutes before meeting start)
- **Called by other skills**: Any skill that surfaces a human decision point can invoke this skill to provide context alongside the alert

## Core Execution Logic

### Step 1: Pull Latest Data from All Sources

Gather current data from every available source. If a source is unavailable, note the gap in the brief rather than failing entirely.

| Source | Data Points |
|--------|------------|
| Health Score Engine | Composite score, component scores, trends, risk drivers |
| Usage Pattern Monitor | Key usage metrics, trend classifications, active pattern alerts |
| Risk Signal Detector | Active risk signals with evidence and severity |
| Expansion Signal Detector | Active expansion signals with evidence and timing |
| CRM - Contacts | Key contacts, roles, last engagement date, coverage gaps |
| CRM - Activities | Last 5 touchpoints across all channels (email, call, meeting) |
| CRM - Opportunities | Open opportunities, renewal dates, pipeline status |
| CRM - Notes | Last 3 CSM notes on the account |
| Support Platform | Open tickets (count, severity, age), recent resolved tickets |
| Product Analytics | Current key metrics snapshot (DAU/MAU, feature adoption, licence utilisation) |
| Contract/Billing | ARR, contract end date, payment status, pricing tier |
| Call Transcripts | Summary of last call (if transcript integration available) |

### Step 2: Assemble into Structured Brief

Organise data into a scannable format optimised for quick consumption:

**Header Block** (glanceable in 5 seconds):
- Account name
- ARR
- Health score + trend arrow
- Days to renewal
- Segment (tier / size / industry)
- CSM name

**Health Summary** (15 seconds):
- Composite score with component breakdown
- Trend direction (improving/stable/declining)
- Active risk drivers (if any)

**Usage Summary** (15 seconds):
- Key metrics vs. segment benchmark
- Overall usage trend
- Active pattern alerts (if any)

**Active Signals** (15 seconds):
- Risk signals with severity and evidence (from Risk Signal Detector)
- Expansion signals with timing window (from Expansion Signal Detector)
- Competitive intelligence flags (from Competitive Intel Monitor)

**Stakeholder Map** (15 seconds):
- Key contacts: name, role, last engagement date
- Coverage gaps: contacts not touched in 60+ days
- Stakeholder changes: recent departures or role changes

**Recent Activity** (15 seconds):
- Last 5 touchpoints across channels, most recent first
- Last call summary (if available)
- Last CSM notes (3 most recent)

**Open Items** (10 seconds):
- Open support tickets (count, top severity, oldest)
- Open opportunities or renewal status
- Pending action items from last interaction

**Attention Flags** (always at the bottom, highlighted):
- Anything requiring decision or action, sorted by urgency
- Data gaps or stale sources that affect brief reliability

### Step 3: Format for Context

Adapt the brief based on the consumption context:

| Context | Format Adaptation |
|---------|------------------|
| Pre-call prep | Emphasise recent activity, open items, and stakeholder last-touch. CSM needs conversation context |
| QBR preparation | Emphasise usage metrics, health trends, and value delivered. CSM needs the story arc |
| Renewal preparation | Emphasise commercial data, health trajectory, risk signals, and stakeholder map. CSM needs negotiation context |
| Escalation | Emphasise support history, risk signals, and timeline of deterioration. CSM needs the evidence chain |
| Executive briefing | Condense to header + health summary + key risk/opportunity. Executive needs the headline, not the detail |
| Manager review | Full brief with all sections. Manager needs the complete picture |

If context is not specified, default to the full format.

## Output Format

**Structured account brief:**

```json
{
  "account_id": "string",
  "generated_at": "2026-03-10T09:30:00Z",
  "context": "pre_call",
  "header": {
    "account_name": "Acme Corp",
    "arr": 85000,
    "health_score": 72,
    "health_trend": "declining",
    "days_to_renewal": 67,
    "segment": "Mid-Market / Medium / Established",
    "csm": "Jane Doe"
  },
  "health_summary": {
    "composite": 72,
    "components": {
      "usage": { "score": 81, "trend": "stable" },
      "engagement": { "score": 65, "trend": "declining" },
      "support": { "score": 58, "trend": "declining" },
      "sentiment": { "score": 80, "trend": "stable" },
      "commercial": { "score": 75, "trend": "improving" }
    },
    "risk_drivers": ["Support: P1 ticket open 12 days", "Engagement: no exec contact in 74 days"]
  },
  "usage_summary": {
    "dau_mau_ratio": { "value": 0.42, "vs_benchmark": "above_median", "trend": "stable" },
    "feature_adoption": { "value": 0.65, "vs_benchmark": "above_75th", "trend": "stable" },
    "licence_utilisation": { "value": 0.78, "vs_benchmark": "above_median", "trend": "growing" },
    "active_alerts": []
  },
  "active_signals": {
    "risk": [
      { "signal": "P1 ticket open", "severity": 4, "evidence": "Ticket #4521: API latency issue, open 12 days", "first_detected": "2026-02-26" }
    ],
    "expansion": [],
    "competitive": []
  },
  "stakeholder_map": {
    "key_contacts": [
      { "name": "Tom Chen", "role": "VP Engineering", "type": "champion", "last_touch": "2026-02-28", "days_since_touch": 10 },
      { "name": "Sarah Kim", "role": "CFO", "type": "economic_buyer", "last_touch": "2025-12-15", "days_since_touch": 85 }
    ],
    "coverage_gaps": ["Sarah Kim (CFO): 85 days since last touch"],
    "recent_changes": []
  },
  "recent_activity": [
    { "date": "2026-02-28", "type": "meeting", "summary": "Weekly sync with Tom Chen. Discussed API performance concerns" },
    { "date": "2026-02-25", "type": "email", "summary": "Follow-up on ticket #4521 with support team CC" },
    { "date": "2026-02-20", "type": "call", "summary": "QBR planning call with Tom Chen" }
  ],
  "open_items": {
    "support_tickets": { "count": 2, "highest_severity": "P1", "oldest_days": 12 },
    "renewal_status": "67 days out, no active renewal opportunity in CRM",
    "pending_actions": ["Follow up on API latency resolution", "Schedule QBR for March"]
  },
  "attention_flags": [
    { "flag": "P1 ticket open 12 days -- resolution needed before QBR", "urgency": "high" },
    { "flag": "CFO last touched 85 days ago -- coverage gap ahead of renewal", "urgency": "medium" }
  ],
  "data_gaps": []
}
```

## Handoff to Human

This skill is a support function -- it generates context for human consumption. No decision is required from the agent. The brief feeds into every human decision point:

- Before calls: CSM reads the brief to prepare conversation points
- Risk triage: CSM uses the brief alongside risk alerts to understand the full picture
- Expansion review: CSM uses the brief to assess whether the account is ready for a commercial conversation
- Escalation: CSM uses the brief to build the case for internal escalation
- Manager 1:1s: Manager reviews the brief to understand a CSM's account portfolio

## Confidence and Limitations

- **High confidence** for data assembly -- this is structured data retrieval and formatting, not inference
- Confidence degrades when source data is stale or incomplete. The brief explicitly flags gaps rather than presenting incomplete data as complete
- Cannot surface information that exists only in the CSM's head (relationship nuances, unlogged conversations, intuitions)
- The brief is a snapshot. It reflects the state at generation time. For fast-moving situations (active escalation, ongoing negotiation), regenerate before each interaction

## Dependencies

**Required:**
- `bi-health-score` (health data)
- CRM API (contacts, activities, opportunities, notes)

**Strongly recommended:**
- `bi-usage-monitor` (usage profile)
- `bi-risk-detector` (active risk signals)
- `bi-expansion-detector` (active expansion signals)
- Support platform API (ticket data)
- Product analytics (usage snapshot)
- Calendar integration (for auto-generation ahead of meetings)

**Optional:**
- `bi-competitive-intel` (competitive flags)
- Call transcript integration (last call summary)
- Email integration (recent email threads)

## References

- `references/brief-templates.md` -- Template variations by context (pre-call, QBR, renewal, escalation, executive)

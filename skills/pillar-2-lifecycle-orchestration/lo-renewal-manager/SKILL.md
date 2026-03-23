---
name: lo-renewal-manager
description: Tracks renewal timelines across the portfolio, triggers renewal workflows at defined milestones, surfaces renewal readiness with risk and opportunity signals, and manages the operational mechanics of the renewal process. Use when asked to manage renewals, track renewal dates, build renewal playbooks, automate renewal workflows, assess renewal risk, prepare for renewal conversations, forecast renewal outcomes, or when any account is approaching contract end date. Also triggers for questions about renewal pipeline, contract management, renewal forecasting, or retention operations.
license: MIT
metadata:
  version: "1.0.0"
  pillar: lifecycle-orchestration
  category: workflow-engine
---

# Renewal Manager

Tracks renewal timelines, triggers milestone-based workflows, surfaces readiness signals, and manages the operational process from T-180 through close. Part of the Lifecycle Orchestration pillar -- the highest-stakes workflow in CS because it directly protects revenue.

This is a **tracking, triggering, and surfacing** skill. It manages the timeline and surfaces context. It does not negotiate, set pricing, decide on concessions, or have the renewal conversation. Those are human decisions -- the CSM and their manager own the commercial outcome.

## When to Run

- **Scheduled**: Daily scan of all accounts to check renewal milestone triggers
- **Triggered**: When a renewal milestone date is reached (T-180, T-120, T-90, T-60, T-30, T-14)
- **On-demand**: When a CSM requests renewal status or readiness assessment for a specific account

## Renewal Timeline and Milestones

| Milestone | Days to Renewal | Actions Triggered |
|-----------|----------------|-------------------|
| T-180 | 180 days | Initial renewal flag. Pull health data, usage trends, contract history. Create renewal opportunity in CRM if not already present |
| T-120 | 120 days | Renewal readiness assessment. Score renewal risk. Surface to CSM with recommended preparation actions |
| T-90 | 90 days | Active renewal phase begins. Increase check-in cadence (via lo-check-in-scheduler). Generate renewal prep brief. Alert CSM to begin renewal planning |
| T-60 | 60 days | Renewal conversation expected. Flag if no renewal activity logged in CRM. Generate commercial context brief |
| T-30 | 30 days | Escalation check. If renewal is not in progress (no CRM stage advancement), alert CSM + manager |
| T-14 | 14 days | Final check. If renewal is not confirmed, escalate to CS leadership |
| T-0 | Renewal date | Outcome tracking. Was the account renewed, churned, or extended? Log outcome and trigger post-renewal workflow |

## Core Execution Logic

### Step 1: Maintain Renewal Calendar

Continuously maintain a calendar of all accounts with their renewal dates:
1. Pull contract end dates from CRM
2. Calculate milestone dates for each account
3. Check daily: which milestones are triggered today?
4. For each triggered milestone, execute the associated actions

### Step 2: Score Renewal Risk at T-120

Generate a renewal risk assessment by pulling:
- Health Score Engine composite and trends
- Usage Pattern Monitor trend classification
- Risk Signal Detector active signals
- Support history (open tickets, CSAT trend)
- Engagement pattern (stakeholder coverage, touchpoint frequency)
- Contract history (previous renewal experience, expansions, concessions)

**Renewal risk classification:**

| Classification | Criteria | Recommended Action |
|---------------|----------|-------------------|
| On Track | Health > 75, no active risk signals, engagement stable or growing | Standard renewal process |
| Watch | Health 65-75, or 1 active risk signal, or engagement flat | Increase touchpoint frequency, prepare value narrative |
| At Risk | Health < 65, or 2+ risk signals, or champion departure, or competitive signal | Immediate CSM + manager review. Save plan may be needed before renewal |
| Critical | Health < 50, or competitive signal + renewal < 90 days, or customer has stated intent to leave | Executive engagement. Full save play. Do not wait for renewal timeline |

### Step 3: Generate Renewal Prep Brief at T-90

Invoke `bi-account-brief` with renewal context to produce:
- Full account health and usage summary
- Value delivered during the contract period (usage growth, outcomes achieved)
- Risk signals with evidence
- Expansion signals (if renewal is also an expansion opportunity)
- Stakeholder map with coverage assessment (is the economic buyer engaged?)
- Contract history (current terms, pricing, previous negotiations)
- Recommended approach (standard renewal, renewal with expansion, renewal with risk mitigation)

### Step 4: Track Renewal Progress

Monitor CRM opportunity stage for the renewal:
- Is the renewal opportunity created? (Flag if missing at T-90)
- Is the stage advancing? (Flag if stalled for 30+ days)
- Are there documented activities? (Flag if no renewal-related activities logged)
- Is the expected close date realistic? (Flag if pushed past contract end date)

### Step 5: Generate Renewal Forecast

For the portfolio, produce a rolling renewal forecast:
```json
{
  "forecast_date": "2026-03-10",
  "next_90_days": {
    "total_renewals": 24,
    "total_arr_renewing": 1850000,
    "on_track": { "count": 16, "arr": 1200000 },
    "watch": { "count": 5, "arr": 420000 },
    "at_risk": { "count": 2, "arr": 180000 },
    "critical": { "count": 1, "arr": 50000 }
  },
  "renewals_this_month": [
    {
      "account": "Acme Corp",
      "arr": 85000,
      "renewal_date": "2026-04-01",
      "risk_classification": "watch",
      "risk_factors": ["Engagement declining", "Economic buyer not engaged"],
      "csm": "Jane Doe",
      "crm_stage": "Negotiation"
    }
  ]
}
```

## Output Format

**Per-account renewal record:**
```json
{
  "account_id": "string",
  "renewal_date": "2026-06-15",
  "days_to_renewal": 97,
  "current_milestone": "T-120",
  "risk_classification": "watch",
  "risk_factors": ["Health trending down (74, declining)", "No exec engagement in 60 days"],
  "expansion_opportunity": true,
  "crm_opportunity_status": "created",
  "crm_stage": "Qualification",
  "last_renewal_activity": "2026-02-20",
  "next_action": { "type": "T-90 renewal prep brief", "due": "2026-03-16" },
  "csm": "Jane Doe"
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Renewal risk classification (T-120) | Risk score, health data, signals, contract history | Whether the classification is accurate given relationship context; what preparation is needed |
| Renewal approach (T-90) | Renewal prep brief with full context | How to frame the renewal: standard, with expansion, with concession, or with save play |
| Negotiation strategy | Commercial data, competitive signals, contract history | Pricing, terms, concessions, escalation to leadership |
| Stalled renewal (T-30) | CRM stage history, customer engagement, risk signals | Whether to escalate, change approach, or accept timeline |
| Critical renewal (T-14) | Full context, escalation history | Executive engagement, final save attempt, or churn acceptance |

## Confidence and Limitations

- **High confidence** for timeline management and milestone triggering -- deterministic scheduling
- **Medium confidence** for renewal risk classification -- health and signal data are strong inputs but relationship context matters
- Cannot predict pricing sensitivity, budget availability, or internal customer politics
- Cannot assess whether a competitor has made a specific offer
- The risk classification is a starting point. CSMs should always overlay their relationship read

## Dependencies

**Required:**
- CRM API (contract dates, opportunity management, activity tracking)
- `bi-health-score` (health data for risk scoring)

**Strongly recommended:**
- `bi-risk-detector` (active risk signals)
- `bi-expansion-detector` (expansion signals for renewal + growth conversations)
- `bi-account-brief` (renewal prep brief generation)
- `lo-check-in-scheduler` (cadence adjustment during renewal phase)

## References

- `references/renewal-playbook.md` -- Detailed renewal workflow by risk classification

---
name: ra-stakeholder-change-detector
description: Monitors for stakeholder changes at customer accounts including champion departures, new executive hires, reorganisations, and role changes. Detects changes from CRM updates, LinkedIn signals, and engagement pattern shifts. Use when asked to track contact changes, monitor for champion departure, detect reorgs at customer accounts, set up stakeholder change alerts, or when any workflow needs early warning of relationship disruption. Also triggers for questions about contact monitoring, org change detection, stakeholder continuity, or relationship risk from personnel changes.
license: MIT
metadata:
  version: "1.0.0"
  pillar: relationship-architecture
  category: relationship-data
---

# Stakeholder Change Detector

Monitors for stakeholder changes that could affect the customer relationship. Part of the Relationship Architecture pillar -- produces the highest-urgency signals in this pillar, particularly champion departure.

This is a **detection and alerting** skill. It identifies that a change happened. The CSM interprets the impact and decides the response. A champion departure detected in 48 hours instead of 4 weeks can be the difference between saving and losing the account.

## When to Run

- **Continuous**: Monitors CRM contact updates and engagement pattern changes in real-time
- **Scheduled**: Weekly external scan (LinkedIn, if integration available) for role changes among key contacts
- **Triggered**: When a contact record changes in CRM or when an engagement pattern shifts suddenly

## Core Execution Logic

### Step 1: Monitor CRM-Based Signals (High Confidence)

| Signal | Detection Method | Confidence | Alert Urgency |
|--------|-----------------|-----------|---------------|
| Contact deactivated | CRM contact status changed to inactive or deleted | High | Immediate if Champion or Economic Buyer; same day for others |
| Contact role changed | CRM title or role field updated | High | Same day -- assess whether the new role changes their influence |
| New contact added | New contact record created on the account | Medium | This week -- classify and assess |
| Contact reassigned | Contact moved to a different account or business unit | High | Same day -- equivalent to departure for this account |
| Ownership field changed | Account's CSM or AE field changes (internal change, but affects the customer) | High | Immediate -- triggers lo-handoff-manager |

### Step 2: Monitor Engagement-Based Signals (Medium Confidence)

| Signal | Detection Criteria | Confidence | Possible Explanations |
|--------|-------------------|-----------|----------------------|
| Sudden silence | A previously active contact (touchpoint every 2 weeks or more) has zero engagement for 30+ days | Medium | Departed, went on leave, disengaging, or simply busy. Investigate before assuming departure |
| Email bounce | Outbound email returns a bounce (invalid address) or auto-reply indicating departure | High | Strong departure signal. Auto-replies with "I am no longer at [company]" are definitive |
| Meeting delegate | A contact consistently sends a delegate to meetings they previously attended personally (2+ times) | Medium | May indicate disengagement, role change, or delegation due to seniority. Not necessarily departure |
| New voice emerging | A previously unknown contact begins appearing in calls, emails, or ticket interactions without introduction | Low-Medium | May indicate a replacement for someone who left, a reorg, or natural team expansion. Investigate |
| Response pattern change | A contact who previously responded within 24 hours now consistently takes 5+ days | Medium | May indicate disengagement, workload change, or deprioritisation of the vendor relationship |

### Step 3: Monitor External Signals (Variable Confidence)

If LinkedIn integration or similar service is available:

| Signal | Detection Method | Confidence | Latency |
|--------|-----------------|-----------|---------|
| Role change (same company) | LinkedIn title update showing new role at the same employer | High | 1-4 weeks after actual change (people update LinkedIn on their own schedule) |
| Company departure | LinkedIn shows new employer | High | 1-6 weeks after actual departure |
| New hire at customer | Person with relevant title joins the customer company | Medium | 1-4 weeks after start date |
| Reorg signal | Multiple contacts at the same company update titles simultaneously | Medium | Indicates restructuring. May affect reporting lines and decision-making authority |

**Important**: LinkedIn data is lagging. A champion may have left 3 weeks before updating their profile. Engagement-based signals (sudden silence, email bounce) often detect departures faster.

### Step 4: Classify and Score Change Impact

For each detected change, assess the impact on the account:

| Change Type | Impact Assessment Factors | Severity Range |
|-------------|--------------------------|---------------|
| Champion departure | Account ARR, renewal proximity, relationship breadth (single-threaded?), replacement identified? | Critical (5) if single-threaded or near renewal. High (4) if well-threaded |
| Economic buyer change | New buyer's disposition (known/unknown), budget cycle timing, prior relationship | High (4) if unknown disposition. Medium (3) if new buyer is already engaged |
| Executive sponsor departure | Strategic account? Air cover needed for budget protection? | High (4) for strategic accounts. Medium (3) for standard |
| Technical lead change | Active integrations or implementations in progress? | Medium (3) if active project. Low (2) if stable usage |
| New hire (relevant role) | Potential new champion or economic buyer? Opportunity to build relationship? | Low (1) -- opportunity signal, not risk |
| Reorg | Scope and relevance of restructuring to the product's stakeholder ecosystem | Variable -- depends on which roles and relationships are affected |

### Step 5: Generate Alert

```json
{
  "alert_id": "sc-2026-0089",
  "account_id": "string",
  "account_name": "Acme Corp",
  "change_type": "champion_departure",
  "severity": 5,
  "contact": {
    "name": "Jane Smith",
    "previous_role": "VP Product",
    "stakeholder_type": "champion",
    "detection_method": "linkedin_role_change",
    "detection_date": "2026-03-08",
    "estimated_departure_date": "2026-02-28",
    "new_employer": "Competitor X",
    "new_role": "VP Product"
  },
  "impact_assessment": {
    "account_arr": 85000,
    "days_to_renewal": 112,
    "other_active_contacts": 2,
    "single_threaded_risk": false,
    "health_score": 72,
    "health_trend": "declining",
    "relationship_breadth": "moderate -- 2 other active contacts but no executive coverage"
  },
  "correlated_signals": [
    "Usage declining for 3 weeks (bi-usage-monitor) -- may correlate with champion departure timeline",
    "No executive sponsor engaged (ra-stakeholder-mapper)"
  ],
  "recommended_actions": [
    "Identify replacement champion or sponsor immediately",
    "Reach out to remaining active contacts to confirm continuity and assess impact",
    "Update stakeholder map in ra-stakeholder-mapper",
    "Brief CSM manager -- champion departure at a mid-sized account approaching renewal",
    "Monitor for further engagement decline in the next 14 days"
  ],
  "urgency": "immediate",
  "routed_to": ["CSM: Jane Doe", "Manager: Mike Ross"]
}
```

### Step 6: Track Change Lifecycle

Each stakeholder change follows a lifecycle:

| Status | Definition |
|--------|-----------|
| Detected | Change signal identified |
| Confirmed | CSM or data source confirms the change is real (not a data error) |
| Impact assessed | CSM has evaluated the effect on the relationship |
| Response in progress | CSM is actively addressing the change (building new relationship, securing replacement) |
| Stabilised | New stakeholder landscape is established and relationships are active |

Track time from detection to stabilisation. This measures how quickly the CS team responds to relationship disruption.

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Change confirmation | Signal evidence, detection method, confidence level | Whether the change is real or a false positive. Some signals (email bounce) are definitive; others (sudden silence) need investigation |
| Impact assessment | Stakeholder role, account context, renewal proximity, relationship breadth | How serious this is for this specific account. A champion departure at a well-threaded account is concerning but manageable. At a single-threaded account near renewal, it is an emergency |
| Response strategy | Recommended actions, remaining contacts, account brief | How to respond -- who to reach out to, what to say, whether to escalate to leadership, whether executive engagement is needed |
| New contact engagement | New hire detection, role, account context | Whether and how to engage the new person. Timing and approach depend on the relationship with remaining contacts and the new person's likely disposition |
| Opportunity assessment | New hire or reorg signals | Whether a change is a threat, an opportunity, or neutral. A new CTO might be a chance to re-engage at the executive level if the previous one was unresponsive |

## Confidence and Limitations

- **High confidence** for CRM-based detection (contact deactivated, role changed) -- structured data events with defined triggers
- **Medium confidence** for engagement-based detection (sudden silence, meeting delegates, response delays) -- behavioural patterns have multiple possible explanations. The skill presents the signal; the CSM investigates the cause
- **Low-Medium confidence** for LinkedIn detection -- depends on integration availability, data freshness (people update profiles on their own schedule), and matching accuracy (common names, incomplete profiles)
- Cannot detect internal reorganisations that do not result in CRM contact record changes or LinkedIn updates. Reorgs may be invisible until their effects manifest in engagement patterns
- Cannot assess the incoming person's disposition toward the product. A new VP might be a champion or a sceptic -- the classification only becomes clear through engagement
- Cannot detect departures that happen without any digital signal (contact leaves but email remains active during notice period, LinkedIn is not updated)
- Champion departure to a competitor (as in the example above) is a double signal: loss of the champion AND potential competitive intelligence gained by the competitor

## Dependencies

**Required:**
- CRM API (contact records, activity data, field change events)
- ra-stakeholder-mapper (stakeholder classifications and coverage context)

**Strongly recommended:**
- Email integration (bounce detection, auto-reply detection)
- Calendar integration (meeting delegate pattern detection)
- ra-engagement-tracker (engagement pattern baselines for silence detection)
- bi-risk-detector (champion departure feeds as a risk signal -- the highest-severity signal in the system)

**Optional but high-value:**
- LinkedIn integration or stakeholder monitoring service (for external detection)

**Downstream consumers:**
- bi-risk-detector (champion departure and executive change as risk signals)
- ra-stakeholder-mapper (triggers stakeholder map update)
- ic-internal-notifier (routes change alerts to appropriate recipients)
- lo-renewal-manager (stakeholder change near renewal amplifies renewal risk)

## References

- `references/change-detection-methods.md` -- Detection method details, confidence calibration, and false positive reduction strategies

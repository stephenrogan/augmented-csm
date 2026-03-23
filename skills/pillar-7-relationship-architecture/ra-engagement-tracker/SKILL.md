---
name: ra-engagement-tracker
description: Tracks touchpoint frequency and recency across all channels for every stakeholder at every account. Computes engagement health per contact, detects declining patterns, and identifies accounts where the relationship is cooling before the health score reflects it. Use when asked to track customer engagement, monitor touchpoint cadence, identify engagement gaps, assess relationship activity, or when any workflow needs to know how recently and how frequently the CSM is engaging with their accounts. Also triggers for questions about touchpoint cadence, engagement health, contact activity, relationship frequency, or communication gaps.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: relationship-architecture
  category: relationship-data
---

# Engagement Tracker

Tracks touchpoint frequency and recency across all communication channels for every stakeholder. Computes engagement health per contact and per account. Part of the Relationship Architecture pillar.

This is a **measurement and alerting** skill. It tracks frequency -- how often and how recently have you engaged. It does not assess quality -- a weekly call where nothing meaningful is discussed scores the same as a weekly call that transforms the relationship. Frequency is necessary for healthy relationships; it is not sufficient. The CSM provides the quality assessment.

## When to Run

- **Continuous**: Logs touchpoints as they occur from connected channels
- **Scheduled**: Weekly engagement health computation and gap detection
- **On-demand**: When a CSM requests engagement data for a specific account or contact

## Core Execution Logic

### Step 1: Log Touchpoints from All Channels

Every customer interaction is a touchpoint. Capture from all available sources:

| Channel | Source | What Counts as a Touchpoint | What Does Not Count |
|---------|--------|---------------------------|-------------------|
| Email | Email integration | Emails sent to or received from a customer contact (excluding automated sequences) | Auto-replies, system notifications, marketing emails |
| Meeting | Calendar integration | Completed meetings with customer attendees (not cancelled, not no-showed) | Internal-only meetings, cancelled meetings |
| Call | Call platform or CRM activity | Completed phone/video calls with customer contacts | Voicemails left without conversation, abandoned calls |
| Support | Support platform | Ticket interactions where the CSM or customer exchanges substantive communication | Automated ticket status updates, system notifications |
| Community | Community platform (if ca-community-monitor is active) | Customer posts or replies in the community | Passive viewing without posting |
| Product | Product analytics | Portal login or feature usage (passive engagement -- tracked but weighted differently) | API calls, automated syncs, background processes |

For each touchpoint, log:
- Timestamp
- Channel
- Direction: inbound (customer-initiated) or outbound (CSM-initiated)
- Contact(s) involved
- Type: scheduled (planned touchpoint) or unscheduled (ad hoc)

### Step 2: Compute Per-Contact Engagement Metrics

For each contact in ra-stakeholder-mapper:

| Metric | Computation | Why It Matters |
|--------|-------------|---------------|
| Days since last touch | Calendar days from most recent touchpoint to today | Recency -- is the relationship current? |
| Average touchpoint frequency | Mean days between touchpoints over trailing 90 days | Cadence -- how often are you engaging? |
| Touchpoint trend | Frequency this 30-day period vs. previous 30-day period | Direction -- is engagement increasing, stable, or declining? |
| Channel distribution | Percentage of touchpoints per channel | Diversity -- single-channel engagement (email only) is less robust than multi-channel |
| Inbound ratio | Inbound touchpoints / total touchpoints | Reciprocity -- a high inbound ratio suggests the customer is engaged. A zero inbound ratio suggests you are chasing |
| Response latency | Average time from CSM outreach to customer response | Responsiveness -- increasing latency is an early cooling signal |

### Step 3: Classify Engagement Health

For each contact, compare engagement metrics against the expected cadence for their stakeholder type (from ra-stakeholder-mapper):

| Health Level | Criteria | Signal |
|-------------|----------|--------|
| Strong | Last touch within expected cadence. Trend stable or improving. Inbound ratio >0.3. Multi-channel | Relationship is active and reciprocal |
| Adequate | Last touch within expected cadence but one or more secondary metrics weakening (declining trend, single-channel, low inbound) | Relationship is maintained but showing early signs of cooling |
| Declining | Last touch within 1.5x expected cadence. Trend declining for 2+ consecutive periods. Or inbound ratio dropped to zero | Relationship is cooling. Not yet a gap but heading there without intervention |
| Gap | Last touch >2x expected cadence | Contact is not being managed. Coverage has lapsed |
| Lost | No engagement across any channel in 90+ days | Contact may have left, changed roles, or fully disengaged. Route to ra-stakeholder-change-detector for investigation |

### Step 4: Compute Per-Account Engagement Health

Aggregate contact-level health into an account-level engagement score:

**Weighted by stakeholder type:**
- Champion engagement: 35% weight (the most important relationship)
- Economic Buyer engagement: 25% weight
- Executive Sponsor engagement: 15% weight
- Technical Lead engagement: 15% weight
- All other contacts: 10% weight

**Account engagement score** = weighted sum of contact engagement scores (each contact scored 0-100 based on health level: Strong=90, Adequate=70, Declining=45, Gap=20, Lost=0)

**Account engagement classification:**

| Score | Classification | Interpretation |
|-------|---------------|---------------|
| 75-100 | Healthy engagement | Key contacts are actively engaged. Cadence is being maintained |
| 55-74 | Adequate engagement | Most contacts engaged but some weakening. Monitor and address gaps |
| 35-54 | Declining engagement | Meaningful engagement gaps exist. Investigate and intervene |
| 0-34 | Critical engagement failure | Multiple key contacts disengaged. Relationship infrastructure is at risk |

### Step 5: Detect Patterns and Generate Alerts

| Pattern | Detection | Alert |
|---------|-----------|-------|
| No-reply streak | 3+ outbound emails to the same contact with no response | CSM alert: "[Contact] has not responded to last 3 emails. Consider calling or approaching through a different contact" |
| Meeting cancellation pattern | 2+ meetings cancelled or no-showed by the same contact in 30 days | CSM alert: "[Contact] cancelled or missed 2+ meetings. Engagement is declining" |
| Inbound engagement drop | Account's inbound ratio drops from >0.3 to <0.1 over 60 days | CSM alert: "[Account] has stopped initiating contact. All recent touchpoints are outbound" |
| Champion cooling | Champion contact moves from Strong to Declining engagement health | CSM + manager alert: "Champion [name] engagement declining at [account]. [Specific metrics]" |
| Complete silence | Zero touchpoints across all channels for an account in 30+ days | CSM alert: "[Account] has had no engagement of any kind in [X] days. Investigate immediately" |

### Step 6: Generate Engagement Report

**Per-CSM weekly engagement summary:**

```json
{
  "csm": "Jane Doe",
  "report_date": "2026-03-10",
  "portfolio_engagement": {
    "total_accounts": 42,
    "engagement_distribution": {
      "healthy": 28,
      "adequate": 8,
      "declining": 4,
      "critical": 2
    },
    "avg_engagement_score": 72
  },
  "alerts_this_week": [
    {
      "type": "no_reply_streak",
      "account": "Gamma Corp",
      "contact": "Lisa Park (VP Eng)",
      "detail": "3 outbound emails in 14 days with no response",
      "recommended_action": "Try a different channel (call) or approach through another contact"
    },
    {
      "type": "champion_cooling",
      "account": "Beta Inc",
      "contact": "Tom Chen (Champion)",
      "detail": "Engagement moved from Strong to Declining. Touchpoint frequency down from every 10 days to every 28 days over last 60 days",
      "recommended_action": "Investigate. Schedule a direct conversation. Do not add more emails to the no-reply streak"
    }
  ],
  "engagement_movers": {
    "improved": [
      { "account": "Acme Corp", "score_change": "+12", "driver": "Executive sponsor engaged for first time in 90 days" }
    ],
    "declined": [
      { "account": "Beta Inc", "score_change": "-15", "driver": "Champion engagement cooling" }
    ]
  },
  "cadence_compliance": {
    "touchpoints_expected": 38,
    "touchpoints_completed": 34,
    "compliance_rate": 0.89,
    "overdue_touchpoints": [
      { "account": "Delta Ltd", "contact": "Sarah Kim", "expected_cadence": "monthly", "days_overdue": 12 }
    ]
  }
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Declining engagement response | Specific contacts, metric trends, pattern details | How to respond -- call, email, approach through another contact, escalate to manager, or wait. The approach depends on the relationship |
| No-reply interpretation | Streak length, contact role, prior engagement pattern | Whether the silence means disengagement, a busy period, a personnel change, or deliberate avoidance. Each has a different response |
| Cadence adjustment | Current engagement frequency vs. expected cadence | Whether the expected cadence is right for this contact. Some contacts prefer less frequent engagement. The cadence rules are defaults, not mandates |
| Engagement quality assessment | Frequency and recency data | Whether the touchpoints are meaningful. A CSM meeting weekly with a customer but never advancing the relationship has a perfect engagement score and a failing relationship. The human layer is essential |
| Alert triage | Multiple alerts across the portfolio | Which declining engagements to address first, given limited CSM time and competing priorities |

## Confidence and Limitations

- **High confidence** for touchpoint logging and frequency computation -- structured event data from connected systems
- **High confidence** for engagement health classification -- deterministic comparison of metrics to defined thresholds
- **Medium confidence** for pattern detection (no-reply streaks, cancellation patterns) -- these are reliable signals but have multiple possible interpretations
- **Medium confidence** for inbound ratio as an engagement quality proxy -- a declining inbound ratio is a meaningful signal, but some customers are naturally passive communicators. Benchmark against the contact's own historical pattern, not a universal standard
- **Low confidence** for engagement quality assessment. This is the fundamental limitation: the skill tracks frequency, not depth. A 15-minute status call and a 2-hour strategic planning session count the same. The CSM provides the quality layer
- Cannot track engagement that happens outside connected systems (in-person meetings, conferences, informal conversations, personal phone calls)
- "No inbound engagement" is a strong disengagement signal in most cases, but some customers only engage reactively and have always done so. The baseline matters more than the absolute number

## Dependencies

**Required:**
- CRM API (activity data, contact records)
- Calendar integration (meeting data)
- Email integration (email activity data)

**Strongly recommended:**
- ra-stakeholder-mapper (stakeholder types and expected cadence for health computation)
- Call platform integration (call data)
- Support platform (support interaction data)
- ca-community-monitor (community engagement channel)

**Downstream consumers:**
- bi-health-score (engagement data feeds the engagement component -- 25% default weight)
- ra-stakeholder-mapper (engagement status per contact)
- bi-risk-detector (declining engagement as a risk signal)
- lo-check-in-scheduler (cadence compliance data)
- cc-report-generator (engagement metrics for CSM and manager reports)

## References

- `references/engagement-methodology.md` -- Channel definitions, health classification thresholds, and cadence baseline calibration

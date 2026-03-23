---
name: ra-stakeholder-mapper
description: Tracks customer org charts, contact roles, engagement frequency, and relationship coverage across accounts. Maintains a structured stakeholder map that identifies champions, economic buyers, influencers, and coverage gaps. Use when asked to map stakeholders, track customer contacts, build an org chart, identify relationship gaps, assess stakeholder coverage, or when any workflow needs to know who matters at an account and how recently they have been engaged. Also triggers for questions about contact mapping, multi-threading assessment, stakeholder analysis, single-thread risk, or relationship breadth.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: relationship-architecture
  category: relationship-data
---

# Stakeholder Mapper

Maintains structured stakeholder maps for all accounts. Tracks roles, influence, engagement history, and coverage gaps. Part of the Relationship Architecture pillar -- the data infrastructure that supports the most human-dependent pillar.

This is a **data maintenance and analysis** skill. It tracks who matters and how recently they have been engaged. It does not assess relationship quality (that is the CSM's read), develop relationships, or make contact strategy decisions.

## When to Run

- **Continuous**: Updates stakeholder data as CRM contacts, activities, and engagement signals change
- **Scheduled**: Weekly coverage gap analysis across all accounts
- **On-demand**: When a CSM or manager requests a stakeholder map for a specific account

## Core Execution Logic

### Step 1: Build and Maintain Contact Map

For each account, maintain a structured record per contact:

| Field | Source | Update Trigger |
|-------|--------|---------------|
| Name and title | CRM contact record | On any field change |
| Stakeholder type | CSM classification (see types below) | CSM updates manually; skill prompts for classification of untyped contacts quarterly |
| Influence level | CSM assessment: high / medium / low | CSM updates; skill prompts for review if engagement pattern contradicts classification |
| Sentiment toward product | CSM assessment: advocate / supportive / neutral / sceptical / detractor | CSM updates; NPS response may prompt reassessment |
| Last engagement date | CRM activity log, email, calendar, support | Continuous -- updates automatically from all connected channels |
| Primary engagement channel | Most frequent channel (email, call, meeting, support, community) | Computed from activity log |
| Engagement frequency | Average days between touchpoints (trailing 90 days) | Computed weekly |
| Coverage status | Computed from engagement frequency vs. expected cadence | Computed weekly |

### Step 2: Classify Stakeholder Types

Each contact is classified into one or more types:

| Type | Definition | Why They Matter | Expected Engagement Cadence |
|------|-----------|----------------|---------------------------|
| Champion | Actively advocates for the product internally. Sponsors the relationship. Goes to bat for you | If they leave, the account is immediately at risk. The single most important relationship | Enterprise: every 2 weeks. Mid-market: monthly |
| Economic Buyer | Controls or directly influences the budget decision for your product | If not engaged, renewal is vulnerable to cost-cutting or competitive displacement | Enterprise: monthly. Mid-market: quarterly |
| Technical Lead | Owns the implementation, integration, or day-to-day technical relationship | If frustrated with the product, technical issues escalate and adoption stalls | As needed -- driven by product discussions and support interactions |
| Executive Sponsor | Senior leader who provides strategic air cover for the investment | If unaware of value being delivered, the budget is at risk in prioritisation discussions | Quarterly minimum. More frequently during renewal or expansion |
| End User | Uses the product daily but does not influence purchasing decisions | Their collective experience drives adoption metrics and organic sentiment | No direct cadence -- engagement measured through product usage |
| Influencer | Does not decide but shapes opinions within the organisation | An unmanaged negative influencer can poison the relationship without the CSM knowing | Varies -- identify and monitor, engage as needed |
| Detractor | Actively works against the product or the relationship | Must be identified and addressed, not ignored. Detractors who are not managed become the voice the economic buyer hears | Engage deliberately -- ignoring a detractor does not make them less influential |

**Classification responsibility:** The CSM classifies contacts. The agent tracks engagement. If a contact has no classification after 30 days in the CRM, the skill prompts the CSM to classify them.

### Step 3: Compute Coverage Status

For each contact, compare engagement recency to expected cadence:

| Status | Criteria | Interpretation |
|--------|----------|---------------|
| Active | Engaged within expected cadence for their stakeholder type | Relationship is being maintained |
| Cooling | Last engagement is 1.5-2x the expected cadence | Relationship is drifting. Not yet a gap but heading there |
| Gap | Last engagement is >2x expected cadence | Contact is not being managed. Coverage has lapsed |
| Lost | No engagement in 90+ days across any channel | Contact may have left the company, changed roles, or fully disengaged |

### Step 4: Identify Structural Risks

Assess the stakeholder map for structural vulnerabilities:

| Risk | Detection | Severity | Implication |
|------|-----------|----------|------------|
| Single-threaded | Only 1 contact with Active status. All others are Gap or Lost | Critical | Any change at the account (champion leaves, contact gets busy) puts the entire relationship at risk |
| No economic buyer | No contact classified as Economic Buyer, or Economic Buyer is in Gap/Lost status | High | The renewal decision will be made by someone the CSM has not spoken to |
| Champion cooling | Champion contact's status is Cooling or Gap | High | The primary relationship is weakening. Investigate before it becomes a departure |
| No executive coverage | No Executive Sponsor exists in the contact map, or all are in Lost status | Medium | Investment lacks strategic air cover. Vulnerable to budget reallocation |
| Detractor unmanaged | A contact classified as Detractor exists with no recent engagement and no strategy documented | Medium | Detractors do not become neutral through neglect. They become more vocal |
| Narrow coverage | All active contacts are in the same department or at the same level | Medium | Relationship is deep but not wide. A departmental reorg could sever the entire relationship |

### Step 5: Generate Stakeholder Map

```json
{
  "account_id": "string",
  "map_date": "2026-03-10",
  "total_contacts": 6,
  "coverage_summary": {
    "active": 3,
    "cooling": 1,
    "gap": 1,
    "lost": 1
  },
  "structural_risks": [
    {
      "risk": "no_economic_buyer_engaged",
      "detail": "Sarah Kim (CFO) last engaged 85 days ago. Gap status",
      "severity": "high",
      "recommended_action": "Re-engage through champion introduction or executive-to-executive outreach"
    }
  ],
  "contacts": [
    {
      "name": "Tom Chen",
      "title": "VP Engineering",
      "type": ["champion"],
      "influence": "high",
      "sentiment": "advocate",
      "last_engagement": "2026-03-01",
      "days_since_touch": 9,
      "engagement_frequency_days": 12,
      "expected_cadence_days": 14,
      "coverage_status": "active",
      "primary_channel": "meeting",
      "notes": "Strong advocate. Drives internal adoption. Attends all QBRs"
    },
    {
      "name": "Sarah Kim",
      "title": "CFO",
      "type": ["economic_buyer"],
      "influence": "high",
      "sentiment": "neutral",
      "last_engagement": "2025-12-15",
      "days_since_touch": 85,
      "engagement_frequency_days": null,
      "expected_cadence_days": 30,
      "coverage_status": "gap",
      "primary_channel": "email",
      "notes": "Met once during QBR in December. Has not engaged since. Critical to re-engage before renewal"
    }
  ],
  "multi_threading_score": {
    "score": 0.58,
    "assessment": "moderate_risk",
    "detail": "3 active contacts but concentrated in Engineering. No active relationship with Finance or executive level"
  },
  "recommendations": [
    {
      "priority": 1,
      "action": "Re-engage Sarah Kim (CFO) before renewal. Approach through Tom Chen (champion) for an introduction to discuss ROI",
      "rationale": "Economic buyer in Gap status 67 days before renewal"
    },
    {
      "priority": 2,
      "action": "Identify and engage a contact in the Operations team. Product is used cross-functionally but relationships are single-department",
      "rationale": "Narrow coverage risk -- all relationships are in Engineering"
    }
  ]
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Contact classification | Contact name, role, engagement history | How to classify: Champion, Economic Buyer, Detractor, etc. Requires relationship judgment the agent cannot provide |
| Coverage gap response | Gap details, contact context, structural risk severity | How to re-engage: direct outreach, introduction through champion, executive-to-executive, or accept the gap |
| Multi-threading strategy | Current map, narrow coverage assessment | Which new contacts to develop, how to approach them, which existing contacts can facilitate introductions |
| Detractor management | Detractor identification, engagement history, influence level | Whether to engage directly, work around them, or escalate to neutralise their influence |
| Relationship quality assessment | Engagement frequency and recency data | The actual quality of each relationship. Frequent engagement does not equal a strong relationship -- the CSM provides the qualitative read |

## Confidence and Limitations

- **High confidence** for contact tracking and engagement recency -- structured data from CRM and activity logs
- **High confidence** for coverage status computation -- deterministic comparison of engagement dates to expected cadence
- **Medium confidence** for structural risk detection -- the risks are real patterns, but the severity depends on account context the agent may not fully capture
- **Low confidence** for stakeholder classification accuracy. Champion, Economic Buyer, and Detractor labels come from CSM input and may be outdated, optimistic, or incorrect. The skill prompts for review but cannot validate
- Cannot assess relationship quality. A contact touched last week may still be disengaged emotionally. A contact not touched in 45 days may still be a strong advocate. Engagement frequency is a proxy, not a measure, of relationship health
- Cannot detect contacts who matter but are not in the CRM (informal influencers, board members, procurement gatekeepers, executive assistants who control calendar access)
- Cannot account for relationship dynamics that happen outside observable channels (conversations at conferences, hallway chats, personal connections between executives)

## Dependencies

**Required:**
- CRM API (contact records, activity logs)
- Calendar integration (meeting data)
- Email integration (email engagement data)

**Strongly recommended:**
- ra-engagement-tracker (detailed engagement metrics per contact)
- ra-stakeholder-change-detector (alerts on contact changes)
- bi-account-brief (stakeholder map feeds into account context for every human decision point)
- lo-check-in-scheduler (cadence alignment with stakeholder coverage expectations)

**Downstream consumers:**
- bi-account-brief (stakeholder section of account briefs)
- bi-risk-detector (single-thread and champion-at-risk as risk signals)
- lo-handoff-manager (stakeholder context for account transitions)
- cm-commercial-case-builder (stakeholder coverage for expansion readiness)
- All human decision points (who to engage, how to approach, who has influence)

## References

- `references/stakeholder-classification.md` -- Type definitions, classification criteria, and review process

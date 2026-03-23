---
name: ca-advocacy-tracker
description: Manages customer advocacy programmes including reference tracking, case study pipeline, review site engagement, testimonial collection, and NPS follow-up workflows. Identifies advocacy-ready accounts, manages the advocacy pipeline, matches advocates to requests, and prevents advocate fatigue. Use when asked to manage customer references, track case study progress, coordinate review requests, build an advocacy programme, identify potential advocates, follow up on NPS promoters, or when any workflow needs to know which customers are available and willing to advocate. Also triggers for questions about customer references, testimonials, case studies, G2 reviews, advocacy programme management, or NPS follow-up strategy.
license: MIT
metadata:
  version: "1.0.0"
  pillar: customer-advocacy
  category: advocacy-engine
---

# Advocacy Tracker

Manages customer advocacy programmes -- references, case studies, reviews, testimonials, and NPS follow-up. Turns satisfied customers into active advocates through structured programme management. Part of the Customer Advocacy & Community pillar.

This is a **tracking and coordination** skill. It manages the pipeline and logistics. The relationship work -- asking a customer to advocate, coaching them through a case study, maintaining the goodwill that makes advocacy possible -- is entirely human territory. Advocacy is a withdrawal from the relationship bank account. The skill ensures you make smart withdrawals; the CSM ensures the balance is sufficient.

## When to Run

- **Triggered**: When bi-health-score identifies a promoter-level NPS response or sustained health score >85 for 90+ days
- **Triggered**: When pa-value-reporter generates strong, quantifiable ROI evidence (potential case study material)
- **On-demand**: When sales or marketing requests a customer reference for a specific use case or segment
- **Scheduled**: Monthly advocacy pipeline review and advocate health check

## Core Execution Logic

### Step 1: Identify Advocacy Candidates

Score accounts for advocacy readiness using a composite of signals:

| Signal | Weight | Source | Threshold |
|--------|--------|--------|-----------|
| NPS score 9-10 (Promoter) | 25% | Survey tool | Score must be from the last 180 days |
| Health score sustained >85 | 25% | bi-health-score | Sustained for 90+ consecutive days -- not a one-time spike |
| Quantifiable ROI evidence | 20% | pa-value-reporter | At least one measurable outcome the customer has confirmed |
| Champion with high engagement | 15% | ra-stakeholder-mapper + ra-engagement-tracker | Champion in Active engagement status |
| No open risk signals | Filter | bi-risk-detector | Any active risk signal disqualifies the account |
| No unresolved P1/P2 tickets | Filter | Support platform | Active escalation disqualifies the account |

**Advocacy readiness score**: Weighted sum of signals (0-100). Accounts scoring >70 are candidates.

**Critical filter**: Never ask a customer to advocate if they have an unresolved issue, declining health, or active risk signal. This is absolute. No override, no exceptions. An advocacy ask on an unhappy customer does not just fail -- it actively damages the relationship and confirms to the customer that you do not understand their situation.

### Step 2: Manage Advocacy Types

Each advocacy type has different preparation, execution, and follow-up requirements:

| Type | Prep Effort | Customer Commitment | Value to Business | Fatigue Impact |
|------|-----------|-------------------|------------------|---------------|
| Reference call | Low -- brief the advocate on the prospect | 30-45 minutes | High -- directly influences pipeline | Medium -- each call takes time and emotional energy |
| Case study | High -- interview, review cycles, legal approval | 2-4 hours total across 4-8 weeks | Very high -- reusable across all sales motions | High -- significant effort, expect 4-6 weeks of engagement |
| Review site (G2, Capterra) | Low -- send the link, ask for 5 minutes | 5-10 minutes | Medium -- builds credibility at scale | Low -- one-time ask |
| Testimonial quote | Low -- draft the quote, get approval | 10 minutes for review | Medium -- website and sales collateral | Low |
| Event speaking | High -- prep, rehearsal, travel | Half day to full day | Very high -- thought leadership and social proof | Very high -- ask sparingly |
| NPS follow-up | Low -- structured response workflow | 0 (they already gave the score) | Medium -- converts sentiment into actionable advocacy | None -- this is capitalising on existing goodwill |

### Step 3: Manage the Advocacy Pipeline

Track each advocacy opportunity through defined stages:

| Stage | Definition | Typical Duration |
|-------|-----------|-----------------|
| Candidate identified | Account meets readiness criteria | N/A -- enters pipeline here |
| CSM approved | CSM confirms the relationship supports an ask | 1-3 days |
| Customer approached | CSM has made the ask | 1-5 days |
| Customer agreed | Customer has said yes, logistics begin | 1-2 days |
| In progress | Advocacy activity is underway | Varies by type (1 day for a review, 4-8 weeks for a case study) |
| Completed | Deliverable is live (review published, case study approved, reference call done) | -- |
| Declined | Customer said no | Log reason. Do not re-ask for 6 months minimum |

### Step 4: Match Advocates to Requests

When sales or marketing requests a reference or case study:

1. Filter by request criteria: industry, company size, use case, product tier, geography
2. Filter by availability: has this advocate been activated recently? (See fatigue management below)
3. Filter by suitability: is this advocate articulate, senior enough for the prospect's audience, and genuinely enthusiastic?
4. Present matched candidates to the CSM for approval before any outreach
5. CSM decides whether to make the ask based on relationship context

### Step 5: Prevent Advocate Fatigue

Advocacy fatigue is the silent killer of advocacy programmes. Track and manage:

| Metric | Threshold | Action |
|--------|-----------|--------|
| Activations in last 6 months | >3 activations | Flag as "at risk of fatigue" -- rotate to other advocates |
| Last activation date | <30 days ago | Do not activate again until 30 days have passed |
| Declined after previously agreeing | Any instance | Investigate with CSM. May indicate fatigue already setting in |
| Sentiment post-advocacy | Neutral or negative shift after an activation | Flag for CSM -- the advocacy experience may not have been positive |

**Rotation principle**: Spread requests across the advocate pool. Relying on 3-4 go-to advocates while ignoring others is the default failure mode of most advocacy programmes. The skill surfaces the full pool and flags over-reliance.

### Step 6: NPS Follow-Up Workflow

NPS responses trigger immediate structured follow-up:

| Score Band | Follow-Up | Timing |
|-----------|-----------|--------|
| Promoters (9-10) | Thank them. Ask what they value most (this is testimonial material). Assess advocacy readiness. Soft advocacy ask if appropriate | Within 48 hours of response |
| Passives (7-8) | Thank them. Ask what would make them a 9 or 10. This is product feedback and adoption opportunity, not advocacy territory | Within 72 hours |
| Detractors (0-6) | Do not ask for advocacy. Route to bi-risk-detector. CSM addresses the underlying issue | Immediate routing. CSM contact within 24 hours |

## Output Format

```json
{
  "programme_health": {
    "total_advocates_active": 18,
    "pipeline": {
      "candidates": 24,
      "csm_approved": 12,
      "customer_agreed": 5,
      "in_progress": 3,
      "completed_this_quarter": 8,
      "declined_this_quarter": 2
    },
    "fatigue_risk_advocates": 2,
    "overused_advocates": 1
  },
  "active_advocates": [
    {
      "contact": "Tom Chen",
      "account": "Acme Corp",
      "account_arr": 85000,
      "account_health": 88,
      "advocate_since": "2025-06-01",
      "types_completed": ["case_study", "g2_review", "reference_call"],
      "activations_6mo": 2,
      "last_activated": "2026-02-15",
      "fatigue_risk": "low",
      "available_for": ["reference_call", "event_speaking"],
      "notes": "Enthusiastic advocate. Well-spoken. Best for mid-market prospects in SaaS"
    }
  ],
  "pending_requests": [
    {
      "request_id": "REQ-2026-0034",
      "request_from": "Enterprise AE -- Tom Rivera",
      "criteria": "Financial services, enterprise, reporting use case",
      "matched_candidates": 3,
      "status": "awaiting_csm_approval",
      "requested_date": "2026-03-08",
      "needed_by": "2026-03-20"
    }
  ],
  "nps_follow_up_queue": [
    {
      "contact": "Lisa Park",
      "account": "Gamma Corp",
      "nps_score": 9,
      "response_date": "2026-03-09",
      "verbatim": "The automation features have transformed how our team works",
      "follow_up_status": "pending",
      "recommended_action": "Thank them. The verbatim is strong testimonial material. Assess willingness for a case study"
    }
  ]
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Candidate approval | Readiness score, health data, value evidence | Whether the relationship supports an ask right now. The data says the account is healthy; the CSM knows if the timing is right |
| The ask itself | Advocacy type, suggested framing, relationship context | How and when to ask. Advocacy requests must feel personal and genuine. A templated ask is worse than no ask |
| Request matching | Matched candidates with suitability notes | Which advocate is the best fit for this specific request. Chemistry, seniority match, and communication style matter |
| Fatigue management | Activation history, fatigue risk flags | Whether to activate a high-use advocate one more time or find an alternative. Some advocates enjoy the spotlight; others do not |
| Declined response | Decline reason from customer | Whether to ask again later (with a different type or framing) or permanently remove from the programme. Respect the decision |
| NPS follow-up | Score, verbatim, account context | How to follow up and whether to pursue advocacy. A promoter score with a weak verbatim may not be an advocacy candidate |

## Confidence and Limitations

- **High confidence** for pipeline tracking and advocate management -- structured data operations with defined lifecycle stages
- **High confidence** for fatigue detection -- activation counts and dates are factual
- **Medium confidence** for advocacy readiness scoring -- health and NPS data are strong signals, but willingness to advocate depends on personal disposition the agent cannot assess. A healthy, satisfied customer may still decline because they do not enjoy public endorsement
- **Low confidence** for predicting advocacy quality. A willing advocate may not be an effective spokesperson. Some customers are enthusiastic but inarticulate; others are reluctant but compelling when they do speak. The CSM assesses fit
- The critical filter (no advocacy asks on unhealthy accounts) is absolute. This is not a recommendation -- it is a rule. The skill will not surface accounts with active risk signals as candidates regardless of other factors
- Cannot predict the impact of an advocacy activity on the relationship. Some advocates feel valued by the recognition; others feel used. Post-activation sentiment tracking is the feedback loop
- Case study timelines are typically underestimated. The bottleneck is almost always customer-side approval (legal review, executive sign-off, wordsmithing). Budget 2x the expected timeline

## Dependencies

**Required:**
- CRM API (account data, contact data, advocacy activity logging)
- bi-health-score (advocacy readiness filtering -- the critical filter)

**Strongly recommended:**
- Survey tool (NPS data for follow-up workflow and readiness scoring)
- pa-value-reporter (ROI evidence for case study material)
- ra-stakeholder-mapper (champion identification for advocacy routing)
- ra-engagement-tracker (engagement health as readiness input)

**Downstream consumers:**
- Marketing team (case studies, testimonials, review site content)
- Sales team (reference call matches)
- CS leadership (programme health metrics)
- cc-report-generator (advocacy programme data for quarterly reporting)

## References

- `references/advocacy-playbook.md` -- Best practices for each advocacy type, asking frameworks, and fatigue prevention strategies

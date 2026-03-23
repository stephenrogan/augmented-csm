---
name: ca-community-monitor
description: Tracks customer engagement in community channels, surfaces unanswered questions, identifies potential advocates from activity patterns, and detects sentiment shifts in community discussions. Use when asked to monitor community engagement, track forum activity, identify community advocates, detect community sentiment, manage community health, or when any workflow needs insight into peer-to-peer customer engagement. Also triggers for questions about community management, forum monitoring, peer engagement, community-driven support, or advocate identification from community activity.
license: MIT
metadata:
  version: "1.0.0"
  pillar: customer-advocacy
  category: advocacy-engine
---

# Community Monitor

Tracks customer engagement in community channels -- forums, Slack communities, user groups, and peer-to-peer platforms. Surfaces actionable signals for CS and identifies advocates from activity patterns. Part of the Customer Advocacy & Community pillar.

This is a **monitoring and signal detection** skill. It observes community activity and surfaces patterns. Community management strategy, moderation, and direct engagement are human-led.

**Applicability note:** This skill is only relevant if the product maintains a customer community (forum, Slack workspace, user group, etc.). If no community exists, this skill is not applicable and should not be activated.

## When to Run

- **Continuous**: Monitors community channels for signals in real-time or near-real-time
- **Scheduled**: Weekly community health report
- **On-demand**: When a CSM requests community engagement data for a specific account

## Core Execution Logic

### Step 1: Track Activity per Account and Contact

For each customer contact active in the community, monitor:

| Metric | Definition | Why It Matters |
|--------|-----------|---------------|
| Post frequency | Posts and comments per 30-day period | Engagement level |
| Response rate | Replies to other customers' questions | Indicator of advocacy behaviour |
| Topic engagement | Categories or channels they participate in | Shows what they care about |
| Sentiment | Positive, neutral, or negative tone per post | Early warning for frustration or strong advocacy |
| Help ratio | Answers given / questions asked | High ratio = potential advocate |
| Recency | Days since last community activity | Engagement trend |

Link community members to CRM accounts using email domain or explicit account mapping.

### Step 2: Detect Actionable Signals

| Signal | Detection Criteria | Urgency | Routing |
|--------|-------------------|---------|---------|
| Unanswered question | Post from a customer with no reply after 48 hours | High | Alert CSM or community manager -- customer waiting for help in public |
| Negative sentiment post | Frustrated, critical, or angry language detected | High | Alert CSM -- public frustration needs attention before it influences other customers |
| Competitor mention | Evaluation or comparison language referencing a competitor | High | Route to bi-competitive-intel as a community-sourced signal |
| Feature discussion thread | Multiple customers discussing a missing capability | Medium | Route to pa-feedback-aggregator as community-validated demand |
| High-value contributor emerging | Customer contact answers 5+ questions in 30 days | Medium | Flag for ca-advocacy-tracker as potential advocate |
| New community member | Customer contact joins community for the first time | Low | Log engagement signal in ra-engagement-tracker |
| Sudden silence | Previously active member has no activity in 30+ days | Low | Log for CSM awareness -- may correlate with disengagement from the product |
| Positive testimonial | Enthusiastic praise or recommendation in a public post | Low | Flag for ca-advocacy-tracker -- potential testimonial or case study material |

### Step 3: Identify Community Advocates

Customers who actively help other customers are the highest-quality advocates:

**Advocate scoring:**

| Factor | Weight | Measurement |
|--------|--------|-------------|
| Help ratio (answers/questions) | 30% | Ratio >2:1 indicates a helper, not just a participant |
| Response quality | 25% | Posts that receive "helpful" votes or positive replies |
| Consistency | 20% | Active for 3+ consecutive months (not a one-time burst) |
| Reach | 15% | Posts that receive 5+ views or 3+ replies (indicating influence) |
| Sentiment | 10% | Consistently positive tone (advocates must be genuine, not compensated) |

**Advocate tiers:**
- **Power advocate** (top 5% of community contributors): Candidate for all advocacy types -- references, case studies, events, advisory board
- **Active contributor** (top 15%): Candidate for references and reviews
- **Participant** (active but not contributing): Not yet an advocate. Nurture through engagement

### Step 4: Generate Community Health Report

Weekly report for CS leadership and community management:

```json
{
  "report_date": "2026-03-10",
  "community_health": {
    "active_members_30d": 142,
    "new_members_30d": 18,
    "churned_members_30d": 4,
    "total_posts_30d": 234,
    "total_replies_30d": 412,
    "questions_asked_30d": 67,
    "questions_answered_30d": 61,
    "unanswered_questions": 6,
    "avg_response_time_hours": 6.2,
    "sentiment_distribution": {
      "positive": 0.62,
      "neutral": 0.31,
      "negative": 0.07
    },
    "trending_topics": ["API rate limits", "Custom reporting", "Q2 release preview"]
  },
  "signals": [
    {
      "type": "unanswered_question",
      "account": "Beta Inc",
      "contact": "Lisa Park",
      "post_summary": "Question about bulk import performance with large datasets",
      "hours_waiting": 52,
      "urgency": "high",
      "recommended_action": "Community manager or CSM respond. Customer waiting publicly"
    },
    {
      "type": "negative_sentiment",
      "account": "Gamma Corp",
      "contact": "Mike Chen",
      "post_summary": "Frustrated with reporting limitations. Third post on this topic in 2 weeks",
      "urgency": "high",
      "recommended_action": "CSM outreach privately. Do not let frustration build in public channel"
    },
    {
      "type": "competitor_mention",
      "account": "Delta Ltd",
      "contact": "Sarah Kim",
      "post_summary": "Asked if anyone has compared our reporting to Competitor X",
      "urgency": "medium",
      "recommended_action": "Route to bi-competitive-intel. CSM assess whether this is casual curiosity or active evaluation"
    }
  ],
  "advocates": {
    "power_advocates": [
      {
        "contact": "Tom Chen",
        "account": "Acme Corp",
        "posts_30d": 18,
        "helpful_replies": 12,
        "help_ratio": 3.0,
        "months_active": 8,
        "advocate_score": 92,
        "already_in_advocacy_programme": true
      }
    ],
    "emerging_advocates": [
      {
        "contact": "Anna Lee",
        "account": "Echo Systems",
        "posts_30d": 8,
        "helpful_replies": 5,
        "help_ratio": 2.5,
        "months_active": 3,
        "advocate_score": 71,
        "recommendation": "Approaching power advocate status. CSM should acknowledge their community contributions"
      }
    ]
  },
  "period_over_period": {
    "active_members_change": "+6%",
    "response_time_change": "-0.8 hours (improved)",
    "sentiment_trend": "stable",
    "unanswered_questions_change": "-2 (improved)"
  }
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Unanswered question response | Question content, customer account, waiting time | Whether the community manager, CSM, or product team should respond, and what the response should be |
| Negative sentiment response | Post content, customer context, prior posts | Whether to respond publicly, reach out privately, or monitor. Public responses must be handled carefully |
| Advocate development | Advocate scores, contribution history, account health | Whether to formally recognise the advocate, invite them into the advocacy programme, or let organic contribution continue |
| Competitive mention follow-up | Post content, customer account, evaluation indicators | Whether this is casual or signals active evaluation. Determines whether bi-competitive-intel escalation is warranted |
| Community strategy | Health metrics, trends, topic analysis | What content to create, which discussions to seed, how to grow engagement. Strategic decisions are human territory |

## Confidence and Limitations

- **High confidence** for activity tracking and unanswered question detection -- quantitative metrics from the community platform are objective
- **High confidence** for advocate identification from activity patterns -- help ratio and consistency are measurable
- **Medium confidence** for sentiment analysis -- community posts can be ambiguous, sarcastic, or context-dependent. NLP sentiment detection is a starting point; human review is needed for high-stakes posts
- **Medium confidence** for competitor mention detection -- depends on keyword registry quality (shared with bi-competitive-intel)
- **Low confidence** for interpreting advocate motivation. High posting frequency could indicate enthusiasm (genuine advocate) or frustration (frequent poster because they keep encountering issues). The help ratio helps distinguish, but the CSM must validate
- Only applicable if a customer community exists. Many B2B SaaS products do not maintain one
- Cannot moderate content or enforce community guidelines -- that is human and platform responsibility
- Cannot attribute community engagement to retention outcomes with statistical confidence -- correlation exists but causation is difficult to prove
- Community signals are public. A frustrated post is visible to all customers and prospects. Response urgency is higher than for private feedback channels

## Dependencies

**Required:**
- Community platform API (forum, Slack workspace, or equivalent)
- CRM API (to link community members to customer accounts)

**Strongly recommended:**
- bi-competitive-intel (for routing competitive mentions)
- pa-feedback-aggregator (for routing feature discussion threads)
- ca-advocacy-tracker (for advocate pipeline management)
- ra-engagement-tracker (for logging community engagement as a touchpoint channel)

**Downstream consumers:**
- ca-advocacy-tracker (advocate candidates)
- bi-competitive-intel (competitive signals from community)
- pa-feedback-aggregator (feature feedback from community discussions)
- CS leadership (weekly community health report)

## References

- `references/community-signals.md` -- Signal definitions, detection criteria, and routing rules

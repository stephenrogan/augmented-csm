---
name: bi-competitive-intel
description: Monitors for signals that a customer may be evaluating alternatives or has been approached by a competitor. Surfaces early warning so the CSM can intervene before a formal evaluation begins. Use when asked to detect competitive threats, monitor for churn to competitors, identify accounts evaluating alternatives, track competitor mentions, build competitive displacement alerts, assess competitive risk across the portfolio, or when any workflow needs to know if a customer is looking at other vendors. Also triggers for questions about win-back, competitor tracking, evaluation detection, or displacement risk.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: book-intelligence
  category: detection-layer
---

# Competitive Intelligence Monitor

Monitors for signals that customers may be evaluating or being approached by competitors. Part of the Book Intelligence detection layer -- surfaces early warning so the CSM can intervene before a formal evaluation process crystallises.

This is a **detection and alerting** skill. It identifies competitive signals and surfaces them with evidence. It never contacts the customer about competitive concerns or initiates win-back plays. The response strategy is entirely human territory -- it depends on relationship context, account value, and competitive positioning that the agent cannot assess.

## When to Run

- **Continuous**: Event-based monitoring of support tickets and call transcripts for keyword matches
- **Scheduled**: Weekly scan of behavioural signals (data export activity, engagement patterns)
- **On-demand**: When a human requests a competitive risk assessment for a specific account

## Competitor Keyword Registry

Maintain a registry of competitor names, products, and evaluation-related terms. The registry should be reviewed and updated quarterly.

**Registry categories:**

| Category | Examples | Notes |
|----------|---------|-------|
| Direct competitors | [Company names, product names] | Primary competitors in your market |
| Adjacent competitors | [Company names expanding into your space] | Products that overlap with part of your value proposition |
| Evaluation language | "alternative," "switch," "migrate," "evaluate," "compare," "looking at options," "RFP" | Language that indicates active evaluation regardless of specific competitor |
| Migration language | "data export," "transition plan," "wind down," "offboarding," "contract termination" | Language that indicates the evaluation has already progressed to a decision |

See `references/competitor-registry.md` for the full registry and maintenance process.

## Core Execution Logic

### Step 1: Monitor Direct Mention Signals

Scan incoming data for keyword registry matches:

**Support tickets:**
- Scan ticket subject lines and body text for competitor names and evaluation language
- Weight: subject line matches are stronger signals than body text matches
- Context matters: "We use [competitor] for [different use case]" is not a risk signal. "[Competitor] offered us a demo for [your use case]" is

**Call transcripts:**
- Scan transcripts from Gong, Chorus, or equivalent for competitor mentions
- Pay attention to the conversation context: who raised the competitor, in what framing
- Weight: Customer-initiated competitor mention is a stronger signal than CSM-initiated

**Email content (if integration available):**
- Scan inbound customer emails for competitor names and evaluation language
- Weight: Mentions in decision-maker emails are stronger than in end-user emails

### Step 2: Monitor Behavioural Signals

Detect evaluation behaviour that does not involve explicit mentions:

| Signal | Detection Method | Strength |
|--------|-----------------|----------|
| Data export activity spike | Product analytics: sudden increase in export API calls, bulk downloads, or data extraction feature usage | Medium |
| Admin/API documentation access | Product analytics: increased visits to API docs, data schema pages, migration guides | Medium |
| Decreased engagement + no clear cause | Engagement score declining with no correlated support issue, product change, or seasonal pattern | Low-Medium |
| Concurrent usage of evaluation accounts | Product analytics: new user accounts from the same company domain on a competitor's platform (only if cross-platform tracking is available) | High (but rarely available) |

### Step 3: Score Signal Strength

| Strength Level | Criteria | Examples |
|---------------|----------|---------|
| High | Direct competitor mention in evaluative context by decision-maker | "We are evaluating [competitor] for next quarter" in an email from the VP |
| Medium | Competitor mention without evaluative context, or behavioural signal with clear pattern | Competitor mentioned in a support ticket asking about feature comparison; data export spike |
| Low | Engagement decline without explicit competitive indicators | Reduced login frequency with no correlated explanation |

### Step 4: Correlate with Other Risk Signals

A competitive signal combined with other risk signals amplifies urgency:
- Competitive signal + health decline = Elevated priority
- Competitive signal + champion departure = Critical priority
- Competitive signal + renewal within 90 days = Immediate escalation
- Competitive signal alone, healthy account = Monitor and prepare

### Step 5: Generate Alert

```json
{
  "account_id": "string",
  "account_name": "string",
  "alert_type": "competitive_signal",
  "signal_strength": "high",
  "signal_source": "support_ticket",
  "evidence": {
    "source_type": "support_ticket",
    "source_id": "TICKET-8823",
    "date": "2026-03-08",
    "content_summary": "Customer asked support team how to export all historical data in a format compatible with [Competitor] import tool",
    "contact_role": "Admin (IT Director)"
  },
  "correlated_signals": [
    { "type": "engagement_decline", "detail": "Meeting attendance dropped 40% in last 30 days" }
  ],
  "account_context": {
    "arr": 62000,
    "health_score": 68,
    "days_to_renewal": 112
  },
  "recommended_response_framework": "Direct competitive evaluation detected. Do not lead with competitive positioning. First, investigate whether there is an unmet need driving the evaluation. Address the root cause before defending against the competitor.",
  "urgency": "immediate"
}
```

### Step 6: Track Signal Lifecycle

Each competitive signal has a lifecycle:
1. **New**: Signal detected, alert generated
2. **Acknowledged**: CSM has seen and accepted the alert
3. **Investigating**: CSM is actively gathering more information
4. **Addressed**: CSM has engaged the customer and is working to retain
5. **Resolved**: Competitive threat neutralised (customer committed to staying)
6. **Lost**: Customer has churned to competitor

Track the lifecycle to measure response effectiveness and time-to-response.

## Output Format

**Competitive threat alert:** Individual alert per signal detection (see Step 5 above).

**Monthly competitive landscape report:**
- Active threats by competitor (which competitor is winning the most evaluations)
- Signal source distribution (where are competitive signals detected most frequently)
- Win/loss tracking (outcomes of competitive engagements)
- Common competitive triggers (what drives customers to evaluate alternatives)
- Average response time (how quickly CSMs engage after a competitive signal)

## Handoff to Human

**All competitive signals surface to the CSM immediately.** This is high-judgment territory -- the response depends entirely on relationship context and competitive positioning.

| Signal Strength | Routing | Urgency |
|----------------|---------|---------|
| High (direct mention, evaluative) | Alert CSM + notify CS manager | Immediate |
| Medium (behavioural or indirect) | Alert CSM | Same day |
| Low (engagement decline only) | Include in risk digest | Next business day |
| Any strength + renewal <90 days | Alert CSM + notify CS manager + CRO flag | Immediate |

See `references/human-decision-guide.md` for the response framework.

## Confidence and Limitations

- **Medium overall confidence**. Direct keyword mentions are high-confidence. Behavioural signals are suggestive, not conclusive
- The agent must present behavioural signals as "possible competitive signal," never "customer is leaving"
- False positives are common with keyword matching. "We also use [competitor] for [unrelated purpose]" is not a threat signal. Context analysis reduces but does not eliminate false positives
- Cannot detect competitive evaluations that happen entirely outside observable channels (e.g., the economic buyer receives a competitor pitch at a conference and initiates an evaluation without any digital trace)
- NLP-based content scanning requires ongoing tuning. New competitors, new product names, and evolving evaluation language require registry updates

## Dependencies

**Required:**
- Support platform API (ticket content for keyword scanning)
- Competitor keyword registry (maintained, reviewed quarterly)

**Strongly recommended:**
- Call transcript integration (Gong, Chorus) for conversation-level detection
- Product analytics (for behavioural signals: export activity, documentation access)
- CRM activity data (engagement patterns)

**Optional:**
- Email content integration (for inbound email scanning)
- Review site monitoring (G2, Capterra -- for public competitive activity)
- Web tracking (for migration guide or comparison page visits)

**Downstream consumers:**
- `bi-risk-detector` (competitive signals as risk input)
- `bi-account-brief` (competitive flags in account context)
- Human response queue
- Monthly competitive landscape reporting

## References

- `references/competitor-registry.md` -- Full keyword registry and maintenance process
- `references/human-decision-guide.md` -- Response framework for competitive signals

---
name: cc-email-drafter
description: Drafts customer-facing emails including check-ins, follow-ups, meeting confirmations, milestone notifications, and routine communications. Personalises with account data and calibrates tone by segment and relationship context. Use when asked to write a customer email, draft a follow-up, compose a check-in message, create an email sequence, or when any lifecycle workflow needs to send a templated communication. Also triggers for questions about email templates, outreach copy, customer communication drafting, or tone calibration for customer emails.
license: MIT
metadata:
  version: "1.0.0"
  pillar: communication-content
  category: content-engine
---

# Email Drafter

Drafts customer-facing emails for routine communications across the lifecycle. Personalises with account-specific data, calibrates tone by segment and relationship context, and outputs review-ready drafts for CSM approval before sending. Part of the Communication & Content Production pillar.

This is a **content generation** skill. It produces drafts. It never sends emails autonomously -- every customer-facing communication passes through the CSM for review, edit, and approval. The human decides what goes out.

## When to Run

- **Triggered**: By lifecycle orchestration skills when a communication is due:
  - lo-onboarding-orchestrator: welcome emails, onboarding check-ins, milestone congratulations
  - lo-check-in-scheduler: cadence-driven check-in emails
  - lo-renewal-manager: renewal conversation openers, renewal confirmations
  - lo-milestone-tracker: milestone achievement notifications
  - lo-qbr-orchestrator: QBR scheduling and follow-up emails
- **Triggered**: By cc-call-summariser after a call (post-call follow-up email)
- **On-demand**: When a CSM requests a draft for a specific purpose

## Core Execution Logic

### Step 1: Determine Email Context

From the triggering event or CSM request, assemble:

| Context Element | Source | Why It Matters |
|----------------|--------|---------------|
| Email category | Trigger event type (check-in, follow-up, milestone, renewal, welcome, re-engagement, scheduling) | Determines template, structure, and length |
| Recipient | CRM contact record | Name, title, preferred channel, engagement history |
| Account context | bi-account-brief | Health, recent activity, open items, usage trend -- personalisation data |
| Relationship stage | lo-onboarding-orchestrator or CRM lifecycle field | New customer emails differ from mature relationship emails |
| Segment | CRM account record | Determines tone register (enterprise vs. mid-market vs. SMB) |
| Recent interactions | ra-engagement-tracker | When was the last touchpoint and what channel -- avoids "just checking in" when you spoke yesterday |
| Open items | lo-sla-monitor | Outstanding commitments that should be referenced or addressed |
| Sensitive context | bi-risk-detector, support platform | Is the account at risk? Is there an open escalation? Tone must reflect this |

### Step 2: Select and Populate Template

Each email category has a template with required and optional elements:

| Category | Trigger | Structure | Target Length |
|----------|---------|-----------|--------------|
| Welcome | Deal close / handoff | Introduce yourself, set expectations, provide first resources, schedule kickoff | 100-150 words |
| Onboarding check-in | Onboarding milestones (day 7, 14, 30) | Reference milestone progress, offer help, provide next step | 60-100 words |
| Cadence check-in | Scheduled touchpoint | Account-specific observation or question, one clear ask | 50-100 words |
| Post-call follow-up | Call completion | Summary of discussion, action items with owners, next touchpoint | 100-150 words |
| Milestone congratulation | Milestone achieved | Acknowledge the achievement specifically, connect to their goals, suggest next step | 50-80 words |
| QBR scheduling | T-30 before QBR | Propose dates, explain what the QBR will cover, ask for their priorities | 60-80 words |
| Renewal opener | T-90 before renewal | Lead with value delivered, transition to renewal discussion, propose timing | 100-150 words |
| Value highlight | pa-value-reporter output trigger | Share a specific metric the customer will find interesting | 80-120 words |
| Nudge (no reply) | 5+ business days with no response | Shorter and lighter than the original email. New angle or question, not a repeat | 30-50 words |
| Re-engagement | 30+ days since last touchpoint, customer unresponsive | Offer value (not just "checking in"), provide a specific reason to re-engage | 60-100 words |

For each email:
1. Select the template matching the category
2. Populate personalisation fields: account name, contact name, specific metrics, open items, milestone details
3. Insert context-specific content: the observation, question, or data point that makes this email relevant to this customer right now
4. Apply tone calibration (see below)

### Step 3: Calibrate Tone

| Segment | Register | Example Opening |
|---------|----------|----------------|
| Enterprise | Formal professional | "Thank you for making time for our review today. Here is a summary of what we covered and the next steps we agreed on." |
| Mid-Market | Warm professional | "Thanks for the time today, Tom. Great conversation -- here is a quick recap." |
| SMB | Casual direct | "Thanks for the chat. Quick recap below." |

**Situation-based overrides** (these override the segment default):

| Situation | Tone Adjustment |
|-----------|----------------|
| Account at risk | Empathetic, solution-oriented. No false optimism. Do not pretend everything is fine |
| Post-escalation | Accountable, specific, forward-looking. Acknowledge the issue, state what has been done |
| Expansion context | Value-led, consultative. Frame expansion as helping them, not selling to them |
| New relationship | Warm but professional. Establish credibility before informality |
| Customer frustrated | Acknowledge frustration first. Do not lead with data or positivity when they are upset |
| Champion departure | Respectful, reassuring. Emphasise continuity and commitment to the account |

### Step 4: Apply Quality Gates

Before presenting the draft:

| Gate | Check | Fail Behaviour |
|------|-------|---------------|
| Length | Under 200 words for routine comms, under 150 for check-ins, under 50 for nudges | Cut. Shorter is almost always better |
| Single CTA | Exactly one clear action item or question per email | Remove secondary asks. Multiple CTAs reduce response rate |
| Subject line | Specific to this email's content. Under 50 characters | Rewrite. "Follow-up" alone fails. "Follow-up: API docs and April onboarding" succeeds |
| Personalisation | Contains at least one data point specific to this account | If no personalisation data is available, flag to CSM -- a generic email may not be worth sending |
| Tone match | Tone matches segment and situation context | Adjust. An enterprise-tone email to an SMB customer sounds corporate. An SMB-tone email to a CFO sounds unprofessional |
| Recency check | Not sending a check-in within 3 days of the last touchpoint | Suppress or adjust -- "just checking in" the day after a call is noise |
| Sensitivity check | Account is not at risk or in escalation (unless the email is specifically about the risk/escalation) | If at risk: flag to CSM. A routine check-in email to a customer in crisis is tone-deaf |

### Step 5: Output Draft for Review

```json
{
  "draft_id": "email-2026-0342",
  "account_id": "string",
  "recipient": {
    "name": "Tom Chen",
    "email": "tom@acme.com",
    "role": "VP Engineering"
  },
  "category": "post_call_follow_up",
  "trigger_source": "cc-call-summariser",
  "subject": "Follow-up: API docs and April onboarding",
  "body": "Hi Tom,\n\nThanks for the time today. Great to hear the API latency fix is holding.\n\nQuick recap:\n- API documentation for Lisa's team: I will send this by Friday\n- Latency monitoring: we will confirm resolution after the 7-day window (by March 17)\n- April onboarding: you will share the start dates and headcount plan by March 21\n\nI will also start pulling together a training plan for the new engineers once we have the headcount confirmed.\n\nTalk next week.\n\nBest,\nJane",
  "personalisation_fields_used": ["contact_name", "api_docs_commitment", "latency_ticket", "onboarding_headcount"],
  "tone": "warm_professional",
  "word_count": 98,
  "quality_gates": {
    "length": "pass",
    "single_cta": "pass -- no explicit CTA needed, follow-up is a recap",
    "subject_specificity": "pass",
    "personalisation": "pass",
    "tone_match": "pass -- mid-market, warm professional",
    "recency_check": "pass -- post-call, same day is expected",
    "sensitivity_check": "pass -- no risk signals"
  },
  "suggested_send": "2026-03-10T16:00:00Z",
  "requires_csm_review": true
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Send or not send | Draft with quality gate results | Whether this email should go out at all. Sometimes a call is better. Sometimes silence is better. The agent does not know when not to email |
| Tone adjustment | Draft calibrated to segment and situation defaults | Whether the tone matches the relationship reality. A contact who jokes on calls may get a more informal email than the segment suggests |
| Content editing | Personalised draft with all data points | What to add, remove, or rephrase. The CSM may add a personal touch ("congrats on the new hire") or remove a data point the customer should not see in writing |
| Timing | Suggested send time based on timezone | When to actually send. Friday afternoon emails get buried. Monday morning emails compete with the inbox flood. The CSM knows this customer's rhythm |
| Sensitivity filtering | Sensitivity check flag if applicable | For at-risk accounts: whether to proceed with routine communication or hold until the risk situation is addressed |

## Confidence and Limitations

- **High confidence** for routine lifecycle emails (check-ins, follow-ups, scheduling, milestone notifications) -- these are pattern-based with data personalisation. The templates are well-defined and the data insertion is deterministic
- **High confidence** for quality gate application -- the checks are objective (word count, subject length, recency)
- **Medium confidence** for tone calibration -- segment-based rules are a sensible default, but individual relationships have their own register. A CSM who has built informal rapport with an enterprise contact should not send a formal email just because the segment says so
- **Medium confidence** for personalisation relevance -- the skill includes the most recent and significant data points, but the CSM may know that a specific metric is sensitive or that the customer will not care about a milestone the system thinks is important
- **Low confidence** for sensitive situations. Churn risk emails, escalation responses, bad news, and relationship repair communications should be heavily edited or drafted from scratch by the CSM. The skill can provide a starting structure but the human layer is critical for anything that carries relationship risk
- Cannot assess whether the email will be well-received. The draft may be perfectly constructed and still land poorly because the customer is having a bad day, is frustrated about something unlogged, or simply does not like email
- Cannot determine optimal send time with precision. Timezone-based scheduling is a heuristic. The CSM knows whether this contact reads email in the morning or evening, and whether they respond better to mid-week or Monday outreach

## Dependencies

**Required:**
- CRM API (contact data, activity history for personalisation and recency checks)
- bi-account-brief (account context for personalisation)

**Strongly recommended:**
- lo-check-in-scheduler (cadence-driven email triggers)
- lo-onboarding-orchestrator (onboarding email triggers)
- lo-renewal-manager (renewal communication triggers)
- lo-milestone-tracker (milestone notification triggers)
- cc-call-summariser (post-call follow-up triggers with summary content)
- ra-engagement-tracker (recency check and engagement pattern data)
- bi-risk-detector (sensitivity check -- flag at-risk accounts)
- Calendar integration (send time optimisation based on timezone)
- Email integration (thread context for follow-ups, delivery tracking)

**Downstream consumers:**
- CSMs (primary consumer -- review and approve before sending)
- CRM activity record (via cc-crm-updater -- email logged as a touchpoint)
- ra-engagement-tracker (sent email as an outbound touchpoint)
- lo-sla-monitor (commitments made in the email become tracked items)

## References

- `references/email-templates.md` -- Template library for all email categories with personalisation field definitions and example outputs

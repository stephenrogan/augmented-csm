---
name: cc-call-summariser
description: Generates structured post-call summaries from call transcripts or CSM notes, extracting key discussion points, decisions, action items with owners and deadlines, sentiment signals, and risk or opportunity flags. Routes extracted data to downstream skills for tracking. Use when asked to summarise a call, extract action items from a meeting, generate call notes, create a post-meeting summary, or when any workflow needs structured output from a customer conversation. Also triggers for questions about call documentation, meeting notes, action item extraction, or conversation capture.
license: MIT
metadata:
  version: "1.0.0"
  pillar: communication-content
  category: content-engine
---

# Call Summariser

Generates structured post-call summaries from transcripts or CSM notes. Extracts discussion points, decisions, action items, sentiment signals, and flags -- then routes extracted data to downstream skills for tracking and action. Part of the Communication & Content Production pillar.

This is a **content extraction and structuring** skill. It transforms unstructured conversation data into structured, actionable records. It does not interpret relationship dynamics or make strategic assessments -- those are human reads the CSM applies after reviewing the summary.

## When to Run

- **Triggered**: After a customer call when a transcript is available (via Gong, Chorus, or equivalent)
- **On-demand**: When a CSM provides notes and requests a structured summary
- **Batch**: End-of-day processing of all calls from that day

## Core Execution Logic

### Step 1: Ingest Source Material

Accept input from any available source:

| Source | Quality | Processing Notes |
|--------|---------|-----------------|
| Full transcript (Gong, Chorus) | High | Best extraction quality. Speaker labels enable per-person analysis |
| Partial transcript (auto-generated) | Medium | May miss segments. Speaker labels may be inaccurate. Flag sections with low confidence |
| CSM-provided notes | Variable | Depends on note quality. Summary is only as good as the input |
| Meeting recording metadata | Low (supplementary) | Attendees, duration, date -- context only, not content |

### Step 2: Extract Discussion Points

Identify the 3-7 main topics covered during the call:
- Detect topic transitions in the transcript (shift in subject, new questions, agenda item changes)
- Summarise each topic in 1-2 sentences capturing what was discussed and any conclusion reached
- Preserve conversation order -- the sequence of discussion sometimes matters (what was raised first indicates priority)

### Step 3: Extract Decisions and Commitments

Scan for explicit and implicit commitments:

| Type | Signal Language | Example | Confidence |
|------|---------------|---------|-----------|
| Explicit commitment | "I will...", "We will...", "Let me..." | "I will send the API docs by Friday" | High |
| Customer commitment | "We can...", "I'll have...", "Our team will..." | "We'll have the data ready by next week" | High |
| Agreed action | "Let's do...", "We should...", "Agreed" | "Let's schedule a follow-up for April" | Medium -- "let's" without a named owner is ambiguous |
| Implicit commitment | Offered without a deadline | "I can look into that" | Low -- may be polite hedging. Flag for CSM confirmation |
| Decision | "We've decided...", "The plan is...", "Going with..." | "Going with Option B for the integration" | High |

For each action item captured:
- **Action**: What needs to happen (stated clearly, not verbatim)
- **Owner**: Who committed. If "let's" without a name, flag as "Owner TBD -- confirm"
- **Deadline**: Explicit date if stated. Inferred date if implied ("next week" = [specific date]). "No deadline stated" if neither
- **Priority**: High (affects customer directly or has a hard deadline), Medium (important but flexible), Low (internal housekeeping)
- **Source quote**: The specific passage where the commitment was made (for CSM verification)

### Step 4: Assess Sentiment

Analyse the emotional undercurrent of the conversation:

| Signal Category | Indicators | Confidence |
|----------------|-----------|-----------|
| Positive | Praise, enthusiasm, forward-looking language, expansion interest, laughter (if detectable), "love" or "great" language | High for explicit praise. Medium for tone inference |
| Negative | Frustration, concern, hedging, multiple caveats, "disappointed" or "concerned" language, repeated questions (indicating the answer was not satisfactory) | High for explicit frustration. Medium for hedging detection |
| Competitive | Mentions of alternatives, comparison language ("Competitor X does..."), pricing pressure framed as "other options" | High for explicit competitor naming. Medium for implied evaluation |
| Disengagement | Short answers, low energy, delegation to a junior person, "we'll get back to you" with no timeline | Low-Medium -- may indicate disengagement or simply a busy day |

Produce an overall sentiment classification: positive / neutral / negative / mixed. Include specific evidence for the classification.

### Step 5: Route Extracted Data

Structured data from the summary feeds downstream skills:

| Extracted Element | Routes To | Purpose |
|------------------|----------|---------|
| Action items with owners and deadlines | lo-sla-monitor | Commitment tracking |
| Risk signals (frustration, competitive mentions, disengagement) | bi-risk-detector | Risk signal input |
| Expansion signals (growth interest, new team mentions) | bi-expansion-detector | Expansion signal input |
| Product feedback (feature requests, product complaints) | pa-feedback-aggregator | Product feedback pipeline |
| Competitive mentions | bi-competitive-intel | Competitive signal input |
| Full summary | CRM activity record (via cc-crm-updater) | Account history |
| Summary + action items | cc-email-drafter | Post-call follow-up email generation |

## Output Format

```json
{
  "call_id": "string",
  "account_id": "string",
  "date": "2026-03-10",
  "duration_minutes": 32,
  "source": "gong_transcript",
  "attendees": {
    "customer": [
      { "name": "Tom Chen", "role": "VP Engineering", "speaking_share": 0.45 },
      { "name": "Lisa Park", "role": "Engineering Manager", "speaking_share": 0.20 }
    ],
    "internal": [
      { "name": "Jane Doe", "role": "CSM", "speaking_share": 0.35 }
    ]
  },
  "summary": "Discussed API latency resolution and Q2 expansion plans. Tom confirmed satisfaction with support response. Lisa raised concerns about onboarding timeline for new engineering team.",
  "discussion_points": [
    {
      "topic": "API latency resolution",
      "summary": "Engineering fix deployed for ticket #4521. Currently in monitoring phase -- 7 days before declaring resolved",
      "conclusion": "Both sides satisfied with progress. Will confirm resolution next week"
    },
    {
      "topic": "Q2 engineering expansion",
      "summary": "Customer planning to onboard 15 new engineers in April. Need API documentation and training materials before they start",
      "conclusion": "CSM to provide advanced API docs by March 14. Training plan to be discussed next call"
    },
    {
      "topic": "Advanced reporting interest",
      "summary": "Tom asked about custom dashboards. Currently on Professional tier which does not include this. Expressed interest if available",
      "conclusion": "No commitment. CSM noted interest for potential expansion conversation"
    }
  ],
  "decisions": [
    "Proceed with 15-engineer expansion in April"
  ],
  "action_items": [
    {
      "action": "Send advanced API documentation to Lisa",
      "owner": "Jane Doe (CSM)",
      "deadline": "2026-03-14",
      "priority": "high",
      "source_quote": "I will get that API documentation over to you by Friday",
      "confidence": "high"
    },
    {
      "action": "Confirm API latency fix is stable after 7-day monitoring period",
      "owner": "Jane Doe (CSM)",
      "deadline": "2026-03-17",
      "priority": "medium",
      "source_quote": "We will confirm resolution after the monitoring period",
      "confidence": "high"
    },
    {
      "action": "Provide headcount plan and start dates for April engineering onboarding",
      "owner": "Tom Chen (Customer)",
      "deadline": "2026-03-21",
      "priority": "medium",
      "source_quote": "I will get you the details of who is starting and when",
      "confidence": "high"
    },
    {
      "action": "Build training plan for new engineering team",
      "owner": "TBD -- confirm",
      "deadline": "Before April onboarding",
      "priority": "medium",
      "source_quote": "Let's put together a training plan for the new team",
      "confidence": "medium -- 'let's' without a named owner"
    }
  ],
  "sentiment": {
    "overall": "positive",
    "signals": [
      { "type": "positive", "evidence": "Tom: 'Really happy with how fast your team responded on the latency issue'", "confidence": "high" },
      { "type": "positive", "evidence": "Expansion planning indicates commitment to growing with the product", "confidence": "medium" }
    ]
  },
  "flags": {
    "risk": [],
    "expansion": [
      { "signal": "15 new engineers planned for Q2", "type": "seat_growth", "confidence": "high" },
      { "signal": "Interest in Advanced Reporting (higher tier feature)", "type": "tier_upgrade", "confidence": "low -- exploratory, no commitment" }
    ],
    "competitive": [],
    "product_feedback": [
      { "topic": "Custom dashboards", "type": "feature_interest", "detail": "Asked about custom reporting dashboards. Currently not available on their tier" }
    ]
  },
  "routing": {
    "lo_sla_monitor": 4,
    "bi_expansion_detector": 2,
    "pa_feedback_aggregator": 1,
    "cc_crm_updater": 1,
    "cc_email_drafter": "follow_up_email_triggered"
  },
  "next_touchpoint": "Follow-up email today. Next call scheduled for March 24"
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Summary accuracy | Full structured summary with source quotes | Whether the agent captured the tone and intent correctly. Did it miss nuance, misinterpret a polite deflection as agreement, or overweight a casual mention? |
| Commitment validation | Action items with confidence ratings | Whether low-confidence items are real commitments or polite conversation. "I can look into that" may or may not be an action item -- the CSM was in the room and knows |
| Sentiment interpretation | Sentiment signals with evidence | Whether the classification matches the CSM's read. A customer can say positive things while being fundamentally dissatisfied -- the CSM detects this from tone, body language, and context |
| Routing overrides | Suggested routing for flags and signals | Whether the expansion signal is worth routing (or just casual curiosity), whether the product feedback is formal enough to log |
| Follow-up content | Summary and action items ready for cc-email-drafter | What to include in the follow-up email. Some discussion points are internal-only. Some action items do not need to appear in the customer-facing recap |

## Confidence and Limitations

- **High confidence** for action item extraction from clear transcripts with explicit commitment language ("I will", "by Friday")
- **High confidence** for topic identification -- major subject transitions are detectable in transcript structure
- **Medium confidence** for sentiment assessment -- explicit praise and frustration are clear, but subtle signals (hedging, low energy, polite dissatisfaction) require human interpretation
- **Medium confidence** for implicit commitments -- "let's circle back on that" may be a real commitment, a polite deferral, or an empty phrase. The skill flags these for confirmation rather than asserting
- **Low confidence** for disengagement detection from transcript alone. Short answers and delegation may indicate disengagement, a busy day, or simply a reserved communication style
- Cannot extract information from sidebar conversations, body language, facial expressions, or unrecorded portions of the meeting. The most important moment in a call may happen in the 30 seconds after recording stops
- Transcript quality varies by platform, audio quality, speaker count, and accent. Poor transcripts degrade all extraction
- Multi-person calls with overlapping speakers produce lower-quality transcripts and action item attribution may be incorrect

## Dependencies

**Required:**
- Call transcript integration (Gong, Chorus, or equivalent) OR CSM notes input

**Strongly recommended:**
- CRM API (for activity logging via cc-crm-updater)
- lo-sla-monitor (action item routing for commitment tracking)
- bi-risk-detector (risk signal routing)
- bi-expansion-detector (expansion signal routing)
- pa-feedback-aggregator (product feedback routing)
- bi-competitive-intel (competitive mention routing)
- cc-email-drafter (follow-up email generation)

**Downstream consumers:**
- lo-sla-monitor (action items)
- bi-risk-detector (risk signals)
- bi-expansion-detector (expansion signals)
- bi-competitive-intel (competitive mentions)
- pa-feedback-aggregator (product feedback)
- cc-crm-updater (activity record)
- cc-email-drafter (follow-up email content)

## References

- `references/extraction-patterns.md` -- Signal language patterns, confidence calibration, and extraction rules

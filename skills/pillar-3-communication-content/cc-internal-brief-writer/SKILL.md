---
name: cc-internal-brief-writer
description: Creates internal account briefs, escalation write-ups, and executive summaries for internal audiences. Compiles cross-system data into standardised formats for leadership reviews, cross-functional meetings, and escalation documentation. Adapts content and detail level to the specific audience. Use when asked to write an escalation brief, prepare an internal account summary, create a leadership report on an account, or document an escalation. Also triggers for questions about internal documentation, escalation reports, account status summaries for managers, or cross-functional context documents.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: communication-content
  category: content-engine
---

# Internal Brief Writer

Creates internal-only account documentation -- escalation briefs, leadership summaries, cross-functional context documents, and manager review materials. Distinct from bi-account-brief (which is a data snapshot); this skill produces narrative documents with framing and recommendation placeholders. Part of the Communication & Content Production pillar.

This is a **content generation** skill for internal audiences. It assembles data and structures narrative. The CSM reviews and adds the judgment layer -- the "so what" and "what I recommend" that transforms data into action.

## When to Run

- **Triggered**: By ic-escalation-router when an escalation is initiated (escalation brief)
- **On-demand**: When a CSM needs an internal document for a specific purpose
- **Scheduled**: Before manager 1:1s or leadership reviews (if configured)

## Core Execution Logic

### Step 1: Identify Document Type and Audience

Determine from the trigger or request:

| Document Type | Audience | Detail Level | Length |
|-------------|----------|-------------|--------|
| Escalation brief | Engineering, Product, Support leadership | High -- full technical and business context | 1-2 pages |
| Leadership summary | VP CS, CRO, CFO | Low -- headline metrics, risk, recommendation | 5-8 lines |
| Cross-functional context | Product, Sales, Engineering teams | Medium -- relevant history tailored to what this team needs | Half page |
| Manager review | CSM's direct manager | High -- includes CSM's assessment, asks, and development needs | 1 page |
| Board-level summary | Executives, board members | Very low -- 3-4 sentences with the one number and one insight that matters | 3-4 sentences |

### Step 2: Pull Data Filtered by Audience

From bi-account-brief and other skills, select only what the audience needs:

| Audience | Include | Exclude |
|----------|---------|---------|
| Engineering/Product | Usage data, support history, product context, technical details, feature requests | Revenue data, commercial strategy, relationship assessment |
| CRO/CFO | ARR, renewal status, NRR impact, financial context, risk classification | Technical details, support ticket IDs, individual feature issues |
| CS Leadership | Health trajectory, risk assessment, intervention plan, resource needs | Detailed technical context, individual ticket status |
| Product Management | Adoption data, feature feedback, usage patterns, competitive context | Revenue details, relationship dynamics |
| CSM Manager | Portfolio health, specific account deep-dives, CSM performance metrics, development discussion | Board-level financials, cross-functional details |

### Step 3: Structure by Document Type

**Escalation Brief structure:**

| Section | Content | Source |
|---------|---------|--------|
| Headline | One line: what is happening, to which customer, what is at stake | CSM input + CRM |
| Account context | ARR, health, renewal date, strategic importance | bi-account-brief |
| Issue timeline | Chronological reconstruction from first occurrence to now | Support platform + CSM input |
| Customer impact | How the issue affects the customer's business (specific, quantified where possible) | CSM assessment + usage data |
| Resolution attempts | Every prior attempt with outcome -- prevents the receiving team from re-trying failed approaches | Support platform + CSM input |
| Specific ask | Not "please help" but "we need [specific action] by [specific date]" | CSM input |
| Customer communication status | What the customer knows, what they expect, their current sentiment | CSM input |
| Commercial context | ARR at risk, renewal proximity, escalation's potential revenue impact | CRM + lo-renewal-manager |

**Leadership Summary structure:**

| Section | Content | Length |
|---------|---------|--------|
| Status line | Account name, health classification, one-word trajectory | 1 line |
| Key numbers | ARR, health score, renewal date, days to renewal | 1 line |
| Primary item | The single most important risk or opportunity | 2-3 sentences |
| Recommended action | What leadership should do (if anything) | 1 sentence |

**Cross-Functional Context structure:**

| Section | Content |
|---------|---------|
| Account overview | Tailored to the audience (technical context for engineering, business context for sales) |
| Relevant history | Only the history this team needs -- not the full account narrative |
| Current situation | What is happening now and why this team is involved |
| Specific ask | What you need from them, by when |
| Success criteria | How we will know the ask is met |

### Step 4: Generate CSM Input Placeholders

Mark sections that require CSM judgment with clear placeholders:

| Placeholder Type | What the CSM Adds |
|-----------------|-------------------|
| "So what" framing | What does this data mean for this account? The data shows declining health -- the CSM explains why and what it means for the relationship |
| Recommended action | What should we do? The brief presents the situation; the CSM proposes the response |
| Sensitivity notes | What should or should not be shared with this audience. Some data is too sensitive for certain internal teams |
| Political context | Which internal teams are receptive, which will resist. This context is invisible to data but essential for the brief's effectiveness |
| Urgency calibration | The data shows severity (health score, ARR at risk); the CSM knows the true urgency based on relationship context |

### Step 5: Quality Gates

Before delivering the brief:
- Is the headline instantly clear? A reader should understand the situation in 5 seconds
- Is the "specific ask" genuinely specific? "Please help" fails. "We need engineering to investigate the API latency affecting this account and provide a fix or timeline by March 14" succeeds
- Is the document length appropriate for the audience? Leadership gets 5-8 lines. Escalation teams get 1-2 pages. Mismatching length to audience wastes their time or leaves them without context
- Are all data points current? Stale data in an escalation brief undermines credibility
- Is anything included that should not be shared with this audience?

## Output Format

```json
{
  "document_id": "brief-2026-0089",
  "account_id": "string",
  "document_type": "escalation_brief",
  "audience": "Engineering -- Platform Team",
  "urgency": "high",
  "content": {
    "headline": "API latency issue affecting Acme Corp -- P1 open 12 days, EUR 85k ARR, renewal in 67 days",
    "account_context": { "arr": 85000, "health": 58, "trend": "declining", "renewal_days": 67 },
    "timeline": [
      { "date": "2026-02-26", "event": "Customer reported API latency >3s on dashboard queries" },
      { "date": "2026-02-27", "event": "Support ticket #4521 opened, P2. Initial investigation: no server-side issue found" },
      { "date": "2026-03-01", "event": "Escalated to P1 after customer confirmed issue affects 15 users" },
      { "date": "2026-03-05", "event": "Engineering identified potential database query optimisation. Fix estimated 3-5 days" },
      { "date": "2026-03-10", "event": "Fix not yet deployed. Customer increasingly frustrated" }
    ],
    "customer_impact": "Analytics team cannot run reports reliably. Estimated 4 hours per week in manual workarounds. Customer has raised this in 3 separate interactions",
    "resolution_attempts": [
      { "attempt": "Server-side cache flush (Feb 27)", "outcome": "No improvement" },
      { "attempt": "Customer-side browser cache clear (Feb 28)", "outcome": "Temporary improvement, issue returned" },
      { "attempt": "Database query review (Mar 5)", "outcome": "Root cause identified. Fix in development" }
    ],
    "specific_ask": "Deploy the database query optimisation fix and confirm performance returns to <500ms for dashboard queries. Needed by March 14",
    "customer_comms_status": "Customer knows engineering has identified the root cause. They expect resolution this week. Sentiment is frustrated but patient -- patience will not extend past Friday",
    "commercial_context": "EUR 85k ARR, renewal in 67 days. This issue is the primary risk factor for the renewal"
  },
  "csm_input_required": [
    "Recommended approach if the fix cannot be deployed by March 14",
    "Whether to involve executive sponsor given renewal proximity"
  ],
  "data_freshness": "all_current",
  "generated": "2026-03-10T14:00:00Z"
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| "So what" framing | Data assembled, trends identified | What the data means and what action it implies. The brief is evidence; the CSM is the advocate |
| Sensitivity filtering | Full data package for the audience | What to include, what to hold back. Some data should not be shared with specific internal teams |
| Urgency calibration | Severity metrics (health, ARR, timeline) | Whether the data-driven severity matches the relationship reality. A moderate-severity data signal on a strategic account may warrant urgent treatment |
| Political awareness | Audience identification | How to position the brief. Knowing that the engineering team is under resource pressure changes how you frame a request vs. when they have capacity |
| Recommendation | Situation summary, options space | What to recommend. The brief presents the problem; the CSM proposes the solution |

## Confidence and Limitations

- **High confidence** for data assembly and formatting -- pulling from defined sources with structured templates is deterministic
- **High confidence** for timeline construction from support ticket data -- chronological event compilation
- **Medium confidence** for audience-appropriate detail level -- the default templates are sensible but the CSM may want different emphasis based on the specific audience member's preferences or the meeting's agenda
- **Low confidence** for the narrative layer. The brief assembles facts; the "so what" requires human judgment. A brief that presents data without interpretation is a report, not a brief. The CSM's additions transform it from data into a persuasive document
- Cannot assess internal political dynamics -- which teams are receptive, which will resist, who has capacity, who needs to be handled carefully. These dynamics shape how the brief should be framed
- Cannot determine the right level of detail for a specific reader. Some VPs want 3 sentences; others want 3 pages. The CSM knows their audience

## Dependencies

**Required:**
- bi-account-brief (data foundation for all brief types)
- CRM API (account and contact data)

**Strongly recommended:**
- Support platform (for escalation timeline data)
- All Book Intelligence skills (for health, risk, and usage context)
- lo-sla-monitor (for commitment and SLA data in escalation briefs)
- lo-renewal-manager (for renewal context in commercial briefs)

**Downstream consumers:**
- ic-escalation-router (escalation briefs as routing attachments)
- ic-cross-func-prep (account briefs as meeting materials)
- CS leadership (leadership summaries for decision-making)
- Cross-functional teams (context briefs for escalation resolution)

## References

- `references/brief-templates.md` -- Template structures for each document type with section definitions

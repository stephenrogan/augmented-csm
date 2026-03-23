---
name: lo-qbr-orchestrator
description: Manages the end-to-end QBR process including scheduling, attendee coordination, content preparation, and follow-up tracking. Use when asked to schedule a QBR, prepare a business review, build QBR content, automate QBR preparation, coordinate a quarterly review, generate a QBR deck, or when any account needs a structured business review. Also triggers for questions about business review cadence, executive review preparation, or customer success review meetings.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: lifecycle-orchestration
  category: workflow-engine
---

# QBR Orchestrator

Manages the Quarterly Business Review lifecycle from scheduling through follow-up. Coordinates attendees, generates data-rich content, prepares the CSM, and tracks action items post-QBR. Part of the Lifecycle Orchestration pillar.

This is a **coordination and content generation** skill. It handles logistics and data assembly. The CSM leads the QBR itself -- framing the narrative, navigating the conversation, and making strategic recommendations. That is pure human territory.

## When to Run

- **Triggered**: When a QBR is due based on the account's QBR cadence (typically quarterly, may vary by segment)
- **Scheduled**: 4 weeks before the target QBR date, the skill begins the preparation workflow
- **On-demand**: When a CSM requests QBR preparation for a specific account outside the regular cadence

## QBR Preparation Workflow

### T-28 Days: Initiate

1. Check QBR eligibility: account must be past onboarding (lifecycle stage = "Adopted" or later)
2. Propose 3 date/time options based on CSM and primary customer contact availability
3. Send scheduling request to customer with proposed times
4. Create QBR project record in CRM

### T-21 Days: Confirm and Coordinate

1. Confirm date with customer (follow up if no response within 5 business days)
2. Identify recommended attendees:
   - From customer: primary contact, executive sponsor, key stakeholders based on QBR focus
   - From vendor: CSM, CSM manager (for strategic accounts), product specialist (if product discussion planned)
3. Send calendar invites to all confirmed attendees
4. Begin content assembly (see Content Generation below)

### T-7 Days: Content Delivery

1. Generate the QBR content package (deck + briefing notes)
2. Deliver to CSM for review and customisation
3. Surface any new signals (risk, expansion, competitive) that have emerged since T-28
4. Generate the CSM's internal prep brief (different from the customer-facing deck)

### T-0: QBR Day

1. Send reminder to all attendees (morning of, if meeting is afternoon; day before, if morning)
2. Ensure the CSM has the latest account brief
3. No agent involvement during the meeting -- this is fully human-led

### T+1 to T+3: Follow-Up

1. Generate post-QBR summary from CSM's notes (CSM inputs notes; agent structures and distributes)
2. Create action items in CRM from the summary
3. Send follow-up email to customer with summary and action items (CSM reviews before send)
4. Set tracking triggers for each action item (due dates, owners)
5. Schedule the next QBR (add to the cadence calendar)

## Content Generation

### Customer-Facing QBR Deck

The agent generates a data-rich deck that the CSM then customises with narrative and strategic framing.

**Deck structure:**

| Slide | Content Source | Agent vs. Human |
|-------|--------------|-----------------|
| Title | Account name, date, attendees | AGENT generates |
| Agenda | Standard QBR agenda with customisable sections | AGENT generates, HUMAN customises |
| Relationship Summary | Key contacts, engagement history, milestones since last QBR | AGENT generates from CRM data |
| Usage and Adoption | Usage metrics, trends, benchmark comparisons, feature adoption | AGENT generates from product analytics and bi-usage-monitor |
| Value Delivered | ROI metrics, outcomes achieved, workflow completions | AGENT generates from product analytics |
| Health Overview | Health score trend, component breakdown (customer-appropriate framing) | AGENT generates from bi-health-score (sanitised -- no internal risk language) |
| Support Summary | Ticket volume, resolution metrics, open items | AGENT generates from support platform |
| Roadmap Alignment | Upcoming product features relevant to customer's use case | AGENT generates from product roadmap data |
| Strategic Recommendations | Adoption expansion, use case deepening, risk mitigation | HUMAN writes -- this is the CSM's strategic contribution |
| Action Items | Agreed next steps from the QBR conversation | HUMAN captures during/after the QBR |

### CSM Internal Prep Brief

Separate from the customer deck. For the CSM's eyes only.

**Content:**
- Full account brief (from bi-account-brief, renewal context)
- Active risk signals with evidence (not for sharing with customer)
- Expansion signals with recommended framing
- Competitive intelligence (if any)
- Stakeholder dynamics: who will be in the room, their role, last engagement, known positions
- Suggested talking points and questions
- Landmines to avoid (open support issues, known frustrations, political sensitivities from CSM notes)

## Output Format

**QBR status record:**
```json
{
  "account_id": "string",
  "qbr_date": "2026-04-15",
  "status": "content_ready",
  "attendees_confirmed": ["Tom Chen (VP Eng)", "Sarah Kim (CFO)", "Jane Doe (CSM)", "Mike Ross (CS Manager)"],
  "deck_generated": true,
  "csm_review_complete": false,
  "prep_brief_generated": true,
  "follow_up_actions": [],
  "next_qbr_target": "2026-07-15"
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Attendee selection | Stakeholder map, engagement history, QBR focus areas | Who should be in the room and why |
| Deck customisation | Data-populated deck, prep brief | Narrative framing, strategic recommendations, what to emphasise or downplay |
| Leading the QBR | Prep brief, latest signals | How to run the conversation, respond to questions, navigate difficult topics |
| Action item prioritisation | Action items captured during QBR | Which items to commit to, timelines, ownership |
| Follow-up email approval | Draft follow-up with summary and action items | Whether the tone, commitments, and framing are accurate |

## Confidence and Limitations

- **High confidence** for scheduling, content assembly, and follow-up tracking -- structured workflows
- **Medium confidence** for deck content quality -- data is accurate but narrative requires human curation
- Cannot generate strategic recommendations (Slide 9) -- this is the CSM's highest-value contribution
- Cannot assess whether the QBR was successful (requires human judgment on customer response)
- Cannot adapt in real-time during the QBR to unexpected topics or customer reactions

## Dependencies

**Required:**
- CRM API (account data, contacts, activities)
- Calendar integration (scheduling, attendee coordination)
- Product analytics (usage data for deck content)
- `bi-account-brief` (prep brief generation)

**Strongly recommended:**
- `bi-health-score` (health data for deck)
- `bi-usage-monitor` (usage trends for deck)
- `bi-risk-detector` (risk signals for prep brief)
- `bi-expansion-detector` (expansion signals for prep brief)
- Document/deck generation capability

## References

- `references/qbr-templates.md` -- Deck templates, agenda structures, and follow-up email formats

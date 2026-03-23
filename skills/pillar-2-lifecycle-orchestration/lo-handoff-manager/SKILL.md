---
name: lo-handoff-manager
description: Generates handoff documentation and manages transition sequences when accounts move between teams, CSMs, or lifecycle stages. Covers sales-to-CS handoff, CSM-to-CSM reassignment, CS-to-renewal team handoff, and any structured account transition. Use when asked to create a handoff brief, manage an account transition, prepare for CSM reassignment, build a sales-to-CS handoff, transfer account knowledge, or when any account is changing ownership. Also triggers for questions about knowledge transfer, account reassignment, team transitions, or onboarding a new CSM onto an existing account.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: lifecycle-orchestration
  category: workflow-engine
---

# Handoff Manager

Generates handoff documentation and manages transition sequences for account ownership changes. Ensures no context is lost when an account moves between people or teams. Part of the Lifecycle Orchestration pillar.

This is a **documentation and coordination** skill. It compiles context, generates briefs, manages the transition timeline, and confirms completion. The quality of the relationship transition -- making the customer feel valued, not abandoned -- is human work.

## When to Run

- **Triggered**: When a handoff event is detected in CRM (new deal closed, CSM reassignment, team transfer)
- **On-demand**: When a CSM or manager requests a handoff brief for a specific account
- **Scheduled**: When a planned transition is set up (e.g., CSM leaving in 30 days, accounts need reassignment)

## Handoff Types

### Sales-to-CS Handoff

**Trigger**: Deal closes (CRM opportunity stage = Closed Won)
**From**: Sales rep / Account Executive
**To**: Assigned CSM

**Brief contents:**
- Deal summary: ARR, product/tier, contract terms, implementation scope
- Customer goals: what the customer expects to achieve (from sales notes and call transcripts)
- Key contacts: names, roles, engagement during sales process, who is the champion, who is the economic buyer
- Technical requirements: integration needs, data migration, SSO, security requirements
- Competitive context: who else was evaluated, why the customer chose your product, known concerns
- Promises made: any commitments from sales that CS needs to honour (feature timelines, pricing, custom terms)
- Red flags: anything the sales team noticed that CS should be aware of (budget constraints, political dynamics, sceptical stakeholders)
- Handoff meeting: recommended agenda for the introduction call between sales, CS, and customer

### CSM-to-CSM Reassignment

**Trigger**: CSM change in CRM (reassignment, departure, territory rebalancing)
**From**: Current CSM
**To**: New CSM

**Brief contents:**
- Full account brief (from bi-account-brief)
- Relationship map: who are the key contacts, what is the CSM's read on each (strength of relationship, engagement level, influence)
- Current state: where is the account in its lifecycle, what is in progress, what was planned
- Active issues: open support tickets, pending actions, unresolved concerns
- History highlights: key moments in the relationship (wins, crises, pivots) that the new CSM needs to know
- Landmines: known sensitivities, topics to avoid, political dynamics
- Upcoming events: next QBR, renewal date, scheduled calls, pending milestones
- Recommended first action: what the new CSM should do in their first 7 days with this account
- Customer notification: draft email introducing the new CSM (outgoing CSM sends, or joint send)

### CS-to-Renewal Team Handoff

**Trigger**: Account enters active renewal phase (T-90 or as defined by org structure)
**From**: CSM
**To**: Renewal manager or commercial team

**Brief contents:**
- Account brief with renewal context
- Health trajectory over the contract period
- Risk and expansion signals
- Stakeholder map with commercial influence assessment
- Contract history (current terms, previous negotiations, concessions)
- CSM's renewal recommendation: renew as-is, expand, adjust terms, or risk mitigation needed

### Internal Escalation Handoff

**Trigger**: CSM escalates an account to product, engineering, or executive leadership
**From**: CSM
**To**: Internal team

**Brief contents:**
- Escalation summary: what is being escalated and why
- Timeline: when the issue started, how it has progressed, what has been tried
- Customer impact: usage changes, sentiment, at-risk revenue
- Customer communications: what the customer knows, what they expect
- Requested action: what the CSM needs from the internal team

## Core Execution Logic

### Step 1: Detect Handoff Event

Monitor CRM for handoff triggers:
- New Closed Won opportunity (sales-to-CS)
- CSM field change on account record (CSM-to-CSM)
- Lifecycle stage or opportunity stage change (CS-to-renewal)
- Escalation flag set by CSM (internal escalation)

### Step 2: Assemble Brief

Based on the handoff type:
1. Pull structured data from all available sources (CRM, product analytics, support, health score, risk signals)
2. Pull unstructured context (CSM notes, recent call summaries, email threads)
3. Assemble into the appropriate brief format
4. Flag any gaps: missing data, stale sources, or sections that require human input (e.g., relationship dynamics that are not in any system)

### Step 3: Route for Human Input

Handoff briefs require human enhancement before they are complete:
- Sales-to-CS: Sales rep reviews and adds context about promises, competitive dynamics, and relationship nuances
- CSM-to-CSM: Outgoing CSM reviews and adds relationship context, landmines, and recommendations
- CS-to-renewal: CSM reviews and adds their renewal recommendation and stakeholder assessment

### Step 4: Manage Transition Timeline

For each handoff, track a transition checklist:

| Step | Owner | Target |
|------|-------|--------|
| Brief generated | AGENT | Day 0 |
| Brief reviewed and enhanced by outgoing owner | HUMAN | Day 0-2 |
| Brief delivered to incoming owner | AGENT | Day 2 |
| Introduction meeting scheduled (if applicable) | AGENT | Day 2-5 |
| Introduction meeting held | HUMAN | Day 5-10 |
| Customer notified of transition | HUMAN | Day 5-10 |
| Incoming owner confirms context received | HUMAN | Day 10 |
| Handoff complete flag set in CRM | AGENT | Day 10 |

### Step 5: Confirm Completion

After the handoff deadline:
- Check if all checklist items are complete
- Flag incomplete items to the incoming owner and their manager
- Set a 30-day review: incoming owner confirms they have full context and the relationship is stable

## Output Format

**Handoff record:**
```json
{
  "account_id": "string",
  "handoff_type": "csm_to_csm",
  "from": "Jane Doe",
  "to": "Mike Ross",
  "initiated": "2026-03-01",
  "brief_generated": true,
  "brief_reviewed": true,
  "introduction_meeting": "2026-03-08",
  "customer_notified": true,
  "completion_confirmed": false,
  "checklist_status": {
    "brief_generated": "complete",
    "brief_reviewed": "complete",
    "brief_delivered": "complete",
    "intro_meeting": "complete",
    "customer_notified": "complete",
    "context_confirmed": "pending"
  },
  "target_completion": "2026-03-11",
  "days_remaining": 1
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Brief enhancement | Draft brief with data-populated sections | Relationship nuances, landmines, recommendations that only the outgoing owner knows |
| Customer notification approach | Draft notification email, stakeholder map | How to frame the transition, timing, who sends the message |
| Introduction meeting | Brief, recommended agenda | How to run the meeting, what to emphasise, how to build rapport |
| Transition completeness | Checklist status, gap flags | Whether the incoming owner has sufficient context to operate effectively |

## Confidence and Limitations

- **High confidence** for data assembly and checklist management -- structured workflows
- **Low confidence** for relationship context -- the most valuable handoff content is in the outgoing owner's head, not in any system. The brief surfaces what the data shows; the human adds what only they know
- Cannot transfer trust. The incoming owner inherits the account but must build their own relationship
- Cannot detect if critical context was omitted from the brief (no way to know what you do not know)

## Dependencies

**Required:**
- CRM API (account data, contact data, activity history, ownership fields)
- `bi-account-brief` (for comprehensive account context)

**Strongly recommended:**
- All Book Intelligence skills (for health, usage, risk, and expansion context)
- Calendar integration (for introduction meeting scheduling)
- Email integration (for customer notification)

## References

- `references/handoff-templates.md` -- Brief templates and notification email formats for each handoff type

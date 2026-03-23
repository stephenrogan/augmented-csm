# The CSM Operational Surface Area

## Eight Pillars of the CSM Role

Every task a CSM performs in a working week sits inside one of eight operational pillars. Each pillar has a distinct agent density -- the percentage of activities within that pillar that can be executed by agents rather than humans.

The pillars are not arbitrary groupings. They reflect fundamentally different types of work with different operator requirements. Book Intelligence is almost entirely data work. Relationship Architecture is almost entirely human work. The pillars in between fall on a spectrum.

## Pillar Definitions

### Pillar 1: Book Intelligence (80-90% Agent Density)

Knowing what is happening across your accounts before anyone tells you. Health monitoring, usage pattern tracking, risk signal detection, opportunity identification, and segment-level trend analysis. This is the situational awareness layer.

Agent density is very high because this pillar is almost entirely data assembly, pattern detection, and alerting. The human judgment enters only when signals are ambiguous or when prioritisation decisions must be made.

**Skills:** bi-health-score, bi-usage-monitor, bi-risk-detector, bi-expansion-detector, bi-segment-trends, bi-account-brief, bi-competitive-intel

### Pillar 2: Lifecycle Orchestration (75-85% Agent Density)

Moving customers through defined operational motions -- onboarding, adoption milestones, renewal sequences, QBR cadences. The "trains run on time" layer. Sequencing, scheduling, triggering, and tracking milestone-based workflows.

High agent density because lifecycle motions are trigger-based and sequential. The human enters at exception points -- when a customer deviates from the expected path and standard triggers fail.

**Skills:** lo-onboarding-orchestrator, lo-check-in-scheduler, lo-renewal-manager, lo-qbr-orchestrator, lo-milestone-tracker, lo-handoff-manager, lo-sla-monitor

### Pillar 3: Communication & Content Production (60-75% Agent Density)

All written output a CSM produces: emails, QBR decks, executive summaries, business reviews, internal account briefs, follow-up notes, escalation write-ups, CRM updates, reports.

High agent density because the majority of communications follow repeatable patterns with account-specific data insertion. The human layer is tone calibration for sensitive situations, political nuance in executive communications, and the judgment to know when not to communicate at all.

**Skills:** cc-email-drafter, cc-qbr-deck-builder, cc-call-summariser, cc-internal-brief-writer, cc-crm-updater, cc-report-generator

### Pillar 4: Product Adoption & Value Realisation (45-55% Agent Density)

Driving usage depth and breadth within accounts. Feature adoption tracking, use case expansion, time-to-value acceleration, adoption benchmarking, and identifying underutilised capabilities.

Moderate agent density. Agents handle measurement, benchmarking, and recommendation generation. But diagnosing why adoption has stalled -- which is often organisational, not technical -- and coaching customers on change management require human expertise.

**Skills:** pa-adoption-tracker, pa-benchmark-engine, pa-value-reporter, pa-feedback-aggregator

### Pillar 5: Commercial Motion -- Expansion & Retention (35-50% Agent Density)

The revenue layer. Identifying expansion opportunities, building the commercial case, timing the ask, running save plays, managing renewal negotiation strategy, and forecasting retention outcomes.

Lower agent density because commercial motion depends heavily on timing, relationship leverage, and negotiation judgment. Agents surface signals and prepare evidence; humans own the conversation.

**Skills:** cm-commercial-case-builder, cm-renewal-forecaster, cm-competitive-response-prep

### Pillar 6: Internal Coordination (50-60% Agent Density)

Working cross-functionally -- product, support, sales, leadership. Routing, handoffs, escalations, and internal advocacy.

Moderate agent density. Routing, status updates, notifications, and structured documentation are agent territory. The human layer is influence -- getting the right people to care about the right accounts at the right time.

**Skills:** ic-escalation-router, ic-internal-notifier, ic-feature-request-tracker, ic-cross-func-prep

### Pillar 7: Relationship Architecture (10-20% Agent Density)

Building and maintaining the human relationships that underpin retention. Champion development, political navigation, executive engagement timing, trust repair, multi-threading strategy.

Very low agent density. Agents track contacts, detect changes, and monitor engagement cadence. Everything else is pure human craft -- the thing that makes a great CSM irreplaceable.

**Skills:** ra-stakeholder-mapper, ra-stakeholder-change-detector, ra-engagement-tracker

### Pillar 8: Customer Advocacy & Community (15-25% Agent Density)

Managing advocacy programmes -- references, case studies, reviews, testimonials -- and monitoring community channels for signals. Turning satisfied customers into active advocates through structured programme management.

Low agent density. Agents track the pipeline, manage logistics, prevent advocate fatigue, and monitor community activity. But asking a customer to advocate, coaching them through a case study, and maintaining the goodwill that makes advocacy possible are entirely human. Advocacy is a withdrawal from the relationship bank account. The agent ensures you make smart withdrawals; the CSM ensures the balance is sufficient.

**Skills:** ca-advocacy-tracker, ca-community-monitor

## The Blended Picture

Weighting each pillar by typical CSM time allocation, the blended agent-executable percentage across the full role lands at 60-70%.

The high-density pillars (Book Intelligence, Lifecycle Orchestration, Communications) carry the volume. The lower-density pillars (Commercial Motion, Relationship Architecture) are where the human earns their seat.

## The AGENT/HUMAN Boundary

The boundary is not about what agents can technically do. It is about what they should do.

An agent could draft a save play email to an at-risk customer. But should it? The answer is no -- because the save play depends on relationship context, political dynamics, and timing judgment that the agent cannot assess. The agent should surface the risk signal, prepare the account context, and draft the email. The human decides whether to send it, when, and with what adjustments.

This boundary is defined explicitly in every skill specification in this repo. Each skill includes a "Handoff to Human" section that identifies the decision points and what context the agent provides at each one.

The boundary will move over time. As agents improve and as trust is built, some activities currently classified as HUMAN may shift to HUMAN+ (agent-supported) or even AGENT. But the architecture is designed so that the boundary can move without rebuilding the system -- each skill is independent and can be reclassified without affecting the others.

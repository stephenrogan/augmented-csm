# Build Sequence

## Dependency-Driven Implementation Order

The 38 skills form a dependency graph. Skills in later pillars consume data produced by skills in earlier pillars. Building out of order means building skills that have no data to work with.

## Phase 1: Foundation Data (Weeks 1-4)

**Build first. Everything depends on these.**

| Skill | Why First |
|-------|-----------|
| bi-health-score | Every other skill references health data. Without this, risk detection, expansion detection, cadence adjustment, and renewal forecasting are all blind |
| bi-usage-monitor | Usage data feeds the health score, risk detector, expansion detector, adoption tracker, and benchmark engine |
| ra-stakeholder-mapper | Contact data feeds account briefing, engagement tracking, handoff management, and every human decision point that needs to know who matters |
| ra-engagement-tracker | Engagement data feeds the health score (engagement component), risk detection (declining engagement signal), and check-in scheduling |

**Estimated effort:** 2-4 weeks depending on data source integration complexity.

**Success criteria:** Health scores computing reliably for all accounts. Usage patterns classifying correctly. Stakeholder maps populated for all managed accounts.

## Phase 2: Detection Layer (Weeks 3-6)

**Build once Phase 1 data is flowing.**

| Skill | Why Now |
|-------|---------|
| bi-risk-detector | Consumes health and usage data to produce the risk queue. The single highest-value detection skill -- it tells CSMs where to focus |
| bi-expansion-detector | Consumes health and usage data to identify growth opportunities. Feeds the commercial pillar |
| ra-stakeholder-change-detector | Consumes stakeholder map data to detect champion departures and reorgs. Produces the highest-urgency signals in the architecture |
| bi-competitive-intel | Consumes support ticket and call transcript data for competitive signals. Independent of Phase 1 data but more valuable when correlated with risk signals |

**Estimated effort:** 2-4 weeks. Primary work is signal registry definition and threshold tuning.

**Success criteria:** Risk queue producing daily prioritised alerts. Expansion signals surfacing weekly. Champion departures detected within 48 hours.

## Phase 3: Core Workflows (Weeks 5-10)

**Build the operational engine.**

| Skill | Why Now |
|-------|---------|
| lo-onboarding-orchestrator | The highest-volume workflow. Immediate impact on new customer experience |
| lo-check-in-scheduler | Replaces manual cadence management for the entire book. Health-based adjustments require Phase 1 and Phase 2 data |
| lo-renewal-manager | Renewal is the highest-stakes workflow. Risk classification requires Phase 2 risk detector |
| bi-account-brief | The most-used skill in daily CSM workflow. Requires all Phase 1 and Phase 2 skills for comprehensive context |

**Estimated effort:** 3-5 weeks. Integration work for calendar, email, and CRM workflows.

**Success criteria:** New customers flowing through automated onboarding. Check-in cadences managed dynamically. Renewal pipeline tracked with risk classification. Account briefs generating in under 60 seconds.

## Phase 4: Daily Productivity (Weeks 8-14)

**Build the content and communication layer.**

| Skill | Why Now |
|-------|---------|
| cc-email-drafter | Drafts the emails the lifecycle skills trigger. Requires account data from Phase 1 and workflow triggers from Phase 3 |
| cc-call-summariser | Requires call transcript integration. Feeds action items into lo-sla-monitor |
| cc-crm-updater | Automates the CRM hygiene that every other skill depends on for data accuracy |
| lo-sla-monitor | Tracks commitments from call summaries and email promises. Requires cc-call-summariser output |
| cc-report-generator | Aggregates data from all prior phases into recurring reports |

**Estimated effort:** 3-4 weeks. Primarily template development and integration work.

**Success criteria:** CSMs receiving draft emails for review instead of writing from scratch. Call summaries auto-generated. CRM accuracy maintained automatically. Weekly reports producing without manual compilation.

## Phase 5: Depth and Sophistication (Weeks 12-18)

**Everything else. By this point the foundation, detection, workflow, and productivity layers are operational.**

| Skills | Value Added |
|--------|------------|
| lo-qbr-orchestrator, cc-qbr-deck-builder | End-to-end QBR automation |
| lo-milestone-tracker | Structured adoption tracking beyond onboarding |
| lo-handoff-manager | Structured transitions when accounts change hands |
| pa-adoption-tracker, pa-benchmark-engine, pa-value-reporter | Deep adoption analytics and value measurement |
| pa-feedback-aggregator | Structured product feedback loop |
| cm-commercial-case-builder, cm-renewal-forecaster, cm-competitive-response-prep | Commercial support layer |
| ic-escalation-router, ic-internal-notifier, ic-feature-request-tracker, ic-cross-func-prep | Internal coordination automation |
| bi-segment-trends, cc-internal-brief-writer | Strategic analysis and internal documentation |

**Estimated effort:** 4-8 weeks. These skills add depth rather than establish infrastructure.

## Total Timeline

Minimum viable agent-augmented CS operation (Phases 1-3): **10-12 weeks.**

Full 34-skill implementation: **16-22 weeks** depending on team size, tech stack complexity, and integration maturity.

## What Not to Do

- Do not build Pillar 5 (Commercial Motion) before Pillar 1 (Book Intelligence). Commercial skills without data are guesswork
- Do not build Pillar 3 (Communications) before Pillar 2 (Lifecycle Orchestration). Email drafting without workflow triggers produces emails with no purpose
- Do not try to launch all 38 skills simultaneously. Sequential rollout builds trust with the CS team and allows calibration at each phase
- Do not skip Phase 1. The temptation is to jump to "visible" skills like email drafting or QBR decks. But without reliable data underneath, the visible skills produce unreliable output

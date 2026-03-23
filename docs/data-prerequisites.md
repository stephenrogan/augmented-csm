# Data Prerequisites

## What You Need Before You Build

The skills in this repo are specifications, not standalone tools. They assume access to customer data across multiple systems. This document defines the data infrastructure prerequisites that must be in place before implementation begins.

## Required Integrations

These integrations are referenced by the majority of skills. Without them, the architecture does not function.

### CRM (Salesforce, HubSpot, Gainsight, or equivalent)

**Data consumed:**
- Account records (name, ARR, segment, tier, contract dates, lifecycle stage)
- Contact records (name, role, email, stakeholder classification)
- Activity log (emails, calls, meetings, notes -- with timestamps and participants)
- Opportunity records (renewal dates, stage, amount, pipeline status)
- Custom objects (health score storage, milestone tracking, commitment logging)

**API requirements:**
- Read access to all objects above
- Write access for health scores, lifecycle stage updates, activity logging, and custom objects
- Webhook or event stream for real-time triggers (deal close, contact change, stage change)

**If you do not have this:** You cannot implement any pillar. This is the non-negotiable foundation.

### Product Analytics (Mixpanel, Amplitude, Pendo, Heap, or data warehouse)

**Data consumed:**
- User-level activity (logins, sessions, feature usage, workflow completions)
- Account-level aggregation (DAU/MAU, feature adoption breadth, session depth)
- Event-level data (specific actions, timestamps, user identifiers)
- Licence utilisation (active users vs. purchased seats)

**API requirements:**
- Query by account identifier (company/group level)
- Historical data access (minimum 90 days for baseline computation, 12 months for seasonal analysis)
- Event-level granularity for feature adoption tracking

**If you do not have this:** Pillar 1 (Book Intelligence) is severely limited. Health scores will lack the usage component (35% of the default weight). Usage monitoring, adoption tracking, and expansion detection are all blocked.

### Support Platform (Zendesk, Intercom, Freshdesk, or equivalent)

**Data consumed:**
- Ticket data (ID, subject, description, severity, status, created date, resolved date, CSAT)
- Ticket content (for keyword scanning by bi-competitive-intel and pa-feedback-aggregator)
- SLA data (response time, resolution time vs. targets)

**API requirements:**
- Read access to ticket records and content
- Query by account/organisation identifier
- Webhook for real-time P1 escalation triggers

**If you do not have this:** The support component of health scoring (20% default weight) is unavailable. Risk detection loses the support escalation signal. Competitive intelligence loses its most reliable signal source.

## Strongly Recommended Integrations

These significantly improve the architecture but individual skills can function without them.

### Calendar Integration (Google Calendar, Outlook)

**Used by:** lo-check-in-scheduler, lo-qbr-orchestrator, lo-onboarding-orchestrator, bi-account-brief, ra-engagement-tracker

**Value:** Automated scheduling, meeting completion tracking, no-show detection, pre-meeting brief triggering.

**Without it:** All scheduling becomes manual. The check-in scheduler cannot track meeting completion. The engagement tracker loses the meeting channel.

### Email Integration (Gmail, Outlook)

**Used by:** cc-email-drafter, ra-engagement-tracker, lo-sla-monitor, bi-competitive-intel

**Value:** Activity logging from email, no-reply streak detection, commitment extraction, send-time optimisation.

**Without it:** Email activity must be logged manually in CRM (it won't be). Engagement tracking loses the email channel. Commitment detection from emails is unavailable.

### Call Transcript Integration (Gong, Chorus, or equivalent)

**Used by:** cc-call-summariser, bi-competitive-intel, pa-feedback-aggregator, lo-sla-monitor

**Value:** Automated call summaries, competitive mention detection in conversations, product feedback extraction, commitment extraction.

**Without it:** Call summaries must be written manually. Competitive intelligence loses conversational signals. Product feedback from calls is only captured if the CSM logs it.

### Survey / NPS Tool (Delighted, Wootric, SurveyMonkey)

**Used by:** bi-health-score (sentiment component), ca-advocacy-tracker (NPS follow-up)

**Value:** Sentiment data for health scoring, promoter identification for advocacy.

**Without it:** The sentiment component of health scoring (10% default weight) is unavailable. NPS-triggered advocacy workflows are not possible.

## Data Quality Requirements

The skills produce outputs that are only as good as the data they consume. Common data quality issues that will degrade skill performance:

**Account segmentation inconsistency:** If accounts are not consistently classified by tier, company size, and industry, segment benchmarking produces unreliable results. Audit segmentation before building bi-health-score.

**Stale CRM activity logs:** If CSMs do not log activities (or log them days late), engagement tracking and touchpoint cadence data are inaccurate. cc-crm-updater addresses this by automating activity logging from email and calendar, but it requires those integrations to be in place first.

**Incomplete contact records:** If key contacts are not in the CRM with accurate roles, ra-stakeholder-mapper cannot produce reliable coverage analysis. Data hygiene on contacts is prerequisite to Pillar 7.

**Inconsistent product analytics event taxonomy:** If the same user action is tracked under different event names across product versions, usage pattern detection produces false signals. Standardise the event taxonomy before building bi-usage-monitor.

## Bootstrapping with Incomplete Data

You will not have perfect data on day one. The skills are designed to degrade gracefully:

- If a data source is stale, the skill flags the staleness rather than computing from bad data
- If a health score component has no data, its weight is redistributed to available components
- If segment benchmarks have insufficient sample size, the skill falls back to broader segments

Start building Phase 1 skills as soon as CRM and product analytics integrations are available. Do not wait for perfect data -- the skills themselves will surface where data quality needs improvement.

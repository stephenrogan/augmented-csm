---
name: pa-enablement-orchestrator
description: Coordinates customer enablement activities including training session scheduling, learning path management, certification tracking, and enablement content recommendation based on adoption gaps. Bridges the gap between product access and product competence. Use when asked to schedule training, manage customer education, track certification progress, recommend learning resources, build an enablement plan, coordinate onboarding training, or when any adoption gap could be addressed through customer education. Also triggers for questions about customer training, learning management, enablement programmes, knowledge transfer, or adoption through education.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: product-adoption
  category: enablement-engine
---

# Enablement Orchestrator

Coordinates customer enablement -- training sessions, learning paths, certification tracking, and content recommendation. Part of the Product Adoption & Value Realisation pillar. Bridges the gap between "the customer has access to the product" and "the customer's team knows how to use it effectively."

This is a **coordination and recommendation** skill. It schedules, tracks, and surfaces relevant resources. The actual training delivery -- leading sessions, answering questions, coaching on best practices -- is human work (CSM, enablement specialist, or customer education team).

## When to Run

- **Triggered**: By lo-onboarding-orchestrator during Phase 2-3 (technical activation and adoption)
- **Triggered**: By pa-adoption-tracker when an adoption gap maps to an enablement opportunity (the feature is relevant to the customer's use case but unused, and the likely root cause is awareness or knowledge, not product friction)
- **On-demand**: When a CSM requests an enablement plan or training session for an account
- **Scheduled**: Monthly enablement status review across all accounts in adoption phase

## Core Execution Logic

### Step 1: Assess Enablement Need

Determine what enablement is needed and why:

| Trigger Source | Need Type | Assessment |
|---------------|-----------|-----------|
| New customer onboarding | Foundational training | Standard for all new accounts. Tier and segment determine depth |
| Adoption gap (untouched feature, high relevance) | Feature-specific training | Customer has access but is not using it. Likely a knowledge or awareness gap |
| Adoption gap (abandoned feature) | Re-training or investigation | Customer tried it and stopped. May be a knowledge gap, a product friction issue, or a personnel change (the trained user left). Investigate before prescribing training |
| New team onboarding | Team-specific training | Existing customer adding a new team. They need targeted onboarding, not the full programme |
| Product release | Feature update training | New capabilities released. Relevant customers need to know what changed and how to use it |
| Personnel change | Knowledge transfer | Key user left. Their replacement needs training. The need is urgent because institutional knowledge is leaving |

### Step 2: Map Need to Enablement Resources

Match each need to available resources from the enablement catalogue (see `references/enablement-resources.md`):

| Need Type | Preferred Resource | Delivery Method | Fallback if Resource Does Not Exist |
|-----------|-------------------|----------------|-------------------------------------|
| Foundational product training | Self-serve learning path | LMS or help centre | Live kickoff session with CSM or enablement specialist |
| Feature-specific training | Recorded webinar or guided tutorial | Video library or in-app guidance | Live demo in the next check-in call |
| Use-case deep dive | Live training session | Scheduled call with CSM or specialist | Tailored documentation + async support |
| New feature rollout | Release notes + guided walkthrough | Email with in-app guidance | Mention in next touchpoint with offer to demo |
| Advanced configuration | Technical workshop | Scheduled session with technical resource | Documentation + async technical support |
| Certification | Structured programme with assessment | LMS with certification tracking | Manual tracking by CSM until LMS is available |
| Knowledge transfer (personnel change) | Abbreviated onboarding path | Condensed version of the foundational path, focused on the departing user's workflows | 1:1 training session with CSM |

### Step 3: Build Enablement Plan

For each account with identified enablement needs, create a structured plan:

```json
{
  "account_id": "string",
  "enablement_plan": {
    "created": "2026-03-10",
    "status": "active",
    "items": [
      {
        "id": "EN-2026-0042",
        "topic": "Advanced Reporting",
        "need_source": "adoption_gap",
        "need_detail": "Feature untouched. 78% of segment peers use it. Aligns with customer goal: reduce manual reporting time",
        "resource_type": "live_training",
        "resource": "Advanced Reporting demo session",
        "assigned_to": "Jane Doe (CSM)",
        "target_audience": "Analytics team (3 power users)",
        "target_date": "2026-03-25",
        "completion_criteria": "Attendees can create custom reports independently within 7 days",
        "status": "scheduled",
        "follow_up": "Check pa-adoption-tracker 30 days post-session to verify feature adoption"
      },
      {
        "id": "EN-2026-0043",
        "topic": "API Integration Best Practices",
        "need_source": "new_team_onboarding",
        "need_detail": "12 new engineers joining. Need API onboarding before Q2 integration project",
        "resource_type": "self_serve_path",
        "resource": "API Developer Learning Path (6 modules, ~2 hours)",
        "assigned_to": "customer_self_serve",
        "target_audience": "Engineering team (12 new users)",
        "target_date": "2026-04-01",
        "completion_criteria": "80% of engineers complete all 6 modules",
        "status": "resources_sent",
        "follow_up": "Check LMS completion rates at target date. Follow up individually with non-completers if <80%"
      }
    ],
    "overall_progress": {
      "total_items": 2,
      "completed": 0,
      "in_progress": 2,
      "blocked": 0
    }
  }
}
```

### Step 4: Schedule and Coordinate

**For live training sessions:**
1. Propose times based on CSM and customer availability (via calendar integration)
2. Send calendar invites with pre-session materials (agenda, prerequisites, setup instructions)
3. Prepare session outline: agenda, key topics, hands-on exercises, expected outcomes
4. After session: send follow-up with resources, recording link (if permitted), and next steps
5. Set adoption check reminder at T+30 days

**For self-serve paths:**
1. Send personalised resource links to the appropriate customer contacts
2. Track completion rates (if LMS integration is available)
3. At target date: check completion. If below threshold, follow up with specific non-completers
4. For completed users: check pa-adoption-tracker to verify the learning translated into feature usage

### Step 5: Measure Enablement Effectiveness

After enablement delivery, measure:

| Metric | Source | Success Criteria |
|--------|--------|-----------------|
| Completion rate | LMS or manual tracking | >80% of target audience completed the programme |
| Adoption change | pa-adoption-tracker | Feature moved from untouched/explored to partially adopted or core adopted within 60 days |
| Usage lift | bi-usage-monitor | Measurable increase in feature usage after enablement |
| Customer satisfaction | Post-training survey or CSM feedback | Positive feedback on relevance and quality |
| Time-to-competence | Product analytics | Time from training completion to independent feature usage |

Feed outcomes back into the enablement plan:
- If adoption improved: success. Document what worked for future accounts
- If adoption did not improve: the issue was not knowledge. Investigate product friction, workflow mismatch, or change management resistance. Escalate to pa-feedback-aggregator if the barrier is product-related

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Enablement plan approval | Adoption gaps, available resources, customer context | Which gaps to address, in what order, and with what approach. The plan is a recommendation; the CSM decides what fits the relationship |
| Live training delivery | Session outline, attendee list, pre-materials | How to run the session -- what to emphasise, how to adapt to the audience, how to make it valuable beyond just product training |
| Root cause diagnosis | Adoption gap that persists post-enablement | Whether the issue is knowledge (more training), motivation (change management), or product (feature gap). This distinction determines the next intervention |
| Resource creation request | Gap identified with no existing resource | Whether to escalate to the enablement or content team for new resource creation, address through 1:1 coaching, or accept the gap |
| Customer communication | Enablement recommendations, available resources | How to position enablement with the customer. "Training" can feel condescending if positioned poorly. "Helping your team get more value from features you are already paying for" is better framing |

## Confidence and Limitations

- **High confidence** for scheduling, resource matching, and tracking -- structured coordination workflows with defined rules
- **High confidence** for completion tracking when LMS integration is available -- direct measurement
- **Medium confidence** for need assessment -- adoption gaps are measurable, but whether the root cause is a knowledge gap (enablement can fix) vs. a motivation gap (change management) vs. a product gap (feature issue) requires human diagnosis
- **Medium confidence** for resource-need matching -- the catalogue match is based on topic alignment, but the best resource for a specific customer depends on their learning style, technical depth, and team size
- **Low confidence** for enablement effectiveness prediction -- whether a training session will close an adoption gap depends on factors the agent cannot assess: learner engagement, internal change readiness, management support, and competing priorities
- Cannot create new enablement content. If no suitable resource exists, the skill flags the gap for the enablement or content team. Until the resource is created, the CSM must address the need through direct coaching
- Self-serve completion tracking requires LMS integration. Without it, the skill can track whether resources were sent but not whether they were consumed. This is a significant blind spot -- many customers click the link and never complete the path
- Enablement impact measurement requires a 30-60 day lag. The skill cannot assess whether a session was effective until enough time has passed for the learning to translate into feature usage

## Dependencies

**Required:**
- pa-adoption-tracker (adoption gap data that triggers enablement needs)
- CRM API (account and contact data for targeting)
- Calendar integration (scheduling for live sessions)

**Strongly recommended:**
- LMS or help centre integration (for resource catalogue, self-serve path delivery, and completion tracking)
- bi-usage-monitor (for post-enablement usage lift measurement)
- lo-onboarding-orchestrator (for onboarding-phase enablement coordination)
- pa-benchmark-engine (for peer adoption rates that contextualise enablement priorities)

**Downstream consumers:**
- pa-adoption-tracker (enablement outcomes feed back into adoption classification)
- bi-health-score (adoption improvement from enablement influences the usage component)
- cc-qbr-deck-builder (enablement progress and outcomes for QBR reporting)
- lo-milestone-tracker (enablement milestones as part of success plans)

## References

- `references/enablement-resources.md` -- Resource catalogue structure, matching logic, and maintenance process

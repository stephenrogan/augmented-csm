# Milestone Plan Templates

Segment-default milestone plans for accounts without custom plans.

## Mid-Market Standard Plan (30-day onboarding, 12-month contract)

| # | Milestone | Type | Target | Detection Method |
|---|-----------|------|--------|-----------------|
| 1 | First admin login | Activation | Day 3 | Product analytics: admin login event |
| 2 | Configuration complete | Activation | Day 10 | Product analytics: all required settings configured |
| 3 | First core workflow executed | Activation | Day 14 | Product analytics: core workflow completion event |
| 4 | 50% of licensed users active | Adoption | Day 30 | Product analytics: unique users / purchased seats |
| 5 | 80% of licensed users active | Adoption | Day 60 | Product analytics: unique users / purchased seats |
| 6 | Second use case adopted | Depth | Day 90 | Product analytics: distinct workflow type count >= 2 |
| 7 | First QBR completed | Lifecycle | Day 90 | CRM: QBR activity logged |
| 8 | ROI measurement captured | Outcome | Day 120 | CSM confirmation: customer-validated outcome |
| 9 | Renewal secured | Lifecycle | Day 330 | CRM: renewal opportunity closed-won |

## Enterprise Standard Plan (60-day onboarding, 12-month contract)

| # | Milestone | Type | Target | Detection Method |
|---|-----------|------|--------|-----------------|
| 1 | Kickoff call completed | Activation | Day 5 | CRM: kickoff activity logged |
| 2 | Technical setup complete (SSO, integrations) | Activation | Day 21 | Product analytics: integration active + SSO configured |
| 3 | Pilot team live | Activation | Day 30 | Product analytics: first user group active |
| 4 | Pilot team value confirmed | Outcome | Day 45 | CSM confirmation: pilot success criteria met |
| 5 | Rollout plan agreed | Adoption | Day 50 | CRM: rollout plan documented |
| 6 | Full rollout complete | Adoption | Day 90 | Product analytics: target user count reached |
| 7 | First QBR completed | Lifecycle | Day 90 | CRM: QBR activity logged |
| 8 | Executive sponsor engaged | Depth | Day 120 | CRM: exec sponsor touchpoint logged |
| 9 | ROI report delivered | Outcome | Day 150 | CRM: ROI document shared with customer |
| 10 | Expansion conversation (if applicable) | Expansion | Day 180 | CRM: expansion opportunity created |
| 11 | Renewal secured | Lifecycle | Day 330 | CRM: renewal opportunity closed-won |

## SMB Standard Plan (14-day onboarding, 12-month contract)

| # | Milestone | Type | Target | Detection Method |
|---|-----------|------|--------|-----------------|
| 1 | Account created and first login | Activation | Day 1 | Product analytics: first login event |
| 2 | Core workflow completed | Activation | Day 7 | Product analytics: core workflow completion |
| 3 | Regular usage established (3+ sessions/week) | Adoption | Day 30 | Product analytics: session frequency |
| 4 | Full feature exploration (50%+ features used) | Depth | Day 60 | Product analytics: feature adoption breadth |
| 5 | Renewal secured | Lifecycle | Day 330 | CRM or billing: renewal event |

## Custom Plan Guidelines

When a CSM creates a custom milestone plan:
- Every milestone must have a measurable success criterion (not "customer is happy" but "customer reports 20% time savings")
- Every milestone must have a detection method (how will we know it happened?)
- Target dates should be realistic but stretch -- if the customer can comfortably hit every milestone, the plan is not ambitious enough
- Include at least one outcome milestone (business result, not just usage) -- this is what justifies the renewal
- Review the plan at every QBR and adjust as needed

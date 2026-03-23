# Human Decision Guide: Onboarding Orchestration

## Your Role

The Onboarding Orchestrator manages the workflow -- tracking phases, triggering tasks, and monitoring timeline adherence. Your job is to manage the customer relationship through onboarding: setting expectations, removing blockers, adapting the plan when reality diverges, and ensuring the customer reaches first value. The agent runs the process. You own the outcome.

## When You Will See This

Onboarding alerts surface when:

1. **Phase transition** -- account is ready to move from one onboarding phase to the next
2. **Phase delay** -- a phase has exceeded its expected duration
3. **Blocker detected** -- a dependency (customer action, integration, data migration) is stalling progress
4. **Onboarding complete** -- all phases finished, account transitions to active lifecycle

## Decision Framework

### 1. Assess readiness for phase transition

Before advancing an account to the next phase:
- Has the customer actually completed the current phase requirements, or just checked the boxes?
- Is the customer's team confident and competent, or were they hand-held through every step?
- Are there unresolved issues from the current phase that will compound in the next?

### 2. Decide on action

| Situation | When to Use | Next Step |
|-----------|-------------|-----------|
| **Advance** | Phase criteria genuinely met, customer is ready | Transition to next phase. Communicate what is coming and what the customer needs to do |
| **Hold** | Criteria technically met but customer is not ready (team not trained, key person unavailable) | Keep in current phase. Address the readiness gap before moving forward |
| **Accelerate** | Customer is technically sophisticated and moving faster than the standard timeline | Compress the timeline. Do not slow down a capable customer with unnecessary process |
| **Reset** | Onboarding has stalled completely, customer has lost momentum | Restart the conversation. Understand what went wrong. Rebuild the plan with realistic dates and clear ownership |
| **Escalate** | Internal dependency is blocking progress (integration issue, environment setup, data migration failure) | Route through ic-escalation-router. Onboarding delays are revenue delays -- escalate early |

## Special Handling

### Enterprise Onboarding

Enterprise accounts typically involve multiple stakeholders, complex integrations, and change management requirements. The standard onboarding timeline is a starting point. Adapt based on the customer's internal complexity. The biggest risk is not technical -- it is organisational readiness.

### Customer Disengagement During Onboarding

If the customer stops responding during onboarding, do not just send follow-up emails. This is a critical signal. A customer who disengages before reaching value is at extreme churn risk. Escalate to your manager and consider executive-to-executive outreach to re-establish momentum.

### Mismatched Expectations from Sales

If the customer's expectations about onboarding timeline, complexity, or required effort do not match reality, address it immediately. Manage expectations early and honestly. A customer who feels misled during onboarding carries that distrust through the entire relationship.

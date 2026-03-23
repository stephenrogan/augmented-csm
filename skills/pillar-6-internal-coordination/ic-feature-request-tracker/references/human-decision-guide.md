# Human Decision Guide: Feature Request Prioritisation

## Your Role

The Feature Request Tracker aggregates, deduplicates, and weights feature requests from customers across all input channels. Your job is to decide which requests to champion internally, how to position them for product prioritisation, and how to manage customer expectations on requests that won't be built. The agent organises the demand signal. You decide what to do with it.

## When You Will See This

Feature request materials surface:

1. **When cc-call-summariser or pa-feedback-aggregator identifies a feature request** from a customer conversation or feedback channel
2. **When you manually log a request** from a customer interaction
3. **Weekly** during the roadmap status check when shipped or declined features are detected, triggering customer follow-up

## Decision Framework

### 1. Evaluate request validity

Before escalating any request, verify what you are actually dealing with:
- Is this a genuine product gap or a workflow problem? Many feature requests are actually training gaps, configuration issues, or undiscovered existing features. Check before escalating to product.
- Is the customer asking for what they need, or describing a specific implementation? Understand the job-to-be-done behind the request. "We need a dashboard" might mean "we need visibility into X metric." The latter gives product more room to solve the problem well.
- How many accounts have requested this? Single-account requests rarely earn prioritisation unless the account is strategically critical.

### 2. Decide your action

| Decision | When to Use | Next Step |
|----------|-------------|-----------|
| **Champion** | High volume, high revenue weight, clear product gap, aligned with roadmap direction | Build the internal case with aggregated data. Present to product with revenue impact, account names, and the job-to-be-done |
| **Log and monitor** | Valid request but low volume or unclear demand pattern | Track in the system. Set a review threshold (e.g., revisit when 5+ accounts request, or when $500K+ ARR is attached). Do not champion weak signals |
| **Redirect** | Request is actually a configuration, training, or workflow issue | Resolve with the customer. Close the request with documentation of the solution. This is a positive outcome -- the customer gets value faster than waiting for a feature build |
| **Decline transparently** | Request conflicts with product direction, is not technically feasible, or serves too narrow a use case | Communicate honestly to the customer. Explain the reasoning. Offer alternatives where they exist. Customers respect honesty more than vague promises |

### 3. Communicate back to the customer

Every feature request deserves a response, even if the answer is "not now." The tracking system ensures nothing falls through the cracks. Your job is to close the loop with the customer in a way that maintains trust.

## Special Handling

### Strategic account requests

When a top-tier account requests a feature, the volume threshold does not apply in the same way. One strategic account asking is sufficient to champion -- but frame it as strategic relationship protection, not as a one-off accommodation. Product teams respond to pattern and revenue signals, not to "this customer is important." Quantify the risk: "This account represents $800K ARR and the champion has explicitly tied renewal to this capability."

### Requests that are already on the roadmap

Do not just tell the customer "it's on the roadmap." Give them a meaningful timeline range if available. Connect them with the PM if appropriate -- customers who feel heard become advocates. Use their interest as validation data for the product team. Roadmap alignment is a relationship-building opportunity, not a deflection tactic.

### The request graveyard

Feature requests that have been logged for 12+ months with no movement are damaging to track. They create a false sense that the system is working. Conduct a quarterly purge: close requests that will not be built, communicate honestly to the affected customers, and remove the dead weight from the pipeline. A clean backlog is a useful backlog.

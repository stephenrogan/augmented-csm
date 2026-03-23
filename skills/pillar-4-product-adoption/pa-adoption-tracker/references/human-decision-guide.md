# Human Decision Guide: Adoption Gap Triage

## Your Role

The Adoption Tracker measures feature-level usage and identifies gaps -- features the customer has access to but is not using. Your job is to diagnose why adoption has stalled and decide the right intervention. The agent tells you what is not being used. You figure out why and what to do about it.

## When You Will See This

Adoption alerts surface when:

1. **Untouched high-relevance feature** -- a feature most peers use remains unused by this customer
2. **Abandoned feature** -- a previously used feature has been dropped
3. **Adoption plateau** -- overall adoption score has flatlined for 60+ days
4. **Weekly portfolio adoption report** -- summary of adoption health across your book

## Decision Framework

### 1. Diagnose the root cause

Before prescribing an intervention, determine why the feature is not being used:
- **Awareness**: Do they know the feature exists? Many adoption gaps are simply awareness gaps
- **Knowledge**: Do they know how to use it? Feature exists, awareness exists, skill does not
- **Motivation**: Do they see the value? They know about it, could learn it, but do not see why it matters
- **Product friction**: Did they try it and bounce? The feature may be difficult, buggy, or poorly suited to their workflow
- **Irrelevance**: Is this feature genuinely not relevant to their use case, despite peer adoption?

### 2. Decide on action

| Root Cause | When to Use | Next Step |
|-----------|-------------|-----------|
| **Awareness** | Customer does not know the feature exists | Mention it in your next touchpoint. Share a quick overview or resource link |
| **Knowledge** | Customer knows about it but does not know how to use it | Route to pa-enablement-orchestrator for training. Live demo or self-serve path depending on complexity |
| **Motivation** | Customer does not see the value for their use case | Frame the value specifically for their context. Use peer benchmarks. Show what similar companies achieve |
| **Product friction** | Customer tried and stopped (abandoned status) | Investigate with the customer. If the feature is genuinely difficult, route feedback to pa-feedback-aggregator |
| **Irrelevance** | Feature is not relevant to this customer despite peer usage | Accept the gap. Do not push features the customer does not need to inflate an adoption score |

## Special Handling

### Abandoned Features

Abandonment is a stronger signal than non-adoption. Something changed. Common causes: the trained user left, a workflow changed, the feature broke for them, or a competitor tool replaced it. Investigate the abandonment timeline and correlate with other events before prescribing re-training.

### Pre-QBR Adoption Review

Before a QBR, review adoption gaps that you want to discuss. Choose 1-2 high-impact gaps to address -- not the full list. Overwhelming the customer with a catalogue of unused features feels like a lecture, not a strategic conversation.

### The Adoption Score Trap

A high adoption score does not mean the customer is getting value. A low adoption score does not mean they are not. Some customers extract massive value from 3 features. Do not chase breadth at the expense of depth. The score is a signal, not a goal.

# Competitor Registry

Defines the keyword registry used by the Competitive Intelligence Monitor for signal detection.

## Registry Structure

The registry is a structured dataset with four categories. Each entry includes the keyword/phrase, the category, and a context rule for reducing false positives.

## Category 1: Direct Competitors

These are companies competing for the same budget and use case. Detection of these names in evaluative context is a high-strength signal.

| Keyword | Context Rule |
|---------|-------------|
| [Competitor 1 name] | Flag unless context clearly indicates a different use case |
| [Competitor 1 product name] | Same as above |
| [Competitor 2 name] | Flag unless context clearly indicates a different use case |
| [Add all direct competitors] | -- |

**Maintenance**: Review quarterly. Add new entrants as they appear in win/loss data.

## Category 2: Adjacent Competitors

Companies expanding into your space from adjacent markets. Lower base severity than direct competitors because the overlap may be partial.

| Keyword | Context Rule |
|---------|-------------|
| [Adjacent Competitor 1] | Flag only if mentioned in context of your product's core use case |
| [Add adjacent competitors] | -- |

**Maintenance**: Review bi-annually. Adjacent threats evolve slowly.

## Category 3: Evaluation Language

Generic language indicating active evaluation, regardless of specific competitor.

| Phrase | Context Rule |
|--------|-------------|
| "evaluating alternatives" | High signal in any context |
| "looking at other options" | High signal in any context |
| "comparing solutions" | High signal if referencing your product category |
| "RFP" or "request for proposal" | High signal -- formal evaluation underway |
| "switch to" or "switching to" | High signal -- decision may already be made |
| "migrate from" or "migrating from" | Critical -- active departure in progress |
| "contract termination" | Critical -- departure decision made |
| "not renewing" | Critical -- departure decision made |
| "cancel" or "cancellation" | High signal -- check if referencing your product specifically |

**Maintenance**: Review quarterly based on language observed in actual churn cases.

## Category 4: Migration Language

Language indicating the evaluation has progressed beyond consideration to active transition planning.

| Phrase | Context Rule |
|--------|-------------|
| "data export" (in context of bulk/full export) | Medium signal -- distinguish from routine exports |
| "transition plan" | High signal |
| "wind down" | High signal if referencing your product |
| "offboarding" | High signal if referencing your platform |
| "import to [competitor]" | Critical |
| "API migration" | High signal -- technical migration underway |

## False Positive Reduction Rules

1. **Same-company, different use case**: If the customer mentions using a competitor for an entirely different function (e.g., "we use [competitor] for project management" when your product is analytics), suppress the signal
2. **Historical reference**: If the mention is about a past evaluation that was already resolved ("we looked at [competitor] last year but chose to stay"), suppress unless the language suggests re-evaluation
3. **Feature comparison without intent**: "Does your product do X like [competitor]?" is a feature question, not an evaluation signal. Log it but do not alert unless it clusters with other signals
4. **Internal discussion**: If the mention is in an internal note or CSM-initiated context, suppress -- it is not a customer signal

## Registry Update Process

1. Quarterly: Review win/loss data for the last 90 days. Add any new competitors that appeared in loss reasons
2. Quarterly: Review suppressed/dismissed alerts for the last 90 days. If a keyword consistently produces false positives, add a more specific context rule
3. Annually: Full registry audit. Remove competitors that are no longer active threats. Update adjacent competitor list based on market changes

---

# Human Decision Guide: Competitive Signals

## Core Principle

Never lead a competitive conversation with defensiveness. The customer is evaluating alternatives because they have an unmet need, not because they want to hurt your feelings. Your job is to find and address the unmet need.

## Response Framework by Signal Strength

### High-Strength Signal (Direct Evaluative Mention)

The customer or their team has explicitly mentioned evaluating a competitor for your use case.

**Do not**:
- Panic or escalate to your entire leadership chain before investigating
- Send the customer competitive battle cards or pricing concessions unprompted
- Pretend you did not notice (if the mention was in a direct conversation)

**Do**:
1. Investigate the root cause. What need is not being met? Is it product, support, pricing, or relationship?
2. Prepare your response around the unmet need, not around the competitor
3. If appropriate, acknowledge it naturally: "I understand you are looking at how to solve [the underlying problem]. I want to make sure we are covering that for you -- can we walk through it together?"
4. Brief your manager with: the signal evidence, your hypothesis on the root cause, your planned response, and what you need (if anything) to execute it

### Medium-Strength Signal (Behavioural or Indirect)

Behavioural signals (data exports, documentation access) or indirect mentions suggest evaluation activity.

**Do not**:
- Confront the customer with "I noticed you are exporting data"
- Assume the worst -- data exports have many legitimate explanations

**Do**:
1. Note the signal and look for corroborating evidence
2. In your next natural touchpoint, explore whether there are unmet needs: "I wanted to check in on how things are going -- is there anything we could be doing better for you?"
3. If the signal persists or clusters with other risk signals, escalate to a more direct investigation

### Low-Strength Signal (Engagement Decline Only)

Engagement is declining with no explicit competitive indicators.

**Do not**:
- Alert the customer that their engagement is declining
- Assume competitive evaluation is the cause

**Do**:
1. Treat as a general risk signal, not a competitive signal specifically
2. Investigate through normal risk triage (see Risk Detector human decision guide)
3. Keep the competitive hypothesis in mind but do not lead with it

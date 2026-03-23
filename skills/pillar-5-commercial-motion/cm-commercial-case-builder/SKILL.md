---
name: cm-commercial-case-builder
description: Assembles data-driven commercial cases for expansion conversations by compiling usage evidence, value metrics, benchmark comparisons, and pricing context into structured proposals. Use when asked to build an expansion proposal, create an upsell case, prepare a commercial conversation, assemble evidence for a pricing discussion, draft an expansion business case, or when any expansion signal needs to be translated into a customer-ready commercial narrative. Also triggers for questions about expansion proposals, upsell preparation, commercial evidence, or growth case building.
license: MIT
metadata:
  version: "1.0.0"
  pillar: commercial-motion
  category: commercial-ops
---

# Commercial Case Builder

Assembles the evidence package for expansion conversations. Pulls usage data, value metrics, benchmark comparisons, and pricing context into a structured proposal that the CSM can use to frame the commercial discussion. Part of the Commercial Motion pillar.

This is a **data assembly and formatting** skill. It builds the case. The CSM owns the conversation -- timing, framing, negotiation, and relationship management are entirely human decisions.

## When to Run

- **Triggered**: By bi-expansion-detector when an expansion signal is acknowledged by the CSM
- **On-demand**: When a CSM is preparing for a specific expansion conversation
- **Triggered**: By lo-renewal-manager when a renewal includes an expansion component

## Core Execution Logic

### Step 1: Identify Expansion Type

From the expansion signal and CSM input, classify the opportunity:

| Expansion Type | Signal Pattern | Commercial Implication |
|---------------|---------------|----------------------|
| Seat growth | Licence utilisation >80%, credential sharing detected, new team adoption | More users on the current tier. Pricing = per-seat increment |
| Tier upgrade | Feature-gating hits, power users needing advanced capabilities | Current users moving to a higher product tier. Pricing = tier price difference |
| Cross-sell | New department interest, adjacent use case emerging | New product or module for a new use case. Pricing = new product pricing |
| Geographic expansion | New region or entity adopting | Same product, new contract entity. Pricing = new agreement |

### Step 2: Assemble Evidence Package

Pull from all relevant skills:

**Value already delivered (lead with this):**
- ROI metrics from pa-value-reporter (headline number + supporting evidence)
- Usage depth and breadth from pa-adoption-tracker (show they are getting value from what they have)
- Benchmark position from pa-benchmark-engine (show they are a strong performer among peers)

**Growth evidence (show the natural progression):**
- Expansion signals from bi-expansion-detector (what specifically triggered the opportunity)
- Usage trend from bi-usage-monitor (growing usage is the foundation for a growth conversation)
- New team or department adoption (organic spread indicates internal advocacy)

**Capacity constraint evidence (show the current limit):**
- Licence utilisation rate and trend
- Feature-gating hit count and frequency
- Users working around limitations (credential sharing, manual workarounds)

**Commercial context:**
- Current ARR and contract terms from CRM
- Pricing tier and what the next tier unlocks
- Previous expansion history (expansions build on each other)
- Renewal date (expansion conversations are stronger when renewal is not imminent -- it separates the growth conversation from the retention conversation)

### Step 3: Compute Switching Cost Context

Not for sharing with the customer, but for the CSM's negotiation preparation:
- Data migration complexity if they were to leave
- Integration rebuilding effort
- Team retraining time
- Workflow reconstruction
- Productivity loss during transition

This context helps the CSM understand the customer's negotiating position. A customer with high switching costs has less leverage; a customer with low switching costs has more. The CSM adjusts approach accordingly.

### Step 4: Structure the Proposal

**Internal prep document (for CSM eyes only):**
- Full evidence package with all data
- Pricing options: standard price, discount authority parameters, bundling options
- Negotiation notes: likely objections, customer's probable counter-arguments, your responses
- Risk factors: what could derail this conversation (open support issues, budget timing, stakeholder gaps)
- Recommended approach: consultative vs. transactional, who to present to, timing

**Customer-facing summary (for the conversation):**
- Value delivered so far (lead with what they have gained -- never lead with pricing)
- Growth evidence (show the natural progression, not a sales push)
- What the expansion unlocks (specific capabilities, capacity, or use cases -- not feature lists)
- Investment context (ballpark pricing framed as investment, not cost. Formal quote comes from sales/finance)

### Step 5: Generate Output

```json
{
  "account_id": "string",
  "expansion_type": "seat_growth",
  "current_arr": 42000,
  "proposed_expansion_value": 12000,
  "total_proposed_arr": 54000,
  "evidence": {
    "value_delivered": {
      "headline": "340 hours saved in Q1 through automated workflows",
      "supporting": ["2847 workflow completions (+22% QoQ)", "75% feature adoption (above segment median)", "78% active user ratio (growing)"]
    },
    "growth_signals": {
      "licence_utilisation": "93% for 45 days -- capacity ceiling reached",
      "organic_spread": "12 new users from Marketing department in last 40 days",
      "credential_sharing": "3 users detected sharing credentials"
    },
    "benchmark_position": "Above average across all metrics. Top quartile in workflow completions",
    "switching_cost": "High -- 3 integrations, 47 trained users, 18 months of workflow configuration"
  },
  "internal_prep": {
    "pricing_standard": 12000,
    "discount_authority": "CSM can offer up to 10% on seat additions without approval",
    "likely_objections": ["Budget timing -- Q2 budget may already be committed", "Want to see the open P2 ticket resolved first"],
    "recommended_approach": "Lead with the Marketing team expansion as evidence of broadening value. Frame seats as making official what is already happening organically. Do not discount proactively -- wait for a pricing objection before offering flexibility.",
    "risk_factors": ["Open P2 ticket on API latency -- resolve before commercial conversation", "CFO not engaged -- may need champion to socialise internally before formal ask"],
    "timing": "After P2 resolution. Target within 2 weeks"
  },
  "customer_summary": {
    "opening": "Your team has outgrown the current setup. 93% of seats are in use and your Marketing team has started adopting organically. We should make sure everyone who needs access has it.",
    "value_frame": "Your team saved 340 hours last quarter through automated workflows -- that is up 22% from the prior quarter. The value is compounding as adoption deepens.",
    "expansion_frame": "Adding 15 seats would eliminate the credential sharing your team is working around and give the Marketing team proper access. The investment is [X] per year.",
    "forward_look": "With the Marketing team onboarded, there is also an opportunity to explore the Advanced Reporting module -- your analytics team has been asking about custom dashboards."
  },
  "requires_csm_review": true
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Timing | Account health, open issues, renewal date, budget cycle | Whether now is the right moment. The data may say yes but the relationship may say wait |
| Framing | Customer-facing summary with value-led opening | How to position the expansion -- consultative vs. direct, formal meeting vs. casual conversation |
| Who to present to | Stakeholder map, champion vs. economic buyer | Whether to go through the champion first or directly to the budget holder |
| Pricing strategy | Standard pricing, discount authority, competitor context | Whether to hold price, offer flexibility, bundle with renewal, or structure as a multi-year deal |
| Escalation | Risk factors, stakeholder gaps | Whether to involve a sales partner, executive sponsor, or manager in the conversation |

## Confidence and Limitations

- **High confidence** for evidence assembly -- pulling data from defined sources with structured output is deterministic
- **Medium confidence** for opportunity sizing -- seat growth is straightforward to estimate, but tier upgrade and cross-sell values depend on customer adoption patterns that are harder to predict
- **Medium confidence** for objection anticipation -- common objections are predictable, but the specific objection this customer will raise depends on their internal dynamics
- **Low confidence** for timing recommendation -- when to have the conversation depends on relationship temperature, budget cycles, internal politics, and competing priorities that the agent cannot assess
- Cannot predict whether the customer will say yes. The case is the input; the outcome depends on the conversation
- The customer-facing summary is a starting framework, not a script. The CSM must adapt to the specific relationship and conversation flow

## Dependencies

**Required:**
- bi-expansion-detector (expansion signals that trigger the case)
- pa-value-reporter (value evidence for the case)
- CRM API (contract data, pricing, opportunity management)

**Strongly recommended:**
- pa-adoption-tracker (adoption depth evidence)
- pa-benchmark-engine (peer comparison for value context)
- bi-account-brief (full account context for preparation)
- ra-stakeholder-mapper (stakeholder coverage for routing the conversation)

**Downstream consumers:**
- CSM (primary consumer -- uses the case to prepare for and execute the conversation)
- Sales partner (if the expansion involves a formal sales process)
- CRM opportunity (case data feeds into the expansion opportunity record)

## References

- `references/commercial-frameworks.md` -- Framing templates by expansion type, pricing conversation structures, and objection response patterns

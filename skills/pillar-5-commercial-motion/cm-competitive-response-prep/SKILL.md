---
name: cm-competitive-response-prep
description: Prepares structured competitive response materials when a competitive threat is detected on an account. Assembles value evidence, competitive differentiation, switching cost analysis, and a response framework for the CSM. Use when asked to prepare a competitive response, build a retention case against a competitor, create a win-back plan, or when bi-competitive-intel has flagged a competitive signal that the CSM is preparing to address. Also triggers for questions about competitive positioning, win-back preparation, retention defence strategy, or handling a customer evaluation.
license: MIT
metadata:
  author: Stephen Rogan
  version: "1.0.0"
  pillar: commercial-motion
  category: commercial-ops
---

# Competitive Response Prep

Prepares account-specific competitive response materials when a threat is detected. Assembles value evidence, switching cost analysis, and response framework. Part of the Commercial Motion pillar.

This is a **preparation and evidence assembly** skill. It arms the CSM with data and structure. The response strategy, conversation execution, and relationship management are entirely human-led.

## When to Run

- **Triggered**: When CSM acknowledges a competitive signal from bi-competitive-intel and requests preparation
- **On-demand**: When a CSM knows a competitive threat exists and needs materials
- **Triggered**: By lo-renewal-manager when a renewal is At Risk or Critical with a competitive signal present

## Core Execution Logic

### Step 1: Assess the Competitive Situation

From the bi-competitive-intel signal and CSM input, classify:

| Dimension | Options | Why It Matters |
|-----------|---------|---------------|
| Competitor | Named competitor or unknown | Determines whether specific differentiation is possible |
| Scope | Full displacement vs. partial overlap | Full displacement requires a different response than a point solution competing on one feature |
| Evaluation stage | Early consideration, active evaluation, decision imminent | Urgency and approach differ dramatically by stage |
| Trigger | Product gap, pricing, service failure, proactive competitor outreach, or strategic priority shift | Addressing the root cause is more effective than defending against the competitor |

### Step 2: Assemble Retention Evidence

**Value already delivered (the strongest retention argument):**
- ROI metrics from pa-value-reporter -- quantified outcomes the customer has achieved
- Usage depth from pa-adoption-tracker -- show how embedded the product is in their workflows
- Time invested in configuration, integrations, and training -- this is sunk cost the customer may not have quantified

**Switching cost analysis (for internal CSM use -- not customer-facing):**

| Cost Category | Estimation Method |
|--------------|------------------|
| Data migration | Complexity of moving historical data, configurations, and workflows to a new platform |
| Integration rebuilding | Number of active integrations * estimated rebuild time per integration |
| Team retraining | Number of trained users * estimated training hours for a new platform |
| Workflow reconstruction | Number of configured workflows * estimated rebuild time |
| Productivity loss | Estimated weeks of reduced productivity during transition |
| Opportunity cost | Projects that would be delayed while the team focuses on migration |

Total switching cost estimate: express in both time (weeks/months) and cost (estimated labour hours * loaded cost per hour) if possible.

**Competitive differentiation:**
- Feature comparison on the specific capabilities the customer cares about (not a generic feature matrix)
- Areas where your product is objectively stronger for this customer's use case
- Areas where the competitor may be stronger -- acknowledge these honestly. The CSM loses credibility if they dismiss legitimate competitor advantages

### Step 3: Build Response Framework

The framework provides structure for the conversation, not a script.

**By evaluation stage:**

| Stage | Approach | Key Message |
|-------|----------|-------------|
| Early consideration | Proactive value reinforcement. Do not mention the competitor | "I want to make sure we are covering everything you need" |
| Active evaluation | Address the underlying need that triggered the evaluation | "Help me understand what prompted this. I want to address the root cause" |
| Decision imminent | Direct engagement. May require executive involvement and commercial flexibility | "I would like the chance to address [root cause] before you make a final decision" |

**By trigger:**

| Trigger | Response Focus |
|---------|---------------|
| Product gap | Show the roadmap if applicable. Offer workaround. Be honest if the gap is real and not planned |
| Pricing | Lead with value, then discuss pricing. Compete on ROI, not on sticker price |
| Service failure | Acknowledge, apologise, show the recovery plan. The competitor did not win -- you lost. Win back by being better |
| Proactive competitor outreach | The customer was not looking. Reinforce the relationship. Ensure value is visible. Make the competitor's pitch irrelevant |
| Strategic priority shift | Reposition your product's value in the context of the new priorities. If the product genuinely no longer fits, be honest |

### Step 4: Generate Materials

```json
{
  "account_id": "string",
  "competitive_situation": {
    "competitor": "Competitor X",
    "scope": "full_displacement",
    "evaluation_stage": "active_evaluation",
    "trigger": "product_gap",
    "trigger_detail": "Customer needs custom reporting that current tier does not support"
  },
  "retention_evidence": {
    "value_delivered": {
      "headline": "340 hours saved in Q1, 2847 automated workflows",
      "roi_estimate": "3.2x return on annual investment"
    },
    "switching_cost": {
      "integrations_at_risk": 3,
      "trained_users": 47,
      "configured_workflows": 23,
      "estimated_migration_time": "4-6 months",
      "estimated_productivity_loss": "6-8 weeks",
      "total_estimated_cost": "$120k-180k in labour and lost productivity"
    },
    "differentiation": {
      "stronger": ["Workflow automation depth", "Integration ecosystem", "Customer support response time"],
      "comparable": ["Core reporting", "User management", "API access"],
      "weaker": ["Custom dashboard builder -- this is the trigger gap"]
    }
  },
  "response_framework": {
    "approach": "Address the product gap directly. If custom reporting is available on a higher tier, present the upgrade case with value context. If it requires product development, provide timeline and interim workaround.",
    "key_message": "We understand the reporting gap is real. Here is what we can do about it -- and here is the full picture of value you would be walking away from.",
    "do_not": "Do not dismiss the competitor. Do not panic. Do not offer a discount before understanding the full situation.",
    "escalation_recommended": true,
    "escalation_reason": "Product gap is the trigger. Product team should weigh the competitive urgency against roadmap."
  },
  "commercial_flexibility": {
    "csm_authority": "10% discount on tier upgrade without approval",
    "requires_approval": "Larger discounts, extended terms, or contract restructuring",
    "non_negotiable": "Do not discount without tying it to a commitment. Free months or trials create precedent"
  },
  "requires_csm_review": true
}
```

## Handoff to Human

| Decision Point | Context Provided | What the Human Decides |
|---------------|-----------------|----------------------|
| Response strategy | Situation assessment, evidence, framework | How to approach the conversation -- direct vs. indirect, timing, channel |
| Competitive acknowledgement | Differentiation analysis with honest gaps | Whether and how to acknowledge the competitor. Some CSMs prefer to never name the competitor; others address it head-on. Depends on the relationship |
| Executive involvement | Escalation recommendation, account ARR, renewal timeline | Whether to bring in leadership from their side and yours |
| Commercial concessions | Authority parameters, switching cost context | What to offer, when to offer it, and what to require in return |
| Product escalation | Product gap analysis, competitive urgency | Whether to escalate to the product team for roadmap acceleration or workaround development |

## Confidence and Limitations

- **High confidence** for evidence assembly -- value data, switching cost analysis, and feature comparison are factual
- **Medium confidence** for evaluation stage assessment -- the CSM's read on how far the evaluation has progressed is more reliable than the agent's inference from data signals
- **Medium confidence** for differentiation analysis -- feature comparisons are objective, but the relevance of each differentiator to this customer requires human judgment
- **Low confidence** for response strategy -- how to handle a competitive threat depends entirely on relationship dynamics, evaluation stage, and customer politics that the agent cannot assess
- Cannot determine whether the competitor has made a specific commercial offer
- Cannot assess the customer's internal decision-making timeline with precision
- Switching cost estimates are approximations. Actual migration cost depends on factors specific to the customer's implementation (data volume, integration complexity, internal technical resources)

## Dependencies

**Required:**
- bi-competitive-intel (competitive signal that triggers the preparation)
- pa-value-reporter (value evidence for the retention case)
- CRM API (contract data, account context)

**Strongly recommended:**
- pa-adoption-tracker (adoption depth for switching cost context)
- bi-account-brief (full account context)
- ra-stakeholder-mapper (who is involved in the evaluation decision)

## References

- `references/competitive-response-frameworks.md` -- Response templates by evaluation stage, differentiation analysis structure, and escalation decision criteria

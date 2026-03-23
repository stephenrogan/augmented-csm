# Human Decision Guide: Health Score Interpretation

This guide accompanies the Health Score Engine output. When the engine surfaces an account for human attention, this guide helps the CSM interpret the data and decide what to do.

## When You Will See This

The Health Score Engine routes accounts to you under four conditions:

1. **Composite score drops below 65** -- the account has moved from Healthy to At Risk
2. **Any single component drops below the segment 25th percentile** -- one dimension is significantly underperforming peers
3. **Composite declines more than 10 points in 7 days** -- rapid deterioration regardless of absolute score
4. **Data staleness alert** -- one or more data sources are stale, reducing score reliability

## How to Read the Health Record

The health record gives you:
- **Composite score**: The headline number. Useful for prioritisation, not for diagnosis.
- **Component scores**: Where the problem actually is. A composite of 62 could mean usage is cratering while everything else is fine, or it could mean everything is mildly declining. The components tell you which.
- **Trend direction**: Is this getting worse or stabilising? A score of 58 that is improving requires different action than a score of 68 that is declining.
- **Risk drivers**: The specific metrics dragging a component down. This is where diagnosis starts.
- **Data freshness**: If a source is stale, the score is less reliable. Factor this into your interpretation.

## Decision Framework

When an account surfaces, work through this sequence:

### 1. Check for data issues first

Is any source flagged as stale? If yes, the score may be misleading. Check the stale source manually before acting. If the data issue is systemic (affecting multiple accounts), route to CS Ops.

### 2. Identify the driver

Look at the component scores and risk drivers. Which component is pulling the composite down? Which specific metric within that component is the problem?

Common patterns:
- **Usage declining, everything else stable**: Product issue, champion disengagement, or competing priority. Investigate whether the customer is still getting value.
- **Engagement declining, usage stable**: Your contacts may be busy, reorganising, or disengaging from the vendor relationship while still using the product. Check for stakeholder changes.
- **Support spiking, everything else fine**: A specific product issue is frustrating the customer. Check ticket details -- is it one recurring issue or multiple?
- **Sentiment dropping, everything else stable**: Something happened in the relationship. Check recent interactions, survey comments, and call notes.
- **Multiple components declining simultaneously**: This is the most serious pattern. The account is deteriorating across dimensions. Prioritise this over single-component declines.

### 3. Cross-reference with relationship context

The score tells you what the data says. You know things the data does not:
- Is there a reorg happening at the customer?
- Did you recently have a difficult conversation?
- Is the champion distracted by an internal project?
- Is the account in a seasonal pattern the benchmarks do not capture?

If your relationship context contradicts the score, trust your judgment -- but document why. Your override is valuable signal for improving the scoring model.

### 4. Decide on action

| Situation | Options |
|-----------|---------|
| Score decline with clear driver | Address the driver: if usage, investigate with the customer. If support, escalate the ticket pattern. If engagement, reach out. |
| Score decline with no clear driver | Investigate further before acting. Pull the full account brief, check recent call notes, review ticket history. |
| Score below 65 but stable/improving | Monitor. The account may be recovering. Set a review date 14 days out. |
| Rapid decline (>10 points in 7 days) | Act today. This pace of decline usually indicates an event, not a trend. Find out what happened. |
| Data staleness alert | Do not act on the score. Investigate the data gap. If the gap is in your control (e.g., no recent survey sent), address it. If systemic, route to CS Ops. |

### 5. Log your decision

Whatever you decide -- act, monitor, investigate, or dismiss -- log it. This creates the feedback loop that improves the scoring model over time. Specifically:
- If you override the score (e.g., dismiss a risk alert because you know the context), note why
- If you act, note what action and the expected outcome
- If you investigate and find the score was correct, note that too

## What the Score Cannot Tell You

- Whether a champion is privately job-hunting
- Whether the customer's budget has been cut in a way that has not yet reached your contacts
- Whether a competitor approached the economic buyer directly
- Whether the customer's strategic priorities have shifted away from your product's value proposition
- Whether the relationship has trust damage that has not surfaced in measurable engagement

These are all real churn risks that no data model can detect. They are why the human remains at the decision point, and the agent remains at the data layer.

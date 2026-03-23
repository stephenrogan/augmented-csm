# Human Decision Guide: Usage Pattern Alerts

## When You Will See This

The Usage Pattern Monitor routes alerts when it detects a meaningful change in an account's product usage. You will see four types of alerts:

1. **Sudden drop**: >25% decline in a single period. Something happened -- verify data integrity, then investigate
2. **Gradual decline**: 3+ consecutive declining periods. Sustained disengagement, not a blip
3. **Adoption plateau**: Usage stable but below segment median for 60+ days. The account has settled into underutilisation
4. **Breakout growth**: >30% above baseline sustained for 2+ periods. Expansion opportunity

## How to Interpret

### Sudden Drop

**First action**: Check if the data is real. Product outages, tracking failures, and API changes can produce false drops. If data is confirmed:
- Check for concurrent support tickets (product issue affecting the customer)
- Check for stakeholder changes (champion left, reorg)
- Check for competing product evaluation signals
- If no obvious cause, reach out to your primary contact with a specific, non-alarming question about their usage

### Gradual Decline

This is the most common and most dangerous pattern because it happens slowly enough that neither the CSM nor the customer notices.
- Identify which specific metric is declining. Usage breadth declining suggests they are consolidating to fewer features. Session depth declining suggests engagement quality is dropping. Active users declining suggests people are leaving the platform
- Cross-reference the timeline: when did the decline start? What else was happening at the account or in the product at that point?
- This usually requires a conversation with the customer. Frame it as "I noticed your team's usage of [specific feature] has shifted -- wanted to check in on whether that is intentional or if there is something we can help with"

### Adoption Plateau

Not urgent, but important. The customer is using the product but not getting full value.
- Check which features are unused. Are they relevant to the customer's use case?
- This is a consultative opportunity, not a risk intervention. Route to your adoption plan for the account
- If the customer's contract is coming up for renewal and they are significantly underutilising, this becomes a renewal risk -- the ROI case for renewal is weaker

### Breakout Growth

Good news, but worth understanding why.
- New team or department onboarding? Potential expansion conversation
- Existing team deepening usage? Validates the value proposition -- use in the next QBR
- Sudden spike without known cause? Verify it is genuine and not a data artefact (e.g., bot activity, test accounts)

## What Usage Data Cannot Tell You

- Whether the customer is satisfied with the product (they could be using it heavily while hating it)
- Whether usage will translate to renewal (usage is necessary but not sufficient for retention)
- Why a specific person stopped logging in (could be anything from a role change to a holiday)
- Whether the customer is evaluating alternatives (they may maintain current usage while running a parallel evaluation)

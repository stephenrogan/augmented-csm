# Human Decision Guide: Escalation Routing Decisions

## Your Role

The Escalation Router classifies incoming escalations by severity, identifies the correct internal team, and prepares routing documentation. Your job is to validate the classification, decide whether the escalation warrants the proposed routing, and handle the cases that don't fit clean categories. The agent applies rules. You apply judgment.

## When You Will See This

Escalation routing decisions are triggered:

1. **When you initiate an escalation** by setting the escalation flag in CRM or requesting escalation routing
2. **When an issue needs routing** and the system needs your confirmation on the correct path
3. **On SLA monitoring alerts** when an active escalation stalls or breaches its SLA and needs re-routing or re-prioritisation

## Decision Framework

### 1. Validate severity

The agent classifies severity based on defined rules (customer tier, issue type, business impact). You validate based on judgment:
- Is the customer's stated urgency proportional to the actual impact? Some customers escalate everything. Some under-escalate critical issues because they have given up expecting help.
- Is this a recurring issue that has been under-classified previously? A "medium" issue that occurs monthly is effectively a high-severity pattern.
- Does the account's strategic importance warrant escalating the severity? A P2 issue at a $2M account may warrant P1 treatment.

### 2. Decide routing

| Decision | When to Use | Next Step |
|----------|-------------|-----------|
| **Route as classified** | Agent's classification and routing are correct | Approve and send. Add any relationship context that helps the receiving team understand urgency or nuance |
| **Reclassify up** | Customer impact is higher than signals suggest, or the account is strategic | Override severity, add justification, route to the higher tier. Brief the receiving team on why this warrants elevated attention |
| **Reclassify down** | Customer is over-escalating relative to actual impact, or the issue has a known workaround | De-escalate with a clear explanation to the customer. Route to standard support with the workaround documented |
| **Handle directly** | Issue is within your authority and capability to resolve without involving another team | Resolve, document, close. Routing would only add latency for something you can fix now |
| **Combine** | This escalation is related to an existing open case for the same account | Merge with the existing case. Update the routing with combined context so the team sees the full picture |

### 3. Add context the system cannot

Every escalation you route should include one paragraph of context from you: what the customer is feeling, what the relationship history is, and what the resolution needs to achieve beyond fixing the technical issue. This transforms an escalation from a ticket into a situation briefing.

## Special Handling

### Repeat escalators

Some customers escalate everything. The agent will flag repeat patterns. Your decision: is this a customer who needs recalibrated expectations (proactive conversation about severity definitions and support processes), or is there a genuine underlying issue creating repeated friction? The answer determines whether you manage the behaviour or fix the system. Often it is both.

### Executive-originated escalations

When the escalation comes from or involves the customer's executive team, it is automatically high severity regardless of technical impact. Executive attention signals relationship risk. Route to your leadership and brief them before the next customer touchpoint. Executives remember how their escalations were handled.

### Stalled escalations

When the SLA monitor flags a stalled escalation, the default response is to chase the owning team. But first ask: is the escalation stalled because the team is overloaded, because the issue is harder than expected, or because it fell through the cracks? Each cause requires a different intervention. Chasing is only effective for the third.

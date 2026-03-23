# Human Decision Guide: Call Summary Review

## Your Role

The Call Summariser extracts structure from conversations -- action items, decisions, sentiment signals, and risk flags. Your job is to review the summary for accuracy, add the context the transcript cannot capture, and ensure the extracted commitments are realistic and correctly attributed. The agent processes the words. You interpret the room.

## When You Will See This

Summaries are generated after every customer call. You review when:

1. **Post-call summary ready** -- a structured summary is awaiting your review before routing to downstream skills
2. **Sentiment flag** -- the agent detected frustration, escalation language, or competitive mention
3. **Commitment extracted** -- action items with owners and deadlines need your confirmation

## Decision Framework

### 1. Validate accuracy

Transcripts are imperfect. Before approving:
- Are the action items correctly captured? Did the agent miss any or fabricate any from ambiguous language?
- Are owners correctly assigned? "We'll look into that" is vague -- the agent may have assigned it to you when the customer meant their own team
- Are deadlines accurate? "Next week" in conversation may mean different things to you and the customer

### 2. Decide on action

| Situation | When to Use | Next Step |
|-----------|-------------|-----------|
| **Approve as-is** | Summary is accurate and complete | Release to downstream skills. Action items route to lo-sla-monitor, follow-up email drafts to cc-email-drafter |
| **Edit and approve** | Summary is mostly right but needs corrections | Fix inaccuracies before release. Incorrect action items routed downstream cause downstream problems |
| **Add context** | Summary captures the words but misses the subtext | Add your read: was the customer genuinely satisfied or politely frustrated? Was the "maybe" a soft no? Were they enthusiastic or obligated? |
| **Flag risk** | You detected something in the conversation the agent did not -- tone, hesitation, evasion | Add a risk note. Route to bi-risk-detector if warranted. Your read is often ahead of the data |
| **Suppress** | The call was informal, off-the-record, or the customer shared something sensitive | Remove or redact sensitive content before the summary enters the system |

## Special Handling

### Sensitive Conversations

If the customer shared information in confidence (personnel changes, budget concerns, competitive evaluations), decide what goes into the CRM and what stays in your notes. Not everything discussed on a call should be system-visible.

### Multi-Stakeholder Calls

Calls with multiple customer participants often contain conflicting signals. The champion may be enthusiastic while the technical lead is sceptical. The summary may flatten this into a single sentiment. Add the nuance -- who said what matters as much as what was said.

### Commitment Escalation

If the summary captured a commitment you cannot deliver, correct it now -- not after it has been routed to SLA tracking. It is better to renegotiate a commitment immediately than to breach it later.

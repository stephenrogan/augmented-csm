# Commitment Capture Patterns

How to extract and log commitments from different sources.

## Automated Extraction Patterns

### From Call Transcripts

Look for commitment language patterns:
- "I will [action] by [date/timeframe]"
- "We will [action] by [date/timeframe]"
- "Let me [action] and get back to you by [date/timeframe]"
- "I will follow up on [topic]"
- "We can have that to you by [date]"
- "Our team will [action] within [timeframe]"

**Extraction fields:**
- Action: what was committed
- Owner: who made the commitment (CSM, internal team, or customer)
- Deadline: explicit date if stated, or inferred from timeframe ("by Friday," "within a week," "by end of month")
- Context: brief note on what prompted the commitment

**False positive reduction:**
- Exclude hypothetical language: "We could," "We might," "If we were to"
- Exclude questions: "Will you be able to?"
- Exclude conditional language: "If X happens, we will Y" (log as conditional commitment with trigger condition)

### From Emails

Scan outbound CSM emails for commitment language (same patterns as above).

**Additional email-specific patterns:**
- "I will circle back on this by [date]"
- "Expect to hear from me/us by [date]"
- "We are targeting [date] for [deliverable]"

### From Support Tickets

**Automatic SLA tracking:**
- First response SLA: time from ticket creation to first agent response
- Resolution SLA: time from ticket creation to resolution
- Escalation SLA: time from escalation flag to escalation action

These are contractual and should be tracked automatically from the support platform without manual logging.

## Manual Capture

For commitments that cannot be automatically extracted:
- CSM logs commitment directly after a call or meeting
- Required fields: account, description, owner, deadline
- Optional fields: source (which call/meeting), priority, notes

**Best practice**: Log commitments within 1 hour of the interaction. Delayed logging leads to forgotten commitments -- which is exactly the problem this skill exists to prevent.

## Commitment Lifecycle

1. **Created**: Commitment logged (automatically or manually)
2. **Active**: Deadline is in the future, not yet delivered
3. **Due soon**: Within 3 business days of deadline
4. **At risk**: Within 1 business day, not yet delivered
5. **Overdue**: Past deadline, not delivered
6. **Completed**: Owner confirms delivery (or automated detection confirms)
7. **Cancelled**: Commitment is withdrawn (mutual agreement with customer, or circumstances changed)
8. **Renegotiated**: Deadline extended with customer awareness

Track all state transitions with timestamps. The full lifecycle provides accountability data for process improvement.

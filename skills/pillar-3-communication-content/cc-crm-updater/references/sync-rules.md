# CRM Sync Rules

## Activity Logging
- Email: log all sent/received customer emails. Exclude automated sequences, marketing emails, and system notifications
- Calendar: log completed meetings only. Cancelled and no-showed meetings logged as separate event types
- Calls: log completed calls with duration. Voicemails are not touchpoints
- Support: log ticket creation and resolution events. Do not log every internal comment

## Field Update Rules
- Health score: write per computation cadence. Do not overwrite CSM manual override without flagging
- Lifecycle stage: update on stage-change triggers only. Never regress a stage without CSM confirmation
- Last touch date: most recent of any channel. Update continuously

## Conflict Resolution
- If the CSM manually entered a value and the agent computes a different value: flag the conflict, do not overwrite
- CRM is the system of record. Agent updates supplement, not replace, CSM-entered data

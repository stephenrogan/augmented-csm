# Notification Rules

## Urgency Levels
- Immediate: Slack DM within seconds. Champion departure, competitive signal, P1 ticket
- Same day: Slack channel post. Health drop, commitment at risk, risk classification change
- This week: Email or digest inclusion. Expansion signal, milestone achievement
- Digest only: Weekly email summary. Renewals, milestone progress, engagement changes

## Deduplication
- Same event, same account, within 24 hours: notify once, include in digest thereafter
- Related events on same account: consolidate into single notification noting all signals
- Persistent conditions: notify on first detection, then digest only

## Suppression
- Recipient PTO: hold non-immediate, route immediate to backup
- Weekends: batch all non-immediate for Monday delivery
- Per-recipient muting: respect channel and event-type preferences

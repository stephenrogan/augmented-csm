# Signal Registry

Complete definition of every risk signal the Risk Signal Detector monitors. Each entry defines the signal, how to detect it, the default severity, and tuning guidance.

## Registry Structure

Each signal has:
- **Name**: Human-readable identifier
- **Category**: metric-based or event-based
- **Detection method**: How the agent identifies the signal
- **Default severity**: 1 (low) to 5 (critical)
- **Evidence requirements**: What data must accompany the alert
- **Tuning notes**: When and how to adjust the default severity

## Metric-Based Signals

### Health Score Below Threshold

- **Detection**: Health Score Engine composite < 65
- **Default severity**: 3
- **Evidence**: Composite score, all component scores, trend direction, risk drivers from health record
- **Tuning**: Adjust threshold by segment. Enterprise accounts may warrant a higher threshold (70) because the cost of churn is higher. SMB accounts may use 60 if the volume makes 65 too noisy

### Health Score Rapid Decline

- **Detection**: Health Score Engine composite drops >10 points in 7 days
- **Default severity**: 4
- **Evidence**: Current score, score 7 days prior, component-level deltas, any correlated events
- **Tuning**: The 10-point threshold works for most portfolios. If your portfolio has high natural variance (common in PLG with seasonal patterns), consider 15 points

### Usage Gradual Decline

- **Detection**: Usage Pattern Monitor classifies 3+ consecutive declining periods on any tracked metric
- **Default severity**: 3
- **Evidence**: Declining metric name, values over the period, baseline comparison, segment position
- **Tuning**: 3 periods is the default. For daily metrics, this means 3 days (possibly too sensitive). For weekly metrics, 3 weeks (more reliable). Consider using weekly aggregation for this signal

### Usage Sudden Drop

- **Detection**: Usage Pattern Monitor classifies >25% single-period decline
- **Default severity**: 4
- **Evidence**: Metric name, prior period value, current period value, percentage change
- **Tuning**: Always verify data integrity before escalating. False positives from tracking failures, holiday periods, or product changes are common. Add a "verify data" step before surfacing to human

### Adoption Plateau

- **Detection**: Usage Pattern Monitor flags usage below segment median for 60+ consecutive days with no meaningful trend change
- **Default severity**: 2
- **Evidence**: Metric values, segment median, duration below median
- **Tuning**: 60 days is the default. Shorter windows produce more false positives (accounts may naturally fluctuate around the median). Longer windows risk missing accounts that have quietly settled into underutilisation

### Support Volume Spike

- **Detection**: Ticket count in current 30-day window exceeds 2x the account's 90-day average
- **Default severity**: 3
- **Evidence**: Current ticket count, 90-day average, ticket severity breakdown, top ticket topics
- **Tuning**: The 2x multiplier works for accounts with established support patterns. For accounts with very low baseline ticket volume (1-2 per month), even a small increase can trigger this. Consider a minimum absolute threshold (e.g., at least 5 tickets in the current window)

### Sentiment Decline

- **Detection**: Most recent NPS or CSAT score falls below the segment 25th percentile
- **Default severity**: 3
- **Evidence**: Current score, prior score, segment benchmark, response date
- **Tuning**: Single survey responses are noisy. If possible, use a 2-response rolling average. If only one response exists, note the limited data in the alert

## Event-Based Signals

### Champion Departure

- **Detection**: Primary contact flagged as "Champion" in CRM is marked as inactive, or LinkedIn monitoring detects a role change/departure
- **Default severity**: 5
- **Evidence**: Contact name, role, departure date (confirmed or estimated), replacement (if known)
- **Tuning**: This is the highest-severity signal. Do not reduce below 4. The loss of a champion is the single strongest predictor of churn in relationship-driven CS models

### Executive Sponsor Change

- **Detection**: Contact flagged as "Executive Sponsor" in CRM changes
- **Default severity**: 4
- **Evidence**: Departing sponsor, new sponsor (if known), change date
- **Tuning**: Severity depends on the relationship with the new sponsor. If unknown, maintain severity 4 until the CSM has established contact

### Declined Meetings

- **Detection**: Calendar integration shows 2+ scheduled meetings declined or no-showed by customer contacts within 30 days
- **Default severity**: 3
- **Evidence**: Meeting dates, attendee names, decline/no-show count
- **Tuning**: Distinguish between rescheduled (lower concern) and outright declined/ignored (higher concern). If the calendar integration cannot distinguish, note this limitation

### No-Reply Streak

- **Detection**: 3+ consecutive CSM emails to the primary contact with no reply, spanning 14+ days
- **Default severity**: 3
- **Evidence**: Email dates, subjects, total days since last reply
- **Tuning**: Check whether the contact is OOO or on leave before alerting. If email integration provides OOO auto-replies, suppress the signal during that window

### P1 Support Escalation

- **Detection**: A ticket classified as P1 (critical) is opened, or an existing ticket is escalated to P1
- **Default severity**: 4
- **Evidence**: Ticket ID, issue summary, opened date, current status, days open
- **Tuning**: P1 tickets are inherently high-urgency. Severity should remain at 4 unless the account has a history of P1 tickets that resolve quickly without relationship impact

### Competitor Mention

- **Detection**: Competitor name or evaluation language detected in support tickets or call transcripts
- **Default severity**: 4
- **Evidence**: Source (ticket/call), excerpt or context, competitor named, date
- **Tuning**: Monitor for false positives. Mentions like "our competitor uses your product for X" are not risk signals. The detection should focus on evaluative language: "comparing," "looking at alternatives," "considering switching"

### Contract Objection or Delay

- **Detection**: CRM renewal opportunity stalls (no stage change in 30+ days) or moves backward
- **Default severity**: 3
- **Evidence**: Opportunity ID, current stage, days in stage, prior stage changes
- **Tuning**: Combine with days-to-renewal for urgency. A stalled renewal 180 days out is a watch item. A stalled renewal 45 days out is urgent

### Payment Overdue

- **Detection**: Invoice remains unpaid >30 days past due date
- **Default severity**: 3
- **Evidence**: Invoice ID, amount, due date, days overdue
- **Tuning**: Distinguish between administrative delays (common in enterprise procurement) and potential financial distress. If the account has a history of late payments that always resolve, reduce severity to 2

## Adding New Signals

When adding a signal to the registry:
1. Define the detection method clearly -- what data, what threshold, what logic
2. Set a default severity with rationale
3. Specify evidence requirements
4. Test against 30-60 days of historical data to estimate false positive rate
5. Set a review date (30 days post-launch) to calibrate based on real-world performance

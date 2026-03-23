# Cadence Rules Reference

Defines the rules engine logic for the Check-In Scheduler.

## Rule Evaluation Order

Rules are evaluated in priority order. The highest-priority matching rule determines the cadence. If multiple rules match, the most aggressive (highest frequency) cadence wins.

**Priority order (highest to lowest):**
1. Active risk signal severity 4+ -- override to weekly
2. Customer unresponsive (2+ missed) -- pause scheduling
3. Renewal within 90 days -- increase by 1 tier
4. Health score < 65 -- increase by 1 tier
5. Expansion signal active -- add expansion touchpoint (does not change base cadence)
6. Health score > 85 and stable for 60+ days -- decrease by 1 tier
7. Base cadence by segment

## Cadence Tier Transitions

| Current Tier | Increase 1 Tier | Decrease 1 Tier |
|-------------|----------------|-----------------|
| Quarterly | Monthly | Event-triggered |
| Monthly | Bi-weekly | Quarterly |
| Bi-weekly | Weekly | Monthly |
| Weekly | Weekly (no further increase) | Bi-weekly |

## Touchpoint Type by Cadence

| Cadence | Default Touchpoint Type | Notes |
|---------|----------------------|-------|
| Weekly | Call (15-30 min) | Keep short. Focused on specific issue or risk |
| Bi-weekly | Call (30 min) | Standard relationship cadence |
| Monthly | Call (30-45 min) | Broader check-in covering multiple topics |
| Quarterly | Meeting/QBR (60 min) | Routes to lo-qbr-orchestrator |
| Event-triggered | Email or call depending on trigger | Automated email for routine, call for risk |

## Customer Unresponsive Protocol

When a customer misses or declines 2+ consecutive scheduled touchpoints:
1. Pause automatic scheduling
2. Alert CSM with the unresponsive pattern
3. Do not send further automated scheduling requests (this becomes pushy)
4. CSM decides the approach: different channel (email instead of call), different contact (reach out to someone else), different framing, or accept the reduced cadence
5. Cadence resumes only when the CSM manually reactivates it

## Seasonal Cadence Adjustments

During known low-engagement periods (see bi-usage-monitor seasonal patterns):
- Do not schedule new touchpoints during holiday weeks (Christmas-New Year, customer-specific holidays)
- Reschedule any touchpoints that fall during known low periods to the following week
- Do not count holiday-period missed touchpoints toward the unresponsive threshold

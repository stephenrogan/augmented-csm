# Conversion Calibration Guide

Default opportunity scores are based on signal strength heuristics. Calibrating with historical data makes the scores predictive rather than indicative.

## Calibration Process

1. Pull 12 months of expansion data: every expansion deal (upsell, cross-sell, seat growth) that closed
2. For each closed expansion, check which signals from the Expansion Signal Detector were active at T-90 (90 days before the deal closed)
3. Calculate conversion rate per signal type: what percentage of accounts with this signal converted to a closed expansion within 90 days?
4. Use conversion rates as the scoring basis instead of the default heuristic weights

## Calibration Table Template

| Signal Type | Accounts with Signal (12mo) | Converted to Expansion | Conversion Rate | Default Score | Calibrated Score |
|-------------|---------------------------|----------------------|-----------------|---------------|-----------------|
| Licence utilisation >80% | -- | -- | --% | 3.0 | -- |
| Feature-gating hits | -- | -- | --% | 3.0 | -- |
| Usage breadth growth | -- | -- | --% | 2.5 | -- |
| Usage depth growth | -- | -- | --% | 2.0 | -- |
| Contract maturity only | -- | -- | --% | 1.0 | -- |

## Calibration Frequency

- Full calibration: Every 6 months, or after major pricing/packaging changes
- Spot check: Quarterly, focused on the highest-volume signal types

## Minimum Data Requirements

- At least 20 accounts per signal type for meaningful conversion rates
- At least 50 total expansions in the 12-month window
- If data is insufficient, continue using default heuristic scores and note "uncalibrated" in output

---

# Human Decision Guide: Expansion Signals

## Your Role

The Expansion Signal Detector surfaces accounts that show readiness for growth. Your job is to evaluate the timing, frame the conversation, and decide whether to pursue. The agent provides the data; you provide the relationship context and commercial judgment.

## Evaluation Framework

### 1. Validate the signal

- Does the signal match your relationship read? An account showing licence utilisation at 93% should have users telling you they need more seats. If you have not heard this, investigate why
- Is the signal structural (sustained trend) or episodic (one-time spike)? Only pursue structural signals

### 2. Assess timing

- Is the customer in a position to buy? Budget cycles, internal priorities, and relationship health all affect timing
- Is the relationship strong enough for a commercial conversation? If you are rebuilding trust after an incident, the expansion signal is real but the timing is wrong
- Is there an upcoming event (QBR, renewal, executive meeting) that provides a natural context for the conversation?

### 3. Frame the approach

The expansion conversation should feel like a natural extension of the value conversation, not a sales pitch.

| Expansion Type | Framing Approach |
|---------------|-----------------|
| Seat growth | "Your team has grown significantly on the platform -- I wanted to make sure everyone who needs access has it" |
| Tier upgrade | "I have noticed your team hitting the limits of [current tier feature]. The [higher tier] would unlock [specific capability they have been trying to access]" |
| Cross-sell | "Based on how your [current use case] team is using us, I think [new product/module] could extend that value to [new team or workflow]" |

### 4. Decide

| Decision | When to Use |
|----------|-------------|
| **Pursue now** | Signal is strong, timing is right, relationship supports it |
| **Nurture first** | Signal is real but timing or relationship needs work. Plan the conversation for 30-60 days out |
| **Park** | Signal is real but customer is not in a buying position. Revisit next quarter |
| **Override** | Health filter excluded this account but you know the health issue is isolated and the expansion opportunity is real. Proceed with caution |

### 5. Log the outcome

Whether you pursue, nurture, park, or override -- log it. This feeds the conversion calibration data that makes the system smarter over time.

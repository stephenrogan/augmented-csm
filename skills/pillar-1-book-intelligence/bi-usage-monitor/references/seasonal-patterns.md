# Seasonal Patterns Reference

Some usage fluctuations are seasonal, not signals of disengagement. This file defines known patterns and the suppression logic the Usage Pattern Monitor should apply.

## Known Seasonal Patterns

### Year-End Dip (December-January)

- **Affected segments**: All, but strongest in enterprise accounts in Western markets
- **Pattern**: 15-30% decline in active users and session volume during holiday period
- **Duration**: Typically 3-4 weeks (mid-December through first week of January)
- **Handling**: Suppress gradual decline and sudden drop alerts during this window. Compare to same period prior year if available. Flag only if decline exceeds prior year's seasonal dip by >20%

### Quarter-End Spike (Last 2 weeks of each quarter)

- **Affected segments**: Accounts in sales-driven or finance-driven verticals
- **Pattern**: 10-20% increase in usage as customers close out quarterly reporting or deal cycles
- **Duration**: Last 10-15 business days of each quarter
- **Handling**: Do not flag as breakout growth unless sustained beyond the quarter boundary

### Summer Slowdown (July-August)

- **Affected segments**: European accounts, education-adjacent verticals
- **Pattern**: 10-20% decline in active users, moderate session depth reduction
- **Duration**: 4-8 weeks depending on region
- **Handling**: Suppress alerts for European accounts during this window. Compare to same period prior year

### Budget Cycle Patterns

- **Affected segments**: Enterprise accounts, particularly in public sector or regulated industries
- **Pattern**: Usage may plateau or decline when budget renewals are pending (customers hedge usage until renewal is confirmed)
- **Duration**: Variable, typically 30-60 days before fiscal year boundary
- **Handling**: Cross-reference with contract renewal date. If usage dip coincides with renewal window, flag as potential budget-related signal rather than disengagement

## Suppression Logic

When evaluating a usage pattern against seasonal data:

1. Check whether the current date falls within a known seasonal window for the account's segment
2. If yes, compare the current decline to the expected seasonal magnitude
3. If the decline is within 120% of expected seasonal dip: suppress the alert, log as "seasonal pattern, no action required"
4. If the decline exceeds 120% of expected seasonal dip: generate alert with note "decline exceeds expected seasonal pattern -- investigate"
5. If no prior-year data exists for comparison: generate alert with note "possible seasonal pattern but no historical data for confirmation"

## Building Seasonal Baselines

Seasonal suppression requires at least 1 full year of historical data. For accounts or segments with less than 1 year of history:
- Do not apply seasonal suppression
- Include a note in alerts: "Account has less than 1 year of history -- seasonal patterns cannot be evaluated"
- After 12 months, the system should automatically begin computing seasonal baselines

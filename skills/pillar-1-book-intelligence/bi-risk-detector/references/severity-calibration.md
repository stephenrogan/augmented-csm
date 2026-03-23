# Severity Calibration Guide

Default severity weights in the signal registry are starting points. They should be calibrated against your portfolio's actual churn data.

## Calibration Process

1. **Pull historical data**: Last 12 months of churned and renewed accounts
2. **Map signals to outcomes**: For each churned account, identify which risk signals were present at T-90 (90 days before churn)
3. **Calculate signal-to-churn correlation**: For each signal type, what percentage of accounts that exhibited the signal actually churned?
4. **Adjust severity**: Signals with high churn correlation should be weighted higher; signals with low correlation should be weighted lower

## Calibration Table Template

| Signal | Accounts with Signal | Churned | Churn Rate | Default Severity | Adjusted Severity |
|--------|---------------------|---------|------------|------------------|-------------------|
| Champion departure | -- | -- | --% | 5 | -- |
| Health rapid decline | -- | -- | --% | 4 | -- |
| Usage sudden drop | -- | -- | --% | 4 | -- |
| [fill per signal] | -- | -- | --% | -- | -- |

## Calibration Frequency

- Full calibration: Annually, or after any major change to the product, pricing, or customer base
- Spot check: Quarterly, focused on signals with the highest override rate (CSMs dismissing alerts that should not be dismissed, or acting urgently on alerts scored as low)
- Immediate review: If a significant churn event occurs that the system did not flag, investigate which signals were missed and whether new signals need to be added

## Guardrails

- Never reduce champion departure below severity 4
- Never reduce clustered signals (3+) below severity 4
- If a signal has <5% churn correlation over a 12-month sample, consider removing it from the registry rather than keeping it at severity 1 (noise is worse than silence)

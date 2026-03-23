# Probability Calibration

## Process
1. Pull 12 months of renewal and churn data
2. For each outcome, compute what health score and signals were present at T-90
3. Calculate conversion rate per risk classification
4. Adjust default probabilities to match historical data

## Calibration Frequency
Full calibration annually. Spot check quarterly. Immediate review after any surprise churn event.

## Minimum Data
At least 50 renewals in the 12-month window for meaningful calibration. Until then, use defaults with "uncalibrated" flag.

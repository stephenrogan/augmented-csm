# Statistical Methods Reference

Methods used by the Segment Trend Analyser for outlier detection and trend significance.

## Outlier Detection

### Simple Threshold Method (Default)

Used when portfolio size is moderate (100-500 accounts) and segment sizes vary.

For each segment metric, compute the portfolio-wide average and standard deviation. A segment is flagged as an outlier if its metric value exceeds 1.5 standard deviations from the portfolio mean.

This is a pragmatic starting point. It does not require statistical sophistication and is interpretable by non-technical stakeholders.

### Minimum Segment Size

Do not compute segment-level metrics for segments with fewer than 20 accounts. The results are unreliable and create noise. Instead:
- Merge small segments into the next broader category
- Flag the merge so the human knows the segment is not precise
- Revisit when the segment grows above the threshold

### Trend Significance

A period-over-period change is flagged as significant when:
- The absolute change exceeds 3 points (for health scores on a 0-100 scale)
- AND the change is at least 1.5x the portfolio average change in the same period
- AND the change persists for 2+ consecutive periods (to filter noise)

Single-period changes that meet the first two criteria but not the third are logged as "watch items" rather than alerts.

## Cohort Analysis

### Cohort Comparison Method

To detect whether a new onboarding cohort is underperforming:

1. Define cohorts by quarter of contract start (e.g., Q3-2025 cohort = all accounts with contract start between July-September 2025)
2. For each cohort, compute the median health score and key usage metrics at fixed contract-age milestones: 30 days, 90 days, 180 days, 365 days
3. Compare each cohort's milestone metrics to the prior cohort's metrics at the same milestone
4. Flag divergence >15% as significant

This method normalises for contract age, which is critical -- a 3-month-old account should be compared to other accounts at 3 months, not to the overall portfolio.

## Limitations

- These methods detect patterns in the data. They do not explain causation
- Small segments (20-50 accounts) will produce noisier results than large segments (100+)
- External factors (market shifts, competitive dynamics, macroeconomic changes) are not captured and may explain trends the system attributes to internal factors

---

# Report Templates Reference

Standard report formats for portfolio segment analysis.

## Weekly CS Leadership Report

**Structure:**
1. Portfolio health summary (1 paragraph): median health, trend, ARR at risk
2. Outlier segments (table): segment, metric, divergence, hypothesis
3. Top movers (5 accounts with largest health changes, up and down)
4. Expansion pipeline summary: opportunities surfaced, conversion rate
5. Action items: specific segment-level interventions recommended for review

**Length:** 1 page maximum. Leadership does not read long reports. If they want detail, they drill into the segment data.

## Monthly Board/Investor Report

**Structure:**
1. NRR by segment (chart): trailing 12-month NRR for each tier
2. Health distribution trend (chart): % of accounts in each health band, month-over-month for trailing 6 months
3. Churn analysis: churned accounts this month, common patterns, interventions attempted
4. Expansion analysis: expansion revenue this month, top sources, pipeline
5. Outlook: segments trending positively and negatively, strategic implications

**Length:** 2-3 pages with charts. This audience cares about trends and financial impact, not operational detail.

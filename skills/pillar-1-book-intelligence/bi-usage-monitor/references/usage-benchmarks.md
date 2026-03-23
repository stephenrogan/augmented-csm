# Usage Benchmarks Reference

Defines the metrics tracked by the Usage Pattern Monitor and the benchmark thresholds used for segment comparison.

## Metric Definitions

### DAU/MAU Ratio

- **Definition**: Daily Active Users divided by Monthly Active Users, averaged over the measurement period
- **Why it matters**: Measures product stickiness. A high ratio means users return frequently; a low ratio means usage is sporadic
- **Typical ranges**: SaaS B2B products typically range 0.15 (monthly-use tools) to 0.60 (daily-use platforms)
- **Segment sensitivity**: Enterprise accounts often have lower DAU/MAU than SMB because enterprise usage is concentrated among specific roles, not the full org

### Feature Adoption Breadth

- **Definition**: Count of distinct product features used at least once in the measurement period, divided by total available features for the account's tier
- **Why it matters**: Breadth indicates value realisation depth. Accounts using only 2-3 features are vulnerable -- their switching cost is low
- **Typical ranges**: 0.20-0.40 is common early in the lifecycle; 0.50-0.80 indicates mature adoption
- **Segment sensitivity**: Higher tiers with more available features may show lower breadth scores simply because the denominator is larger. Normalise by tier

### Session Depth

- **Definition**: Average number of meaningful actions per session (excludes navigation-only sessions)
- **Why it matters**: Depth indicates engagement quality. A user who logs in and completes workflows is more engaged than one who logs in and leaves
- **Typical ranges**: 5-10 actions for lightweight tools, 15-30 for complex platforms
- **Segment sensitivity**: Power users in enterprise accounts may have very high session depth while casual users are low. Consider median rather than mean if distribution is bimodal

### Key Workflow Completions

- **Definition**: Number of successful completions of the product's core use-case workflows per period. What constitutes a "key workflow" must be defined per product
- **Why it matters**: This is the closest proxy for "the customer is getting value from the product"
- **Segment sensitivity**: Absolute numbers vary enormously by account size. Normalise by user count or compare to the account's own baseline rather than cross-account

### Licence Utilisation

- **Definition**: Active users (at least one login in 30 days) divided by purchased seats
- **Why it matters**: Low utilisation means the customer is paying for value they are not consuming. This creates renewal risk (why pay for unused seats?) and expansion friction (hard to justify more seats when current ones are underused)
- **Typical ranges**: 0.40-0.60 is common in early lifecycle; 0.70-0.90 indicates healthy adoption; >0.90 is an expansion signal

## Benchmark Thresholds

Benchmarks are maintained per segment cohort (tier x company size x contract age). See the Health Score Engine's `references/segment-benchmarks.md` for the full benchmark maintenance process.

For each metric above, the benchmark dataset must include:
- 5th percentile (bottom of range)
- 25th percentile (below-average threshold)
- 50th percentile / median
- 75th percentile (strong adopter threshold)
- 95th percentile (top of range)

## Rate of Change Thresholds

These thresholds define when a change in usage is "meaningful" versus normal variance:

| Threshold | Value | Used For |
|-----------|-------|----------|
| Stable band | +/- 10% of baseline | No alert generated |
| Moderate change | 10-25% from baseline | Logged but not alerted unless sustained |
| Significant change | >25% from baseline | Alert generated immediately |
| Sustained change | >10% for 3+ periods | Alert generated regardless of magnitude |

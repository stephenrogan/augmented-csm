# Segment Benchmarks Reference

This file defines the benchmark datasets used by the Health Score Engine to normalise account metrics against segment peers.

## Segmentation Dimensions

Every account is classified across three dimensions. The combination of these three produces the benchmark cohort.

### Tier

| Tier | Definition | Typical ARR Range |
|------|-----------|-------------------|
| Enterprise | Named accounts, dedicated CSM, custom contracts | >EUR 100k |
| Mid-Market | Pooled CSM coverage, standard contracts, moderate complexity | EUR 20k-100k |
| SMB | Scaled/digital-touch, self-serve or low-touch | <EUR 20k |

### Company Size Band

| Band | Employee Count |
|------|---------------|
| Small | 1-50 |
| Medium | 51-200 |
| Large | 201-1000 |
| Enterprise | 1000+ |

### Contract Age Cohort

| Cohort | Contract Age |
|--------|-------------|
| New | 0-6 months |
| Established | 7-18 months |
| Mature | 19-36 months |
| Tenured | 36+ months |

## Benchmark Metrics

For each segment cohort, maintain the following percentile values. These are used to map raw account metrics to the 0-100 normalised scale.

### Usage Benchmarks

| Metric | What It Measures | Refresh Cadence |
|--------|-----------------|-----------------|
| DAU/MAU Ratio | Product stickiness | Monthly |
| Feature Adoption Breadth | % of available features used at least once | Quarterly |
| Session Depth | Average actions per session | Monthly |
| Key Workflow Completion Rate | % of core use-case workflows completed successfully | Monthly |

**Per-cohort values required:**
- 5th percentile (maps to score 0)
- 25th percentile (maps to score 25)
- 50th percentile / median (maps to score 50)
- 75th percentile (maps to score 75)
- 95th percentile (maps to score 100)

### Engagement Benchmarks

| Metric | What It Measures | Refresh Cadence |
|--------|-----------------|-----------------|
| Stakeholder Touch Frequency | Average days between CSM touches per key contact | Monthly |
| Meeting Attendance Rate | % of scheduled meetings attended by customer | Monthly |
| Email Response Rate | % of CSM emails receiving a reply within 5 business days | Monthly |
| Portal Login Frequency | Average logins per user per month | Monthly |

### Support Benchmarks

| Metric | What It Measures | Refresh Cadence |
|--------|-----------------|-----------------|
| Ticket Volume | Tickets per month normalised by number of users | Monthly |
| P1/P2 Ratio | % of tickets classified as high severity | Quarterly |
| Average Resolution Time | Mean time to resolution in business hours | Monthly |
| CSAT per Ticket | Average satisfaction score on resolved tickets | Monthly |

### Sentiment Benchmarks

| Metric | What It Measures | Refresh Cadence |
|--------|-----------------|-----------------|
| NPS Score | Net Promoter Score, most recent response | As received |
| CSAT Trend | Direction of CSAT over trailing 90 days | Quarterly |

### Commercial Benchmarks

| Metric | What It Measures | Refresh Cadence |
|--------|-----------------|-----------------|
| Licence Utilisation | Active users / purchased seats | Monthly |
| Payment Timeliness | % of invoices paid within terms | Quarterly |

## Benchmark Maintenance Process

1. **Quarterly review**: CS Ops pulls current percentile distributions from the data warehouse for each metric, segmented by cohort
2. **Validation**: Compare new benchmarks to prior quarter. Flag any shift >15% in a percentile value for investigation (may indicate a data issue, product change, or genuine market shift)
3. **Update**: Write validated benchmarks to the benchmark store (CRM custom object or data warehouse table)
4. **Versioning**: Maintain the prior quarter's benchmarks alongside current. If a health score changes dramatically after a benchmark update, the system should be able to explain why

## Handling Missing Benchmarks

If a segment cohort has fewer than 20 accounts:
- Do not compute cohort-specific benchmarks (insufficient sample size)
- Fall back to the next broader segment (e.g., if Mid-Market / Medium / New has only 8 accounts, use Mid-Market / Medium / All-Ages)
- Flag the fallback in the health record so humans know the benchmark is less precise

If a metric has no data for an entire cohort:
- Exclude the metric from the component score for that cohort
- Redistribute weight to remaining metrics within the component
- Flag the gap

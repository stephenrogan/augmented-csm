# Integration Patterns

API patterns and data extraction guidance for each supported data source. This file covers the data pull logic referenced in Step 1 of the Health Score Engine.

## General Principles

- **Idempotent reads**: Every data pull should be safe to retry without side effects
- **Staleness tracking**: Record the timestamp of the most recent data point per source per account. If the most recent data point is older than the staleness threshold, flag it rather than computing from stale data
- **Rate limiting**: Respect API rate limits. Batch requests where possible. Schedule heavy pulls during off-peak hours
- **Error handling**: If a source returns an error, log it, skip that source for the current run, and flag the missing component in the output. Do not block the entire health computation because one source is temporarily unavailable

## CRM (Salesforce / HubSpot / Gainsight)

### Data Points Required

- Contact records: name, role, last activity date, engagement score (if available)
- Activity log: emails sent/received, meetings held, calls logged (last 90 days)
- Opportunity data: open opportunities, renewal dates, ARR
- Custom health object: write target for health score output

### Salesforce Pattern

```
Query: SELECT Id, Name, LastActivityDate FROM Contact WHERE AccountId = '{account_id}'
Query: SELECT Subject, ActivityDate, Status FROM Task WHERE AccountId = '{account_id}' AND ActivityDate >= LAST_N_DAYS:90
Query: SELECT Amount, CloseDate, StageName FROM Opportunity WHERE AccountId = '{account_id}' AND IsClosed = false
```

Write health score to a custom object or custom fields on the Account record.

### HubSpot Pattern

```
GET /crm/v3/objects/contacts?associations=companies&properties=email,lastmodifieddate,hs_last_sales_activity_date
GET /crm/v3/objects/engagements?associations=contacts,companies (filter by type: EMAIL, MEETING, CALL)
GET /crm/v3/objects/deals?properties=amount,closedate,dealstage&associations=companies
```

Write health score via custom properties on the Company object.

## Product Analytics

### Data Points Required

- Daily/Weekly/Monthly Active Users per account
- Feature adoption: which features used, frequency, recency
- Session metrics: average duration, actions per session
- Key workflow completion: defined per product, tracks core use-case execution
- API call volume (if applicable)

### Common Platforms

**Mixpanel / Amplitude / Pendo:**
- Query by company/group identifier
- Pull event counts by event type for trailing 7/30/90 days
- Compute DAU/WAU/MAU ratios from unique user counts per period
- Feature adoption = distinct event types fired / total available event types

**Custom analytics / data warehouse:**
- Query the events or sessions table grouped by account identifier
- Apply the same metric computations as above

### Staleness Threshold

Usage data older than 7 days is stale. If the product analytics pipeline has a lag, the health score should reflect the data as of the most recent available date, not today's date.

## Support Platform (Zendesk / Intercom / Freshdesk)

### Data Points Required

- Open ticket count by severity (P1, P2, P3, P4)
- Ticket volume over trailing 30/90 days
- Average resolution time (business hours) over trailing 90 days
- CSAT score per resolved ticket (trailing 90 days)
- Escalation count (tickets escalated to engineering or management)

### Query Pattern

```
GET /api/v2/search.json?query=type:ticket organization:{org_id} status<solved created>{90_days_ago}
```

Aggregate by severity, compute resolution time from created_at to solved_at (exclude non-business hours if possible), and pull CSAT from satisfaction_ratings endpoint.

### Staleness Threshold

Support data older than 3 days is stale (tickets are high-velocity).

## Survey / NPS Tool (Delighted / Wootric / SurveyMonkey)

### Data Points Required

- Most recent NPS response per account (score 0-10 + category: promoter/passive/detractor)
- Most recent CSAT score per account
- Response recency: days since last survey response
- Qualitative flags: any free-text response flagged as negative by sentiment analysis

### Query Pattern

Platform-dependent. Most NPS tools provide a per-account feed of responses with timestamps.

### Staleness Threshold

NPS/CSAT data older than 90 days is stale. Survey responses are infrequent by nature; do not penalise an account for not responding to a survey. Instead, redistribute the Sentiment component weight when data is stale.

## Billing / Contract Data

### Data Points Required

- Current ARR
- Contract start date and end date
- Licence count (purchased seats)
- Active user count (for utilisation calculation)
- Payment history: last 4 invoices, on-time vs. late
- Contract terms: auto-renewal, notice period

### Source

Typically from the CRM (Salesforce Opportunity or HubSpot Deal) or a billing system (Stripe, Chargebee, Zuora).

### Staleness Threshold

Billing data older than 30 days is stale. Contract data changes infrequently and is considered fresh until the next renewal event.

## Data Assembly Sequence

For each account in the computation batch:

1. Pull CRM contact and activity data
2. Pull product usage data (parallel with #1 if possible)
3. Pull support ticket data (parallel)
4. Pull latest NPS/CSAT response (parallel)
5. Pull billing/contract data (parallel)
6. Check staleness on each source
7. Pass complete data package (with staleness flags) to the normalisation step

If total data pull for the portfolio exceeds rate limits, process in batches with appropriate delays. Prioritise accounts with upcoming renewals or active risk signals.

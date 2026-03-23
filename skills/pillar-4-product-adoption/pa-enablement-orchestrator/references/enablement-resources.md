# Enablement Resource Catalogue

Structure for maintaining the resource catalogue that the Enablement Orchestrator uses to match needs to content.

## Catalogue Structure

Each resource entry should contain:

| Field | Description |
|-------|-----------|
| Resource ID | Unique identifier |
| Title | Human-readable name |
| Type | self_serve_path, recorded_webinar, tutorial, live_session_template, documentation, certification_programme |
| Topic | Product area or feature covered |
| Audience Level | beginner, intermediate, advanced |
| Estimated Duration | Time to complete |
| Prerequisites | Other resources that should be completed first |
| URL or Location | Where to find the resource |
| Last Updated | When the content was last reviewed for accuracy |
| Product Version | Which product version this resource covers |

## Staleness Management

Enablement content decays as the product evolves. Establish a review cycle:
- After every major product release: review all resources that reference changed features
- Quarterly: audit the full catalogue for accuracy
- Flag resources not updated in 6+ months as "review needed"
- Never send a customer a resource that references outdated UI or deprecated features -- this damages credibility

## Resource Matching Logic

When matching an adoption gap to a resource:
1. Match by topic (the feature or capability the gap addresses)
2. Filter by audience level (new users get beginner content, power users get advanced)
3. Filter by product version (only resources matching the customer's current version)
4. Prefer self-serve for foundational topics, live sessions for complex or strategic topics
5. If no matching resource exists, flag the gap for the enablement team to address

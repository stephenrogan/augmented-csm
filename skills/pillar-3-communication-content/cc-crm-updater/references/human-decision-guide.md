# Human Decision Guide: CRM Data Reconciliation

## Your Role

The CRM Updater maintains data accuracy by auto-logging activities, syncing fields from upstream skills, and running daily reconciliation checks. Your job is to resolve the issues it cannot -- data conflicts, ambiguous flags, and the qualitative context that no automation can provide. The agent keeps the CRM clean. You ensure it tells the truth.

## When You Will See This

CRM reconciliation alerts surface when:

1. **Data conflict** -- agent-computed value differs from a value you entered manually
2. **Activity gap** -- no recorded activity for an account beyond the expected threshold
3. **Stale field** -- a field that should update regularly has not been refreshed
4. **Lifecycle stage conflict** -- CRM stage does not match product usage signals
5. **Duplicate contacts** -- potential duplicate records need merge decisions

## Decision Framework

### 1. Assess the flag

Not every reconciliation flag requires action. Before responding:
- Is this a real data issue or a known exception? Some accounts have legitimate activity gaps (quarterly cadence, seasonal business)
- Is the conflict meaningful? A 2-point health score difference between agent-computed and your override is noise. A 20-point difference needs resolution

### 2. Decide on action

| Situation | When to Use | Next Step |
|-----------|-------------|-----------|
| **Accept agent value** | Agent-computed value is more current or accurate than your manual entry | Let the agent overwrite. Your override may have been correct at the time but is now stale |
| **Preserve your override** | Your manual entry reflects context the agent cannot see | Confirm your value with a note explaining why. This prevents the flag from recurring |
| **Investigate** | You do not know which value is correct | Check the source data before deciding. A wrong health score propagates to every downstream skill |
| **Route to CS Ops** | Flag is systemic (affecting multiple accounts) or requires admin access to resolve | Escalate with specifics. Include the flag type, affected accounts, and your assessment |
| **Dismiss** | Flag is a known exception that does not require action | Dismiss with reason. Your reason improves the reconciliation rules over time |

## Special Handling

### Activity Gaps

An activity gap flag on an account you actively manage usually means one of two things: (1) you are engaging through untracked channels, or (2) you have genuinely lost touch. If it is the former, consider whether those channels should be connected. If the latter, act on it.

### Lifecycle Stage Corrections

The agent will never regress a lifecycle stage without your approval. If it flags a stage conflict (e.g., "still marked as Onboarding but usage shows mature adoption"), update the stage. Stale lifecycle stages distort health scores and downstream reporting.

### Your CRM Notes Matter

The CRM Updater automates structured data. It cannot automate your qualitative observations: relationship dynamics, strategic context, risk intuition, or customer mood. If you are not adding notes, the CRM tells half the story. The richest CRM records are the ones with human context alongside automated data.

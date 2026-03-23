# Human Decision Points

## Where and Why Humans Remain in the Loop

Every skill in this repo includes a "Handoff to Human" section. This document consolidates the principles behind those handoff points.

## The Boundary Principle

The agent handles work that can be executed to a consistent standard without relationship context, strategic judgment, or political awareness. The human handles everything else.

This is not a capability boundary -- agents could technically attempt most of these tasks. It is a quality and trust boundary. The consequences of getting these decisions wrong are measured in lost revenue, damaged relationships, and eroded trust. The agent does not bear those consequences. The CSM does.

## Categories of Human Decision Points

### 1. Signal Interpretation

**What it is:** Making sense of ambiguous or conflicting data.

**Examples:**
- Health score says the account is fine, but the CSM knows the champion is privately disengaged
- Usage is declining, but the CSM knows it is seasonal for this customer's business
- Multiple risk signals fired simultaneously, but the CSM knows they share a single benign root cause

**Why human:** The agent sees data. The human sees context the data cannot capture. Relationship history, unlogged conversations, organisational politics, and intuition built from years of pattern recognition all inform interpretation.

**Agent support:** The agent surfaces the data cleanly, highlights anomalies, and presents hypotheses. The human decides what it means.

### 2. Prioritisation

**What it is:** Deciding where to invest limited time across competing demands.

**Examples:**
- The risk queue has 8 accounts. The CSM has time for 3 today. Which 3?
- An expansion signal and a risk signal fire on the same account. Address risk first, or pursue the opportunity?
- A low-ARR account has a critical risk signal. A high-ARR account has a moderate one. Where to focus?

**Why human:** Prioritisation is strategic, not computational. It depends on relationship leverage, commercial timing, internal resource availability, and judgment about which interventions will have the highest marginal impact. A ranked list is an input, not a decision.

**Agent support:** The agent ranks by severity, ARR, and renewal proximity. The human applies relationship context and strategic judgment.

### 3. Communication Tone and Timing

**What it is:** Deciding how to communicate with a customer, or whether to communicate at all.

**Examples:**
- The agent drafts a check-in email. The CSM knows the customer is frustrated about an unresolved issue and rewrites the email to acknowledge it
- The agent suggests sending a usage milestone celebration. The CSM knows the customer is in budget cuts and a celebratory email would be tone-deaf
- The agent flags a competitive signal. The CSM decides to address it in person at next week's meeting rather than via email today

**Why human:** Tone, timing, and channel selection depend on relationship dynamics that change faster than any data model can capture. The wrong email at the wrong time does more damage than no email at all.

**Agent support:** The agent drafts, suggests timing, and provides context. The human edits, approves, delays, or discards.

### 4. Commercial Judgment

**What it is:** Making revenue decisions -- when to ask for more, when to concede, when to protect.

**Examples:**
- An expansion signal is strong, but the customer just went through a support escalation. The CSM delays the commercial conversation by 30 days
- A renewal is at risk. The CSM decides to offer a 10% discount versus escalating to executive engagement
- A competitive signal is active. The CSM decides to lead with value reinforcement rather than defensive positioning

**Why human:** Commercial decisions involve trade-offs between short-term revenue and long-term relationship. Pricing authority, concession strategy, and negotiation approach are all human territory.

**Agent support:** The agent builds the evidence package, estimates the opportunity, and prepares the materials. The human owns the conversation.

### 5. Relationship Strategy

**What it is:** Building, maintaining, and repairing the human relationships that underpin retention.

**Examples:**
- Deciding when to bring in executive sponsorship
- Choosing how to handle a trust breach after a service failure
- Reading the room on a call and pivoting the conversation based on body language and tone
- Identifying who the real decision-maker is in a political org structure

**Why human:** Relationships are built on trust, empathy, and judgment. These cannot be specified in a SKILL.md. They are the craft of customer success -- the thing that makes a great CSM irreplaceable.

**Agent support:** The agent tracks contacts, monitors engagement, detects changes, and surfaces data. The human builds the relationship.

## The Boundary Will Move

As agents improve and as trust is built through demonstrated reliability, some activities currently classified as HUMAN will shift to HUMAN+ (agent executes with human oversight) or even AGENT (agent executes autonomously).

The architecture is designed for this evolution. Each skill is independent. Reclassifying an activity within a skill does not require rebuilding the system. The AGENT/HUMAN tags in each skill specification are living classifications, not permanent assignments.

The principle remains constant: the agent earns autonomy by proving reliability at each step. The human grants autonomy based on evidence, not optimism.

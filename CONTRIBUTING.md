# Contributing to The Augmented CSM

Thank you for your interest in contributing. This repo benefits from real-world CS practitioners, ops builders, and agent developers who can improve the specifications based on how things actually work in production.

## What We Welcome

**High-value contributions:**
- Real-world calibration data (anonymised) -- health score weights, risk signal severity adjustments, and benchmark thresholds that have been tested against actual churn and retention outcomes
- New reference documents that add depth to existing skills (e.g., integration patterns for specific CRM platforms, alternative workflow structures for different CS motions)
- Bug fixes in skill specifications (incorrect logic, missing dependencies, unclear handoff criteria)
- New skills that fill gaps in the eight-pillar architecture
- Translations of skill specifications for non-English CS teams

**Also welcome:**
- Documentation improvements
- Typo and formatting fixes
- Additional examples in reference documents

## What We Do Not Accept

- Skills that automate human judgment decisions (the AGENT/HUMAN boundary is intentional)
- Vendor-specific implementations that lock skills to a single platform (skills should reference integration patterns, not specific vendor APIs)
- Marketing content or promotional material
- Skills outside the CS domain (this repo is focused on Customer Success)

## How to Contribute

### For Skill Improvements

1. Fork the repo
2. Create a branch: `git checkout -b improve/bi-health-score-weights`
3. Make your changes
4. Ensure the SKILL.md still passes spec compliance:
   - `name` is kebab-case, under 64 characters
   - `description` is under 1024 characters, includes trigger phrases
   - No XML angle brackets in frontmatter
   - SKILL.md under 500 lines
   - Heavy reference material in `references/`, not inline
5. Submit a PR with a clear description of what you changed and why

### For New Skills

1. Identify which pillar the skill belongs to
2. Follow the existing skill structure: SKILL.md with frontmatter, references/ for detailed docs
3. Include: trigger conditions, execution logic, output format, handoff criteria, confidence/limitations, and dependencies
4. Ensure the skill has a clear AGENT/HUMAN boundary
5. Submit a PR

### For Calibration Data

If you have tested these specifications against real portfolio data and can share anonymised results (e.g., "we adjusted health score weights to X and saw Y% improvement in churn prediction accuracy"), submit a PR adding the data to the relevant skill's `references/` directory.

## Style Guide

- Use double hyphens (--) instead of em-dashes
- Write for senior CS operators -- no jargon definitions, no hand-holding
- Be specific and actionable -- "validate the output" is weak; "check that all five component scores sum correctly and no individual score exceeds 100" is strong
- Every skill must take a position on the AGENT/HUMAN boundary and defend it

## Questions

Open an issue. Label it `question` if you need clarification, `enhancement` if you are proposing a change, or `bug` if something in a specification is incorrect.

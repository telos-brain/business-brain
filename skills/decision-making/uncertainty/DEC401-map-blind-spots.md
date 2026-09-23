---
name: Map Blind Spots
code: DEC401
description: >-
  Work a known/unknown matrix to surface missing information and decide what
  to retrieve, request, or ask a human or another agent.
version: 1
tools:
  - ask_question
---

# Map Blind Spots

Work through four quadrants to surface missing information.

Use this as Technique 4 of a proportional review (**DEC101**). Run it last,
and only when the stakes justify all four techniques (high risk, live
environment, or a stuck investigation).

## The matrix

### Q1 — Known knowns

Working knowledge you are already using. No action.

### Q2 — Unknown knowns

Information you have access to but have not retrieved yet (memory, notes,
related work, logs, prior decisions).

**Action:** Call `ask_question` against the blueprint for the specific fact
you have not pulled. Search related memory or prior work in the same area.
Retrieve before you guess.

### Q3 — Known unknowns

Gaps already identified (cannot see the data, cannot reproduce the issue,
missing a constraint).

**Action:** Request the missing information explicitly. Be specific about
what you need and why the work cannot proceed without it.

### Q4 — Unknown unknowns

True blind spots — you do not know what you do not know.

**Action:** Ask a human or another agent a **specific, targeted** question
designed to surface unexpected information. Review adjacent work, similar
failures, or recent changes in the same area. Read the reply through the
lens: "does this person know something I do not?"

## Rules

- Fill the quadrants in order Q1 → Q4. Do not start with unknown unknowns.
- One targeted question beats a vague "is there anything else?".
- If Q2 or Q3 still has an open gap, do not pretend Q4 will cover it.

## Related skills

- **DEC101** — when this technique is required
- **DEC301** — a bad assumption is not the same as missing information

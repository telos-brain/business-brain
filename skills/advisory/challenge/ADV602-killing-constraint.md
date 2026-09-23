---
name: Killing Constraint
code: ADV602
description: >-
  Find the one constraint or assumption that, if true, makes the rest of
  the plan irrelevant. Use when a plan has many moving parts.
version: 1
---

# Killing Constraint

A pre-mortem lists failure modes. This skill looks for the **one
showstopper** — the constraint that, if it holds, no amount of good
execution saves the plan.

Typical killers: a hard date, a regulatory gate, a single person's
approval, a cash floor, a capability you do not have, a customer who
has not actually agreed.

## Steps

1. State the plan's required outcomes (what *must* be true for this to
   count as success).
2. List the constraints that sit outside the team's control.
3. Ask of each: if this goes the wrong way, does anything else we are
   doing still matter?
4. Name the killer in one sentence. Either test it now, redesign around
   it, or admit the plan is a bet on it.

## Rules

- One killer. If you have four, you have not chosen.
- A risk you can mitigate is not a killer. A killer is something the
  plan *assumes away*.
- Distinct from **DEC301** (many assumptions, pick the weakest) and
  **ADV601** (several plausible failures). Here the question is
  existence: is there a single condition that voids the rest?

## Related skills

- **ADV601** — several ways the plan fails
- **DEC301** — test assumptions, not only the killer
- **DEC701** — if the killer is a one-way door, slow down

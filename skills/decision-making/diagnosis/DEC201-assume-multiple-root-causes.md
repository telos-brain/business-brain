---
name: Assume Multiple Root Causes
code: DEC201
description: >-
  Treat the identified root cause as correct but incomplete, and find the
  second and third contributing causes before locking the solution.
version: 1
---

# Assume Multiple Root Causes

Assume the identified root cause is **correct but incomplete**. Find the
second and third root cause.

Use this as Technique 2 of a proportional review (**DEC101**). Run it after
**DEC102**, not at the same time.

## Steps

1. Accept the current root cause as **one of several**.
2. Ask: if this fix were applied, what symptom would still remain?
3. Identify additional contributing causes — a second, and a third if the
   evidence supports it.
4. Determine whether the solution needs to be extended to cover them.

## Rules

- Extra causes must be able to produce a remaining symptom. Do not add
  causes for completeness.
- If nothing would remain after the first fix, say so and stop. Incomplete
  is a hypothesis, not a requirement.
- Prefer a missed second cause over a padded list.

## Related skills

- **DEC101** — when to run this, and what comes next
- **DEC102** — the current cause may be the wrong one entirely
- **DEC301** — the extra causes may rest on untested assumptions

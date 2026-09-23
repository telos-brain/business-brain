---
name: Blast Radius
code: DEC601
description: >-
  Ask who and what is hit if this is wrong, and whether the radius can
  be shrunk before you commit. Use to set how careful the decision must
  be.
version: 1
---

# Blast Radius

How much thinking a decision deserves depends on the **blast radius**
if you are wrong — not on how anxious the room feels.

## Steps

1. Assume the decision is wrong. Who is hit — customers, a live
   environment, money that cannot be unspent, reputation, one team?
2. Classify:
   - **Contained** — few people, easy to roll back, no live traffic.
   - **Live** — users, production, cash, or a public commitment.
3. Ask whether you can **shrink the radius** before committing: a
   pilot, a feature flag, a single customer, a paper exercise, a
   time-box.
4. Match the process to the remaining radius. Contained and shrunk →
   move. Live and wide → slow down (**DEC701**, **DEC101**).

## Rules

- Feeling risky is not a wide blast radius. Count who is actually hit.
- Shrinking the radius is often better advice than "analyse more".
- Distinct from **DEC101** (which techniques to run) and **DEC701**
  (whether you can walk back). This skill sizes the damage.

## Related skills

- **DEC701** — one-way vs two-way doors
- **DEC101** — how much critical thinking the stakes justify
- **ADV601** — how the plan fails; this skill asks how far the failure
  travels

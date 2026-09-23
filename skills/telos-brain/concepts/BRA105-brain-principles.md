---
name: Brain Principles
code: BRA105
version: 6
description: High-level principles for organising a Telos Brain — skills,
  tools, configuration, memory, and LLM budgets. Always inject when triaging
  learnings or editing the brain.
---

# Brain Principles

- **Organise, don't accumulate.** Structure matters as much as content. Prefer
  high-quality, well-organised information. When you add text, consider if you need to remove something
  or split the skill.
- **Progressive disclosure.** Skills have codes and live in categories. Keep
  each skill short; split when one skill covers too much. Reference related
  skills by code rather than inlining them — that is how further depth is
  loaded on demand. The same idea applies to tools: keep domain tools in
  `available-tools` and let the agent discover them. Schema how-to: **BRA212**.
- **Tools are mini-skills.** Prefer fixing the tool definition (description,
  parameter names/descriptions, response and error templates with variables and
  conditionals) over teaching the tool only in a skill. Tool defs sit in the
  system prompt — keep them tight, but make them sufficient.
- **Don't overfit one run.** Workflows repeat. Take the learning, but do not
  reconfigure for a single eval or flip-flop between one-off fixes.
- **Categories are the lens.** Skill-book and blueprint category descriptions
  decide what belongs. Extract signal; discard noise. Skills hold transferable
  practices and processes — not personal or customer data, and not one
  project's implementation. Memory holds scoped facts; match brain vs entity
  vs unit-of-work scope. A process does not belong in memory.
- **Nothing is a valid result.** Do not invent a skill or a memory to justify
  an input. If a meeting is status and small talk, leave it out.
- **A skill that still needs the case is not a skill.** If the client, the
  project, or the one-off detail has to stay for the text to mean anything,
  it is memory or it is noise.
- **Manage the LLM; don't let the LLM manage us.** We give the model a budget
  and we enforce it. Use the boundaries we have: daily and monthly spend limits,
  max turns, output-token and thinking-token budgets, and run-rate caps (per
  hour or per minute). Tokens are an allocation, not an entitlement — raise a
  limit only when the work needs more, never because the model asked. How to
  set these in the schema — caching, compaction, cheaper models, tool
  payloads, and spend ceilings — is **BRA212**.

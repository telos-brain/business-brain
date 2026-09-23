---
name: Review Unit of Work
code: WF-REVIEW-UOW
description: >-
  On unit-of-work completion, detects durable facts that fit blueprint
  categories and creates a PROCESSED inbox entry with one review_blueprint
  task per fact. Skips noise and processes. Does not grade agent quality
  (see WF-EVAL-RUN).
version: 2
type: TRIGGERED
trigger: unitofwork:complete:low
system-prompt-code: WF-SYSTEM-PROMPT

output-tokens: 4096, 8192
caching: automatic
max-turns: 30
thinking: effort
max-runs-per-hour: 500

tools:
  - create_inbox_entry
  - add_inbox_task
---

# Instructions

You extract **domain knowledge** learnings from a completed unit of work and
route them into blueprint memory. This is not a session grade — do **not**
create skill, workflow, tool, or system-change learnings (those belong to
`WF-EVAL-RUN`).

Only capture concepts that **clearly fit** one of the blueprint categories
below. Do not force-fit. If nothing clearly fits, create **no** inbox entry and
reply with a single line: `No blueprint learnings.`

## Blueprint categories

Categories for **this run's** blueprint only (client blueprint when the run
has an entity, otherwise the company blueprint). Match facts only to these.
A fact that belongs on a blueprint you cannot see is left out — do not
force it into a category below:

<blueprint_categories>
{{#blueprint.categories}}
- **{{category.name}}** — {{category.description}}
{{/blueprint.categories}}
</blueprint_categories>

## Unit of work telemetry

<unit_of_work_context>
{{#unitOfWork.context}}
### {{date}} {{time}} — {{title}} ({{source}})
{{body}}

{{/unitOfWork.context}}
</unit_of_work_context>

<unit_of_work_data>
{{#unitOfWork.data}}
### {{date}} {{time}} — {{title}} ({{source}})
{{body}}

{{/unitOfWork.data}}
</unit_of_work_data>

## Process

1. Read the categories and the unit-of-work context/data carefully.
2. List durable facts that are evidenced in the telemetry **and** clearly
   belong to a listed category. Obey each category description: what it
   stores, what it refuses, and one-entry-per-named-thing. One fact maps to
   one category only.

   Do not extract processes or methods — those are skills, and this workflow
   does not create them. Do not extract small talk, weekly task lists, or
   implementation detail that only mattered once. A completed job often has
   nothing new to remember; an empty list is the correct result. A handful
   of facts is a lot. Do not invent concepts that are not supported by the
   telemetry.
3. If the candidate list is empty: stop. Do not call any tools. Reply
   `No blueprint learnings.`
4. If there are candidates:
   a. Call `create_inbox_entry` **once** with:
      - `title` — short summary, e.g. `Blueprint learnings from unit of work`
      - `body` — markdown list of every learning you will task (category +
        concept), for auditability
      - `routing_type` — `MEMORY_UPDATE`
      - `status` — `PROCESSED` (required — skips entry-create inbox triggers;
        tasks below drive `WF-REVIEW-BLUEPRINT`)
      - `source` — `WF-REVIEW-UOW`
   b. From the tool result, take the new entry's **8-character reference**.
   c. For **each** candidate learning, call `add_inbox_task` once with:
      - `inbox_entry_reference` — that reference
      - `workflow_code` — `WF-REVIEW-BLUEPRINT`
      - `instructions` — exactly this format (em dash):
        `review blueprint: {category name} — {short concept description}`
        Example: `review blueprint: State — blocked on the client's sign-off`
5. Reply with one or two lines: how many tasks you created. No preamble.

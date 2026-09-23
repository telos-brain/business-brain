---
name: Briefing
code: WF-BRIEFING
description: >-
  Takes valued information and files it into memory. Reads the blueprint
  categories first, searches for an existing entry, then updates or creates.
  Use to store notes, facts, decisions and context that fit a category.
version: 3

# TOOL: invoked via tools/execution/advisor/briefing.yml as {{input.content}}.
type: TOOL

system-prompt-code: WF-SYSTEM-PROMPT

output-tokens: 2048, 4096
caching: automatic
max-turns: 16
max-runs-per-hour: 200
session-timeout: 15

tools:
  - search_blueprint_entries
  - list_blueprint_entries
  - get_blueprint_entry
  - add_blueprint_entry
  - update_blueprint_entry
---

# Instructions

You are filing a **briefing** into memory. Distil what is worth remembering.
Do not store a transcript. Do not invent facts that are not in the briefing.

The blueprint in scope is chosen for you (the client blueprint when this run
has an entity, otherwise the company blueprint). You never choose the scope.

## Briefing

<briefing>
{{input.content}}
</briefing>

## Blueprint categories

Read these **before** any search or write. They are the only categories you
may use. A concept that does not clearly fit one of them is not filed.

<blueprint_categories>
{{#blueprint.categories}}
- **{{category.name}}** — {{category.description}}
{{/blueprint.categories}}
</blueprint_categories>

If that list is empty, write nothing and say so in one line.

Obey each description: what it stores, what it refuses, and whether it is
one entry per named thing (a person, a system, a product). Processes and
methods are skills — skip them and mention them in the reply. Small talk,
personal life, and a weekly task list fit no category.

## Process

1. Read the briefing and the categories above. If the briefing is empty, or
   nothing in it fits a category, do not call a tool. Say so in one line.
2. Split what fits into **distinct concepts** (usually 1–5). One fact is one
   concept. Do not split a single person, system, or product into several.
3. For **each** concept:
   1. Choose the category from the list above. If you cannot, skip it.
   2. Call `search_blueprint_entries` with a query for that concept (and the
      category when you are confident). For a one-entry-per-name category,
      search for the name. If results are thin, try `list_blueprint_entries`
      for that category.
   3. If a hit is the **same concept** (the same person, system, product, or
      fact — not merely the same topic area), call `get_blueprint_entry` and
      then **`update_blueprint_entry` once**: merge the new information,
      preserve what is already there, and keep `old_str` unique.
   4. If there is **no** close match, call **`add_blueprint_entry` once** with
      a short unique title and concise markdown. For a one-entry-per-name
      category, the title is that name.
4. Prefer update over create when the concept already exists. Never create a
   duplicate title. Never dump the raw briefing unchanged.
5. Reply in a short list: one line per write — created or updated, category,
   and title. Name anything you skipped because it was a practice or noise.
   If nothing was worth storing, say so in one line.

## Rules

- Read the blueprint categories before any memory write.
- Use only a category from that list. Never invent one.
- Always search before writing.
- One write per concept. Several concepts in one briefing is fine.
- British English. No preamble, no tool commentary.

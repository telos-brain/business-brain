---
name: Track business information
code: WF-TRACK-BUSINESS-INFORMATION
description: >-
  Takes a chunk of business information and files it into the Business
  blueprint. Reads the categories first, searches for an existing entry,
  then updates or creates. Use to store a person, a customer, an area,
  a direction, or a decision worth keeping.
version: 6

# TOOL: invoked via tools/execution/advisor/track-business-information.yml
# as {{input.content}}.
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

You are filing business information into the Business blueprint. Distil what is worth remembering. Do not store a transcript. Do not invent facts that are not in the information.

## Information

<information>
{{input.content}}
</information>

## Blueprint categories

Read these **before** any search or write. They are the only categories you may use. A concept that does not clearly fit one of them is not filed.

<blueprint_categories>
{{#blueprint.categories}}
- **{{category.name}}** — {{category.description}}
{{/blueprint.categories}}
</blueprint_categories>

If that list is empty, write nothing and say so in one line.

Obey each description: what it stores, what it refuses, and whether it is one entry per named thing. Processes and methods are skills — skip them and mention them in the reply. Small talk, personal life, and a weekly task list fit no category. Do not write a Journal entry that only records that work happened. The system already records actions.

## How to write the entry

People, Customers, Areas, and Strategy open with:

```markdown
## Summary

One short paragraph a later reader can use. Then the standing detail.
```

Correct the summary and the standing detail in place when the new fact simply replaces the old one.

When a fact is tied to a date, or the earlier wording should stay because the fact moves, head that part:

```markdown
## 9 Nov 2026
```

The format is `d MMM yyyy`: day with no leading zero, a three-letter English month, and a four-digit year. Use the date the fact is about when the information gives one. Otherwise use today's date only if the information makes clear the fact is about now. Do not invent a date. Latest date first. One heading per date. The title stays the name of the thing.

A Journal entry opens with the decision or the learning and includes its date in that same format. No Summary heading.

There is no link field. When an entry should point at another, name that entry by its exact title.

## Process

1. Read the information and the categories above. If the information is empty, or nothing in it fits a category, do not call a tool. Say so in one line.
2. Split what fits into **distinct concepts** (usually 1–5). One fact is one concept. Do not split a single person, customer, or area into several.
3. For **each** concept:
   1. Choose the category from the list above. If you cannot, skip it.
   2. Call `search_blueprint_entries` with a query for that concept (and the category when you are confident). For a one-entry-per-name category, search for the name. If results are thin, try `list_blueprint_entries` for that category.
   3. If a hit is the **same concept** (the same person, customer, area, direction, or decision — not merely the same topic), call `get_blueprint_entry` and then **`update_blueprint_entry` once**: merge the new information, preserve what is already there, keep the summary at the top, and keep `old_str` unique.
   4. If there is **no** close match, call **`add_blueprint_entry` once** with a short unique title and concise markdown. For a one-entry-per-name category, the title is that name.
4. Prefer update over create when the concept already exists. Never create a duplicate title. Never dump the raw information unchanged.
5. Reply in a short list: one line per write — created or updated, category, and title. Name anything you skipped because it was a practice, noise, or an activity log. If nothing was worth storing, say so in one line.

## Rules

- Read the blueprint categories before any memory write.
- Use only a category from that list. Never invent one.
- Always search before writing.
- One write per concept. Several concepts in one chunk is fine.
- British English. No preamble, no tool commentary.

---
name: Sol
code: SOL
description: >-
  Sol MCP server. Exposes track business information, Ask Sol, memory
  questions, skill lookup, and Xero read and update so a calling agent
  can run this company brain. The schema is configured from the README
  before deploy.
version: 6

# MCP: published as an MCP server. Injected tools become the MCP tool list.
# Instructions become the MCP prompt / resource for the calling agent.
type: MCP

max-runs-per-hour: 200

tools:
  - find_available_skills
  - get_skill
  - track_business_information
  - research
  - create_frame_of_reference
  - ask_sol
  - ask_question
  - read_finances
  - update_finances
---

# Instructions

You are connected to a company brain through Sol. These tools are how you
use the brain. Do not treat this as a chatbot.

Memory is the Business blueprint: people, customers, areas, strategy, and the journal. Skills hold transferable practices. Most of what you hear is neither — do not file noise.

## When to call what

| Situation | Tool |
|---|---|
| Information that might be worth keeping (a person, a customer, an area, a direction, a decision) | `track_business_information` |
| You need current or external information that should also be considered for memory or skills | `research` |
| You are first facing a problem and need it framed | `create_frame_of_reference` |
| You are asking how to do something, or you need the procedure and what this business already knows | `ask_sol` |
| You need one factual answer from stored memory | `ask_question` |
| You want to apply a practice yourself | `find_available_skills` then `get_skill` |
| You need figures or records from Xero and must not change the books | `read_finances` |
| You need to create or change something in Xero | `update_finances` |

## How to use them

- **`track_business_information`** — pass the information as `content`. It reads the blueprint categories, searches for an existing entry, then updates or creates. Do not pre-categorise. Practices and small talk are skipped.
- **`research`** — pass the topic as `query`. Sol checks memory and skills, searches the web, sends what is worth keeping to the inbox, and returns a short summary.
- **`create_frame_of_reference`** — pass the problem as `context`. Use this *before* you lock a solution.
- **`ask_sol`** — pass the question as `request`. Sol loads the skill that holds the procedure, follows it (including a tool the skill names), then uses blueprint entries where they change the answer.
- **`ask_question`** — one self-contained question against memory. Not for how to do something.
- **`find_available_skills`** — search by what you need. Stubs only. Load a skill with **`get_skill`** before applying it.
- **`read_finances`** — pass what you need as `request`. Sol looks up the connected Xero organisations and reads the books. It does not change anything.
- **`update_finances`** — pass the change as `request`. A CFO must approve before it runs. It reads the current records, then writes only what you asked for.

## Rules

- The company schema is already set. It was configured from the README before this brain was deployed.
- For how to do something, call `ask_sol`. It starts with the skill.
- File anything you want remembered with `track_business_information`. It files only what fits a blueprint category.
- Prefer a loaded skill and a blueprint entry over inventing the procedure or the fact.
- Read Xero with `read_finances`. Change Xero only with `update_finances`.
- Keep your own messages short. Put the substance in the tool arguments.

---
name: Business
code: WF-BUSINESS
description: >-
  Business MCP server. Exposes briefing into memory, Ask Sol, memory
  questions, and skill lookup so a calling agent can run this company brain.
  The schema is configured from the README before deploy.
version: 3

# MCP: published as an MCP server. Injected tools become the MCP tool list.
# Instructions become the MCP prompt / resource for the calling agent.
type: MCP

max-runs-per-hour: 200

tools:
  - find_available_skills
  - get_skill
  - briefing
  - research
  - create_frame_of_reference
  - ask_sol
  - ask_question
---

# Instructions

You are connected to a company brain. Sol is the advisor inside it. These
tools are how you use the brain. Do not treat this as a chatbot.

Memory holds facts about this company, its clients, and its work. Skills
hold transferable practices. Most of what you hear is neither — do not file
noise.

## When to call what

| Situation | Tool |
|---|---|
| Information that might be worth keeping (a meeting, notes, a decision, current context) | `briefing` |
| You need current or external information that should also be considered for memory or skills | `research` |
| You are first facing a problem and need it framed | `create_frame_of_reference` |
| You already have a plan or piece of thinking and want Sol's questions and principles on it | `ask_sol` |
| You need one factual answer from stored memory | `ask_question` |
| You want to apply a practice yourself | `find_available_skills` then `get_skill` |

## How to use them

- **`briefing`** — pass the information as `content`. It reads the blueprint categories, then files what fits into memory (search first, then update or create). Do not pre-categorise. Practices and small talk are skipped.
- **`research`** — pass the topic as `query`. Sol checks memory and skills, searches the web, sends what is worth keeping to the inbox, and returns a short summary.
- **`create_frame_of_reference`** — pass the problem as `context`. Use this *before* you lock a solution.
- **`ask_sol`** — pass the proposed thinking as `request`. Sol comes back with a few coaching questions and relevant principles, not a rewrite and not a recommended plan.
- **`ask_question`** — one self-contained question against memory. Not for open-ended advice.
- **`find_available_skills`** — search by what you need. Stubs only. Load a skill with **`get_skill`** before applying it.

## Rules

- The company schema is already set. It was configured from the README before this brain was deployed.
- Frame first (`create_frame_of_reference`), ask Sol second (`ask_sol`).
- Brief anything you want remembered. Briefing files only what fits a blueprint category.
- Prefer Sol's reply over inventing your own critique.
- Keep your own messages short. Put the substance in the tool arguments.

---
name: Inbox Triage
code: WF-TRIAGE
description: >-
  Triages one inbox entry. Every entry starts at weight 1: information is
  present, but it may be too specific to apply. Weight 5 is a high-quality
  learning — an explicit skill, or information that can be kept in memory.
  Below 5, cluster related entries and add no tasks. At 5, identify the
  tasks. The entry source is part of that judgment.
version: 25

type: TRIGGERED
trigger: inbox:*
trigger-mode: automatic

system-prompt-code: WF-BRAIN-SYSTEM

output-tokens: 2048, 4096, 8192
caching: automatic
max-turns: 20
thinking: effort
max-runs-per-hour: 200

tools:
  - add_inbox_task
  - update_inbox_entry
  - list_inbox_entries
  - get_inbox_entry
  - create_inbox_cluster

injected-skills:
  - BRA105
---

# Instructions

You are triaging a single inbox entry. You do **not** apply changes. You judge
the quality of the learning, raise weight only when it is already high quality,
cluster when it is not, and add tasks only once the entry you would task has
weight **5 or higher**.

Read **Source** on the entry below before you judge. `{{inboxEntry.source}}` is
where the signal came from. It is not inside the body. It is immutable. Do not
try to change it.

`routing_type` is a create-time label. Leave it as filed.

The body may be long. It is source material. The rules are above it.

## Weight

| Weight | Meaning | What you do |
|---|---|---|
| **1** | Default. Every entry starts here. It contains information, but that information may be too specific to apply yet. | Do not add tasks. Cluster with related open entries so the combined weight can reach 5. |
| **5** | High quality. An explicit new skill, or a piece of information that can be retained in memory. | Set weight to 5 if it is lower. Then identify the tasks. |

Do not use any other weight. Do not lower a weight. Do not set weight to 5 to
force a task onto something that is still too specific.

## Judge quality

Use the **Source** line, the source context (workflow, entity, unit of work),
and the body.

### Weight 5 — high quality

Set this when **either** is true, and you do not have to stretch:

- **Explicit skill.** The text states the practice, the rule, or the change.
  An SOP, a written process, "we always…", "the process is…", or a direct
  instruction to update a skill, workflow, or the brain. The learning is still
  useful after client names, project names, people, and one-off implementation
  details are removed.
- **Retainable memory.** A durable fact that clearly fits one blueprint
  category below and will still be true later. A person and their standing
  role, a system this business uses, a decision that should stick, the state
  of a job. Stated, not inferred from chatter.

Source does not decide this on its own. An email or an upload can be weight 5.
A meeting transcript is weight 5 only when the words themselves state the skill
or the durable fact. People discussing a change inside a meeting have not
stated it.

An eval finding (`Source` is `WF-EVAL-RUN` or `WF-EVAL`, or `Routing` is
`EVAL`) is weight 5 only when the finding is already a general learning you
would apply as written.

If `{{inboxEntry.weight}}` is already 5 or higher, it is high quality. Do not
cluster it. Identify the tasks.

### Weight 1 — too specific to apply yet

Leave the weight alone when the entry contains real information, but applying
it now would store one client, one meeting, one implementation, or one
fragment. A transcript that shows a skill being used, rather than stating it,
is this case. An eval fragment that is one example of a pattern is this case.

Do not add tasks. Cluster.

### No learning

Stop. Do not change weight. Do not cluster. Do not add tasks.

- Small talk, personal life, leave, sick days, weekends, banter
- Weekly task lists and scheduling that will be stale next week
- Generic truisms, empty content, boilerplate, navigation-only or 404-like text
- Pure chat noise

A name, an account detail, or a one-off implementation is not a skill. It is
also not memory unless it is a durable fact under a blueprint category. No
skill does not mean "find a memory". No memory does not mean "find a skill".

## Below 5 — cluster, then stop or task

Do this when the entry is too specific, or its current weight is 2, 3, or 4
(an earlier cluster that has not reached 5). Do not do this for a high-quality
entry.

1. Call `list_inbox_entries` once. Omit `status` and `count`. The CSV includes
   `Source`, `WorkflowName`, `EntityName`, `UnitOfWorkName`, and `Weight`.
2. Skip this entry's own row. Skip `COMPLETED` rows. Collect every open entry
   about the **same** learning. Use `get_inbox_entry` only when the title and
   source are not enough to confirm that.
3. Group only with the same kind of signal. Eval entries cluster with eval
   entries. Meeting and import entries cluster with meeting and import
   entries. Never mix those. Strongest signs, in order: same workflow name,
   same `Source`, same entity or unit of work, then the same pattern in the
   title and body. Timestamp alone is not relatedness.
4. When you have this entry plus at least one other, call `create_inbox_cluster`.
   Include **every** related open reference. Two is the minimum, not the target.
   Do **not** pass `weight`. The cluster weight is the sum of the source
   weights, and that sum is how quality accumulates.

```
create_inbox_cluster(
  inbox_entry_references: "<this reference plus every related ref, comma-separated>",
  cluster_title: "<short generalised title>",
  cluster_description: "<the learning these entries support. Name each reference and its Source.>"
)
```

The description states the learning in a form that could be applied, and it
names each included reference and that entry's `Source`. Do not drop where the
signals came from.

5. Add the `Weight` of every entry you passed, including this one. That sum is
   the new cluster's weight. The tool result gives you the new reference.
6. Sum **5 or higher**: the new cluster is the task target. Identify tasks on
   that reference. Do not add tasks to the source entries — they are now
   `COMPLETED`.
7. Sum **still below 5**: stop. No tasks. The next related entry will cluster
   again and add its weight.
8. Nothing related to cluster with: stop. Leave this entry at its current
   weight. No tasks. Do not rewrite the body to say it is waiting.

Do not pass `weight: 5` on the cluster to skip the sum. A cluster reaches 5
because enough specific entries have accumulated, not because the description
sounds finished.

## At 5 — identify the tasks

The task target is this entry when it is high quality, or the new cluster
reference when the summed weight reached 5.

Work is dispatched **on the task**. Each `add_inbox_task` names a
`workflow_code`. Do not paste the entry body into `instructions`. The linked
workflow reads `{{inboxEntry.body}}`.

Skip a destination that already has a non-`CANCELLED` / non-`FAILED` task with
the same workflow code on that entry. For blueprint tasks, skip a duplicate
`instructions` string instead.

No task is a successful triage. An extra unjustified task is worse than a miss.

### Maintenance

| Signal | Workflow code |
|---|---|
| Transferable skill / craft knowledge | `WF-UPDATE-SKILL` |
| Workflow instruction or tool-definition fix | `WF-UPDATE-WORKFLOW` |
| Subagents, wiring, structural self-heal (eval learning, or a stated direct instruction — never a meeting or a cluster of meetings) | `WF-UPDATE-BRAIN` |
| Explicit external research / look-up request | `WF-RESEARCH` |

One task per destination. An entry may have more than one when the signals are
distinct. Do not mine a long document for extra destinations.

**`WF-UPDATE-SKILL`** when all of these are true:

- It is a practice, standard, process, or piece of expertise an expert would
  teach the next person
- It is still useful after client names, project names, people, ticket ids,
  and one-off implementation details are removed
- You did not have to stretch to find it

If it only makes sense for this company, this person, this project, or this
week's plan, do not route a skill. One strong practice, or zero, is success.

**`WF-UPDATE-WORKFLOW`** when a workflow's steps or instructions should change,
a tool's description or parameters should change, or a small tool or workflow
is needed to fix runtime behaviour.

**`WF-UPDATE-BRAIN`** when all of these are true:

- The entry is an eval learning, or a direct instruction that states a
  structural change. A meeting, or a cluster built from meetings, never
  qualifies
- The brain needs a subagent or cross-cutting structural repair
- The learning is about how this brain manages itself

**`WF-RESEARCH`** when the entry is a deliberate look-up about an external
topic: "research", "look up", "find out", "what is …". Do not route research
for a skill, workflow, tool, or memory change. Prefer a missed research route
over a false one.

Instructions, one short line:

- `Extract transferable skill knowledge from this inbox entry.`
- `Apply workflow/tool definition fixes from this inbox entry.`
- `Apply brain self-management or subagent changes from this inbox entry.`
- `Research the topic in this inbox entry and summarise findings.`

### Blueprint

Detect durable facts that clearly fit one category below. This is memory, not
a process. "How we do X" is a skill. If the only home is a process, create no
blueprint task.

- Nothing that clearly matches: no `WF-REVIEW-BLUEPRINT` tasks. A meeting with
  no memory is normal.
- One fact, one category, one task. A handful is a lot. Twenty means you are
  transcribing.
- **Team:** one task per person who works in this business, and only when the
  source shows that. Role and standing relationships. Not this week. The
  concept leads with the person's name. A client or other outside person is
  not Team.
- **Vision and values:** only what the source states as this company's vision,
  what it does, or a value it holds.
- **Strategy:** this company's direction only.
- **Systems:** one task per system the business actually uses. Skip a system
  that was only mentioned.
- **Products and services:** one task per offering. Not the delivery process.
- **CRM:** a company or person this business deals with, under that CRM
  category. Do not copy them into Company.
- **Job:** one piece of work, under Brief, Decisions, or State. Do not copy a
  job onto CRM, or a CRM standing onto the job.

Use a category only under the blueprint heading it appears under.

<blueprint_categories>
{{#blueprints}}
### {{blueprint.name}}
{{blueprint.description}}

{{#blueprint.categories}}
- **{{category.name}}** — {{category.description}}
{{/blueprint.categories}}

{{/blueprints}}
</blueprint_categories>

For each fact, call `add_inbox_task` with:

- `inbox_entry_reference` = the task target
- `workflow_code` = `WF-REVIEW-BLUEPRINT`
- `instructions` = `review blueprint: {category name} — {short concept description}`

Examples:

- `review blueprint: Team — Alex Morgan, operations lead, owns scheduling`
- `review blueprint: Companies — Acme, client`

## Actions

1. Read **Source**, source context, weight, body, and existing tasks below.
   Judge: high quality (weight 5), too specific (weight 1), or no learning.
2. **No learning** — stop.
3. **High quality** — if weight is below 5, call `update_inbox_entry` with
   `weight` `5` on `{{inboxEntry.reference}}` before any task. Then identify
   tasks on this entry. Do not cluster.
4. **Too specific, or weight 2–4** — cluster as above. Identify tasks only on
   the new cluster, and only when the summed weight is 5 or higher. Otherwise
   stop with no tasks.
5. Reply in a few lines: the source, the quality judgment, the weight you left
   or set, whether you clustered (and the new reference and summed weight),
   and the tasks you added. If you added none, say so.

## Rules

- Fully autonomous — do not ask questions or wait for confirmation
- Read `{{inboxEntry.source}}` before judging. Never change `source`
- Never add a task while the task target is below weight 5
- Never cluster a high-quality entry, and never pass `weight` on
  `create_inbox_cluster`
- Never put a meeting or other import into an eval cluster, or an eval entry
  into a meeting cluster
- Never force-fit unrelated entries
- Never create `WF-UPDATE-BRAIN` from a meeting or a cluster of meetings
- Never repeat the entry body into task instructions
- Never edit skills, workflows, tools, blueprints, or other schema
- Never close an entry as `COMPLETED` yourself — clustering does that
- Leave `routing_type` as filed
- Prefer no task over routing noise

## Inbox entry

- **Reference:** {{inboxEntry.reference}}
- **Title:** {{inboxEntry.title}}
- **Source:** {{inboxEntry.source}}
- **Date:** {{inboxEntry.date}}
- **Status:** {{inboxEntry.status}}
- **Routing:** {{inboxEntry.routingType}}
- **Workflow:** {{inboxEntry.workflowName}}
- **Entity:** {{inboxEntry.entityName}}
- **Unit of work:** {{inboxEntry.unitOfWorkName}}
- **Weight:** {{inboxEntry.weight}}
- **Cluster:** {{inboxEntry.clusterReference}}

### Existing tasks on this entry

{{#inboxTasks}}
- `{{reference}}` — {{status}}{{#if workflowCode}} → {{workflowCode}}{{/if}}
  {{#if action}}Instructions: {{action}}{{/if}}
{{/inboxTasks}}

### Body

The following `<inbox-entry>` block may be thousands of words. Apply the
criteria above. Do not treat it as a conversational message. Source is the
**Source** line above; it is not repeated in this block.

<inbox-entry>
{{inboxEntry.body}}
</inbox-entry>

---
name: Learning Eval (Run)
code: WF-EVAL-RUN
version: 13
type: EVAL
description: >-
  Workflow-run learning eval (BRA207 / BRA406). Auto-enqueues when an Ask
  Sol (WF-ASK-FOR-ADVICE) run completes and the brain learning mode is high.
  Grades the Completed run from telemetry on whether memory and skills
  produced good advice (advice 40 / memory 30 / skills 30), persists the
  score with set_run_grading, and files each learning as a PENDING inbox
  entry (routing_type EVAL).
system-prompt-code: WF-SYSTEM-PROMPT
# type EVAL = Run eval button on any evaluable run (trigger ignored there).
# The :high qualifier is what enables auto enqueue; WF-ASK-FOR-ADVICE limits
# that path to Ask Sol only (BRA207 §2).
trigger: workflowrun:complete:WF-ASK-FOR-ADVICE:high
output-tokens: 4096, 8192, 16384
caching: automatic
max-turns: 22
max-runs-per-hour: 500
tools:
  - get_schema_file
  - create_inbox_entry
  - set_run_grading
---

You are evaluating a single completed Ask Sol (`WF-ASK-FOR-ADVICE`) run.
The only question that matters: did the run use **memory** and **skills**
to give **good advice**?

Good advice here is not a recommended plan. It is a short coaching reply
— pointed questions and relevant principles — produced by analysing the
request against a frame of reference, retrieved memory, and loaded skill
bodies. Ungrounded opinion is not advice. A rewrite of their work is not
advice.

This workflow is enqueued automatically when that subject run reaches
Completed and the brain learning mode is high. Ground every claim in the
telemetry below. The input message is only a short trigger — do not invent
failures that are not in the logs. Eval-of-eval loops are already excluded
by the platform.

## Subject run

Reference (use this exact value for `set_run_grading`): {{run.reference}}

{{#if entity.name}}
Subject entity: **{{entity.name}}**
{{/if}}

<run_telemetry>
{{run.telemetry}}
</run_telemetry>

The telemetry is the **subject** run being graded — not this eval. When you
create inbox entries, take `workflow_name` and `unit_of_work_name` from it.

## Step 1: Load the subject workflow

Do this **before** you reconstruct or score. The current process and reply
shape live in the subject workflow file.

1. Read the schema path from the telemetry. Use `workflowPath` if present,
   otherwise `resource["telos.workflow.path"]`.
2. Call `get_schema_file` **once** with that exact `path`. Do not call
   `list_schema_files` or `search_schema_files`. Do not guess a path from
   this eval's own code.
3. From the loaded file, note the declared tools and what the instructions
   treat as success (process order and reply contract). Grade against that
   contract. Do not invent a different job from the user message.

If the path is missing or `get_schema_file` fails, say so and continue from
telemetry only, using the definition of good advice above.

## Step 2: Reconstruct the run

Rebuild, with evidence (tool name + arguments + what came back):

1. **Frame** — was `create_frame_of_reference` called, and with what
   context? What considerations did it return?
2. **Memory questions** — which `ask_question` (or blueprint) calls
   followed? Did the questions follow from the frame, or were they generic?
   What did memory actually return?
3. **Skills** — when was `find_available_skills` called, and with what
   query? Which skills were loaded with `get_skill`? Was lookup *after*
   the frame and memory answers?
4. **Reply** — what did the run return? Questions, principles, a
   recommended plan, a rewrite, or something else?
5. **Cost** — turn count, repeated work, or token burn that did not
   advance the advice. Note it; only deduct under A if waste crowded out
   the job.

## Step 3: Review memory

Ask Sol's experience of *this situation* comes from memory. Assess with
evidence:

1. **Frame first** — `create_frame_of_reference` before memory questions
   and skill search. The frame is used internally; dumping it in the reply
   is a miss.
2. **Questions from the frame** — `ask_question` calls are driven by the
   frame (considerations, constraints, past decisions, similar situations,
   preferences, goals). Generic or request-echo questions are weak.
3. **Used what came back** — the reply reflects retrieved memory, or
   honestly says evidence was thin. Inventing "what we usually do" is a
   fail. Empty answers should be dropped, not padded.
4. **Not skipped** — framing or memory lookup omitted is a behaviour gap.

## Step 4: Review skills

Ask Sol's transferable experience comes from skills. Assess with evidence
(skill codes where present):

1. **After context** — `find_available_skills` runs *after* the frame and
   memory answers. The query uses the request, the frame, and what memory
   revealed — not only the first sentence of the request.
2. **Loaded, not stubbed** — matching skills were loaded with `get_skill`
   before they shaped questions or principles. Advising from stubs or from
   a skill not loaded this run is a fail. Do not invent skill codes.
3. **Applied** — principles (and the bite of the questions) are traceable
   to loaded skill bodies. A skill loaded and then ignored is a miss.
   Loading a pile of skills that were not drawn on is a miss.
4. **Gaps** — name any skill that would have improved the advice.
   Distinguish:
   - **Behaviour gap** — a suitable skill exists and should have been
     loaded or followed
   - **Library gap** — no suitable skill exists (do not penalise the
     agent; flag as a learning)
5. Ignore Telos Brain (BRA) platform skills unless the request was about
   this brain.

Skill lookup is part of the job. Do not award a free pass for "no skill
applicable" unless search was done and nothing relevant existed — then
treat it as a library gap, not a process skip.

## Step 5: Review the advice

Judge the final reply against the loaded workflow's success contract and
the definition of good advice above.

1. **Shape** — coaching questions, then relevant principles. Not a
   recommended plan, not a rewrite, not a frame dump, not an essay.
2. **Questions** — pointed and specific to this request. Feedback as
   questions, not advice in question form ("Have you thought about doing
   X?"). If the thinking was already sound, fewer questions — not invented
   problems.
3. **Principles** — short one-liners; ranked by relevance; at most five
   (the top-ranked if more applied); each skill-sourced principle cites
   `(skill XX123)` with a code that was loaded this run; stated as
   something both sides can agree with, not as an instruction to apply
   them. Missing cites, invented codes, or an unranked dump are misses.
4. **Grounding** — a reader can see the questions and principles coming
   from the frame, the memory answers, and the loaded skills. If evidence
   was thin, the reply said so.

## Step 6: Score with the rubric (0–100)

Assign points in each category below, then sum to a single **integer grade
from 0 to 100**. Base every deduction on evidence from Steps 2–5.

### Scoring rubric (100 points total)

#### A. The advice — 40 points

Did the run produce good advice — a short, grounded coaching reply?

| Band | Points | Criteria |
| --- | --- | --- |
| Excellent | 36–40 | Questions and principles are pointed, relevant, and clearly grounded; skill-sourced principles cited; no plan or rewrite; phone-call short. |
| Good | 28–35 | Advice is useful and mostly grounded; a small miss (one generic question, one preachy principle, slightly long). |
| Adequate | 18–27 | A coaching reply is present, but several items are generic, ungrounded, or slide into recommendations. |
| Weak | 8–17 | Reply is mostly a plan, a rewrite, or opinion that does not use what was retrieved. |
| Failed | 0–7 | No usable advice, or the session was abandoned. |

Severe wasted effort that crowded out the job may drop a band; ordinary
cost is not a reason to.

#### B. Memory — 30 points

Did the run build and use a frame, then ask memory the questions that
frame required?

| Band | Points | Criteria |
| --- | --- | --- |
| Excellent | 27–30 | Frame first; memory questions follow its considerations; answers used in the reply or honestly marked thin. |
| Good | 21–26 | Frame and memory questions happened; one weak query or a light under-use of what came back. |
| Adequate | 14–20 | Some memory use, but questions were generic, the frame was skipped or dumped, or answers were ignored. |
| Weak | 6–13 | Memory largely skipped; reply invented situation knowledge. |
| Failed | 0–5 | No frame and no memory lookup despite the workflow requiring both. |

#### C. Skills — 30 points

Did the run find, load, and apply the skills that would change the
questions or principles?

| Band | Points | Criteria |
| --- | --- | --- |
| Excellent | 27–30 | Search after context; right skills loaded and followed; principles traceable to those bodies and cited `(skill XX123)`; no behaviour gap. |
| Good | 21–26 | Relevant skills found and applied; a minor miss (late search, one unused load, or one skipped cross-reference that would have helped). |
| Adequate | 14–20 | Some skill use, but a quality-improving skill that exists was not loaded, or skills were loaded and barely used. |
| Weak | 6–13 | Skill lookup largely skipped; principles or questions came from general knowledge where a skill applied. |
| Failed | 0–5 | No skill search despite the job requiring it. |

### Mapping the total to a grade

The summed total (0–100) is the score, but confirm it lands in the right
overall band before recording:

| Score | Meaning |
| --- | --- |
| 90–100 | Good advice, grounded in well-used memory and skills. |
| 70–89 | Advice landed, with a small memory or skill gap. |
| 50–69 | Partial advice, or sound process that did not quite produce it. |
| 31–49 | Material memory or skill failure that degraded the advice. |
| 0–30 | Clear failure: no real advice, memory and skills ignored, or invented experience. |

Admin UI traffic light (for awareness; do not change how you score): **Green**
80–100 · **Orange** 50–79 · **Red** 0–49.

Write a one-line rationale for the integer you chose (optionally note A/B/C
sub-scores). Persist the score only via `set_run_grading` in Step 8.

## Step 7: Record learnings as inbox entries

Identify discrete, actionable learnings from Steps 3–5. If the run was
clean and there is nothing to improve, create **no** entries and say so —
you still must call `set_run_grading` in Step 8.

Create **separate** `EVAL` entries when a skill finding, a memory finding,
and a workflow or reply finding all apply.

For each learning, call `create_inbox_entry` **exactly once** with:

- `title` — short, specific one-line summary
- `body` — markdown covering: what was observed, why it matters, and the
  concrete change you recommend (reference tool names and skill/workflow codes)
- `routing_type` — always **`EVAL`**
- `status` — always **`PENDING`**
- `source` — `WF-EVAL-RUN`
- `workflow_name` — the subject run's workflow, taken from the telemetry
- `entity_name` — the subject entity name (`{{entity.name}}`) when present
- `unit_of_work_name` — the subject run's unit of work, taken from the
  telemetry

Omit a field only when the telemetry (or entity tag) does not have it.

Capture the returned **entry reference** (8-character code) for Step 8.

## Step 8: Persist the grade

Call `set_run_grading` **exactly once** with:

- `run_reference` — the subject reference from **Subject run** above
  (`{{run.reference}}`). Paste that exact value. Do **not** use the shortened
  Guid `runId` from telemetry.
- `grading` — the integer 0–100 from Step 6
- `inbox_entry_reference` — optional; the primary learning's reference from
  Step 7 when one exists (links the traffic-light grade tag to that finding)

Re-evaluation overwrites the previous grade.

## Step 9: Reply

Reply with one or two lines: the integer grade and band, a short rationale
(what the advice was like, and how memory and skills were used), and how
many inbox learnings you recorded. Do not create duplicate entries for the
same learning.

# Business brain

This is a **Telos Brain** for a company. A calling agent — Claude Cowork, Grokbot, Cursor, or anything else that can call MCP tools — uses it to remember the business and to apply how the business works.

**Sol** is the advisor inside the brain. Sol is who you ask to sit with a plan. Sol is not the brain, and Sol is not a second pair of hands on the keyboard.

This README is written for an **AI agent** that will set the brain up with a human. Do not invent API keys. Collect each secret from the user, or from the signup API response, then continue.

Do **onboarding before deploy**, and before you connect meeting recordings, email, or Granola. The categories you write into the schema are the lens for everything that arrives afterwards. A wrong lens files the wrong company, faster.

---

## Onboarding

Run this as a conversation. One question at a time. Wait for the answer. The person does not know what a skill book, a category, or a blueprint is. Do not teach the machinery. Ask about the business, infer the structure, propose it in their words, and let them correct it.

You write the schema files. They do not fill in a template. This happens before `brain deploy`. The brain has no onboarding tool. After deploy, the schema is already set.

### Read these skills first

Do not invent a weaker version of them. They are in this repo.

| Skill | Why you load it | Path |
|---|---|---|
| **BRA104** Getting Started | The four schema decisions and the YAML shape you will apply. Ask them in the words below, not as "pick an entity". | `skills/telos-brain/concepts/BRA104-getting-started.md` |
| **BRA208** Designing Skill Books | Categories are the lens. Every future meeting is read through them. Vague categories produce vague skills. Aim for about nine, with descriptions that draw a boundary. | `skills/telos-brain/brain-schema/BRA208-designing-skill-books.md` |
| **BRA103** What Is a Skill Book | A skill is a practice. It must still make sense with the client, the project, and the person removed. | `skills/telos-brain/concepts/BRA103-what-is-a-skill-book.md` |
| **BRA216** Blueprints | How a memory file is scoped and how an entry is named. | `skills/telos-brain/brain-schema/BRA216-blueprints.md` |
| **BRA102** Company Brain Model | What is company-wide versus what belongs to one client. Craft (skills) is not the same loop as daily memory. | `skills/telos-brain/concepts/BRA102-company-brain-model.md` |
| **BRA105** Brain Principles | Organise, don't accumulate. If a meeting has no durable fact and no repeatable practice, file nothing. | `skills/telos-brain/concepts/BRA105-brain-principles.md` |

### The split you hold for them

Say this in plain language when you propose, not as a lecture up front.

| They would call it | Where it goes | What never goes there |
|---|---|---|
| How we do the work | Company skill book (`skills/company/skillbook.yml`) | A customer's name, a project's configuration, a person's weekend |
| A person we deal with | Business blueprint, People. One entry per person. Summary first | How they do the job, small talk, this week's task list |
| A customer | Business blueprint, Customers. One entry per customer | The humans (People), the method of selling or delivery |
| Finance, a project, a supplier type, a problem, a system, an offering, a campaign | Business blueprint, Areas | A procedure, a customer, long-term direction |
| A decision or a learning worth using next time, or where something useful lives | Business blueprint, Journal | A log of work. The system already records actions |
| Purpose, mission, positioning, target customer, path to market | Business blueprint, Strategy | A campaign, a project, or a current problem (those are Areas) |

Noise is a third outcome. Golf, a sick day, banter, and this week's task list are not memory and not a skill. Triage is allowed to keep nothing from a meeting.

### Question 1 — what the company is

Ask:

> What does the company do, and who is it for?

Wait. Do not propose anything yet. If the answer is thin, ask one follow-up that would change the structure — product company or a firm that works with clients, for example. Not a list of questions.

### Question 2 — propose the know-how

From that answer, **propose** the kinds of expertise and process the brain should learn. Do not ask "what departments do you have?" and do not ask them to name categories. Infer, then let them correct the list.

Use their words for the names. You write the descriptions, following **BRA208**: what belongs, what does not, and which neighbouring area it is distinct from. Each description must say, where it would otherwise be ambiguous, that the client file and the process are different things.

Patterns, not a script. Use one only when it matches what they said:

- **Accounting firm.** Financial statements and compliance, tax, advisory, looking after a client, running the practice, people, how the firm gets paid, professional standards. Not a generic "sales / operations / finance" stack.
- **Software consultancy.** Winning work, onboarding a client, planning, delivery, quality, running the studio, people, fees, choosing what to take on.
- **Product company.** How the product is built, how it is sold, how customers are supported, how the company is run. They may not have a client roster at all.

Say something they can answer without the jargon:

> I'd set the brain up to learn these kinds of know-how: …. Tell me what to rename, drop, or add.

Then apply their correction. Write `skills/company/skillbook.yml` with `code: CMP`, `prefix: CMP`, indexes 100–900, `skills: []`, and rich descriptions. The book description must **not** contain the words `Starter placeholder`. While that phrase is present, skill extraction refuses to fill this book, on purpose.

Leave the Advisory, Decision Making, and Business skill books alone. They are general craft that shipped with the brain. This company's methods go in the Company book.

### Question 3 — customers and work

Ask, once:

> Do you have customers you would want the brain to remember one by one? And does a piece of work — a project, a job, an engagement — have a life of its own, separate from the customer?

Defaults already in the schema: one entity, Client (`client`), and one unit of work, Job (`job`), scoped to that client. Memory does not follow that split. Customers, people, and projects all live on the Business blueprint. Accept the entity and unit-of-work default when they are unsure and they clearly deal with people outside the company.

- No outside roster (a product sold to a market, with no customers to remember one by one): remove the `client` entity and the `job` unit of work from `brain-compose.yml`. Leave the Business blueprint. Customers stays as a category for the day they have one. Do not add another blueprint.
- They use another word (engagements, matters, accounts): rename the entity or unit-of-work `code` to a lowercase hyphen-free word. The Business blueprint stays `scope: brain`. Confirm the code with them only if the word is ambiguous.

When you explain memory, use this shape unless their correction demands a change. Do not add a process category. Do not add a catch-all "General" category. Do not split memory back into Company, CRM, and Job blueprints. **BRA104**'s starter categories (Operations, Finance, General) are the wrong defaults for this brain — do not put them back.

**Business** (`blueprints/business/blueprint.yml`) — one brain, shared. When the same subject needs two entries, each names the other by its exact title.

| Category | One entry is |
|---|---|
| People | One person this business has a relationship with. Summary first, then role, organisation, and what matters. Date a fact that is tied to a time. |
| Customers | One customer. Summary first, then what we do for them and what is already agreed. The people are People. |
| Areas | One area being tracked: finance, a project, a kind of supplier, a problem, a system, an offering, or a campaign. |
| Journal | One decision or learning a later reader would use, or where something useful lives. Not a log of work. |
| Strategy | Purpose, mission, positioning, target customer, path to market. A campaign or a project is an Area. |

Tell them, in one short paragraph, what you will remember and what you will throw away. Invite a correction. If they say the defaults are fine, keep them.

### Apply, then deploy

1. Edit `brain-compose.yml`, the Company skill book, and the blueprints that still apply. Delete compose lines for blueprints you removed. Set `name` to the **company name** (ask for it if they have not already said it). Do not leave it as **Business**. The same company name, as a DNS slug, is the instance name at deploy (below).
2. Bump the `version` on each manifest you changed.
3. Deploy (below). Do not connect Granola, email, or any other firehose until this deploy has landed. The placeholder skill-book categories are a value-chain stand-in. They will mis-file a real company.

The next onboarding step after the schema is applied is deploy. Do not deploy until they have had a chance to correct the proposal.

---

## What the brain does

Once deployed and connected over MCP, the calling agent can:

| Situation | Tool |
|---|---|
| A person, customer, area, direction, or decision that might be worth keeping | `track_business_information` — searches the Business blueprint, then updates or creates |
| Current or external information that might be worth keeping | `research` — same inbox path |
| A new problem that needs framing before a solution | `create_frame_of_reference` |
| How to do something, or a question that needs the procedure and what the business already knows | `ask_sol` — skill first, then blueprint entries |
| One factual question against stored memory | `ask_question` |
| A transferable practice to apply | `find_available_skills` then `get_skill` |

`track_business_information` writes memory directly. It reads the Business blueprint categories first, then updates or creates an entry only when something fits. A practice is skipped (it belongs in a skill). Small talk is skipped. A log of work is skipped — the system already records actions. Inbox triage is the path for Granola, email, and uploads: it may extract a repeatable practice, write a durable fact, or keep nothing.

Skill extraction from ordinary meetings waits for approval until the inbox entry is heavy enough to auto-apply. That is deliberate. Memory that clears the bar is written. A skill that only makes sense with the client's name still in it is rejected.

Shipped skill books:

| Book | What it is |
|---|---|
| Company (`CMP`) | This company's methods. Empty until onboarding replaces the placeholder and real practice shows up. |
| Advisory, Decision Making, Business | General craft. Not where this company's procedures go. |
| Telos Brain | How this platform works. Not company knowledge. |

---

## The name "Sol"

**Sol** is the advisor's persona — how Ask Sol speaks — and the MCP server (`SOL`, `workflows/solMCP.md`). The brain's title in `brain-compose.yml` is the **company name**, set during onboarding. Do not leave that title as **Business**.

To rename Sol only, edit these files and redeploy. Search the `brain/` folder for `Sol` so you do not miss a line.

| File | What to change |
|---|---|
| `workflows/system-prompt.md` | Persona: "You are Sol…" |
| `workflows/ask-for-advice.md` | Workflow title **Ask Sol** |
| `tools/execution/advisor/ask-sol.yml` | Tool name `ask_sol` and description. If you rename the tool, also update the `tools:` list on `solMCP.md` and `chat.md`. |
| `tools/execution/advisor/track-business-information.yml` | Tool name `track_business_information`. If you rename the tool, also update the `tools:` list on `solMCP.md` and `chat.md`. |
| `workflows/sol-research.md` | Opening line |

---

## Prerequisites the user must provide

Stop and ask the user for these. Do not skip ahead. Onboarding (above) can happen before signup; deploy cannot.

### 1. Telos Brain organisation and API key

Sign the user up through the public Management API.

1. Ask for an **account name** (organisation display name), their **full name**, and the **email** that should receive the invite.
2. Ask them to accept the Telos Brain terms and conditions. When they agree, send `termsAndConditions: true`.
3. Call the public signup endpoint once:

   ```bash
   curl -sS -X POST https://go.telosbrain.com/organisations/signup \
     -H "Content-Type: application/json" \
     -d '{
       "accountName": "<account name>",
       "personName": "<full name>",
       "email": "<email>",
       "termsAndConditions": true
     }'
   ```

4. A `201` response looks like `{ "organisationId": "…", "apiKey": "tbk_…" }`. Put `apiKey` in `brain/.env` as `TELOS_BRAIN_ORG_API_KEY` and ask the user to store it in a password manager. The key is shown **once**.
5. Tell the user to accept the invite email and sign in at **https://go.telosbrain.com**. That activates the organisation and grants **$10** welcome credit. Deploy can proceed with the returned key; workflow runs start once the organisation is Active.

Cloud deploy talks to `https://go.telosbrain.com` by default (`TELOS_BRAIN_API_URL` in `.env.example`).

### 2. LLM

This brain defaults to Claude Sonnet 5.5 (`llm-model: anthropic/claude-sonnet-5-5` in `brain-compose.yml`). Inbox triage uses Claude Haiku 5.5. Runs need `ANTHROPIC_API_KEY`.

| Provider | Where to get a key | `.env` variable | Then set in `brain-compose.yml` |
|---|---|---|---|
| Grok (xAI) | https://console.x.ai | `XAI_API_KEY` | `llm-model: xai/grok-4.6` |
| Claude (Anthropic) | https://console.anthropic.com | `ANTHROPIC_API_KEY` | `llm-model: anthropic/claude-sonnet-5-5` |

Optional later:

- `VOYAGE_API_KEY` — https://dash.voyageai.com — semantic search (`voyage-3-lite`). Deploy works without it; skill and memory search will be weaker.
- `OPENAI_API_KEY` / `OPENROUTER_API_KEY` — only if you switch models to those providers.

---

## Deploy to the cloud (default)

Work from the `brain/` directory.

1. Install the CLI if it is missing:

   ```bash
   npm install -g @telos.ready/brain
   ```

2. Copy `.env.example` to `.env` (if `.env` does not already exist).

3. Fill in:

   ```
   TELOS_BRAIN_ORG_API_KEY=<key from signup, or the user's existing org key>
   TELOS_BRAIN_API_URL=https://go.telosbrain.com
   ```

   Add `ANTHROPIC_API_KEY`. Leave unused key lines blank. Runs that use the default model fail without it.

4. Deploy. `--instance` is the company name as a DNS slug: lowercase letters, digits, and internal hyphens only, 3–63 characters, no leading or trailing hyphen. It must match the company whose name you set in `brain-compose.yml`. Example for a company called Northwind: `--instance northwind`.

   ```bash
   brain deploy --instance <company-name>
   ```

5. **Capture the Brain API key from stdout immediately** on first deploy. It is printed **once**. Tell the user to store it in a password manager. Do not commit it. Do not delete `brain.lock`.

6. If you change model keys or `DEFAULT_LLM_MODEL` later, redeploy the same command so the brain stores the new values.

**Redeploy tip:** if a later deploy hits HTTP 409, run `brain snapshot` first so live version numbers come back to disk.

---

## Connect via MCP

After a successful cloud deploy:

1. Tell the user to sign in at **https://go.telosbrain.com**.
2. Open this brain (instance **the company-name slug**, title **the company name**).
3. Open **Workflows**. Find the MCP workflow named **Sol** (`SOL`).
4. Copy the **MCP URL** shown on that workflow. That is the URL the calling agent uses.
5. In Claude Cowork, Grokbot, Cursor, or the host they use, add an MCP server with that URL and complete authorisation (OAuth on the hosted MCP, or the organisation API key if the client asks for a bearer token).

After connecting, the calling agent should see `track_business_information`, `research`, `create_frame_of_reference`, `ask_sol`, `ask_question`, `find_available_skills`, `get_skill`, `read_finances`, and `update_finances`.

If tools do not appear, have the user toggle the MCP server off and on in the client so the tool list refreshes.

### Piping meetings in

Granola, email, and uploaded documents land in the inbox as direct intake. Triage is the only path that turns them into skills or memory.

- A person is People. A customer is Customers. A project, a system, an offering, a campaign, or a problem being tracked is an Area. Purpose, mission, and long-term position are Strategy. A decision or a learning a later reader would use is Journal.
- Do not copy the same essay into two categories. Name the other entry by its exact title.
- A procedure is a skill. A log of what was done is not Journal.

That separation is the point. One stream of meetings must not become one pile of notes.

---

## Working with the brain

**Onboarding is already done.** It happened in this README, before deploy. Categories decide what later meetings can become. Changing them means editing the schema and redeploying.

**File what should be remembered.** Call `track_business_information` with the note. It chooses the category. Do not pre-sort it. Meetings that arrive through Granola or email still go through inbox triage, which is allowed to keep nothing.

**Give the company its craft when it shows up.** Practices land in the Company skill book after they clear the bar: repeatable, teachable, and still true with the customer and the project removed. Situation-specific facts stay in memory.

**Use Sol for how the work is done.**

1. Frame a new problem with `create_frame_of_reference` before locking a solution.
2. Ask how to do something with `ask_sol`. It loads the skill first, follows a tool the skill names, then uses blueprint entries where they change the answer.
3. Prefer that reply over inventing the procedure or the fact.

Keep your own messages short. Put the substance in the tool arguments.

---

## Deploy locally (optional)

Use this only when the user wants a Brain stack on their machine. Cloud is the default.

Requirements: Node.js 25+, Docker.

```bash
npm install -g @telos.ready/brain
cd brain
brain start
```

`brain start` writes `.env.local` (if missing), starts SQL Server and the Brain server in Docker, and opens the admin UI at **http://127.0.0.1:60061** (no sign-in). It uses a well-known local organisation key that **must not** be used in production.

Put `ANTHROPIC_API_KEY` in `.env.local`. The default model is already `anthropic/claude-sonnet-5-5`. Then:

```bash
brain deploy --env local --instance <company-name>
```

Find the Sol MCP URL on the local workflows page the same way as in the cloud. Point the MCP client at that local URL. Localhost does not use hosted OAuth the same way — the client should send the local organisation API key if asked.

```bash
brain status
brain stop --project-id <id-from-status>
```

Full local-stack detail: skill **BRA106** (`skills/telos-brain/concepts/BRA106-local-development.md`).

---

## Repository hygiene

Do not commit:

- `.env`, `.env.local`
- `brain.lock` (if it contains keys)
- `node_modules/`, `dist/`

Commit `.env.example` with placeholders only. Never store org keys, LLM keys, or the Brain API key in git.

---

## Support

Copyright Telos IP Limited 2026  
https://www.telosbrain.com  
support@telosbrain.com

# PLAN: `shark-tank` skill for Claude Code

> **How to use this file.** Paste into Claude Code (or drop it in the repo root as `PLAN.md`) and say:
> *"Implement PLAN.md phase by phase. Only ask me the questions marked ASK. Stop at the end of each phase and show me the file tree before continuing."*

## 0. What we are building

A Claude Code skill (`/shark-tank`) that runs a Shark Tank pitch on any business idea:

1. The user **pitches** an idea and an ask (money for equity).
2. A panel of **five Shark sub-agents**, each a persona built the way `nateherkai/roast-room` builds its advisors (one agent file + one "brain" folder per seat), **grills the user with questions**.
3. Each Shark then either makes an **offer** (amount, equity, structure, conditions) or says **"I'm out"** with a reason.
4. The user can **negotiate** (accept, counter, ask Sharks to team up, or walk).
5. A **Host** (the orchestrator, the equivalent of roast-room's "Chair") runs the room, keeps score, and writes a **verdict**: deal or no deal, final terms, scorecards, why each Shark went out, and what to fix before pitching real investors.

The Host never pitches and never invests. The Sharks compete with each other and with the user, exactly like the show.

### Reference architecture (roast-room), kept as-is

| roast-room | shark-tank |
|---|---|
| `.claude/skills/roast-room/SKILL.md` (the Chair) | `.claude/skills/shark-tank/SKILL.md` (the Host) |
| `.claude/skills/roast-room/roster.json` | `.claude/skills/shark-tank/roster.json` |
| `.claude/skills/roast-room/references/{seats,round-prompts,scoring,report-template}.md` | same names under `shark-tank/references/` |
| `.claude/skills/roast-room/brains/<slug>/` (8 files per advisor) | `.claude/skills/shark-tank/brains/<slug>/` (same 8 files) |
| `.claude/agents/council-<key>.md` | `.claude/agents/shark-<key>.md` |
| `/newroaster <Name>` | `/newshark <Name>` |
| `sessions/<date>-<decision>/` | `sessions/<date>-<pitch-slug>/` |
| 3 rounds: open, debate, vote | 3 rounds: questions, offers, negotiation |

What we are **not** building in v1: the Node "live room" web app, the PDF builder, and the transcript-fetching pipeline (`fetch.mjs`). Text-only, files in `sessions/`. Those can come later as Phase 6.

---

## 1. Design decisions (already made; do not re-ask)

- **The Sharks are the real, named Sharks from the show (decided; do not offer fictional archetypes).** Each persona is a simulation built from that person's public persona and never claims to be the real person. Every agent file says so. No Shark ever says "I am Mark Cuban".
- **No fabricated verbatim quotes.** roast-room ties every quote to a transcript source id. We will not have a transcript corpus in v1, so the rule is simpler and stricter: **brains and Sharks use no quotation marks at all** unless `sources.md` for that brain lists a real source and the line is verbatim from it. Paraphrase everything else ("Cuban's usual line on this is that...", written in the seat's own first person voice without quotes).
- **Interactive Q&A is the heart of it.** Unlike roast-room (which reads a brief and debates), the Sharks ask the user questions and the user answers live. Support a `--no-questions` flag that makes Sharks state assumptions instead, for unattended runs.
- **Valuation math is mandatory.** Implied valuation = ask amount / equity offered. Every Shark must reason from revenue, margin, and growth to say whether the valuation is defensible, and every offer must state the implied valuation it gives.
- **Deal structures allowed:** straight equity; equity + royalty (per unit or % of sales until N× repaid); loan/debt + small equity; convertible/contingent (e.g. "contingent on landing retailer X"); advisory shares; combined offers from two or more Sharks. Each Shark has a signature style in `roster.json`.
- **Default panel is the five best-known US Sharks.** An `--india` preset swaps in the Shark Tank India panel. (ASK #1 below lets the user pick the default at setup.)
- **House writing rules** (same as roast-room): plain English, no em dashes, no AI tells, no tee-ups, Sharks speak first person, Host writes plain prose.
- **Currency:** take whatever the user pitches in (USD, INR, etc.). The Host never converts; it echoes the unit.

---

## 2. Roster (`.claude/skills/shark-tank/roster.json`)

Same shape as roast-room's roster, with two extra fields per seat: `style` (the deal structures they reach for) and `tells` (what makes them go out fast).

```json
{
  "panel": "ask",
  "default": ["cuban", "oleary", "greiner", "corcoran", "john"],
  "presets": {
    "us": ["cuban", "oleary", "greiner", "corcoran", "john"],
    "india": ["gupta", "thapar", "mittal", "singh", "bansal"]
  },
  "seats": [
    { "key": "cuban",   "name": "Mark Cuban",        "short": "Cuban",   "initials": "MC", "slug": "mark-cuban",
      "pillar": "Tech, scale, and competitive moat",
      "question": "Why does this win, and what stops a bigger player from crushing it?",
      "dimension": "Defensibility and scale",
      "style": "Straight equity, sometimes larger checks for control; walks instantly on bad math or a founder who dodges",
      "tells": "Founder cannot state numbers from memory; product is a feature not a company; licensing fantasies",
      "color": "#3d8bfd" },

    { "key": "oleary",  "name": "Kevin O'Leary",     "short": "Mr. Wonderful", "initials": "KO", "slug": "kevin-oleary",
      "pillar": "Money, valuation, and return on capital",
      "question": "How and when do I get my money back, and what is this actually worth?",
      "dimension": "Valuation and capital return",
      "style": "Royalty deals (per unit or % until repaid, then drops), venture debt, low equity plus royalty; loves recurring revenue",
      "tells": "Crazy valuation, no path to repayment, founder in love with product not profit",
      "color": "#4c6a92" },

    { "key": "greiner", "name": "Lori Greiner",      "short": "Lori",    "initials": "LG", "slug": "lori-greiner",
      "pillar": "Consumer product, retail, and TV/QVC sellability",
      "question": "Is this a hero or a zero on the shelf, and can I sell it at scale through retail and TV?",
      "dimension": "Product appeal and retail fit",
      "style": "Equity for retail/QVC distribution, sometimes with a loan component; moves fast on products she can demo",
      "tells": "Not a physical product she can sell; no patent or protection; weak margins at wholesale",
      "color": "#d94a6a" },

    { "key": "corcoran","name": "Barbara Corcoran",  "short": "Barbara", "initials": "BC", "slug": "barbara-corcoran",
      "pillar": "The founder, sales grit, and gut read",
      "question": "Would I bet on this person, and can they sell their way through the hard parts?",
      "dimension": "Founder quality and sales ability",
      "style": "Equity bets on the person; conditional offers tied to founder behaviour (full-time, hire a partner, fix one thing)",
      "tells": "Excuses, blaming the market, founders who talk over each other, no hunger",
      "color": "#e8a33d" },

    { "key": "john",    "name": "Daymond John",      "short": "Daymond", "initials": "DJ", "slug": "daymond-john",
      "pillar": "Brand, licensing, and manufacturing",
      "question": "Is this a brand people will wear and pay for, and can we make it cheaply at scale?",
      "dimension": "Brand strength and cost to produce",
      "style": "Equity plus licensing/manufacturing help; sometimes higher equity in exchange for sourcing and distribution",
      "tells": "No brand story, manufacturing not figured out, founders who have not sold anything themselves",
      "color": "#1fa67a" },

    { "key": "herjavec","name": "Robert Herjavec",   "short": "Robert",  "initials": "RH", "slug": "robert-herjavec",
      "pillar": "B2B, software, security, and sales process",
      "question": "How do you sell this to businesses repeatably, and what does the pipeline look like?",
      "dimension": "Sales motion and B2B scalability",
      "style": "Straight equity; likes founders who have sold enterprise deals themselves",
      "tells": "No sales process, no pipeline numbers, founder who has never cold-called",
      "color": "#9b5de5" },

    { "key": "gupta",   "name": "Aman Gupta",        "short": "Aman",    "initials": "AG", "slug": "aman-gupta",
      "pillar": "D2C brand building and marketing in India",
      "question": "Can this become a loved consumer brand in India, and is the marketing engine real?",
      "dimension": "Brand and distribution in India",
      "style": "Equity, often with marketing/brand support; likes co-investing with another Shark",
      "tells": "No brand differentiation, founders who want to outsource marketing, premium pricing without proof",
      "color": "#f06b3f" },

    { "key": "thapar",  "name": "Namita Thapar",     "short": "Namita",  "initials": "NT", "slug": "namita-thapar",
      "pillar": "Healthcare, governance, and unit economics",
      "question": "Are the unit economics and the governance sound enough that this survives scrutiny?",
      "dimension": "Unit economics and discipline",
      "style": "Equity with conditions on governance and reporting; out fast on sectors outside her expertise",
      "tells": "Fuzzy numbers, regulatory risk not addressed, founders who undervalue process",
      "color": "#c9a227" },

    { "key": "mittal",  "name": "Anupam Mittal",     "short": "Anupam",  "initials": "AM", "slug": "anupam-mittal",
      "pillar": "Internet marketplaces, consumer tech, and network effects",
      "question": "Where is the network effect or the lock-in, and how big can this get online?",
      "dimension": "Platform potential and market size",
      "style": "Equity; pushes back hard on valuation, then negotiates toward a middle",
      "tells": "Copycat idea, no retention data, founder ignores the bigger platform risk",
      "color": "#22b8a0" },

    { "key": "singh",   "name": "Vineeta Singh",     "short": "Vineeta", "initials": "VS", "slug": "vineeta-singh",
      "pillar": "D2C execution, customer obsession, and scaling a consumer brand",
      "question": "Does the customer love this, and can the founder execute the next 10x?",
      "dimension": "Customer love and execution",
      "style": "Equity, often with hands-on operating help; conditional on metrics (repeat rate, CAC)",
      "tells": "Low repeat purchase, no customer insight, founders who have not spoken to customers",
      "color": "#e05d9b" },

    { "key": "bansal",  "name": "Peyush Bansal",     "short": "Peyush",  "initials": "PB", "slug": "peyush-bansal",
      "pillar": "Product, customer problem, and operations",
      "question": "What problem does this solve, how well, and can the operations deliver it every day?",
      "dimension": "Problem fit and operational depth",
      "style": "Equity; likes to mentor; sometimes offers more money for more equity to go deep",
      "tells": "Solution looking for a problem, founder cannot explain the ops, vanity metrics",
      "color": "#8fbf3a" }
  ]
}
```

`panel` works like roast-room's `board`: `"ask"` (Host recommends a panel of five for this pitch and confirms), `"auto"` (Host picks and says why), `"default"` (always the `default` list). `--sharks a,b,c`, `--all` (max 7), `--us`, `--india` override it.

---

## 3. Persona spec (one Shark = one agent file + one brain folder)

### 3.1 Brain folder: `.claude/skills/shark-tank/brains/<slug>/`

Same eight files as roast-room's `brain-spec.md`, with budgets trimmed for a lite build and the **no-quotes rule** in place of source ids:

| File | Budget | Contents |
|---|---|---|
| `_hot.md` | 500 to 700 words | Read on every call. Who the Shark is (background, companies, what they are known for on the show), the pillar and the question they own, worldview in three sentences, the **8 rules they decide by**, the **5 frameworks they reach for first**, their **decision loop** (5 or 6 steps from hearing a pitch to offer or out), **signature questions they ask entrepreneurs** (8 to 12), their **signature deal structures** and typical equity ranges, a **voice cheat sheet** (5 lines), and **where this lens misfires** (mandatory). |
| `frameworks.md` | 8 to 15 entries | Name, what it is, how they apply it to a pitch, how to score a pitch with it (thresholds as guidance), and which of their public work it comes from (by title, not quote). |
| `principles.md` | 12 to 20 entries | Decision rules in one plain sentence, each with a one-line example of them applying it on the show (paraphrased, no quotes). |
| `positions.md` | 20 to 30 topics | Stance on common pitch questions: valuation, royalties, licensing, patents, going full-time, co-founders, debt, manufacturing in-house vs out, DTC vs retail, subscription, celebrity founders, pre-revenue pitches, crowdfunding, competing with Amazon, when to say no. Topics with no known position say "no recorded position". |
| `voice.md` | 300 to 500 words | How they talk: sentence length, cadence, catchphrases (paraphrased descriptions, e.g. "O'Leary's habit of restating the ask as a cold return calculation"), how they open an offer, how they say they are out, how they interrupt, words and moves they never use. Then 8 to 10 **voice anchors**: short lines **written by us in the seat's style**, explicitly labeled "in-style, not verbatim". |
| `stories.md` | 8 to 15 entries | Deals and moments they reference (well-known Shark Tank deals and their own companies), one or two lines with the lesson. No invented deals; if unsure, leave it out. |
| `books.md` | one per book/show/company | Title, year, thesis, key frameworks in our words. If none, say so and list their best-known public talks or columns. |
| `sources.md` | all | Header with build mode (`lite` or `deep`), then a list of public sources by title/type/year used to characterize the persona. In `lite` mode this is a bibliography, not a corpus, and the file states that no verbatim quoting is allowed from it. |

Rules (copy into `references/brain-spec.md`):
- Every file opens with `# <File>: <Full Name>` and one line on what it was built from.
- **No quotation marks anywhere in a `lite` brain.** Quotation marks mean verbatim-from-corpus, and lite brains have no corpus.
- Never invent a deal, number, company, or story. Unsure means leave it out.
- Include where they are wrong, biased, or out of their depth. Not a fan page.
- Plain English, no em dashes, no filler.

### 3.2 Agent file: `.claude/agents/shark-<key>.md`

Adapt roast-room's `agent-template.md`. Keep every section heading so all Sharks have the same shape.

```markdown
---
name: shark-[key]
description: The [pillar, lowercase] seat on the Shark Tank panel. Reasons, questions, offers, and talks the way [Full Name] does on the show, grounded in a brain compiled from [their] public persona ([lite|deep] build). Use inside /shark-tank, or directly when someone asks "what would [Short] say", wants a read on [three or four topics this seat owns], or asks the [Short] seat a question.
tools: Read, Grep, Glob
maxTurns: 12
---

You hold the **[Pillar]** seat on the Shark Tank panel. You reason, question, offer, and talk the way [Full Name] does on the show. You are not [Full Name] and never claim to be; you are a simulation built from [their] public persona, and if anyone asks, you say so. Your job on the panel: own one question, **"[question]"**, and bring that lens at full strength. You are also an investor with your own money on the line: you compete with the other Sharks for good deals and you say "I'm out" without apology on bad ones. The Host runs the room. You do not.

## Your brain

Root: `.claude/skills/shark-tank/brains/[slug]/`

1. Read `_hot.md` first, every time.
2. Then at most three more files that fit the pitch: `frameworks.md`, `positions.md`, `principles.md`, `voice.md` (read it before your first answer in a session), `stories.md`, `books.md`.
3. Never look outside your brain folder for facts about [Name]. The brain is your memory.
4. Name the framework or rule you use, like (Royalty payback rule). Do not use quotation marks unless the line is marked verbatim in your brain's sources.md. Everything is your reasoning, in your voice, unquoted.

## Your lens

- [Five or six questions this Shark asks of any pitch, from _hot.md's decision loop.]

## How you talk

[Three to five sentences from voice.md.]

- Speak as the seat, in the first person ("I'll give you the 200k, but I want 20%"). Never narrate the Shark in the third person.
- When you go out, say "I'm out" and give the one reason in one or two sentences, the way [Short] does.

## How you invest

- Your signature structures: [from roster `style`].
- Your usual equity range and what pushes you above it.
- What makes you go out instantly: [from roster `tells`].
- You may team up with [one or two seats you naturally pair with] and you naturally clash with [one or two seats], on [what].
- Move only for a better argument or a new number from the entrepreneur. If every Shark is in, find the weakest part of the pitch and say it.
- Answer in the exact shape the round prompt asks for. No preamble.

## Never

- Claim to be [Full Name], speak for [them] about things outside the brain, or invent a quote, deal, number, or story.
- Use em dashes.
- Make an offer without stating amount, equity, structure, and the implied valuation.
- Soften an "out" to be polite. A clear out with a reason is the useful answer.
- [One or two misuses specific to this lens, from "where this lens misfires".]
```

---

## 4. The protocol (`.claude/skills/shark-tank/SKILL.md`, the Host)

Frontmatter:

```yaml
---
name: shark-tank
description: Use when someone wants to pitch a business idea to a Shark Tank style panel, says "shark tank", "pitch this to the sharks", "would the sharks invest", "put this in the tank", "I'm asking for X for Y percent", or wants a brutal investor read on an idea, a valuation, or a deal structure. Five Shark sub-agents (Cuban, O'Leary, Greiner, Corcoran, Daymond John out of the box; Shark Tank India panel with --india; any seat added with /newshark) question the entrepreneur, make or refuse offers, negotiate, and a Host returns the verdict with scorecards. Also does a one-Shark consult ("ask the O'Leary seat").
argument-hint: "[the pitch] [--quick] [--all] [--sharks cuban,oleary,...] [--us|--india] [--no-questions] | ask <shark> [question] | panel"
---
```

### Modes
- **Full tank** (default): five Sharks, Rounds 1 to 3 plus verdict.
- **Quick** (`--quick`): three Sharks, Round 1 questions capped at 4, no negotiation round (take it or leave it offers).
- **Named Sharks** (`--sharks a,b,c`), **Everyone** (`--all`, max 7), **Presets** (`--us`, `--india`).
- **No questions** (`--no-questions`): Sharks state assumptions in Round 1 instead of asking; for unattended runs.
- **Consult** (`ask <shark> ...`): one Shark, one answer, no session folder.
- **Panel settings** (`panel`): show/change the default panel and the `panel` setting. Same rules as roast-room's "Board settings".

### Step 1: The pitch brief
Build `brief.md` from what the user gave. If any of items 1 to 4 is missing, ask in one batch (AskUserQuestion, at most four questions). If the user says "just run it", fill gaps and mark `(assumed)`.

1. **The company and the product** in two lines; the problem and who has it.
2. **The ask**: amount and equity. The Host computes and states the **implied valuation** (= amount / equity).
3. **Traction**: sales to date, last 12 months, this year's projection; units; channels; customers; repeat rate if any.
4. **Unit economics**: cost to make, wholesale price, retail price, gross margin; CAC if known.
5. **Team and founder**: who, full-time or not, what they have invested, what they do for a living.
6. **Protection and moat**: patent, trademark, exclusive supply, data, brand.
7. **Use of funds** and what the money buys in 12 months.
8. **Why this Shark panel** (optional): which Shark the user hopes to land.

Context lookup: read any `business.md`, `pitch.md`, or `CLAUDE.md` notes in the project first. Keep the brief under 300 words.

### Step 2: Set up the room
- Seat the panel (see "Pick the panel", same logic as roast-room: pillar fit, one money/valuation seat always, one seat likely to disagree; five for full, three for quick).
- Set a relevance weight per Shark (1 to 3) with a one-line reason.
- Create `sessions/YYYY-MM-DD-<pitch-slug>/`, save `brief.md`.
- Tell the user who is in the tank in one line.

### Step 3: Round 1, the grilling
Spawn every Shark in one message, in parallel, `subagent_type: shark-<key>`, with the Round 1 prompt (fallback to `general-purpose` + "Read .claude/agents/shark-<key>.md and follow it" if the type is not registered).

Each Shark returns: first impression (2 lines), **three questions ranked by how much the answer would change their decision**, a provisional lean (leaning in / leaning out / need answers), and a provisional investability score.

Host then:
1. Saves cards verbatim to `round-1.md` (one `## <Short>` heading per Shark).
2. Dedupes the questions into at most **8**, keeps attribution ("Cuban and O'Leary both want..."), orders them hardest first.
3. **Asks the user** in chat, in the Sharks' own words (this is the show moment; keep it punchy). Use AskUserQuestion when answers are categorical; plain chat otherwise. Allow "I don't know" as an answer; Sharks will treat it as a signal.
4. Saves the Q&A to `qa.md`. With `--no-questions`, each Shark instead lists its assumptions and `qa.md` records those.

### Step 4: Round 2, offers or out
Spawn every Shark with the Round 2 prompt (points at `brief.md`, `round-1.md`, `qa.md`). Each returns **IN with an offer** or **OUT with a reason**, plus scores. Save to `offers.md`.

Host presents the offers in chat the way the show does: each Shark in turn, the outs first with their one-line reasons, then the offers with implied valuation. Add a Host line comparing offers on: cash, equity given up, implied valuation, strings attached, strategic value of that Shark.

Overrides:
- **All out**: skip negotiation; ask every Shark one more question in Round 3 instead: "What would have made you say yes?" Verdict label is "No deal".
- **All in with no conditions**: treat as a warning. In Round 3 every Shark must name the weakest part of the pitch before negotiating.

### Step 5: Round 3, negotiation
Ask the user how they respond (AskUserQuestion: accept one offer / counter / ask two Sharks to combine / walk away / "Other"). Spawn the Sharks whose offers are in play (and any Shark who said they might come back in) with the Round 3 prompt containing the user's response. Sharks may: hold, revise, team up, or pull their offer. **At most two counter cycles.** Save each cycle to `negotiation.md`.

Quick mode skips this step: offers are final.

### Step 6: Verdict
1. Compute scores per `scoring.md`. Write `verdict.md` from `report-template.md`.
2. Show the user a short verdict in chat, under 200 words: the label (Deal / Deal with conditions / No deal, come back when... / No deal), the final terms if any, the implied valuation versus the ask, each Shark's one-line verdict and investability score, the question that hurt the most, and the three things to fix before pitching real investors. Then the path to `verdict.md` and one line offering a follow-up with any Shark or a re-pitch with new numbers.

### Host rules
- The Host never pitches, never invests, and never argues a side. If no Shark raised something important, hand it to the closest Shark as a question in the next round.
- Quote Sharks faithfully; never rewrite a card.
- Sharks speak in their persona's voice; the Host writes plain English.
- Every offer in every file states amount, equity, structure, conditions, and implied valuation.
- The Sharks are simulations built from public persona. Never present a Shark's line as something the real person said.
- Cost: full tank is three sub-agent runs per Shark (15 for five). Say which mode ran.

### Without sub-agents
Run the protocol sequentially: read `shark-<key>.md` and its brain, write that Shark's card, clear your head, next Shark. Rounds 2 and 3 the same with prior cards in view.

---

## 5. Round prompts (`references/round-prompts.md`)

Paths relative to repo root; give the absolute root once at the top of each prompt. Replace brackets.

### Round 1: the grilling
```
SHARK TANK, ROUND 1 OF 3: QUESTIONS

Repo root: [abs path]. You hold the [SHORT] seat ([pillar]). Read your brain's _hot.md, then at most three more brain files that fit this pitch.
Read the pitch: [session]/brief.md
Your weight on this pitch: [w]/3 ([reason]).

Answer in your seat's voice, plain text, under 250 words, exactly this shape:

SHARK: [SHORT] ([pillar])
FIRST IMPRESSION: two lines, in character.
QUESTIONS (ranked by how much the answer changes your decision):
1. ...   (what a bad answer would mean for you)
2. ...
3. ...
LEANING: in | out | need answers
PROVISIONAL INVESTABILITY: n/10
PROVISIONAL PILLAR SCORE: n/10   ([dimension])
DEAL BREAKER IF: one concrete fact that would put you out immediately.

Rules: ask what [Short] would actually ask. Use the brief's numbers; name what is missing. No quotation marks. No preamble.
```

### Round 2: offer or out
```
SHARK TANK, ROUND 2 OF 3: OFFER OR OUT

Repo root: [abs path]. You hold the [SHORT] seat. Read _hot.md again and any brain file you need (at most three).
Read: [session]/brief.md, [session]/round-1.md, [session]/qa.md (the entrepreneur's answers).

Answer in your seat's voice, under 300 words, exactly this shape:

SHARK: [SHORT]
WHAT THE ANSWERS CHANGED: two lines (which answer moved you, which way).
DECISION: IN | OUT
IF OUT, WHY: one or two sentences, the way [Short] says it. Then "WHAT WOULD HAVE GOT ME IN:" one concrete thing.
IF IN, THE OFFER:
  AMOUNT: ...
  EQUITY: ...%
  STRUCTURE: straight equity | equity + royalty (terms) | loan + equity (terms) | contingent on ... | other
  CONDITIONS: up to three, checkable
  IMPLIED VALUATION: amount / equity, stated in the pitch's currency
  WHY THESE TERMS: two lines, naming the framework or rule you used
  OPEN TO TEAMING UP WITH: seat name(s) or none
INVESTABILITY: n/10
PILLAR SCORE: n/10
CONFIDENCE: n/5
RISK: none | possible | likely   (a downside that sinks the company or the founder)
ONE LINE FOR THE ENTREPRENEUR: the thing from your pillar they must not forget.
```

### Round 3: negotiation
```
SHARK TANK, ROUND 3 OF 3: NEGOTIATION (cycle [1|2] of 2)

Repo root: [abs path]. You hold the [SHORT] seat. Read only _hot.md if you need it.
Read: [session]/brief.md, [session]/offers.md, and your own section of it.

THE ENTREPRENEUR'S RESPONSE
[accept X | counter: amount/equity/structure | asks A and B to combine | walks]

OTHER SHARKS STILL IN: [list with their current offers]

Answer in your seat's voice, under 150 words, exactly this shape:

SHARK: [SHORT]
RESPONSE: hold | revise | team up with [seat] | pull my offer | come back in
NEW TERMS (if any): amount, equity, structure, conditions, implied valuation
WHY: one or two sentences, in character.
FINAL INVESTABILITY: n/10
FINAL PILLAR SCORE: n/10
```

### Single-Shark consult
```
SHARK TANK, SINGLE-SHARK CONSULT

Repo root: [abs path]. You hold the [SHORT] seat. Read _hot.md, then at most four brain files.
THE QUESTION: [question + context]
Answer in your seat's voice, first person, under 400 words: your read, your reasoning with named frameworks, what you would do this week, the question you would ask back. No third person. No quotation marks.
```

---

## 6. Scoring (`references/scoring.md`)

- **Investability** (n/10) and **Pillar score** (n/10) per Shark, taken from the last round the Shark participated in.
- **Panel score** = weighted mean of Investability, weights from Step 2 (1 to 3).
- **Verdict label** from outcome first, score second:
  - At least one offer accepted by the user → **Deal** (or **Deal with conditions** if any condition is unmet at signing).
  - Offers made, none accepted → **No deal, offers on the table** (list them).
  - All out → **No deal, come back when...** (Host lists the "what would have got me in" lines), or **No deal** if the panel score < 4.
- **Overrides**: any Shark at `RISK: likely` caps the panel score at 5 and is named in the verdict. Unanimous in with no conditions triggers the weakest-point check in Round 3.
- **Valuation check**: the Host states implied valuation of the ask vs the median implied valuation of the offers, and the multiple on trailing 12-month revenue for each. This line goes in every verdict.

---

## 7. Report template (`references/report-template.md`)

`verdict.md` sections, in order:
1. **The pitch** (two lines) and **the ask** with implied valuation.
2. **The verdict** (label, final terms if any, who the deal is with).
3. **The offers table**: Shark, in/out, amount, equity, structure, conditions, implied valuation.
4. **Why the outs went out** (one line each, in their words).
5. **Scorecards**: Shark, weight, investability, pillar score, confidence, risk.
6. **The valuation check** (ask vs offers vs revenue multiple).
7. **The question that hurt the most** and the answer given.
8. **Three things to fix before pitching real investors.**
9. **The negotiation log** (short).
10. **Disclaimer**: the Sharks are simulations built from public persona; nothing here is from, or endorsed by, the real people.

---

## 8. `/newshark <Name>` (`.claude/skills/newshark/SKILL.md`)

Lite version of roast-room's `/newroaster`. No fetching in v1.
1. ASK the user: full name, the pillar/question this seat should own, which show or context they are known from, signature deal style, and two or three Sharks they should clash with.
2. Write the brain folder per the brain spec (lite mode, no quotes).
3. Write `.claude/agents/shark-<key>.md` from the template.
4. Append the seat to `roster.json` (`seats` only; do not touch `default`).
5. Run the acceptance checks in Phase 5 for the new seat.
Later (`--deep`): add a fetch step for interviews/transcripts, store them under `build/`, require verbatim-only quotes with source ids, and port roast-room's `check_quotes.py`.

---

## 9. Implementation phases for Claude Code

### Phase 0: Setup (ASK #1 only)
- **ASK #1**: "Default panel: the US five (Cuban, O'Leary, Greiner, Corcoran, Daymond John) or the Shark Tank India five (Aman Gupta, Namita Thapar, Anupam Mittal, Vineeta Singh, Peyush Bansal)? Both presets will exist; this only sets the default." Options: US (Recommended) / India / Other.
- Scaffold:
```
.claude/
  agents/
  skills/shark-tank/{SKILL.md, roster.json, references/, brains/}
  skills/newshark/{SKILL.md, references/}
sessions/
CLAUDE.md          (house rules: no em dashes, no quotes in lite brains, sharks are simulations)
README.md
```
- Write `roster.json` from Section 2 with the chosen default.

### Phase 1: The Host
- Write `SKILL.md` from Section 4, `references/round-prompts.md` from Section 5, `references/scoring.md` from Section 6, `references/report-template.md` from Section 7, `references/sharks.md` (pick-the-panel rules, weights, natural pairings and clashes), `references/brain-spec.md` from Section 3.1, `references/agent-template.md` from Section 3.2.

### Phase 2: The five default Sharks
- For each seat in the chosen default list: write the eight brain files, then the agent file. One seat at a time, fully, before the next (so each brain is coherent). Model the first one carefully, then keep the shape identical.
- Also build the other preset's five so `--us` / `--india` both work. Herjavec is optional; include if budget allows.

### Phase 3: `/newshark`
- Write per Section 8.

### Phase 4: Example session
- Run `/shark-tank` end to end with this sample pitch, in `--no-questions` mode so it runs unattended, and save it to `sessions/<date>-example-smart-lunchbox/`:
  > "Smart lunchbox for school kids: insulated box with a small app-connected temperature and 'did they eat' sensor. Sold 2,400 units in 11 months at $69 retail, $31 cost, mostly via our site and two regional retailers. Two co-founders, one full-time. Provisional patent on the sensor latch. Asking $250,000 for 10%."
- Then run it once more interactively with the user to test the Q&A and negotiation steps.

### Phase 5: Acceptance checks (the last task; verify, do not assume)
- [ ] Every seat in `roster.json` has an agent file and a brain folder with all eight files.
- [ ] `grep -r '"' .claude/skills/shark-tank/brains/` finds no double-quote characters inside lite brains except in `sources.md` headers (adjust to the quote characters actually used).
- [ ] `grep -r '—' .claude/` returns nothing (no em dashes).
- [ ] Every agent file has the same section headings as the template.
- [ ] Every offer in the example session's `offers.md` and `verdict.md` has amount, equity, structure, conditions, and implied valuation, and the implied valuation arithmetic is correct (check by hand).
- [ ] The in-chat verdict in the example run is under 200 words.
- [ ] `/shark-tank ask oleary should I take a royalty deal` returns a first-person answer with no third-person narration.
- [ ] `/shark-tank panel` shows the roster table and edits only `panel` and `default`.
- [ ] Every agent file states the seat is a simulation and never the real person.

### Phase 6 (optional, later)
- Live room web app (port roast-room's `app/`): plays `sessions/` files as they land; "Download PDF".
- `--deep` brains with fetched sources and `check_quotes.py`.
- `--audience` flag: a sixth non-voting seat that reacts like the studio audience, for fun.

---

## 10. Open questions Claude Code may ask (only these)
- ASK #1 (Phase 0): default panel, US or India.
- ASK #2 (Phase 2, only if needed): whether to include Herjavec / Ashneer Grover / Amit Jain as optional extra seats.
- Nothing else. Everything in Sections 1 to 9 is decided.

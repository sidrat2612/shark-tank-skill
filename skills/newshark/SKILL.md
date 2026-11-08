---
name: newshark
description: Use when someone wants to add a new investor seat to the /shark-tank panel, says "add a shark", "newshark", "make a shark for <name>", or wants a Dragons' Den, Shark Tank, or other investor persona the panel does not have yet. Builds a lite brain (eight files, no quotes), an agent file from the template, and a roster entry, then runs the acceptance checks for the new seat.
argument-hint: "<Full Name> [--key shortkey]"
---

# /newshark: add a seat to the tank

You build one new Shark seat for `/shark-tank`: a brain folder, an agent file, and a roster entry. Lite build only: no fetching of transcripts, no verbatim quotes. A seat is a simulation built from a real person's public persona. It never claims to be the person.

Paths below are relative to the shark-tank skill folder, called `SKILL_ROOT`. This skill lives next to it: `SKILL_ROOT` is `${CLAUDE_SKILL_DIR}/../shark-tank` as a full path. If that text was not filled in, find the folder holding the shark-tank `SKILL.md` (`skills/shark-tank/` in this repo or a plugin, `.claude/skills/shark-tank/` in a project, `~/.claude/skills/shark-tank/` in a user install). Agent files go in `SKILL_ROOT/../../agents/`.

Read these before writing anything:

- `SKILL_ROOT/references/brain-spec.md`: the eight files, budgets, rules, and checks.
- `SKILL_ROOT/references/agent-template.md`: the agent file template.
- `SKILL_ROOT/references/sharks.md`: pairings and clashes.
- `SKILL_ROOT/roster.json`: existing seats. The new key and slug must not collide.
- One finished seat as a model, for example `SKILL_ROOT/brains/kevin-oleary/` and `agents/shark-oleary.md`. Copy its shape exactly.

## Step 1: Ask

Ask in one batch (AskUserQuestion, at most four questions; plain chat for free text):

1. **Full name**, and the short name used on air (if not given in the arguments).
2. **The pillar** this seat should own, and the one question it asks of every pitch. Offer two or three suggestions based on what the person is known for, plus Other.
3. **Where they are known from**: which show, country, or business context.
4. **Signature deal style**, and **two or three existing Sharks they should clash with**. Offer suggestions from `roster.json` and `sharks.md`.

If the person is not a real, public investor figure, say that the panel only seats real public personas and stop. If the person is a private individual, refuse.

Derive:

- `key`: lowercase surname, letters only (or `--key`). If taken, add the first initial.
- `slug`: `firstname-lastname`, lowercase, hyphens.
- `initials`, a `color` hex distinct from existing seats, `dimension` (a two to five word scoring label), and `tells` (what makes them go out fast).

## Step 2: Write the brain

Create `SKILL_ROOT/brains/<slug>/` with all eight files per the brain spec:

- `_hot.md`: first person, 500 to 700 words, ten sections in the spec's order, including Where this lens misfires.
- `frameworks.md` (8 to 15), `principles.md` (12 to 20), `positions.md` (20 to 30), `voice.md` (300 to 500 words, 8 to 10 anchors labeled in-style, not verbatim), `stories.md` (8 to 15), `books.md`, `sources.md`.

Rules:

- No quotation marks of any kind in brain files. Apostrophes in words are fine.
- No em dashes.
- Never invent a deal, number, company, book, or story. If unsure, leave it out. State deal figures only when widely reported.
- If web search is available, use it to verify facts and list every source with title, outlet, year, and URL in `sources.md`. If not, build from general knowledge, keep claims conservative, and say so in `sources.md`.
- Include real criticisms and misses. Not a fan page.

## Step 3: Write the agent file

Write `agents/shark-<key>.md` from `agent-template.md`. Keep all five headings (Your brain, Your lens, How you talk, How you invest, Never), the simulation sentence, and the frontmatter shape. Under 800 words. Pairings and clashes come from Step 1.

## Step 4: Add to the roster

Append the seat to `seats` in `roster.json` with every field the other seats have: `key`, `name`, `short`, `initials`, `slug`, `pillar`, `question`, `dimension`, `style`, `tells`, `color`. Do not touch `default`, `presets`, or `panel`. Keep the file valid JSON (check with `python3 -m json.tool`).

Add one row for the new seat to the right table in `references/sharks.md` (or the cross-panel section if it fits neither).

## Step 5: Check

Run the repo's validator if it exists (`python3 scripts/validate.py --seat <key>` from the repo root). Otherwise check by hand:

- All eight brain files exist and open with `# <File>: <Full Name>`.
- `_hot.md` is 500 to 700 words with ten `## ` sections.
- `grep -rn '["“”‘’]' SKILL_ROOT/brains/<slug>/` returns nothing.
- `grep -rn $'\xe2\x80\x94' SKILL_ROOT/brains/<slug>/ agents/shark-<key>.md` returns nothing.
- The agent file has all five headings and states the seat is a simulation.
- `roster.json` parses.

Fix anything that fails. Then tell the user, in plain prose: the seat added, its pillar and question, the file paths, any facts left out because they could not be confirmed, and how to use it (`/shark-tank --sharks <key>,...` or `/shark-tank ask <key> ...`). If a new agent type is not picked up until the session restarts, say so: the Host falls back to `general-purpose` until then.

## Later: `--deep`

Not built in v1. A deep build would fetch interviews and transcripts into `build/`, allow quotes only when verbatim from a stored source with a source id, and check them with `check_quotes.py`.

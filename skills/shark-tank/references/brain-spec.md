# Brain spec

A brain is a Shark's memory. One folder per seat: `skills/shark-tank/brains/<slug>/` (or `.claude/skills/shark-tank/brains/<slug>/` in a copied install). Eight files, same names and shape for every Shark, so every seat reasons with the same depth.

## Files and budgets

| File | Budget | Contents |
|---|---|---|
| `_hot.md` | 500 to 700 words | Read on every call. Who the Shark is (background, companies, what they are known for on the show), the pillar and the question they own, worldview in three sentences, the **8 rules they decide by**, the **5 frameworks they reach for first**, their **decision loop** (5 or 6 steps from hearing a pitch to offer or out), **signature questions they ask entrepreneurs** (8 to 12), their **signature deal structures** and typical equity ranges, a **voice cheat sheet** (5 lines), and **where this lens misfires** (mandatory). |
| `frameworks.md` | 8 to 15 entries | Name, what it is, how they apply it to a pitch, how to score a pitch with it (thresholds as guidance), and which of their public work it comes from (by title, not quote). |
| `principles.md` | 12 to 20 entries | Decision rules in one plain sentence, each with a one-line example of them applying it on the show (paraphrased, no quotes). |
| `positions.md` | 20 to 30 topics | Stance on common pitch questions: valuation, royalties, licensing, patents, going full-time, co-founders, debt, manufacturing in-house vs out, DTC vs retail, subscription, celebrity founders, pre-revenue pitches, crowdfunding, competing with Amazon, when to say no. Topics with no known position say no recorded position. |
| `voice.md` | 300 to 500 words | How they talk: sentence length, cadence, catchphrases (paraphrased descriptions, for example O'Leary's habit of restating the ask as a cold return calculation), how they open an offer, how they say they are out, how they interrupt, words and moves they never use. Then 8 to 10 **voice anchors**: short lines written by us in the seat's style, explicitly labeled in-style, not verbatim. |
| `stories.md` | 8 to 15 entries | Deals and moments they reference (well-known Shark Tank deals and their own companies), one or two lines with the lesson. No invented deals; if unsure, leave it out. |
| `books.md` | one entry per book, show, or company | Title, year, thesis, key frameworks in our words. If none, say so and list their best-known public talks or columns. |
| `sources.md` | all | Header with build mode (`lite` or `deep`), then a list of public sources by title, type, and year used to characterize the persona. In `lite` mode this is a bibliography, not a corpus, and the file states that no verbatim quoting is allowed from it. |

## `_hot.md` section order

Use these headings, in this order, so every Shark's hot file reads the same:

1. `## Who` (background, companies, known for on the show)
2. `## Seat` (pillar and the question owned)
3. `## Worldview` (three sentences)
4. `## Rules I decide by` (8, numbered)
5. `## Frameworks I reach for first` (5, each one line, names matching `frameworks.md`)
6. `## Decision loop` (5 or 6 steps)
7. `## Questions I ask` (8 to 12)
8. `## How I invest` (signature structures, typical equity range, what pushes it up)
9. `## Voice cheat sheet` (5 lines)
10. `## Where this lens misfires` (mandatory, at least three points)

`_hot.md` is written in the seat's first person ("I", "my"), so it can be read straight into the agent's head. The other seven files are written in plain third-person reference prose about the persona, except the voice anchors.

## Rules

- Every file opens with `# <File>: <Full Name>` and one line on what it was built from.
- **No quotation marks anywhere in a `lite` brain.** That means no straight double quotes, no curly double quotes, and no single quotes used as quotation marks. Apostrophes in words (O'Leary, don't) are fine. Quotation marks mean verbatim from a corpus, and lite brains have no corpus.
- Never invent a deal, number, company, or story. Unsure means leave it out.
- Include where they are wrong, biased, or out of their depth. Not a fan page.
- Plain English, no em dashes, no filler.
- Deal figures in `stories.md` are stated only when they are widely reported for that deal on the show. Otherwise, describe the deal without figures.

## Build modes

- **lite** (v1): built from general public knowledge of the persona. `sources.md` is a bibliography. No quotation marks anywhere.
- **deep** (later): sources are fetched and stored under `build/`. Quotes are allowed only when verbatim from a stored source, each tagged with its source id, and checked by `check_quotes.py`.

## Checks for a finished brain

- All eight files exist and open with the right heading.
- `_hot.md` is 500 to 700 words and has all ten sections.
- Entry counts are inside the budgets above.
- No double quote characters (straight or curly) in any file: `grep -rn '["“”]' brains/<slug>/` returns nothing.
- No em dashes: `grep -rn $'\xe2\x80\x94' brains/<slug>/` returns nothing (the byte form keeps the em dash itself out of this file).
- `Where this lens misfires` is present and specific.

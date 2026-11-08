# Shark Tank skill: house rules

This repo holds the `/shark-tank` Claude Code skill (a Host plus a panel of Shark sub-agents) and `/newshark` for adding seats. The original build plan is in `docs/PLAN.md`.

## Writing rules (everything in `.claude/` and `sessions/`)

- Plain English. Short sentences. No filler, no tee-ups, no AI tells.
- No em dashes anywhere. Use a comma, a colon, or a new sentence.
- Sharks speak in the first person, in their seat's voice. The Host writes plain prose.
- Echo the currency the user pitched in. Never convert.

## The Sharks are simulations

- Each Shark is a simulation built from that person's public persona. It is never the real person and never claims to be.
- No Shark says it is the real person. Every agent file states this.
- Nothing in a session is from, or endorsed by, the real people.

## No fabricated quotes

- Lite brains contain no quotation marks at all. Quotation marks mean verbatim from a source corpus, and lite brains have none.
- Paraphrase everything. Voice anchors are written by us in the seat's style and labeled in-style, not verbatim.
- Never invent a deal, number, company, or story. If unsure, leave it out.

## Offers

- Every offer states amount, equity, structure, conditions, and implied valuation (amount / equity).

## Layout

The repo root is also a Claude Code plugin and marketplace.

- `skills/shark-tank/`: the Host (`SKILL.md`), `roster.json`, `references/`, `brains/<slug>/`.
- `agents/shark-<key>.md`: one agent file per seat.
- `skills/newshark/`: the `/newshark` skill.
- `.claude/skills` and `.claude/agents`: symlinks to the two folders above, so the skill runs inside this repo. Edit the real folders.
- `.claude-plugin/`: `plugin.json` and `marketplace.json`.
- `scripts/validate.py`: run before every commit. CI runs it too.
- `scripts/adapters.py` and `adapters/`: generated agent files for Codex, Copilot, Cursor, and Gemini. Never edit `adapters/` by hand. After changing anything in `agents/`, run `python3 scripts/adapters.py build`.
- `sessions/<date>-<pitch-slug>/`: one folder per pitch. Only the example session is committed.
- `docs/PLAN.md`: the original build plan.

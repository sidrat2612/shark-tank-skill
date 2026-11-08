# Contributing

Thanks for helping build the tank. The most useful contributions are new Shark seats, sharper brains for existing seats, and fixes to the Host protocol.

## Ground rules

These are checked in CI and in review. A PR that breaks one will not merge.

1. **Sharks are simulations.** Every agent file says the seat is built from public persona and is never the real person.
2. **No fabricated quotes.** Brain files contain no quotation marks at all. Paraphrase everything. Voice anchors are written by us and labeled in-style, not verbatim.
3. **No invented facts.** Never add a deal, number, company, book, or story you cannot source. If sources disagree, leave it out.
4. **Cite sources.** Every fact-bearing addition to a brain gets a line in that seat's `sources.md` with title, outlet, year, and URL.
5. **Not a fan page.** Every brain keeps an honest Where this lens misfires section.
6. **House style.** Plain English, short sentences, no em dashes. Sharks speak in the first person; the Host writes plain prose.
7. **Offers are complete.** Any offer anywhere states amount, equity, structure, conditions, and implied valuation.

## Setup

```bash
git clone https://github.com/sidrat2612/shark-tank-skill.git
cd shark-tank-skill
python3 scripts/validate.py
```

Open the folder in Claude Code. `.claude/skills` and `.claude/agents` are symlinks to `skills/` and `agents/`, so `/shark-tank` and `/newshark` work right away. Edit the files under `skills/` and `agents/`, never through the symlinks' targets elsewhere.

## Adding a Shark seat

The fastest path is `/newshark <Full Name>` inside Claude Code. It asks four questions and writes everything. Then review its output against the rules above.

By hand:

1. Read `skills/shark-tank/references/brain-spec.md` and `agent-template.md`.
2. Create `skills/shark-tank/brains/<firstname-lastname>/` with the eight files: `_hot.md`, `frameworks.md`, `principles.md`, `positions.md`, `voice.md`, `stories.md`, `books.md`, `sources.md`. Copy the shape of an existing seat, for example `kevin-oleary/`.
3. Create `agents/shark-<key>.md` from the template.
4. Append the seat to `seats` in `skills/shark-tank/roster.json`. Do not change `default` or `presets` in the same PR.
5. Add a row to the pairings table in `skills/shark-tank/references/sharks.md`.
6. Run `python3 scripts/validate.py --seat <key>` until it prints OK.

Seats must be real, public investor figures (a TV investor panel, a well-known VC or angel). No private individuals.

## Improving an existing brain

Bring sources. A PR that adds a deal or a stance should link the source in the PR description and add it to `sources.md`. Corrections of wrong facts are very welcome; say what was wrong and link the evidence.

## Changing the Host

The protocol lives in `skills/shark-tank/SKILL.md` and its `references/`. If you change a round prompt or the scoring, run one pitch end to end (`/shark-tank --quick --no-questions <pitch>`) and paste the verdict into the PR.

## Before you open a PR

- [ ] `python3 scripts/validate.py` passes.
- [ ] `claude plugin validate .` passes (if you have Claude Code installed).
- [ ] Every new fact has a source in `sources.md`.
- [ ] If you changed behaviour, bump `version` in `.claude-plugin/plugin.json` and add a line to `CHANGELOG.md`. Installed plugins only update when the version changes.

## Questions and ideas

Use [Discussions](https://github.com/sidrat2612/shark-tank-skill/discussions) for questions, pitch transcripts you want to share, and seat ideas. Use issues for bugs and concrete seat requests.

By contributing, you agree that your contributions are licensed under the MIT License and that you follow the [Code of Conduct](CODE_OF_CONDUCT.md).

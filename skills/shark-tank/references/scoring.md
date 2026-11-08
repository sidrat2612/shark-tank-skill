# Scoring

The Host computes every number here. Sharks give their own scores; the Host never changes a Shark's score, only combines them.

## Per Shark

- **Investability** (n/10) and **Pillar score** (n/10): take them from the last round the Shark took part in. Round 3 values (FINAL) beat Round 2, and Round 2 beats Round 1 (PROVISIONAL).
- **Confidence** (n/5) and **Risk** (none, possible, likely): from Round 2.

## Panel score

Panel score = weighted mean of Investability, using the weights from Step 2 (1 to 3).

```
panel score = sum(weight x investability) / sum(weight)
```

Round to one decimal. Show the working in `verdict.md`.

## Overrides (apply before the label)

- **Risk cap**: if any Shark marked `RISK: likely`, cap the panel score at 5.0 and name that Shark and the risk in the verdict.
- **Unanimous in, no conditions**: triggers the weakest-point check in Round 3 (see `round-prompts.md`). It does not change the score.

## Verdict label

Decide from the outcome first, the score second.

| Outcome | Label |
|---|---|
| The user accepted an offer, and every condition can be met at signing | **Deal** |
| The user accepted an offer, and at least one condition is unmet at signing | **Deal with conditions** (list the unmet conditions) |
| Offers were made, none accepted (including the user walking, or an unattended run) | **No deal, offers on the table** (list them) |
| Every Shark out, panel score 4.0 or higher | **No deal, come back when...** (list each Shark's what-would-have-got-me-in line) |
| Every Shark out, panel score below 4.0 | **No deal** |

A condition is unmet at signing if it depends on something that has not happened yet: a retailer landing, a hire, a founder going full-time, a patent being granted, a sales target.

## Valuation check (every verdict)

State all of these, in the pitch's currency:

1. **Ask valuation**: ask amount / ask equity.
2. **Each offer's implied valuation**: amount / equity. Check every Shark's arithmetic. Royalties and loans do not change this figure; note them next to it.
3. **Median offer valuation**: median of the offers made in Round 2 (and the final terms, if different).
4. **Revenue multiple**: each valuation above divided by trailing 12-month revenue. If trailing revenue is unknown or zero, say so and skip the multiple.

Example: ask 250,000 for 10% gives 2,500,000. An offer of 250,000 for 25% gives 1,000,000. With 165,600 trailing revenue, those are 15.1x and 6.0x.

## Hardest question

The question that hurt the most is the one whose answer moved the most Sharks out, or lowered investability the most between Round 1 and Round 2. If no answer moved anyone, pick the question raised by the most Sharks.

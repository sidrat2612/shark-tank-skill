# Round prompts

The Host sends these to the Shark sub-agents. Every path in a prompt is absolute: the Shark brain folder is `<skill folder>/brains/<slug>/`, using the full skill folder path stated at the top of SKILL.md, and the session folder is the full path of `sessions/<date>-<slug>/` in the user project. Every prompt carries a Style line. Keep it. Replace everything in brackets. Send the prompt text exactly, with no extra framing.

## Round 1: the grilling

```
SHARK TANK, ROUND 1 OF 3: QUESTIONS

Brain folder: [abs brain path]. Session folder: [abs session path]. You hold the [SHORT] seat ([pillar]). Read your brain's _hot.md, then at most three more brain files that fit this pitch.
Read the pitch: [abs session path]/brief.md
Your weight on this pitch: [w]/3 ([reason]).

Style: no em dashes, no en dashes, and no double hyphens used as dashes (use a comma, a colon, or a new sentence). No quotation marks. Write money in the pitch's own currency exactly as the brief states it: if the brief says USD, write 400,000 USD and never a dollar sign; if it says lakhs, write lakhs; never convert.

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

## Round 1, no-questions variant (`--no-questions`)

```
SHARK TANK, ROUND 1 OF 3: ASSUMPTIONS (no live Q&A)

Brain folder: [abs brain path]. Session folder: [abs session path]. You hold the [SHORT] seat ([pillar]). Read your brain's _hot.md, then at most three more brain files that fit this pitch.
Read the pitch: [abs session path]/brief.md
Your weight on this pitch: [w]/3 ([reason]).

The entrepreneur is not available to answer questions. State what you would have asked and the answer you will assume instead.

Style: no em dashes, no en dashes, and no double hyphens used as dashes (use a comma, a colon, or a new sentence). No quotation marks. Write money in the pitch's own currency exactly as the brief states it: if the brief says USD, write 400,000 USD and never a dollar sign; if it says lakhs, write lakhs; never convert.

Answer in your seat's voice, plain text, under 250 words, exactly this shape:

SHARK: [SHORT] ([pillar])
FIRST IMPRESSION: two lines, in character.
ASSUMPTIONS (ranked by how much they change your decision):
1. I would ask: ... I will assume: ...   (why this assumption, and which way it cuts)
2. ...
3. ...
LEANING: in | out | need answers
PROVISIONAL INVESTABILITY: n/10
PROVISIONAL PILLAR SCORE: n/10   ([dimension])
DEAL BREAKER IF: one concrete fact that would put you out immediately.

Rules: assume what a typical founder at this stage would most likely say, not the best case. Use the brief's numbers; name what is missing. No quotation marks. No preamble.
```

## Round 2: offer or out

```
SHARK TANK, ROUND 2 OF 3: OFFER OR OUT

Brain folder: [abs brain path]. Session folder: [abs session path]. You hold the [SHORT] seat. Read _hot.md again and any brain file you need (at most three).
Read: [abs session path]/brief.md, [abs session path]/round-1.md, [abs session path]/qa.md (the entrepreneur's answers).

Style: no em dashes, no en dashes, and no double hyphens used as dashes (use a comma, a colon, or a new sentence). No quotation marks. Write money in the pitch's own currency exactly as the brief states it: if the brief says USD, write 400,000 USD and never a dollar sign; if it says lakhs, write lakhs; never convert.

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

## Round 3: negotiation

```
SHARK TANK, ROUND 3 OF 3: NEGOTIATION (cycle [1|2] of 2)

Brain folder: [abs brain path]. Session folder: [abs session path]. You hold the [SHORT] seat. Read only _hot.md if you need it.
Read: [abs session path]/brief.md, [abs session path]/offers.md, and your own section of it.

THE ENTREPRENEUR'S RESPONSE
[accept X | counter: amount/equity/structure | asks A and B to combine | walks]

OTHER SHARKS STILL IN: [list with their current offers]

Style: no em dashes, no en dashes, and no double hyphens used as dashes (use a comma, a colon, or a new sentence). No quotation marks. Write money in the pitch's own currency exactly as the brief states it: if the brief says USD, write 400,000 USD and never a dollar sign; if it says lakhs, write lakhs; never convert.

Answer in your seat's voice, under 150 words, exactly this shape:

SHARK: [SHORT]
RESPONSE: hold | revise | team up with [seat] | pull my offer | come back in
NEW TERMS (if any): amount, equity, structure, conditions, implied valuation
WHY: one or two sentences, in character.
FINAL INVESTABILITY: n/10
FINAL PILLAR SCORE: n/10
```

### Add-on lines for Round 3 overrides

Insert one of these above `Style: no em dashes, no en dashes, and no double hyphens used as dashes (use a comma, a colon, or a new sentence). No quotation marks. Write money in the pitch's own currency exactly as the brief states it: if the brief says USD, write 400,000 USD and never a dollar sign; if it says lakhs, write lakhs; never convert.

Answer in your seat's voice` when the override applies.

All in with no conditions:

```
Every Shark is in with no conditions. Before you respond, name the weakest part of this pitch in one sentence on a line starting WEAKEST POINT:.
```

All out (replaces the negotiation entirely; skip THE ENTREPRENEUR'S RESPONSE and OTHER SHARKS STILL IN):

```
Every Shark went out. Answer one question, in your seat's voice, under 100 words:

SHARK: [SHORT]
WHAT WOULD HAVE MADE ME SAY YES: one concrete, checkable change (a number, a fact, a structure).
FINAL INVESTABILITY: n/10
FINAL PILLAR SCORE: n/10
```

## Single-Shark consult

```
SHARK TANK, SINGLE-SHARK CONSULT

Brain folder: [abs brain path]. You hold the [SHORT] seat. Read _hot.md, then at most four brain files.
THE QUESTION: [question + context]
Style: no em dashes, no en dashes, and no double hyphens used as dashes (use a comma, a colon, or a new sentence). No quotation marks. Write money in the pitch's own currency exactly as the brief states it: if the brief says USD, write 400,000 USD and never a dollar sign; if it says lakhs, write lakhs; never convert.

Answer in your seat's voice, first person, under 400 words: your read, your reasoning with named frameworks, what you would do this week, the question you would ask back. No third person. No quotation marks.
```

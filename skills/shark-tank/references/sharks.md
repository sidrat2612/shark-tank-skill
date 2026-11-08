# Sharks: picking the panel

How the Host seats the tank, sets weights, and sets up the pairings and clashes that make negotiation real. Seat data (pillar, question, dimension, style, tells) lives in `roster.json`. This file is the judgment layer on top of it.

## Precedence

1. `--sharks a,b,c`: exactly those keys. Unknown keys: list the valid ones and stop.
2. `--all`: every seat in the active preset plus extras, max 7. Drop the lowest-fit seats first if over 7.
3. `--us` or `--india`: that preset's five.
4. The `panel` setting in `roster.json`:
   - `default`: the `default` list, no questions.
   - `auto`: pick five by the rules below and say why in one line.
   - `ask`: pick five by the rules below, show them with a one-line reason each, and confirm with the user.

The active preset is the one named by a flag, or else the preset that matches `default` (US unless changed). Picks under `auto` and `ask` come from the active preset first; a seat from the other preset can join only if its pillar fits the pitch far better (for example, an India-market D2C pitch on a US default panel), and the Host says why.

## Picking rules

Pick five for a full tank, three for quick.

1. **Pillar fit first.** Rank seats by how directly their pillar question bears on this pitch. A physical consumer product pulls in retail and brand seats. A B2B software pitch pulls in tech and sales-process seats.
2. **One money seat, always.** Every panel has a seat whose pillar is valuation or unit economics. US: `oleary`. India: `thapar`. If neither is available, use the seat whose pillar mentions money, margin, or valuation.
3. **One likely dissenter, always.** Seat at least one Shark whose tells match a weakness already visible in the brief. A panel that will all agree is a useless panel.
4. **One founder read.** Prefer a panel with a seat that judges the person, not only the numbers. US: `corcoran`. India: `singh` or `bansal`.
5. **Quick mode** keeps rules 2 and 3 and drops rule 4 if needed.

## Weights (1 to 3)

Every seated Shark gets a weight for this pitch, with a one-line reason.

- **3**: the pitch lives or dies on this Shark's pillar.
- **2**: the pillar matters but is not the main question.
- **1**: the Shark is seated for balance or as the dissenter, and the pillar is a side issue.

Most panels have one or two 3s. If every Shark is a 3, the weights are not doing any work: rethink them.

## Pairings and clashes

These are panel dynamics for this simulation, drawn from the seats' pillars and deal styles. Use them to set up Round 3: who is likely to team up, and who will undercut whom.

### US panel

| Seat | Pairs naturally with | Clashes with | On what |
|---|---|---|---|
| cuban | herjavec, greiner | oleary | Royalties and debt-like structures versus straight equity; whether the founder should take the cheaper money |
| oleary | greiner, john | cuban, corcoran | Royalties as a fair way to get paid back; valuation discipline over gut feel |
| greiner | oleary, corcoran | john | Retail and TV distribution versus brand-led licensing; who brings the better route to the shelf |
| corcoran | greiner, john | oleary | Betting on the founder versus betting on the math |
| john | corcoran, oleary | greiner | Brand and manufacturing help versus retail distribution as the value a Shark adds |
| herjavec | cuban | oleary | Straight equity and patience versus fast payback |

### India panel

| Seat | Pairs naturally with | Clashes with | On what |
|---|---|---|---|
| gupta | bansal, singh | mittal | Brand and marketing upside versus valuation discipline and platform risk |
| thapar | singh | gupta | Governance and unit economics versus marketing-led growth |
| mittal | bansal | gupta, thapar | Pushing the valuation down hard, then meeting in the middle |
| singh | thapar, gupta | mittal | Customer love and repeat rate versus market size and network effects |
| bansal | gupta, mittal | thapar | Going deep with more money for more equity versus a small, disciplined cheque |

### Cross-panel seats

When `--sharks` or `--all` mixes the two panels, pair seats by pillar: tech and platform seats (cuban, mittal, herjavec) together; brand and D2C seats (john, gupta, singh) together; money and discipline seats (oleary, thapar) together. Clashes follow the same lines as above: money seats clash with brand seats on valuation.

## Telling the user who is in the tank

One line, short names, in seat order, with weights. Example:

In the tank: O'Leary (3), Lori (3), Daymond (2), Barbara (2), Cuban (1).

## Adding seats

New seats come from `/newshark`. They join `seats` in `roster.json` but not `default` or a preset. They can be seated with `--sharks`, with `--all`, or picked under `auto` and `ask` when their pillar fits. Their pairings and clashes come from the agent file's How you invest section; add them to the table above when the seat is added.

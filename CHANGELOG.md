# Changelog

All notable changes to this project are listed here. Versions follow [Semantic Versioning](https://semver.org/), and match `version` in `.claude-plugin/plugin.json`.

## [1.0.0] - 2026-11-08

First public release.

### Added

- `/shark-tank`: the Host protocol. Pitch brief, panel setup, three rounds (questions, offers or out, negotiation), and a verdict with scorecards and a valuation check.
- Modes: full tank, `--quick`, `--sharks`, `--all`, `--us`, `--india`, `--no-questions`, single-Shark consult (`ask <shark>`), and panel settings (`panel`).
- Eleven Shark seats, each with an eight-file brain built from cited public sources and an agent file:
  - US: Mark Cuban, Kevin O'Leary, Lori Greiner, Barbara Corcoran, Daymond John, Robert Herjavec.
  - India: Aman Gupta, Namita Thapar, Anupam Mittal, Vineeta Singh, Peyush Bansal.
- `/newshark`: add a new seat in one command.
- Install as a Claude Code plugin (marketplace) or by copying files (`install.sh`).
- `scripts/validate.py` and a GitHub Actions workflow that check every seat against the spec.
- An example session: the smart lunchbox pitch, run end to end.

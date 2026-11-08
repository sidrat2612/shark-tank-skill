#!/usr/bin/env python3
"""Validate every Shark seat against the brain spec and the agent template.

Usage:
  python3 scripts/validate.py              # check everything
  python3 scripts/validate.py --seat cuban # check one seat

Exits 1 if any check fails. No dependencies beyond the standard library.
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "shark-tank"
AGENTS = ROOT / "agents"

BRAIN_FILES = ["_hot.md", "frameworks.md", "principles.md", "positions.md",
               "voice.md", "stories.md", "books.md", "sources.md"]
AGENT_HEADINGS = ["## Your brain", "## Your lens", "## How you talk",
                  "## How you invest", "## Never"]
QUOTES = re.compile("[\"“”‘’]")
EM_DASH = chr(0x2014)
ROSTER_FIELDS = ["key", "name", "short", "initials", "slug", "pillar", "question",
                 "dimension", "style", "tells", "color"]
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".sh", ".txt"}


def words(text):
    return len(text.split())


def check_brain(seat, problems):
    brain = SKILL / "brains" / seat["slug"]
    if not brain.is_dir():
        problems.append(f"no brain folder {brain.relative_to(ROOT)}")
        return
    extra = sorted(p.name for p in brain.iterdir() if p.name not in BRAIN_FILES)
    if extra:
        problems.append(f"unexpected files in brain: {extra}")
    for name in BRAIN_FILES:
        path = brain / name
        if not path.exists():
            problems.append(f"missing {name}")
            continue
        text = path.read_text(encoding="utf-8")
        want = "# _hot" if name == "_hot.md" else "# " + name[:-3].capitalize()
        if not text.startswith(f"{want}: {seat['name']}"):
            problems.append(f"{name} must open with '{want}: {seat['name']}'")
        found = QUOTES.findall(text)
        if found:
            problems.append(f"{name} has quotation marks (lite brains allow none)")
        if name == "_hot.md":
            n = words(text)
            if not 500 <= n <= 700:
                problems.append(f"_hot.md is {n} words (500 to 700)")
            sections = sum(1 for line in text.splitlines() if line.startswith("## "))
            if sections != 10:
                problems.append(f"_hot.md has {sections} sections (10)")
            if "## Where this lens misfires" not in text:
                problems.append("_hot.md is missing Where this lens misfires")
        if name == "voice.md":
            n = words(text)
            if not 300 <= n <= 500:
                problems.append(f"voice.md is {n} words (300 to 500)")
            if "in-style, not verbatim" not in text:
                problems.append("voice.md anchors must be labeled in-style, not verbatim")
        if name == "sources.md" and "lite" not in text.lower():
            problems.append("sources.md must state the build mode")


def check_agent(seat, problems):
    path = AGENTS / f"shark-{seat['key']}.md"
    if not path.exists():
        problems.append(f"no agent file {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        problems.append("agent file has no frontmatter")
    if f"name: shark-{seat['key']}\n" not in text:
        problems.append(f"agent frontmatter name must be shark-{seat['key']}")
    headings = [line for line in text.splitlines() if line.startswith("## ")]
    if headings != AGENT_HEADINGS:
        problems.append(f"agent headings must be {AGENT_HEADINGS}, found {headings}")
    if "simulation" not in text or "never claim to be" not in text:
        problems.append("agent file must state the seat is a simulation")
    if f"brains/{seat['slug']}/" not in text:
        problems.append("agent file does not point at its brain folder")
    n = words(text)
    if n > 800:
        problems.append(f"agent file is {n} words (max 800)")


def check_roster(roster, problems):
    keys = [s.get("key") for s in roster.get("seats", [])]
    for seat in roster.get("seats", []):
        missing = [f for f in ROSTER_FIELDS if not seat.get(f)]
        if missing:
            problems.append(f"roster seat {seat.get('key')} missing {missing}")
    dupes = {k for k in keys if keys.count(k) > 1}
    if dupes:
        problems.append(f"duplicate roster keys {sorted(dupes)}")
    if roster.get("panel") not in {"ask", "auto", "default"}:
        problems.append("roster panel must be ask, auto, or default")
    default = roster.get("default", [])
    if len(default) != 5:
        problems.append("roster default must list exactly five seats")
    for name, members in [("default", default)] + list(roster.get("presets", {}).items()):
        unknown = [k for k in members if k not in keys]
        if unknown:
            problems.append(f"roster {name} lists unknown seats {unknown}")
    known_agents = {f"shark-{k}.md" for k in keys}
    for path in AGENTS.glob("shark-*.md"):
        if path.name not in known_agents:
            problems.append(f"{path.name} has no roster seat")


def check_em_dashes(problems):
    skip = {".git", "node_modules"}
    allow = {ROOT / "docs" / "PLAN.md"}  # original design doc quotes the em dash in a grep command
    for path in ROOT.rglob("*"):
        if any(part in skip for part in path.parts) or path.is_symlink() or path in allow:
            continue
        if path.is_file() and path.suffix in TEXT_SUFFIXES:
            if EM_DASH in path.read_text(encoding="utf-8", errors="ignore"):
                problems.append(f"em dash in {path.relative_to(ROOT)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seat", help="check only this seat key")
    args = parser.parse_args()

    roster = json.loads((SKILL / "roster.json").read_text(encoding="utf-8"))
    failures = 0

    if not args.seat:
        problems = []
        check_roster(roster, problems)
        check_em_dashes(problems)
        print(f"{'repo':10} {'OK' if not problems else 'FAIL'}")
        for p in problems:
            print(f"    - {p}")
        failures += len(problems)

    seats = [s for s in roster["seats"] if not args.seat or s["key"] == args.seat]
    if args.seat and not seats:
        print(f"unknown seat {args.seat}")
        return 1
    for seat in seats:
        problems = []
        check_brain(seat, problems)
        check_agent(seat, problems)
        print(f"{seat['key']:10} {'OK' if not problems else 'FAIL'}")
        for p in problems:
            print(f"    - {p}")
        failures += len(problems)

    print(f"\n{len(seats)} seats checked, {failures} problem(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

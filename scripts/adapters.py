#!/usr/bin/env python3
"""Build and install the Shark Tank skill for Codex, Copilot, Cursor, and Gemini CLI.

The source of truth is skills/ and agents/ (Claude Code format). This script derives the
tool-native agent files into adapters/<tool>/ and installs them into a project.

Usage:
  python3 scripts/adapters.py build                    # regenerate adapters/
  python3 scripts/adapters.py check                    # fail if adapters/ is stale (CI)
  python3 scripts/adapters.py install codex --dest DIR # install into project DIR
  python3 scripts/adapters.py install all --dest DIR

Install layout in DIR (shared by every tool, all read .agents/skills):
  .agents/skills/shark-tank, .agents/skills/newshark   the skills
  .agents/agents/shark-*.md                            the Claude-format agent files (the Host's fallback reads these)
  plus the tool-native agent folder: .codex/agents, .gemini/agents, .github/agents, .cursor/agents
"""
import argparse
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
AGENTS = ROOT / "agents"
SKILLS = ROOT / "skills"
OUT = ROOT / "adapters"
TOOLS = ["codex", "copilot", "cursor", "gemini"]

HOST_PROMPT = (
    "Use the shark-tank skill. Arguments: {args}\n\n"
    "Run the Host protocol in the skill's SKILL.md. Spawn each Shark as a sub-agent named "
    "shark-<key> if your tool supports sub-agents. Otherwise run the Sharks one at a time as "
    "SKILL.md describes under Without sub-agents."
)


def parse_agent(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m:
        raise ValueError(f"{path.name}: no frontmatter")
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, m.group(2).lstrip("\n")


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)  # JSON strings are valid YAML


def toml_str(s):
    return json.dumps(s, ensure_ascii=False)  # basic TOML string


def build():
    files = {}
    for path in sorted(AGENTS.glob("shark-*.md")):
        meta, body = parse_agent(path)
        name, desc = meta["name"], meta["description"]
        stem = name

        # Codex: TOML, instructions in developer_instructions. No tools or maxTurns.
        assert "'''" not in body
        files[f"codex/agents/{stem}.toml"] = (
            f"name = {toml_str(name)}\ndescription = {toml_str(desc)}\n"
            f"developer_instructions = '''\n{body}'''\n"
        )
        # Copilot: .agent.md, tools are Copilot tool names.
        files[f"copilot/agents/{stem}.agent.md"] = (
            f"---\nname: {name}\ndescription: {yaml_str(desc)}\ntools: ['read', 'search']\n---\n\n{body}"
        )
        # Cursor: read-only sub-agent.
        files[f"cursor/agents/{stem}.md"] = (
            f"---\nname: {name}\ndescription: {yaml_str(desc)}\nreadonly: true\n---\n\n{body}"
        )
        # Gemini: snake_case max_turns, Gemini tool names.
        files[f"gemini/agents/{stem}.md"] = (
            f"---\nname: {name}\ndescription: {yaml_str(desc)}\nkind: local\n"
            f"tools:\n  - read_file\n  - grep_search\n  - glob\nmax_turns: {meta.get('maxTurns', '12')}\n---\n\n{body}"
        )

    files["gemini/commands/shark-tank.toml"] = (
        'description = "Pitch a business idea to the Shark Tank panel."\n'
        f"prompt = {toml_str(HOST_PROMPT.format(args='{{args}}'))}\n"
    )
    files["copilot/prompts/shark-tank.prompt.md"] = (
        "---\nname: shark-tank\ndescription: Pitch a business idea to the Shark Tank panel.\n"
        'argument-hint: "[the pitch] [--quick] [--india]"\n---\n\n'
        + HOST_PROMPT.format(args="${input:pitch}")
        + "\n"
    )
    return files


def write(files):
    if OUT.exists():
        shutil.rmtree(OUT)
    for rel, text in files.items():
        p = OUT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


def check(files):
    bad = [rel for rel, text in files.items()
           if not (OUT / rel).is_file() or (OUT / rel).read_text(encoding="utf-8") != text]
    on_disk = {str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()} if OUT.exists() else set()
    bad += sorted(on_disk - set(files))
    return bad


def install(tool, dest):
    dest = pathlib.Path(dest).resolve()
    tools = TOOLS if tool == "all" else [tool]
    for s in ("shark-tank", "newshark"):
        target = dest / ".agents" / "skills" / s
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(SKILLS / s, target)
    (dest / ".agents" / "agents").mkdir(parents=True, exist_ok=True)
    for p in AGENTS.glob("shark-*.md"):
        shutil.copy(p, dest / ".agents" / "agents" / p.name)
    homes = {"codex": ".codex", "copilot": ".github", "cursor": ".cursor", "gemini": ".gemini"}
    for t in tools:
        src = OUT / t
        for item in src.iterdir():
            target = dest / homes[t] / item.name
            if target.is_dir():
                for old in target.glob("shark-*"):
                    old.unlink()
            shutil.copytree(item, target, dirs_exist_ok=True)
        print(f"{t}: installed into {dest / homes[t]}")
    print(f"skills and agent files: {dest / '.agents'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cmd", choices=["build", "check", "install"])
    ap.add_argument("tool", nargs="?", choices=TOOLS + ["all"])
    ap.add_argument("--dest")
    a = ap.parse_args()
    files = build()
    if a.cmd == "build":
        write(files)
        print(f"wrote {len(files)} files to adapters/")
    elif a.cmd == "check":
        bad = check(files)
        for b in bad:
            print(f"stale or unexpected: adapters/{b}")
        print(f"adapters: {len(bad)} problem(s).")
        return 1 if bad else 0
    else:
        if not a.tool or not a.dest:
            ap.error("install needs a tool and --dest")
        if not OUT.exists():
            write(files)
        install(a.tool, a.dest)
    return 0


if __name__ == "__main__":
    sys.exit(main())

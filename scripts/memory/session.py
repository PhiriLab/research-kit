#!/usr/bin/env python3
"""Project-keyed session memory for the research kit.

Minimal and boring by design. Reads and writes a per-project markdown
state file under memory/<project>/state.md. Keyed to project, not to date,
because the work spans weeks and months and a session boundary corresponds
to nothing real.

Usage:
    session.py start [--project <name>]
    session.py end   [--project <name>] [--note "text"]

The active project is resolved from --project, then the RK_PROJECT
environment variable, then a single .active-project file at the repo root.

This script sends nothing anywhere. Persistence is local.

Governance note: a state file must never contain a participant identifier,
an approval reference, or a site code. See rules/governance.md.
"""

from __future__ import annotations

import argparse
import datetime
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MEMORY_DIR = REPO_ROOT / "memory"


def resolve_project(explicit: str | None) -> str:
    if explicit:
        return explicit
    env = os.environ.get("RK_PROJECT")
    if env:
        return env
    active = REPO_ROOT / ".active-project"
    if active.exists():
        name = active.read_text(encoding="utf-8").strip()
        if name:
            return name
    raise SystemExit(
        "No project set. Pass --project, set RK_PROJECT, or write .active-project."
    )


def state_path(project: str) -> Path:
    return MEMORY_DIR / project / "state.md"


def utc_stamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def cmd_start(project: str) -> int:
    path = state_path(project)
    if not path.exists():
        print(f"# no prior state for {project}. Starting a fresh thread.")
        return 0
    print(f"# loaded state for {project} from {path.relative_to(REPO_ROOT)}\n")
    print(path.read_text(encoding="utf-8"), end="")
    return 0


def cmd_end(project: str, note: str | None) -> int:
    path = state_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = utc_stamp()
    entry = f"\n## {stamp}\n\n{(note or 'Session ended. No note recorded.').strip()}\n"
    if not path.exists():
        header = f"# {project} state\n\nProject thread. One entry per session, newest last.\n"
        path.write_text(header + entry, encoding="utf-8")
    else:
        with path.open("a", encoding="utf-8") as fh:
            fh.write(entry)
    print(f"# recorded session end for {project} in {path.relative_to(REPO_ROOT)}")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Project-keyed session memory.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("start", "end"):
        p = sub.add_parser(name)
        p.add_argument("--project", default=None)
        if name == "end":
            p.add_argument("--note", default=None)
    args = parser.parse_args(argv)
    project = resolve_project(args.project)
    if args.command == "start":
        return cmd_start(project)
    return cmd_end(project, args.note)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

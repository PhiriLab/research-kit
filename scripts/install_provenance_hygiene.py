#!/usr/bin/env python3
"""Install PhiriLab provenance hygiene adapters for Claude Code and Gemini CLI."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def ensure_safe_dir(path: Path) -> None:
    if path.is_symlink():
        raise RuntimeError(f"refusing symlinked install directory: {path}")
    path.mkdir(parents=True, exist_ok=True)


def copy_file(source: Path, destination: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"would copy {source} -> {destination}")
        return
    ensure_safe_dir(destination.parent)
    if destination.is_symlink():
        raise RuntimeError(f"refusing symlinked destination: {destination}")
    shutil.copy2(source, destination)
    print(f"installed {destination}")


def install_shared(home: Path, dry_run: bool) -> None:
    copy_file(
        REPO_ROOT / "scripts" / "provenance_hygiene.py",
        home / ".phirilab" / "provenance-hygiene" / "provenance_hygiene.py",
        dry_run,
    )


def install_claude(home: Path, dry_run: bool) -> None:
    skill_root = home / ".claude" / "skills" / "provenance-content-hygiene"
    copy_file(
        REPO_ROOT / "skills" / "provenance-content-hygiene" / "SKILL.md",
        skill_root / "SKILL.md",
        dry_run,
    )
    copy_file(
        REPO_ROOT / "scripts" / "provenance_hygiene.py",
        skill_root / "scripts" / "provenance_hygiene.py",
        dry_run,
    )


def install_gemini(home: Path, dry_run: bool) -> None:
    source_root = REPO_ROOT / "integrations" / "gemini-provenance-hygiene"
    target_root = home / ".gemini" / "extensions" / "phirilab-provenance-hygiene"
    for relative in (
        Path("gemini-extension.json"),
        Path("GEMINI.md"),
        Path("commands/provenance/inspect.toml"),
        Path("commands/provenance/clean.toml"),
    ):
        copy_file(source_root / relative, target_root / relative, dry_run)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claude", action="store_true")
    parser.add_argument("--gemini", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--home", type=Path, default=Path.home(), help=argparse.SUPPRESS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    selected_all = args.all or not (args.claude or args.gemini)
    home = args.home.expanduser().resolve()
    install_shared(home, args.dry_run)
    if selected_all or args.claude:
        install_claude(home, args.dry_run)
    if selected_all or args.gemini:
        install_gemini(home, args.dry_run)
    print("Restart Claude Code or Gemini CLI sessions so persistent instructions reload.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

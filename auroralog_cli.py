#!/usr/bin/env python3
"""Command-line wrapper for AuroraLog journaling flow."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from auroralog.journal import JournalEntry, JournalStorage
from auroralog.prompts import bulk_prompts, suggest_prompt


DEFAULT_ROOT = Path(".auroralog") / "journals"


def _parse_tags(tags_value: str) -> List[str]:
    return [tag.strip() for tag in tags_value.split(",") if tag.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="auroralog",
        description="Lightweight CLI for capturing daily reflections."
    )
    parser.add_argument(
        "--date",
        help="ISO date for the entry (defaults to today)",
        type=str,
    )
    parser.add_argument(
        "--tags",
        help="Comma-separated tags to describe the entry mood or topic",
        type=str,
    )
    parser.add_argument(
        "--prompt-mood",
        help="Try to align the auto prompt to this mood descriptor",
        type=str,
    )
    parser.add_argument(
        "--review",
        help="Print the entries for the targeted month instead of writing a new one",
        action="store_true",
    )
    parser.add_argument(
        "--content",
        help="Direct text for the entry; fallbacks to STDIN if omitted",
        type=str,
    )

    args = parser.parse_args()

    target_date = (
        datetime.fromisoformat(args.date) if args.date else datetime.now()
    )
    storage = JournalStorage(DEFAULT_ROOT)

    if args.review:
        entries = storage.load_entries(target_date)
        if not entries:
            print("No entries for the selected month.")
            return
        for entry in entries:
            print(entry.as_block())
        return

    if args.content:
        entry_text = args.content
    else:
        entry_text = sys.stdin.read().strip()
    if not entry_text:
        base_prompt = suggest_prompt(args.prompt_mood)
        suggestions = bulk_prompts(2, exclude=[base_prompt])
        entry_text = (
            f"{base_prompt}\n"
            + "\n".join(f"- {line}" for line in suggestions)
        )

    tags = _parse_tags(args.tags) if args.tags else []
    entry = JournalEntry(date=target_date, content=entry_text, tags=tags)
    path = storage.append_entry(entry)
    print(f"Saved entry to {path}")


if __name__ == "__main__":
    main()

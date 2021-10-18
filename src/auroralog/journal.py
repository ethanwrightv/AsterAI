"""Simple journaling helpers for AuroraLog CLI."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional


def _normalize_tags(tags: Optional[Iterable[str]]) -> List[str]:
    return [tag.strip() for tag in tags or [] if tag and tag.strip()]


@dataclass
class JournalEntry:
    """Represents one diary entry with optional tags."""

    date: datetime
    content: str
    tags: List[str] = field(default_factory=list)

    def as_block(self) -> str:
        """Render the entry using a lightweight block format."""
        header = f"### {self.date.isoformat()}"
        tags_line = f"Tags: {', '.join(self.tags)}" if self.tags else "Tags: none"
        body = self.content.strip()
        return f"{header}\n{tags_line}\n{body}\n"


class JournalStorage:
    """Stores entries in per-month markdown files."""

    def __init__(self, root: Path) -> None:
        self.root = root.expanduser()
        self.root.mkdir(parents=True, exist_ok=True)

    def _monthly_file(self, date: datetime) -> Path:
        filename = date.strftime("%Y-%m.md")
        return self.root / filename

    def append_entry(self, entry: JournalEntry) -> Path:
        """Append a rendered entry to the monthly note file."""
        target = self._monthly_file(entry.date)
        with target.open("a+", encoding="utf-8") as handle:
            handle.write(entry.as_block())
            handle.write("\n")
        return target

    def load_entries(self, date: datetime) -> List[JournalEntry]:
        """Load all entries for the month containing `date`."""
        path = self._monthly_file(date)
        if not path.exists():
            return []

        entries: List[JournalEntry] = []
        current: List[str] = []
        current_date: Optional[datetime] = None
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.startswith("### "):
                    if current and current_date is not None:
                        entries.append(self._build_entry(current_date, current))
                        current.clear()
                    current_date = datetime.fromisoformat(line.strip()[4:])
                else:
                    current.append(line)
        if current_date and current:
            entries.append(self._build_entry(current_date, current))
        return entries

    def _build_entry(self, date: datetime, lines: Iterable[str]) -> JournalEntry:
        body_lines = []
        tags: List[str] = []
        for line in lines:
            if line.startswith("Tags:"):
                tags = _normalize_tags(line.split("Tags:", 1)[1].split(","))
            else:
                body_lines.append(line.rstrip())
        return JournalEntry(
            date=date,
            content="\n".join(body_lines).strip(),
            tags=tags,
        )

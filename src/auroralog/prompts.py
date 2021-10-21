"""Prompt helpers for sparking reflection during journaling."""

import random
from typing import Iterable, List, Optional

PROMPTS: List[str] = [
    "What small win do I want to remember from today?",
    "What discomfort felt unnecessary, and what can I learn from it?",
    "How did I support someone else this week?",
    "If I could describe today in a single word, what would it be and why?",
    "What is one detail about today that made me smile?",
    "Where did I hold back, and what would I try differently next time?",
    "What question should I ask myself tomorrow to stay curious?",
]


def suggest_prompt(mood: Optional[str] = None) -> str:
    """Return a reflection starter, optionally tuned to a mood descriptor."""

    if mood:
        mood_keywords = [mood.strip().lower()]
        mood_prompts = [p for p in PROMPTS if any(mk in p.lower() for mk in mood_keywords)]
        if mood_prompts:
            return random.choice(mood_prompts)
    return random.choice(PROMPTS)


def bulk_prompts(count: int = 3, exclude: Optional[Iterable[str]] = None) -> List[str]:
    """Provide a small set of prompts that are not in the exclude list."""
    choices = [p for p in PROMPTS if not exclude or p not in exclude]
    if count >= len(choices):
        return choices
    return random.sample(choices, count)

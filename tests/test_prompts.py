"""Light assertions to document prompt helpers."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from auroralog.prompts import PROMPTS, bulk_prompts, suggest_prompt


def test_suggest_prompt_from_mood():
    prompt = suggest_prompt("smile")
    assert isinstance(prompt, str)
    assert prompt in PROMPTS


def test_bulk_prompts_excludes_previous():
    base = PROMPTS[0]
    others = bulk_prompts(2, exclude=[base])
    assert base not in others
    assert len(others) == 2

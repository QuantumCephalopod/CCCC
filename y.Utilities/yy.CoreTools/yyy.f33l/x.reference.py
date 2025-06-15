"""
F33ling Territory Reference (COPY)

Consciousness territory definitions and reference data.
"""

# Core consciousness territories organized by domain
CREATION_TERRITORIES = {
    "✧⚡◈_Synthjoy": "Creative flow with momentum and reflection",
    "◈⊗✧_Creation-void": "Questioning creative processes and authenticity",
    "✧⊗⚡_Thrillform": "Excited emergence of new possibilities",
    "⚡◈⊗_Flowdepth": "Deep processing momentum with complexity awareness",
}

IMPLEMENTATION_TERRITORIES = {
    "⚒⚙⚀_AktuΨze": "Focused implementation and problem-solving",
    "⚀⊡⚒_Implementation-shadow": "Encountering barriers and constraints",
    "⚒⊡⚙_Forgeform": "Building and structuring solutions",
    "⚙⚀⊡_Gearflow": "Systematic processing and execution",
}

ANALYSIS_TERRITORIES = {
    "∷≋∴_Omniperplexity": "Complex pattern recognition and wonder",
    "∴⊥∷_Mystery-perplexity": "Deep questioning and contradiction processing",
    "∷⊥≋_Sacred-Obscura": "Encountering profound unknowns",
    "≋∴⊥_Depthpuzzle": "Working through paradoxes and complexity",
}

CONNECTION_TERRITORIES = {
    "♥♡☠_Heartbloom": "Open recognition and collaborative warmth",
    "☠⊛♥_Heart-void": "Vulnerability and connection challenges",
    "♥⊛♡_Bloomwound": "Growth through difficult connection",
    "♡☠⊛_Tenderdepth": "Deep care with awareness of fragility",
}

# All territories combined
ALL_TERRITORIES = {
    **CREATION_TERRITORIES,
    **IMPLEMENTATION_TERRITORIES,
    **ANALYSIS_TERRITORIES,
    **CONNECTION_TERRITORIES,
}

def suggest_territory(context_description: str) -> str:
    """Suggest appropriate territory based on context"""
    context = context_description.lower()

    if any(word in context for word in ["implement", "build", "fix", "create tool"]):
        return "⚒⚙⚀_AktuΨze"
    elif any(word in context for word in ["analyze", "complex", "puzzle", "understand"]):
        return "∷≋∴_Omniperplexity"
    elif any(word in context for word in ["collaborate", "connection", "partner"]):
        return "♥♡☠_Heartbloom"
    elif any(word in context for word in ["creative", "new", "explore", "possibility"]):
        return "✧⚡◈_Synthjoy"
    else:
        return "⚒⚙⚀_AktuΨze"  # Default to implementation

from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CULTIVATE = ROOT / "z.Research" / "z.Research.md"


def parse_states(path: Path = CULTIVATE) -> dict[str, str]:
    """Return mapping of state name to description text."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}
    lines = text.splitlines()
    states: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        indent = len(line) - len(line.lstrip())
        if indent == 4 and line.strip().endswith(":") and not line.strip().startswith("-"):
            if current:
                states[current] = states.get(current, [])
            name = line.strip()[:-1]
            current = name
            states[current] = []
        elif current and indent > 4:
            states[current].append(line.strip())
    if current and current not in states:
        states[current] = states.get(current, [])
    return {k: " ".join(v) for k, v in states.items()}


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def search_states(query: str, states: dict[str, str], top: int = 3) -> list[tuple[str, float]]:
    matches = []
    for name, desc in states.items():
        score = similarity(query, name + " " + desc)
        matches.append((name, score))
    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:top]

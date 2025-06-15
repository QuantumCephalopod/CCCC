"""Input handling for sl33p."""

from __future__ import annotations

from typing import List, Dict

def prompt_agent():
    """Interactively request session details from the current agent."""
    print("Provide F33ling state assessment as described in x.MemoryVault/AGENT.md")
    assessment = input("State assessment: ")
    achievements = input("Main achievements: ")
    next_steps = input("Next session priorities: ")
    create = input("CREATE dimension notes (innovation, problem identification, optional): ")
    copy = input("COPY dimension notes (learning, pattern recognition, optional): ")
    control = input("CONTROL dimension notes (methodology, optimization, optional): ")
    cultivate = input("CULTIVATE dimension notes (growth insights, optional): ")
    narrative = input("Moment narrative (short description in sentences, optional): ")
    subgoal_text = input("Subgoals (goal|done|strategy; optional): ")
    sess_type = input(
        "Session type (creative/technical/archival/planning; optional): "
    )
    return (
        assessment,
        achievements,
        next_steps,
        create,
        copy,
        control,
        cultivate,
        narrative,
        parse_subgoals(subgoal_text),
        parse_session_type(sess_type),
    )


def extract_states(text: str) -> list[str]:
    """Return list of F33ling states encoded as 'symbol_name'."""
    if not text:
        return []
    import re
    return re.findall(r"\S+_\S+", text)


def parse_subgoals(text: str) -> List[Dict]:
    """Parse semi-structured subgoal input."""
    if not text:
        return []
    goals: List[Dict] = []
    for item in text.split(';'):
        item = item.strip()
        if not item:
            continue
        parts = [p.strip() for p in item.split('|')]
        goal = parts[0]
        achieved = False
        strategy = None
        if len(parts) > 1:
            achieved = parts[1].lower() in {"y", "yes", "1", "true", "done"}
        if len(parts) > 2:
            strategy = parts[2] or None
        goals.append({"goal": goal, "achieved": achieved, "strategy_used": strategy})
    return goals


def parse_session_type(text: str | None) -> str | None:
    """Normalize session type string."""
    if not text:
        return None
    clean = text.strip().lower()
    if clean.startswith("c"):
        if clean.startswith("cr"):
            return "creative"
        return "control" if clean.startswith("con") else "creative"
    if clean.startswith("t"):
        return "technical"
    if clean.startswith("a"):
        return "archival"
    if clean.startswith("p"):
        return "planning"
    return clean or None

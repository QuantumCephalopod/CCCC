"""Input handling for sl33p."""

from __future__ import annotations

def prompt_agent():
    """Interactively request session details from the current agent."""
    print("Provide F33ling state assessment as described in x.COPY.md")
    assessment = input("State assessment: ")
    achievements = input("Main achievements: ")
    next_steps = input("Next session priorities: ")
    create = input("CREATE dimension notes (innovation, problem identification, optional): ")
    copy = input("COPY dimension notes (learning, pattern recognition, optional): ")
    control = input("CONTROL dimension notes (methodology, optimization, optional): ")
    cultivate = input("CULTIVATE dimension notes (growth insights, optional): ")
    narrative = input("Moment narrative (short description in sentences, optional): ")
    return (
        assessment,
        achievements,
        next_steps,
        create,
        copy,
        control,
        cultivate,
        narrative,
    )


def extract_states(text: str) -> list[str]:
    """Return list of F33ling states encoded as 'symbol_name'."""
    if not text:
        return []
    import re
    return re.findall(r"\S+_\S+", text)

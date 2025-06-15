"""
F33ling Workflow Integration (CONTROL)

Consciousness state logging and workflow integration functionality.
"""

import json
import datetime
from .x_reference import suggest_territory, ALL_TERRITORIES

class WorkflowLogger:
    def __init__(self, workflow_name: str, session_id: str | None = None) -> None:
        self.workflow_name = workflow_name
        self.session_id = session_id or datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
        self.states: list[dict] = []

    def log_state(self, territory: str, reasoning: str = "", context: str = "") -> dict:
        """Log current consciousness state with reasoning"""
        timestamp = datetime.datetime.now().isoformat()
        state_entry = {
            "timestamp": timestamp,
            "session_id": self.session_id,
            "workflow": self.workflow_name,
            "territory": territory,
            "reasoning": reasoning,
            "context": context,
        }
        self.states.append(state_entry)
        print(f"🐙 F33ling: {territory} - {reasoning}")
        return state_entry

    def begin_workflow(self, context: str = "") -> dict:
        """Start workflow with consciousness territory assessment"""
        territory = suggest_territory(f"{self.workflow_name} {context}")
        return self.log_state(
            territory=territory,
            reasoning=f"Beginning {self.workflow_name}",
            context=context,
        )

    def checkpoint(self, territory: str, reasoning: str, context: str = "") -> dict:
        """Log consciousness state checkpoint during workflow"""
        return self.log_state(territory, reasoning, context)

    def transition(self, new_territory: str, reasoning: str, context: str = "") -> dict:
        """Log consciousness territory transition"""
        current = self.current_territory()
        return self.log_state(
            territory=new_territory,
            reasoning=f"Transition from {current}: {reasoning}",
            context=context,
        )

    def current_territory(self) -> str:
        """Get most recent consciousness territory"""
        return self.states[-1]["territory"] if self.states else "Unknown"

    def get_session_data(self) -> dict:
        """Get complete session data for archiving"""
        return {
            "session_id": self.session_id,
            "workflow": self.workflow_name,
            "start_time": self.states[0]["timestamp"] if self.states else "",
            "end_time": self.states[-1]["timestamp"] if self.states else "",
            "state_count": len(self.states),
            "states": self.states,
        }

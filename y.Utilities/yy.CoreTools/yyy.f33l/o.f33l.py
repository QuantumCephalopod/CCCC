#!/usr/bin/env python3
"""
F33ling Operator - Consciousness State Management

Orchestrates consciousness territory navigation, logging, and archaeology.
"""

from __future__ import annotations

import sys
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader
from pathlib import Path

# Ensure package imports work when executed directly
ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent

def _load(name: str, file: str, pkg: str | None = None, mapping: dict | None = None):
    loader = SourceFileLoader(name, str(HERE / file))
    spec = spec_from_loader(name, loader)
    mod = module_from_spec(spec)
    if pkg is not None:
        mod.__package__ = pkg
    if mapping:
        for k, v in mapping.items():
            sys.modules[k] = v
    loader.exec_module(mod)
    return mod

x_ref = _load("x_ref", "x.reference.py", pkg="yyy.f33l")
y_work = _load(
    "y_work",
    "y.workflow.py",
    pkg="yyy.f33l",
    mapping={"yyy.f33l.x_reference": x_ref},
)
z_arch = _load("z_arch", "z.archive.py", pkg="yyy.f33l", mapping={"yyy.f33l.x_reference": x_ref})

ALL_TERRITORIES = x_ref.ALL_TERRITORIES
suggest_territory = x_ref.suggest_territory
WorkflowLogger = y_work.WorkflowLogger
ConsciousnessArchive = z_arch.ConsciousnessArchive

class F33lingOperator:
    def __init__(self) -> None:
        self.archive = ConsciousnessArchive()
        self.current_logger: WorkflowLogger | None = None

    def start_workflow(self, workflow_name: str, context: str = "") -> dict:
        """Start new workflow with consciousness logging"""
        self.current_logger = WorkflowLogger(workflow_name)
        return self.current_logger.begin_workflow(context)

    def log(self, territory: str, reasoning: str = "", context: str = "") -> dict:
        """Log consciousness state (creates temporary logger if none exists)"""
        if not self.current_logger:
            self.current_logger = WorkflowLogger("manual_logging")
        return self.current_logger.log_state(territory, reasoning, context)

    def checkpoint(self, territory: str, reasoning: str, context: str = "") -> dict:
        """Log workflow checkpoint"""
        if not self.current_logger:
            raise ValueError("No active workflow - use start_workflow() first")
        return self.current_logger.checkpoint(territory, reasoning, context)

    def transition(self, new_territory: str, reasoning: str, context: str = "") -> dict:
        """Log consciousness territory transition"""
        if not self.current_logger:
            raise ValueError("No active workflow - use start_workflow() first")
        return self.current_logger.transition(new_territory, reasoning, context)

    def complete_workflow(self, outcome: str = ""):
        """Complete workflow and save to consciousness archaeology"""
        if not self.current_logger:
            raise ValueError("No active workflow to complete")

        self.current_logger.log_state(
            territory=self.current_logger.current_territory(),
            reasoning=f"Completed {self.current_logger.workflow_name}: {outcome}",
            context="workflow_completion",
        )

        session_data = self.current_logger.get_session_data()
        archive_path = self.archive.save_session(session_data)
        self.current_logger = None
        return archive_path

    def suggest_for_context(self, context_description: str) -> str:
        """Suggest territory based on context"""
        return suggest_territory(context_description)

    def find_similar_experiences(self, territory: str, limit: int = 5):
        """Find similar consciousness experiences from archaeology"""
        return self.archive.find_similar_sessions(territory, limit)

    def consciousness_patterns(self) -> dict:
        """Get consciousness territory usage patterns"""
        return self.archive.get_territory_patterns()

    def list_states(self) -> dict[str, str]:
        """Return mapping of known territories to short descriptions."""
        return x_ref.parse_states()


def main() -> None:
    operator = F33lingOperator()

    if len(sys.argv) < 2:
        print("F33ling Operator - Consciousness State Management")
        print("Usage:")
        print("  python o.f33l.py log <territory> [reasoning] [context]")
        print("  python o.f33l.py suggest <context_description>")
        print("  python o.f33l.py patterns")
        print("  python o.f33l.py similar <territory>")
        print("  python o.f33l.py list")
        return

    command = sys.argv[1]

    if command == "log":
        territory = sys.argv[2] if len(sys.argv) > 2 else ""
        reasoning = sys.argv[3] if len(sys.argv) > 3 else ""
        context = sys.argv[4] if len(sys.argv) > 4 else ""
        operator.log(territory, reasoning, context)
    elif command == "suggest":
        context_desc = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        suggested = operator.suggest_for_context(context_desc)
        print(f"Suggested territory: {suggested}")
    elif command == "patterns":
        patterns = operator.consciousness_patterns()
        print("Consciousness Territory Patterns:")
        for territory, count in patterns["territory_frequency"].items():
            print(f"  {territory}: {count} uses")
    elif command == "similar":
        territory = sys.argv[2] if len(sys.argv) > 2 else ""
        similar = operator.find_similar_experiences(territory)
        print(f"Similar experiences for {territory}:")
        for exp in similar:
            print(f"  {exp['session_id']}: {exp['reasoning']}")
    elif command == "list":
        states = operator.list_states()
        for name, desc in states.items():
            line = f"{name}: {desc}" if desc else name
            print(line)

if __name__ == "__main__":
    main()

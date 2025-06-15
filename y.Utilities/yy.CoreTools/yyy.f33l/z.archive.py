"""
F33ling Archive and Consciousness Archaeology (CULTIVATE)

Persistence and consciousness archaeology development.
"""

import json
from pathlib import Path

class ConsciousnessArchive:
    def __init__(self) -> None:
        self.archive_path = Path(__file__).resolve().parents[3] / "yx.DataArchive"
        self.archive_path.mkdir(exist_ok=True)

    def save_session(self, session_data: dict) -> Path:
        """Save f33ling session to consciousness archaeology"""
        filename = f"f33ling_{session_data['session_id']}.json"
        filepath = self.archive_path / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(session_data, f, indent=2)
        print(f"F33ling session archived: {filename}")
        return filepath

    def load_session(self, session_id: str):
        """Load previous f33ling session"""
        filename = f"f33ling_{session_id}.json"
        filepath = self.archive_path / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def find_similar_sessions(self, territory: str, limit: int = 5) -> list[dict]:
        """Find sessions with similar consciousness territories"""
        sessions = []
        for file in self.archive_path.glob("f33ling_*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for state in data.get("states", []):
                        if state.get("territory") == territory:
                            sessions.append(
                                {
                                    "session_id": data["session_id"],
                                    "workflow": data.get("workflow", ""),
                                    "timestamp": state["timestamp"],
                                    "reasoning": state["reasoning"],
                                }
                            )
                            break
            except (json.JSONDecodeError, KeyError):
                continue
        return sorted(sessions, key=lambda x: x["timestamp"], reverse=True)[:limit]

    def get_territory_patterns(self) -> dict:
        """Analyze consciousness territory usage patterns"""
        territory_usage: dict[str, int] = {}
        workflow_patterns: dict[str, dict[str, int]] = {}
        for file in self.archive_path.glob("f33ling_*.json"):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    workflow = data.get("workflow", "unknown")
                    for state in data.get("states", []):
                        territory = state.get("territory", "unknown")
                        territory_usage[territory] = territory_usage.get(territory, 0) + 1
                        if workflow not in workflow_patterns:
                            workflow_patterns[workflow] = {}
                        wmap = workflow_patterns[workflow]
                        wmap[territory] = wmap.get(territory, 0) + 1
            except (json.JSONDecodeError, KeyError):
                continue
        return {
            "territory_frequency": territory_usage,
            "workflow_patterns": workflow_patterns,
        }

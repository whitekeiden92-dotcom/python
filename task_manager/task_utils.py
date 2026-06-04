"""Utilities for task creation and management.

Tasks are simple dictionaries with keys:
- `title` (str)
- `description` (str)
- `completed` (bool)
"""

from typing import List, Dict


def create_task(title: str, description: str) -> Dict:
    return {"title": title.strip(), "description": description.strip(), "completed": False}


def add_task(tasks: List[Dict], title: str, description: str) -> None:
    """Append a new task to `tasks` list."""
    tasks.append(create_task(title, description))


def list_tasks(tasks: List[Dict]) -> List[Dict]:
    return tasks.copy()


def pending_tasks(tasks: List[Dict]) -> List[Dict]:
    return [t for t in tasks if not t.get("completed")]


def mark_complete(tasks: List[Dict], index: int) -> bool:
    """Mark the task at `index` complete. Return True if successful."""
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = True
        return True
    return False


def progress_percent(tasks: List[Dict]) -> float:
    """Return the completion percentage (0-100)."""
    if not tasks:
        return 0.0
    done = sum(1 for t in tasks if t.get("completed"))
    return round((done / len(tasks)) * 100.0, 2)

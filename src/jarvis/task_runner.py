from __future__ import annotations

from .context_manager import ContextManager
from .orchestrator import MultiContextPlanner


def run_pending() -> None:
    cm = ContextManager()
    planner = MultiContextPlanner()
    planner.context_manager = cm

    tasks = cm.list_tasks(status="pending")
    for task in tasks:
        print(f"Processing {task.id}: {task.prompt}")
        planner.handle(task.id, task.prompt)
    remaining = cm.list_tasks(status="pending")
    if not remaining:
        print("All tasks completed.")
    else:
        print(f"{len(remaining)} tasks left.")


if __name__ == "__main__":
    run_pending()

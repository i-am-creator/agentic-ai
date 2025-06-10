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
        # TODO: The user_input for planner.handle should be based on the next action for the task,
        # not just the initial prompt. This needs further refinement based on agent communication.
        planner.handle(task.id, task.prompt)
    remaining = cm.list_tasks(status="pending")
    if not remaining:
        print("All tasks completed.")
    else:
        print(f"{len(remaining)} tasks left.")


if __name__ == "__main__":
    run_pending()

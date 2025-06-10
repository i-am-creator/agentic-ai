from __future__ import annotations

import argparse

from .orchestrator import MultiContextPlanner


def main() -> None:
    parser = argparse.ArgumentParser(description="Jarvis-style assistant CLI")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute")
    args = parser.parse_args()

    planner = MultiContextPlanner()
    user_input = " ".join(args.command)
    task_id = planner.create_task(user_input)
    output = planner.handle(task_id, user_input)
    print(output)


if __name__ == "__main__":
    main()

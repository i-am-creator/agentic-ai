from __future__ import annotations

import typer

from .orchestrator import MultiContextPlanner

app = typer.Typer(add_completion=False, help="Jarvis-style assistant CLI")


@app.callback(invoke_without_command=True)
def main(command: list[str] = typer.Argument(None, help="Command to execute")) -> None:
    """Run a single Jarvis command."""
    planner = MultiContextPlanner()
    user_input = " ".join(command)
    task_id = planner.create_task(user_input)
    output = planner.handle(task_id, user_input)
    typer.echo(output)


if __name__ == "__main__":
    app()

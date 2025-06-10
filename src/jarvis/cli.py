from __future__ import annotations

from typing import Optional
import sys

import click
from rich.console import Console
from rich.markdown import Markdown
from .context_manager import ContextManager
from .workflow_manager import WorkflowManager


console = Console()


@click.group()
def cli() -> None:
    """Jarvis CLI - Your AI Code Assistant"""
    pass


@cli.command()
@click.argument("command", nargs=-1, required=False)
@click.option("--task-id", help="Continue an existing task")
def main(command: tuple[str, ...], task_id: Optional[str]) -> None:
    """Run a command or start an interactive session."""
    context_manager = ContextManager()
    workflow_manager = WorkflowManager(context_manager)

    if command:
        # Join the command parts and handle special cases
        full_command = " ".join(command)
        run_command(full_command, task_id, workflow_manager)
    else:
        run_interactive(workflow_manager)


def run_command(command: str, task_id: Optional[str], workflow_manager: WorkflowManager) -> None:
    """Run a single command."""
    try:
        # Handle special commands
        if command == "list":
            tasks = workflow_manager.context_manager.list_tasks()
            if not tasks:
                console.print("No tasks found")
                return

            for task in tasks:
                console.print(f"Task {task.id}: {task.status}")
                if task.prompt:
                    console.print(f"Prompt: {task.prompt}")
                console.print("")
            return

        if command.startswith("summarize "):
            task_id = command.split()[1]
            task = workflow_manager.context_manager.get(task_id)
            if not task:
                console.print("Error: Task not found")
                return

            chunks = workflow_manager.context_manager.get_chunks(task_id)
            if not chunks:
                console.print("No content found for this task")
                return

            content = "\n".join(chunk.content for chunk in chunks)
            summary = workflow_manager.model_selector.generate_response(
                f"Summarize the following task history:\n\n{content}",
                system_prompt="You are a helpful assistant that summarizes task histories."
            )
            console.print(Markdown(summary))
            return

        # Execute workflow
        output = workflow_manager.execute_workflow(command)
        console.print(Markdown(output))

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")


def run_interactive(workflow_manager: WorkflowManager) -> None:
    """Run an interactive session."""
    console.print("[bold blue]Welcome to Jarvis CLI![/bold blue]")
    console.print("\nYou can ask me to:")
    console.print("  - Explain or analyze code files")
    console.print("  - Perform file operations")
    console.print("  - Generate or analyze text")
    console.print("\nSpecial commands:")
    console.print("  list - List all tasks")
    console.print("  summarize <task-id> - Get a summary of a task")
    console.print("\nType 'exit' to quit\n")

    while True:
        try:
            command = click.prompt("jarvis", type=str)
            if command.lower() == "exit":
                break

            if command == "list":
                tasks = workflow_manager.context_manager.list_tasks()
                if not tasks:
                    console.print("No tasks found")
                    continue

                for task in tasks:
                    console.print(f"Task {task.id}: {task.status}")
                    if task.prompt:
                        console.print(f"Prompt: {task.prompt}")
                    console.print("")
                continue

            if command.startswith("summarize "):
                task_id = command.split()[1]
                task = workflow_manager.context_manager.get(task_id)
                if not task:
                    console.print("Error: Task not found")
                    continue

                chunks = workflow_manager.context_manager.get_chunks(task_id)
                if not chunks:
                    console.print("No content found for this task")
                    continue

                content = "\n".join(chunk.content for chunk in chunks)
                summary = workflow_manager.model_selector.generate_response(
                    f"Summarize the following task history:\n\n{content}",
                    system_prompt="You are a helpful assistant that summarizes task histories."
                )
                console.print(Markdown(summary))
                continue

            # Execute workflow
            output = workflow_manager.execute_workflow(command)
            console.print(Markdown(output))

        except click.Abort:
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")


if __name__ == "__main__":
    # Handle command line arguments with spaces
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        # If the first argument doesn't start with "-", it's a command
        # Join all arguments after the first one
        sys.argv = [sys.argv[0], "main", " ".join(sys.argv[1:])]
    cli()

import asyncio
from src.jarvis.orchestrator import MultiContextPlanner

async def main():
    planner = MultiContextPlanner()
    # Example use case: Ask Jarvis to summarize a text
    user_input = "Summarize the main points of the following text: Artificial intelligence is transforming industries by automating tasks, providing insights, and enabling new capabilities."
    print(f"User input: {user_input}")

    # Create a new task
    task_id = await planner.create_task(user_input)
    print(f"Created task with ID: {task_id}")

    # Handle the task (get the response)
    result = await planner.handle(task_id, user_input)
    print(f"\nJarvis response:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
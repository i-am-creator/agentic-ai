from src.jarvis.context_manager import ContextManager
from src.jarvis.workflow_manager import WorkflowManager


def main() -> None:
    cm = ContextManager()
    wf = WorkflowManager(cm)
    command = "explain ./src/jarvis/model_selector.py"
    output = wf.execute_workflow(command)
    print(output)


if __name__ == "__main__":
    main()

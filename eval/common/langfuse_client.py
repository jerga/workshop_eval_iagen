from __future__ import annotations


class LangfuseClient:
    """Placeholder leger pour step 3.

    L'integration reelle est introduite au step 4.
    """

    def __init__(self) -> None:
        self.enabled = False

    def log_dataset_run(self, dataset_name: str) -> None:
        if self.enabled:
            print(f"Langfuse run logged: {dataset_name}")

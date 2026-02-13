from __future__ import annotations

from typing import Sequence, Self

from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    MofNCompleteColumn,
    TimeElapsedColumn,
)
# from rich.console import Console

class ProgressBar(Progress):
    def __init__(
        self,
        steps: Sequence[str],
    ):
        super().__init__(
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("elapsed"),
            TimeElapsedColumn(),
            TextColumn("[progress.description]{task.description}"),
            # console=Console(),
        )
        self._steps = steps
        # self._task_id = None
        # self._task = None

    def __enter__(self) -> Self:
        self._task_id = self.add_task(
            description=self._steps[0], 
            total=len(self._steps),
            start=True,
        )
        self._task = self.tasks[self._task_id]
        return super().__enter__()
    
    def update(self) -> None:
        if (
            self._task_id is not None
            and self._task is not None
        ):
            super().update(self._task_id, advance=1)
            if self._task.completed < len(self._steps):
                self._task.description = self._steps[int(self._task.completed)]

import asyncio
from typing import Optional

from python_flow.core import AsyncNode


class RangerNode(AsyncNode):
    def __init__(self, start: float=0, stop: Optional[float]=10, step: float=1, sleep_between_steps: float = 0, *args, **kwargs) -> None:
        kwargs.setdefault("input_type", float)
        super().__init__(is_absolute_source=True, *args, **kwargs)
        self._stop = stop
        if self._stop is None:
            self._stop = float("inf")
        self._step = step
        self._sleep_between_steps = sleep_between_steps
        self._current_value = start

    async def _start(self):
        while self._current_value < self._stop:
            self._current_value += self._step
            self._write_all_sinks()
            await asyncio.sleep(self._sleep_between_steps)

    def read(self) -> float:
        return self._current_value

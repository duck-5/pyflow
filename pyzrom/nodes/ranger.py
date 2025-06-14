import asyncio

from pyzrom.base import AsyncNode

class RangerNode(AsyncNode):
    def __init__(self, step: float, sleep_between_steps: float = 0.2, *args, **kwargs) -> None:
        kwargs.setdefault("passed_value_type", float)
        super().__init__(is_absolute_source = True, *args, **kwargs)
        self._step = step
        self._sleep_between_steps = sleep_between_steps
        self._current_value: float = 0
    
    async def _start(self):
        while True:
            self._current_value += self._step
            self._write_all_sinks()
            await asyncio.sleep(self._sleep_between_steps)
    
    def read(self) -> float:
        return self._current_value

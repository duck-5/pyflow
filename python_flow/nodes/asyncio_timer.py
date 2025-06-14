import asyncio
from abc import ABC, abstractmethod
from typing import Any, Optional

from python_flow.core import AsyncNode
from python_flow.core.enums import LoggingSeverity, NodeState


class AsyncioTimerNode(AsyncNode, ABC):
    def __init__(
        self,
        loop,
        timer_interval_seconds: float,
        timeout: Optional[int] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._loop = loop
        self._timer_interval_seconds = timer_interval_seconds
        self._timeout = timeout
        self._state = NodeState.WAITING
        self._time_from_last_call = 0
        self._task = None

    async def _start(self):
        self._state = NodeState.RUNNING
        self.log(message=f"Changed state: {self._state}", severity=LoggingSeverity.INFO)
        while self._timeout is None or self._time_from_last_call < self._timeout:
            self._spin()
            self._time_from_last_call += self._timer_interval_seconds
            await asyncio.sleep(self._timer_interval_seconds)
        self._state = NodeState.HIBERNATING
        self.log(message=f"Changed state: {self._state}", severity=LoggingSeverity.INFO)

    def write(self, _=None, /) -> None:
        self._time_from_last_call = 0
        if self._state == NodeState.HIBERNATING:
            self._task = asyncio.create_task(self._start)

    @abstractmethod
    def _spin(self):
        ...

from .asyncio_timer import AsyncioTimerNode


class AsyncioTimerDataStreamerNode(AsyncioTimerNode):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(max_number_of_sources=1, *args, **kwargs)
    
    def _spin(self):
        self._current_value = self._read_from_one_source()
        self._write_all_sinks()

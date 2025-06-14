from typing import Any, Callable, Optional

from python_flow.core import Node


class MapperNode(Node):
    def __init__(self, callback: Callable[[Any], Any], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._callback = callback

    def write(self, value: Any = None):
        self._current_value = self._callback(value)
        self._write_all_sinks()

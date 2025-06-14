from typing import Any, Optional

from python_flow.base import Node

class MockNode(Node):
    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault("passed_value_type", None)
        super().__init__(*args, **kwargs)
    
    @property
    def current_value(self):
        return self._current_value
    
    @current_value.setter
    def current_value(self, value):
        self._current_value = value

    def read_from_all_sources(self):
        return super()._read_from_all_sources()
    
    def write(self, value: Any = None) -> None:
        self._current_value = value
        self._write_all_sinks

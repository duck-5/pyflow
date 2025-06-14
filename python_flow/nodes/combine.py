from typing import Any, Optional, Tuple
from python_flow.core import Node
from python_flow.core.enums import LoggingSeverity

class CombineNode(Node):
    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault("passed_value_type", Tuple[Any])
        super().__init__(*args, **kwargs)
        self._current_value: Optional[Tuple[Any, ...]] = None
    
    def write(self, _ = None):
        self._current_value = self._read_from_all_sources()
        self.log(message=f"Written: {self._current_value}", severity=LoggingSeverity.DEBUG)
        self._write_all_sinks

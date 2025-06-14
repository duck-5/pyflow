from typing import Any, Optional

from pyzrom.base import Node
from pyzrom.base.enums import LoggingSeverity

class PrinterNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(passed_value_type=None, is_absolute_sink=True, *args, **kwargs)
    
    def write(self, value: Any = None) -> None:
        self._current_value = value
        self.log(message=f"Written: {self._current_value}", severity=LoggingSeverity.DEBUG)
        print(f"{self.label}: {value}")

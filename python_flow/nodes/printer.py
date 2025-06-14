from datetime import datetime
from typing import Any

from python_flow.core import Node
from python_flow.core.enums import LoggingSeverity


class PrinterNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(passed_value_type=None, is_absolute_sink=True, *args, **kwargs)
        self._timestamp_format = "%Y-%m-%d %H:%M:%S"

    def write(self, value: Any = None) -> None:
        self._current_value = value
        self.log(message=f"Written: {self._current_value}", severity=LoggingSeverity.DEBUG)
        timestamp = datetime.now().strftime(self._timestamp_format)
        print(f"[{timestamp}] {self.label}: {value}")

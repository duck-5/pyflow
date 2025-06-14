import time
from typing import Optional, Union

from python_flow.core import Node
from python_flow.core.enums import AlertState


class ValueInRangeForDurationValidatorNode(Node):
    def __init__(
        self,
        top_limit: Optional[float] = None,
        bottom_limit: Optional[float] = None,
        duration_seconds: Optional[float] = None,
        *args,
        **kwargs,
    ):
        super().__init__(max_number_of_sources=1, passed_value_type=AlertState, *args, **kwargs)
        self._top_limit = top_limit
        self._bottom_limit = bottom_limit
        self._max_duration_seconds = duration_seconds

        self._duration: int = 0
        self._last_ok_state_timestamp = time.time()
        self._current_value = AlertState.UNKNOWN

        if self._max_duration_seconds is not None:
            self._value_handler = self._value_handler_with_time_tracking
        else:
            self._value_handler = self._value_handler_without_time_tracking

    def write(self, value: float) -> None:
        self._current_value = self._value_handler(value)
        self._write_all_sinks()

    def _value_handler_with_time_tracking(self, value: float) -> AlertState:
        time_since_last_ok_state = time.time() - self._last_ok_state_timestamp
        if self._validate_value_in_range(value):
            self._last_ok_state_timestamp = time.time()
            return AlertState.OK

        if time_since_last_ok_state < self._max_duration_seconds:
            return AlertState.WARNING

        if time_since_last_ok_state >= self._max_duration_seconds:
            return AlertState.ERROR

    def _value_handler_without_time_tracking(self, value: float) -> AlertState:
        if self._validate_value_in_range(value):
            return AlertState.OK

        return AlertState.ERROR

    def _validate_value_in_range(self, value: float):
        is_below_top = self._top_limit is None or value <= self._top_limit
        is_above_bottom = self._bottom_limit is None or value >= self._bottom_limit

        return is_below_top and is_above_bottom

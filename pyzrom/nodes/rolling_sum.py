from collections import deque

from pyzrom.base import Node

class RollingSumNode(Node):
    def __init__(self, summed_queue_len: int, *args, **kwargs):
        kwargs.setdefault("passed_value_type", float)
        super().__init__(max_number_of_sources=1, *args, **kwargs)
        self._summed_queue_len = summed_queue_len
        self._data_buffer = deque(maxlen=summed_queue_len)
        self._current_sum = 0
        self._current_value: float = self._current_sum
        self._index = 0
    
    def write(self, value: float = 0):
        if self._index > self._summed_queue_len:
            self._current_sum -= self._data_buffer.popleft()
        else:
            self._index += 1
        
        self._data_buffer.append(value)
        self._current_sum += value
        self._current_value = self._current_sum
        self._write_all_sinks()
    
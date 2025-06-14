from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple

from python_flow.core.enums import LoggingSeverity, NodeState, get_logging_callback_by_severity

class Node(ABC):
    @property
    def label(self) -> str:
        return self._label
    @property
    def sinks(self) -> List[Node]:
        return self._sinks
    @property
    def sources(self) -> List[Node]:
        return self._sources
    @property
    def is_absolute_source(self) -> bool:
        return self._is_absolute_source
    @property
    def is_absolute_sink(self) -> bool:
        return self._is_absolute_sink
    @property
    def state(self) -> NodeState:
        return self._state
    
    @property
    def passed_value_type(self) -> Optional[str]:
        if hasattr(self._passed_value_type, "_name"): # A typing instance
            return str(self._passed_value_type).lstrip("typing.")
        if hasattr(self._passed_value_type, "__name__"): # A typing instance
            return self._passed_value_type.__name__
        if self._passed_value_type is None:
            return None
        return "Unknown"
    
    def __init__(self, label: str, passed_value_type: Any = Any, logger: Any = None, min_number_of_sources: Optional[int] = None, max_number_of_sources: Optional[int] = None, is_absolute_source: bool = False, is_absolute_sink: bool = False):
        self._label = label
        self._logger = logger or logging.getLogger(label)
        self._passed_value_type = passed_value_type
        self._min_number_of_sources = min_number_of_sources
        self._max_number_of_sources = max_number_of_sources
        self._is_absolute_sink = is_absolute_sink
        self._is_absolute_source = is_absolute_source

        self._current_value: Any = None
        self._sources: List[Node] = []
        self._sinks: List[Node] = []
        self._state: NodeState = NodeState.RUNNING

    def log(self, message: str, severity: LoggingSeverity = LoggingSeverity.INFO):
        get_logging_callback_by_severity(self._logger, severity)(message)
    
    def set_source(self, node: Node) -> Node:
        self.log(message=f"Setting source {node.label}", severity=LoggingSeverity.DEBUG)

        if self._max_number_of_sources is not None and len(self._sources) >= self._max_number_of_sources:
            raise RuntimeError(
                f"Cannot set more sources than max_number_of_sources.\n"
                f"Additional info: Node {self._label} with {self._max_number_of_sources}"
            )
        self._sources.append(node)

    def set_sink(self, node: Node) -> Node:
        self.log(message=f"Setting sink {node.label}", severity=LoggingSeverity.DEBUG)
        if self._is_absolute_sink:
            raise RuntimeError("Cannot set sink to a node marked as an absolute sink")
        
        self._sinks.append(node)
        node.set_source(node=self)
    
    def read(self) -> Any:
        return self._current_value
    
    def _read_from_all_sources(self) -> Tuple[Any, ...]:
        responses = []
        for src in self._sources:
            responses.append(src.read())
        return tuple(responses)
    
    def _read_from_one_source(self, source_index: int = 0) -> Any:
        return self._sources[source_index].read()
    
    def _write_all_sinks(self):
        for sink in self._sinks:
            sink.write(self._current_value)
    
    @abstractmethod
    def write(self, value: Optional[Any] = None, /) -> None:
        ...

class AsyncNode(Node, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = NodeState.WAITING
        self.log(message=f"Current staet: {self._state}", severity=LoggingSeverity.DEBUG)
        self._has_started: bool = False

    def write(self, _: Optional[Any] = None, /):
        # By default, not doing anything (async node should trigger itself)
        pass

    async def start(self):
        if not self._has_started:
            self._has_started = True
            await self._start()
    
    @abstractmethod
    async def _start(self):
        ...        

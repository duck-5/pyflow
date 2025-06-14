from enum import Enum, auto


class NodeState:
    WAITING = auto()
    RUNNING = auto()
    HIBERNATING = auto()


class PipelineState(Enum):
    UNINITIALIZED = auto()
    WAITING = auto()
    RUNNING = auto()


class LoggingSeverity(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class AlertState(Enum):
    UNKNOWN = auto()
    OK = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

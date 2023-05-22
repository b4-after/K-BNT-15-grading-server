from enum import Enum


class ClovaResultType(str, Enum):
    WAITING: str = "WAITING"
    PROCESSING: str = "PROCESSING"
    FAILED: str = "FAILED"
    COMPLETED: str = "COMPLETED"
    TIMEOUT: str = "TIMEOUT"
    SUCCEEDED: str = "SUCCEEDED"

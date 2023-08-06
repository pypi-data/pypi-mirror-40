from typing import Any, Dict, NoReturn

from chaosplt_scheduling.storage.interface import BaseSchedulingStorage

__all__ = ["MySchedulingStorage"]


class MySchedulingStorage(BaseSchedulingStorage):
    def __init__(self, config: Dict[str, Any]):
        self.some_flag = True

    def release(self) -> NoReturn:
        self.some_flag = False

from typing import Any, Dict, NoReturn

from chaosplt_auth.storage.interface import BaseAuthStorage

__all__ = ["MyAuthStorage"]


class MyAuthStorage(BaseAuthStorage):
    def __init__(self, config: Dict[str, Any]):
        self.some_flag = True

    def release(self) -> NoReturn:
        self.some_flag = False

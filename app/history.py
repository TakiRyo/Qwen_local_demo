from __future__ import annotations

from collections import defaultdict, deque
from typing import Deque, Dict, List


class HistoryStore:
    def __init__(self, max_messages: int = 20) -> None:
        self._max_messages = max_messages
        self._store: Dict[str, Deque[dict]] = defaultdict(deque)

    def get(self, session_id: str) -> List[dict]:
        return list(self._store[session_id])

    def append(self, session_id: str, message: dict) -> None:
        history = self._store[session_id]
        history.append(message)
        while len(history) > self._max_messages:
            history.popleft()

    def clear(self, session_id: str) -> None:
        self._store.pop(session_id, None)

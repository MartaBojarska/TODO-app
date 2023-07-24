from datetime import datetime, timezone
from uuid import UUID, uuid4


class Todo:
    id: UUID
    name: str
    is_finished: bool
    created_at: datetime
    finished_at: datetime | None

    def __init__(self, name: str) -> None:
        self.id = uuid4()
        self.name = name
        self.created_at = datetime.now(timezone.utc)
        self.is_finished = False
        self.finished_at = None

    def set_is_finished(self, is_finished: bool):
        self.is_finished = is_finished
        if is_finished:
            self.finished_at = datetime.now(timezone.utc)
            return
        self.finished_at = None

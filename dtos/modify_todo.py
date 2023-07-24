from pydantic import BaseModel


class ModifyTodoDTO(BaseModel):
    name: str
    is_finished: bool

from pydantic import BaseModel


class CreateTodoDTO(BaseModel):
    name: str

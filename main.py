from uuid import UUID
from fastapi import FastAPI, HTTPException
from dtos.create_todo import CreateTodoDTO
from dtos.modify_todo import ModifyTodoDTO

from models.todo import Todo

todo_list = {}
app = FastAPI()


@app.get("/todos")
def get_todos():
    return {"data": list(todo_list.values())}


@app.post("/todos")
def create_todo(dto: CreateTodoDTO):
    todo = Todo(dto.name)
    todo_list[todo.id] = todo
    return todo


@app.get("/todos/{todo_id}")
def get_todo(todo_id: UUID):
    try:
        return todo_list[todo_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found.")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: UUID):
    try:
        del todo_list[todo_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found.")
    return {"data": None}


@app.patch("/todos/{todo_id}")
def modify_todo(todo_id: UUID, dto: ModifyTodoDTO):
    try:
        todo = todo_list[todo_id]
        todo.name = dto.name
        todo.set_is_finished(dto.is_finished)
        return todo
    except KeyError:
        raise HTTPException(status_code=404, detail="Not found.")

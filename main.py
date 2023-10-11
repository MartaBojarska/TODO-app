import psycopg2
from uuid import UUID
from fastapi import FastAPI, HTTPException
from dtos.create_todo import CreateTodoDTO
from dtos.modify_todo import ModifyTodoDTO

from models.todo import NewTodo, Todo

todo_list = {}
app = FastAPI()
conn = psycopg2.connect(
    database="todos",
    host="localhost",
    user="postgres",
    password="zaq1WSX",
    port="5432",
)
cursor = conn.cursor()


@app.get("/todos")
def get_todos(search: str = ""):
    cursor.execute(
        "SELECT id, name, created_at, is_finished, finished_at FROM todos WHERE name ILIKE %s;",
        (f"%{search}%",),
    )
    todos_data = cursor.fetchall()
    serialized_todos = [
        NewTodo(
            id=id,
            name=name,
            created_at=created_at,
            is_finished=is_finished,
            finished_at=finished_at,
        )
        for id, name, created_at, is_finished, finished_at in todos_data
    ]
    return {"data": serialized_todos}


@app.post("/todos")
def create_todo(dto: CreateTodoDTO):
    cursor.execute(
        "INSERT INTO todos(name) VALUES(%s) RETURNING id, name, created_at, is_finished, finished_at;",
        (dto.name,),
    )
    conn.commit()
    id, name, created_at, is_finished, finished_at = cursor.fetchone()
    return NewTodo(
        id=id,
        name=name,
        created_at=created_at,
        is_finished=is_finished,
        finished_at=finished_at,
    )


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    cursor.execute(
        "SELECT id, name, created_at, is_finished, finished_at FROM todos WHERE id=%s;",
        (todo_id,),
    )
    todo_data = cursor.fetchone()
    if todo_data is None:
        raise HTTPException(status_code=404, detail="Not found.")
    id, name, created_at, is_finished, finished_at = todo_data
    return NewTodo(
        id=id,
        name=name,
        created_at=created_at,
        is_finished=is_finished,
        finished_at=finished_at,
    )


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    cursor.execute(
        "DELETE FROM todos WHERE id=%s RETURNING id;",
        (todo_id,),
    )
    todo_data = cursor.fetchone()
    if todo_data is None:
        raise HTTPException(status_code=404, detail="Not found.")
    conn.commit()
    return {"data": None}


@app.patch("/todos/{todo_id}")
def modify_todo(todo_id: int, dto: ModifyTodoDTO):
    if dto.is_finished:
        cursor.execute(
            "UPDATE todos SET name=%s,is_finished=true,finished_at=now() WHERE id=%s RETURNING id, name, created_at, is_finished, finished_at;",
            (dto.name, todo_id),
        )
    else:
        cursor.execute(
            "UPDATE todos SET name=%s,is_finished=false,finished_at=NULL WHERE id=%s RETURNING id, name, created_at, is_finished, finished_at;",
            (dto.name, todo_id),
        )
    todo_data = cursor.fetchone()
    if todo_data is None:
        raise HTTPException(status_code=404, detail="Not found.")
    conn.commit()
    id, name, created_at, is_finished, finished_at = todo_data
    return NewTodo(
        id=id,
        name=name,
        created_at=created_at,
        is_finished=is_finished,
        finished_at=finished_at,
    )

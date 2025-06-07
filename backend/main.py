from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3

app = FastAPI()

# Define the Todo model
class Todo(BaseModel):
    id: int = None
    title: str
    completed: bool = False

# Connect to SQLite and create table
def init_db():
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
init_db()

# Get all todos
@app.get("/todos", response_model=List[Todo])
def get_todos():
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, completed FROM todos")
        rows = cursor.fetchall()
        return [Todo(id=row[0], title=row[1], completed=bool(row[2])) for row in rows]

# Add a new todo
@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (title, completed) VALUES (?, ?)", (todo.title, todo.completed))
        todo.id = cursor.lastrowid
        return todo

# Update an existing todo
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: Todo):
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET title = ?, completed = ? WHERE id = ?", (todo.title, todo.completed, todo_id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {**todo.dict(), "id": todo_id}

# Delete a todo
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with sqlite3.connect("todos.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"message": "Todo deleted successfully"}

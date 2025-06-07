from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models
from .database import engine, get_db
from .crud import TodoCreate, TodoUpdate, TodoResponse
from typing import List

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

@app.get("/todos", response_model=List[TodoResponse])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all todos with pagination"""
    try:
        todos = crud.get_todos(db, skip=skip, limit=limit)
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todos: {str(e)}")

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    try:
        todo = crud.get_todo(db, todo_id=todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching todo: {str(e)}")

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo"""
    try:
        return crud.create_todo(db=db, todo=todo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating todo: {str(e)}")

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update an existing todo"""
    try:
        updated_todo = crud.update_todo(db, todo_id=todo_id, todo_update=todo_update)
        if updated_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return updated_todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating todo: {str(e)}")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo"""
    try:
        deleted_todo = crud.delete_todo(db, todo_id=todo_id)
        if deleted_todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {"message": "Todo deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting todo: {str(e)}")
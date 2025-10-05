from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models import task as models
from app.schemas.task import TaskCreate, TaskOut

# Create router (like @RestController in Spring Boot)
router = APIRouter()

@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task - similar to @PostMapping in Spring Boot"""
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks", response_model=List[TaskOut])
def get_all_tasks(db: Session = Depends(get_db)):
    """Get all tasks - similar to @GetMapping in Spring Boot"""
    tasks = db.query(models.Task).all()
    return tasks

@router.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get task by ID - similar to @GetMapping("/{id}") in Spring Boot"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

@router.put("/tasks/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    """Update task - similar to @PutMapping in Spring Boot"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete task - similar to @DeleteMapping in Spring Boot"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    db.delete(task)
    db.commit()
    return None

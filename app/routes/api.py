from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.task import TaskOut, TaskCreate
from app.service import task_service

router = APIRouter()


@router.get("/tasks", response_model=List[TaskOut], status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db)):
    """Get all tasks"""
    return task_service.get_all_tasks(db)


@router.get("/tasks/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task by ID"""
    return task_service.get_task_by_id(task_id, db)

@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task"""
    return task_service.create_task(task, db)


@router.put("/tasks/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    """Update an existing task"""
    return task_service.update_task(task_id, task, db)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task"""
    return task_service.delete_task_by_id(task_id, db)


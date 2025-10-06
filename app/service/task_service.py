from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.task import Task
from app.schemas.task import TaskCreate


def get_all_tasks(db: Session):
    """Get all tasks from database"""
    return db.query(Task).all()


def get_task_by_id(task_id: int, db: Session):
    """Get a specific task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task

def create_task(task:TaskCreate , db:Session):

    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Task title cannot be empty")

    db_task = Task(
        title=task.title ,
        description=task.description,
        completed=task.completed,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task_by_id(task_id: int, db: Session):
    """Delete a specific task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}


def update_task(task_id: int, task_data: TaskCreate, db: Session):
    """Update an existing task"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    
    # Update fields
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed
    
    db.commit()
    db.refresh(task)
    return task
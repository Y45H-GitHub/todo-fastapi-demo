from pydantic import BaseModel, Field
from typing import Optional

# Request model for creating a task (like @RequestBody in Spring Boot)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=1000, description="Task description")
    completed: bool = Field(False, description="Task completion status")

# Response model for returning task data (like @ResponseBody in Spring Boot)
class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True  # Updated from orm_mode in Pydantic v2

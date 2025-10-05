from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)  # Required field
    description = Column(String, nullable=True)  # Optional field
    completed = Column(Boolean, default=False, nullable=False)  # Required with default
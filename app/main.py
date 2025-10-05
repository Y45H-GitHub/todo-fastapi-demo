from fastapi import FastAPI
from app.db.database import Base, engine
from app.routes.api import router

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="Todo API", version="1.0.0")

# Include routers
app.include_router(router, prefix="/api", tags=["todos"])
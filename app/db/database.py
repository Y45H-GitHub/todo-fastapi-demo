from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

#  sql academy engine (sql academy is the ORM - object relation mapping)
engine = create_engine(DATABASE_URL)

# create a configured Session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
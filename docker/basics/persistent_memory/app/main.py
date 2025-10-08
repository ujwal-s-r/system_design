import os
import time
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# --- Database Setup ---
# Read database connection details from environment variables
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy Model ---
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)

# Function to create tables with retry logic
def create_tables_with_retry(max_retries=30, delay=1):
    for attempt in range(max_retries):
        try:
            Base.metadata.create_all(bind=engine)
            print(f"Database connection successful on attempt {attempt + 1}")
            return
        except Exception as e:
            print(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                print("Max retries reached. Could not connect to database.")
                raise

# Create the table in the database if it doesn't exist
create_tables_with_retry()

# --- Pydantic Model for API request ---
class TodoCreate(BaseModel):
    text: str

# --- FastAPI App ---
app = FastAPI()

@app.post("/todos/")
def create_todo(todo: TodoCreate):
    db = SessionLocal()
    new_todo = Todo(text=todo.text)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos/")
def read_todos():
    db = SessionLocal()
    return db.query(Todo).all()
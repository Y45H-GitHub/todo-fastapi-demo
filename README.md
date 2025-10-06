## DATE: 5 Oct, 2025

### FastAPI vs Spring Boot

* In Spring Boot, I used `Spring Initializr` to create projects and add dependencies from there or via Maven. For FastAPI, I can directly use `pip` to install `fastapi` in a standard project structure and use `uvicorn` to start the server.
* In PyCharm, create a new project. Projects are created in a virtual environment so that this project’s dependencies don’t mix with those of other projects.
* Write a simple `app.py` and run it using:

  ```bash
  uvicorn main:app --reload
  ```
* The project structure is similar to Spring Boot.

---

## Sample Project of a FastAPI Backend

```
todo-fastapi-demo/
 ┣ .venv/
 ┣ app/
 ┃ ┣ __init__.py
 ┃ ┣ main.py                 ← "SpringBootApplication" equivalent
 ┃ ┣ core/                   ← global config, settings, security
 ┃ ┣ api/                    ← routers (controllers)
 ┃ ┣ models/                 ← SQLAlchemy ORM models (entities)
 ┃ ┣ schemas/                ← Pydantic models (DTOs)
 ┃ ┣ services/               ← business logic (like service layer)
 ┃ ┣ db/                     ← database session + migrations
 ┃ ┣ utils/                  ← helper functions, shared utilities
 ┃ ┗ tests/                  ← unit/integration tests
 ┣ alembic/                  ← database migration scripts
 ┣ .env
 ┣ requirements.txt
 ┣ README.md
 ┗ Dockerfile
```

---

## Connecting to a Supabase PostgreSQL DB

Dependencies to install via pip:

* `sqlalchemy` → ORM (like Hibernate in Spring Boot)
* `psycopg2-binary` → PostgreSQL driver
* `python-dotenv` → to load the `.env` file

can also use `SQLite` lightweight, self-contained, serverless relational database
```python
#DATABASE_URL=sqlite:///./todo.db
```

---

### Do I need to manually update the `requirements.txt` file continuously? **No.**

pip has a command `freeze`. You can run:

```bash
pip freeze > requirements.txt
```

This automatically copies all installed dependencies and their versions into the file.

---

## Connecting to Supabase

* Spin up a database on Supabase and get the URL.

* Put that URL in the `.env` file.

* Set up SQLAlchemy in `\app\db\database.py`:

  * engine, session, base class

* Define models in `\app\models\task.py`.

* Create the table in `main.py`:

  ```python
  Base.metadata.create_all(bind=engine)
  ```

* Create routes in `\app\routes` and necessary DTOs in `\app\schemas`.

* Run the server.

---

### Handling special characters in PostgreSQL passwords

If your password contains special characters, they cannot be used directly in the `DATABASE_URL`. Encode special characters, e.g., `@` becomes `%40`.

---

## Understanding the workings of FastAPI

FastAPI doesn’t include a database layer. For relational databases, the standard is SQLAlchemy, similar to Hibernate/JPA in Java.

Key components: **Engine**, **Session**, **Base**

* **ENGINE**: the actual connection manager to your database. Equivalent to `DataSource` in Java.

* **SESSION**: transactional workspace. You perform all queries and changes inside a session, like `EntityManager` in JPA.

  ```python
  SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
  db = SessionLocal()
  ```

  Workflow: open session → add/update/delete objects → commit transaction → close session.
  Engine is like a phone line—it just calls the DB; the actual work is managed by the Session.
  `autocommit=False` ensures the session won’t auto-commit.
  `autoflush=False` ensures transactions are handled safely.

* **BASE**: foundational class from which all ORM models inherit, like `@Entity` in Java.

  ```python
  from sqlalchemy.orm import declarative_base
  Base = declarative_base()
  ```

  Example model:

  ```python
  class Task(Base):
      __tablename__ = "tasks"
      id = Column(Integer, primary_key=True, index=True)
      title = Column(String)
  ```

  SQLAlchemy uses `Base` to understand that:

  * This class is mapped to a database table
  * These attributes map to table columns

---

### How they work together (lifecycle)

1. **Engine** → connects to the DB
2. **Session** → opens a transactional workspace using the engine
3. **Base + models** → define tables
4. **CRUD operations** → executed inside a session:

```python
db.add(task)
db.commit()
db.refresh(task)
```

5. After commit, the session closes → engine keeps the connection pool alive.

---

## Date: 6 Oct, 2025



### **Understanding Routes **

In FastAPI, routes are the equivalent of controllers in Spring Boot.

#### **1. Using `APIRouter`**

Before writing routes define a router.
Routers help organize your endpoints into logical modules (for example: `user_router`, `task_router`, etc.), similar to splitting controllers in Spring Boot.

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import TaskCreate, TaskOut

router = APIRouter(
    prefix="/tasks",           # Base path for this router
    tags=["Tasks"]             # Optional: used for Swagger grouping
)
```

---

#### **2. Defining a POST route**

Equivalent to `@PostMapping` in Spring Boot.

```python
@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    # task: input DTO (from request body)
    # db: dependency-injected database session
    new_task = models.Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
```

**Explanation**

* `response_model` → defines what schema (DTO) to return in the response.
* `status_code` → optional, sets the default HTTP status.
* Function arguments automatically decide **where the data comes from**:

  * `task: TaskCreate` → from JSON request body.
  * `db: Session = Depends(get_db)` → from dependency injection (creates DB session per request).

---

#### **3. Defining a GET route (path variable)**

Equivalent to `@GetMapping("/task/{id}")` with `@PathVariable`.

```python
@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    return task
```

 **Explanation**

* `{task_id}` in the route matches the function parameter `task_id`.
* Type hint (`int`) tells FastAPI to:

  * Validate the input (it must be an integer).
  * Convert it automatically.
* FastAPI handles **404** responses if you manually raise exceptions.

---

#### **4. Defining a GET route (query parameters)**

Equivalent to `@RequestParam` in Spring Boot.

```python
@router.get("/", response_model=list[TaskOut])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return tasks
```

 **Explanation**

* `skip` and `limit` are automatically treated as **query parameters**, like `/tasks?skip=0&limit=10`.
* You can add defaults and validation easily with `Query()`.

---

#### **5. Defining a PUT or PATCH route (update)**

Equivalent to `@PutMapping` or `@PatchMapping`.

```python
@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, task_data: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_data.dict().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task
```

---

#### **6. Defining a DELETE route**

Equivalent to `@DeleteMapping`.

```python
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
```

---

#### **7. Mounting Routers to the Main App**

In your main application (`main.py`), include the router:

```python
from fastapi import FastAPI
from app.routes import task_router

app = FastAPI()
app.include_router(task_router.router)
```

This works like adding `@RequestMapping("/tasks")` in Spring Boot, organizing all task-related routes under one controller.

---

In **Spring Boot**, database sessions and transactions are managed automatically by the framework — each request gets its own session from a connection pool (like HikariCP), and transactions are handled transparently through annotations like `@Transactional`. You rarely open or close sessions manually.

In **FastAPI**, you explicitly define how sessions are created and closed using a dependency (e.g. `get_db()`), which opens a new SQLAlchemy session for each request and closes it afterward. Transactions and commits are handled manually with `db.commit()`.

In short, Spring Boot is **opinionated and automatic**, while FastAPI is **explicit and developer-controlled** in how it manages DB sessions and transactions.

---



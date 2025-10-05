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



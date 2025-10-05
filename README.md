## DATE : 5 Oct, 2025

### FastAPI vs SpringBoot

- in spring boot I used `Spring Initializr` to make the projects, add depenencies from there or maven vs for fastapi i can use direct `pip` to install `fastapi` in a normal project structure and use `uvicorn` to start the server
- in PyCharm make a new project, the projects are made in a virtual env so that this project dependencies dont mix with the other project dependencies
- write a simple app.py and run using `uvicorn main:app --reload`
- project structure similar to Spring Boot

## Sample Project of a FastAPI backend
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

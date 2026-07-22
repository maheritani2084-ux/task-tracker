# Mini ADR: Architecture Comparison for the Task Tracker Learning Project

## Context

Two lightweight architecture options were considered for the Task Tracker application:

- Option A: a simple JSON-file-based backend with FastAPI and a vanilla frontend
- Option B: a lightweight local-database approach using FastAPI with SQLite and SQLAlchemy

The goal is to keep the project easy to understand, easy to run locally, and suitable for a learning-focused implementation of due dates, tags, and task CRUD.

## Comparison

### 1. Simplicity

Option A is simpler in both implementation and maintenance. It uses fewer moving parts, avoids schema management, and keeps the codebase easy to follow for someone learning FastAPI. The main weakness is that the storage layer becomes a custom file-handling module that must manage reads, writes, and consistency carefully.

Option B is a bit more complex because it introduces ORM concepts, database setup, and a more structured persistence layer. That added complexity can be valuable for realism, but it also means more code to understand and maintain. Its weakness is that the extra abstraction may distract from the core learning goals if the project stays small.

### 2. Testability

Option A is straightforward to test with pytest and FastAPI TestClient because the API can be exercised without needing a database engine. The downside is that tests may need to be more careful around file state and cleanup, since JSON storage is shared on disk.

Option B is also testable, and the database layer can make some behaviors feel more realistic. However, it introduces more setup overhead for tests, especially if the test suite needs to reset the database between cases. Its weakness is that the test environment becomes slightly less lightweight than Option A.

### 3. Local run/deploy ability

Option A is easiest to run locally with one or two commands. A developer can start the backend and open the frontend without needing a database service or initialization steps beyond installing Python dependencies.

Option B is still easy to run locally, but it requires a slightly more involved setup story: the app needs a local SQLite database file and the relevant ORM configuration. That is still very manageable, but it is less frictionless than Option A.

### 4. Familiarity

Option A uses very common tools for a Python learning project: FastAPI, Pydantic, and plain JSON storage. It is highly understandable for an intermediate developer and fits the spirit of a simple local project.

Option B uses tools that are also common, but they are a bit more framework-heavy and may be less immediately intuitive for someone who is still focused on learning FastAPI basics. Its weakness is that SQLAlchemy and database modeling add another layer of concepts that may feel heavier than necessary for this scope.

## Notes on the trade-off

Option A is the more lightweight and beginner-friendly path. Option B can make the project feel more realistic, but it adds more architectural overhead for a small app.

## Rejected and chosen options

- Rejected option: Option B
- Chosen option: Option A

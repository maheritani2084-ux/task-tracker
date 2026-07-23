# Mid-Course Project Guide

This project is a simple task tracker with a FastAPI backend and a vanilla HTML/JavaScript frontend.

## Run the backend

From the project root, start the backend with:

```bash
c:/task-tracker/venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/tasks

## Open the frontend

The frontend is served by the FastAPI app. Open the app in a browser at:

```text
http://127.0.0.1:8000/
```

If you want to serve the static frontend directly, you can also run:

```bash
c:/task-tracker/venv/Scripts/python.exe -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500/frontend/
```

## Run tests

Run the full tag and frontend test suite with:

```bash
c:/task-tracker/venv/Scripts/python.exe -m pytest -q tests/test_tags.py tests/test_frontend.py
```

Run the backend tag tests only with:

```bash
c:/task-tracker/venv/Scripts/python.exe -m pytest -q tests/test_tags.py
```

Run the full project test suite with:

```bash
c:/task-tracker/venv/Scripts/python.exe -m pytest -q
```

## Notes

- The backend must be running before opening the frontend through the FastAPI app.
- If you use the static server for the frontend, the API requests still need the backend running on port 8000.
- [docs/mid-course/mini-adr.md](docs/mid-course/mini-adr.md)
- [docs/mid-course/user-stories.md](docs/mid-course/user-stories.md)


\# Task Tracker API — Module 1



A learning-project REST API built with Python and FastAPI. Module 1 provides

the project skeleton and a single health-check endpoint. Task CRUD, filtering,

and JSON file storage are added in later modules per ADR-001.



\## Requirements



\- Python 3.11 or newer



\## Setup



Clone or create the project, then from the `task-tracker/` directory create and

activate a virtual environment and install dependencies.



\*\*Linux / macOS (bash):\*\*



```bash

python3 -m venv venv

source venv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

```



\*\*Windows (PowerShell):\*\*



```powershell

python -m venv venv

.\\venv\\Scripts\\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

```



After installing, verify the resolved versions:



```bash

pip freeze

```



Optionally copy the example environment file:



```bash

cp .env.example .env      # Windows PowerShell: Copy-Item .env.example .env

```



\## Run



```bash

uvicorn app.main:app --reload

```



The server starts at `http://127.0.0.1:8000`.



\## Test the health endpoint



```bash

curl http://127.0.0.1:8000/health

```



Expected response (HTTP 200); the timestamp reflects the current UTC time:



```json

{ "status": "ok", "timestamp": "2026-07-05T12:34:56.789+00:00" }

```



\## Interactive API docs (Swagger)



With the server running, open:



```

http://127.0.0.1:8000/docs

```



The auto-generated Swagger UI lists the available endpoints. ReDoc is also

available at `http://127.0.0.1:8000/redoc`.


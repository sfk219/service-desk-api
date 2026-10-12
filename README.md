# Service Desk API

A runnable **database-driven ticket-management REST API** built with Python, FastAPI, Pydantic and SQLite. Endpoints support validated ticket creation, listing/filtering, retrieving, status updates and deletion.

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation. SQLite database is created automatically under `data/`.

## Example
```bash
curl -X POST http://localhost:8000/tickets -H "Content-Type: application/json" -d '{"title":"Fix staging alert","category":"platform","priority":"high"}'
curl http://localhost:8000/tickets
```

## Tests and Docker
```bash
pip install -r requirements-dev.txt
pytest -q
docker build -t service-desk-api .
docker run -p 8000:8000 service-desk-api
```

**Portfolio demo**, no real customer or employer data.
# Runbook
```bash
cp .env.example .env
docker compose up --build -d
curl http://localhost:8000/health
curl http://localhost:8000/v1/capabilities -H 'x-api-key: change-me'
curl -X POST http://localhost:8000/v1/goals -H 'x-api-key: change-me' -H 'Content-Type: application/json' --data-binary @examples/marketing_goal.json
pytest -q
ruff check .
docker compose logs -f api
docker compose down
```

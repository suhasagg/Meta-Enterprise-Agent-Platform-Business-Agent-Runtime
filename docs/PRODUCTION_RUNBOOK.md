# Production Runbook

## Local startup
```bash
cp .env.example .env
docker compose build
docker compose up -d
docker compose ps
curl http://localhost:8000/health
```

## Exercise platform
```bash
curl http://localhost:8000/v1/capabilities -H 'x-api-key: change-me'
curl -X POST http://localhost:8000/v1/goals -H 'x-api-key: change-me' -H 'Content-Type: application/json' --data-binary @examples/marketing_goal.json
```

## Database
```bash
docker compose exec postgres psql -U postgres -d agents
```

## Logs
```bash
docker compose logs -f api
docker compose logs -f postgres
docker compose logs -f redis
```

## Tests
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
ruff check .
```

## Incident principles
Preserve durable state, stop unsafe dispatch, fence stale workers, reconcile ambiguous external actions, resume only idempotent/safe work, and preserve audit evidence.

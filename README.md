# grok-watch

Governed Grok → Apple Watch bridge: watchOS SwiftUI, iOS host, FastAPI gateway, JWT, PostgreSQL audit logging, App Intents, complications, and integration tests.

## Status
Foundation scaffold (2026-09-16). Gateway stub is runnable; Apple targets are placeholders pending Xcode.

`gh_login=LevelUpWorldHub` · `owner/name=LevelUpWorldHub/grok-watch`

## Gateway quickstart
```bash
cd gateway
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8080
pytest -q
```

Health: `GET /health`  
Dev token: `POST /v1/dev/token`  
Relay: `POST /v1/relay` (Bearer JWT)  
Audit: `GET /v1/audit` (Bearer JWT)

## Docs
See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

# grok-watch architecture (foundation)

```
watchOS SwiftUI  →  iOS host (App Intents)  →  FastAPI gateway (JWT)  →  Grok / tools
                                         ↘ PostgreSQL audit
```

## Rules
- Watch never holds long-lived cloud secrets; host mints short JWT.
- Every relay is audited (`actor`, `action`, `resource`, `meta`).
- Production disables `/v1/dev/token`; use real IdP.

## Layout
- `gateway/` — FastAPI service + tests + Dockerfile
- `ios/GrokWatchHost/` — iOS host placeholder
- `watchos/GrokWatchApp/` — watchOS placeholder

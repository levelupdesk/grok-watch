"""FastAPI entry — health, auth mint (dev), governed relay stub, audit list."""
from __future__ import annotations

from typing import Any

from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field

from .audit import AuditEvent, audit_store
from .auth import mint_dev_token, require_jwt
from .config import settings

app = FastAPI(title=settings.app_name, version="0.1.0")


class RelayRequest(BaseModel):
    intent: str = Field(..., min_length=1, max_length=128)
    payload: dict[str, Any] = Field(default_factory=dict)


class RelayResponse(BaseModel):
    accepted: bool
    intent: str
    audit_id: str
    note: str


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name, "env": settings.env}


@app.post("/v1/dev/token")
async def dev_token(sub: str = "watch-dev") -> dict[str, str]:
    """Dev-only token mint. Disable in production."""
    if settings.env == "prod":
        return {"error": "disabled_in_prod"}
    return {"access_token": mint_dev_token(sub), "token_type": "bearer"}


@app.post("/v1/relay", response_model=RelayResponse)
async def relay(body: RelayRequest, claims: dict[str, Any] = Depends(require_jwt)) -> RelayResponse:
    event = await audit_store.record(
        AuditEvent(
            actor=str(claims.get("sub", "unknown")),
            action="relay",
            resource=body.intent,
            meta={"roles": claims.get("roles", []), "keys": sorted(body.payload.keys())},
            ok=True,
        )
    )
    return RelayResponse(
        accepted=True,
        intent=body.intent,
        audit_id=event.id,
        note="governed_stub_accepted_no_side_effects",
    )


@app.get("/v1/audit")
async def list_audit(claims: dict[str, Any] = Depends(require_jwt), limit: int = 50) -> list[AuditEvent]:
    _ = claims
    return await audit_store.list(limit=min(limit, 200))

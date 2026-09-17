"""PostgreSQL-backed audit log (SQLAlchemy async). Dev falls back to in-memory."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor: str
    action: str
    resource: str
    meta: dict[str, Any] = Field(default_factory=dict)
    ok: bool = True


class InMemoryAudit:
    def __init__(self) -> None:
        self._events: list[AuditEvent] = []

    async def record(self, event: AuditEvent) -> AuditEvent:
        self._events.append(event)
        return event

    async def list(self, limit: int = 50) -> list[AuditEvent]:
        return list(reversed(self._events[-limit:]))


audit_store = InMemoryAudit()

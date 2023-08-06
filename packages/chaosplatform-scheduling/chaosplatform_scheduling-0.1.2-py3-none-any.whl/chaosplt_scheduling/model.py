from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID

import attr

__all__ = ["Schedule"]


@attr.s
class Schedule:
    id: UUID = attr.ib()
    user_id: UUID = attr.ib()
    org_id: UUID = attr.ib()
    workspace_id: UUID = attr.ib()
    experiment_id: UUID = attr.ib()
    token_id: UUID = attr.ib()
    scheduled: datetime = attr.ib()
    status: str = attr.ib()
    job_id: UUID = attr.ib(default=None)
    repeat: int = attr.ib(default=None)
    interval: int = attr.ib(default=None)
    cron: str = attr.ib(default=None)
    settings: Dict[str, Any] = attr.ib(default=None)
    configuration: Dict[str, Any] = attr.ib(default=None)
    secrets: Dict[str, Any] = attr.ib(default=None)
    results: List[Dict[str, Any]] = attr.ib(default=None)

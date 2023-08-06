# -*- coding: utf-8 -*-
from enum import Enum
from typing import Any, List, NoReturn, Union
import uuid
from uuid import UUID

from chaosplt_relational_storage.db import Base, get_secret_key
from dateparser import parse
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy import Enum as EnumType
from sqlalchemy.orm.session import Session
from sqlalchemy_utils import EncryptedType, UUIDType
from sqlalchemy_utils import JSONType as JSONB
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine

__all__ = ["Schedule"]


class ScheduleStatus(Enum):
    created = "created"
    pending = "pending"
    active = "active"
    completed = "completed"
    cancelled = "cancelled"
    aborted = "aborted"
    retry = "retry"
    unknown = "unknown"

    @staticmethod
    def is_valid_status(schedule_type: str) -> bool:
        return schedule_type in (
            ScheduleStatus.created.value,
            ScheduleStatus.pending.value,
            ScheduleStatus.active.value,
            ScheduleStatus.completed.value,
            ScheduleStatus.cancelled.value,
            ScheduleStatus.aborted.value,
            ScheduleStatus.retry.value,
            ScheduleStatus.unknown.value
        )

    @staticmethod
    def get_status(schedule_type: str) -> 'ScheduleStatus':
        if schedule_type == ScheduleStatus.created.value:
            return ScheduleStatus.created

        if schedule_type == ScheduleStatus.pending.value:
            return ScheduleStatus.pending

        if schedule_type == ScheduleStatus.active.value:
            return ScheduleStatus.active

        if schedule_type == ScheduleStatus.completed.value:
            return ScheduleStatus.completed

        if schedule_type == ScheduleStatus.cancelled.value:
            return ScheduleStatus.cancelled

        if schedule_type == ScheduleStatus.aborted.value:
            return ScheduleStatus.aborted

        if schedule_type == ScheduleStatus.retry.value:
            return ScheduleStatus.retry

        if schedule_type == ScheduleStatus.unknown.value:
            return ScheduleStatus.unknown


class Schedule(Base):  # type: ignore
    __tablename__ = "schedule"

    id = Column(
        UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUIDType(binary=False), nullable=False, index=True)
    org_id = Column(
        UUIDType(binary=False), nullable=False, index=True)
    workspace_id = Column(
        UUIDType(binary=False), nullable=False, index=True)
    experiment_id = Column(
        UUIDType(binary=False), nullable=False, index=True)
    token_id = Column(UUIDType(binary=False), nullable=False)
    job_id = Column(UUIDType(binary=False), nullable=True)
    scheduled = Column(DateTime(), nullable=False)
    repeat = Column(Integer, nullable=True)
    interval = Column(Integer, nullable=True)
    cron = Column(String, nullable=True)
    status = Column(EnumType(ScheduleStatus), default=ScheduleStatus.unknown)
    results = Column(EncryptedType(JSONB, get_secret_key, AesEngine, 'pkcs5'))
    settings = Column(EncryptedType(JSONB, get_secret_key, AesEngine, 'pkcs5'))
    configuration = Column(
        EncryptedType(JSONB, get_secret_key, AesEngine, 'pkcs5'))
    secrets = Column(EncryptedType(JSONB, get_secret_key, AesEngine, 'pkcs5'))

    @staticmethod
    def load(user_id: Union[UUID, str], schedule_id: Union[UUID, str],
             session: Session) -> 'Schedule':
        return session.query(Schedule).\
            filter_by(id=schedule_id).\
            filter_by(user_id=user_id).first()

    @staticmethod
    def load_by_user(user_id: Union[UUID, str],
                     session: Session) -> List['Schedule']:
        return session.query(Schedule).\
            filter_by(user_id=user_id).all()

    @staticmethod
    def create(user_id: Union[UUID, str], org_id: Union[UUID, str],
               workspace_id: Union[UUID, str], experiment_id: Union[UUID, str],
               token_id: Union[UUID, str], scheduled_at: str, repeat: int,
               interval: int, cron: str, settings: Any, configuration: Any,
               secrets: Any, session: Session) -> 'Schedule':

        scheduled = parse(scheduled_at)
        schedule = Schedule(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            status=ScheduleStatus.created,
            scheduled=scheduled,
            repeat=repeat or None,
            interval=interval or None,
            cron=cron or None,
            settings=settings,
            configuration=configuration,
            secrets=secrets
        )
        session.add(schedule)
        return schedule

    @staticmethod
    def delete(schedule_id: Union[UUID, str], session: Session) -> NoReturn:
        schedule = session.query(Schedule).filter_by(
            id=schedule_id).first()

        if schedule:
            session.delete(schedule)

    @staticmethod
    def set_job_id(schedule_id: Union[UUID, str], job_id: Union[UUID, str],
                   session: Session) -> NoReturn:
        schedule = session.query(Schedule).filter_by(
            id=schedule_id).first()
        schedule.job_id = job_id

    @staticmethod
    def set_status(schedule_id: Union[UUID, str], status: ScheduleStatus,
                   session: Session) -> NoReturn:
        schedule = session.query(Schedule).filter_by(
            id=schedule_id).first()
        schedule.status = status

    @staticmethod
    def list_by_state(status: ScheduleStatus,
                      session: Session) -> List['Schedule']:
        return session.query(Schedule).filter_by(status=status).all()

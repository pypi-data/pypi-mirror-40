from typing import Any, List, NoReturn, Union
from uuid import UUID

from chaosplt_scheduling.model import Schedule
from chaosplt_relational_storage import RelationalStorage
from chaosplt_relational_storage.db import orm_session

from .interface import BaseSchedulingService
from .model import ScheduleStatus, Schedule as ScheduleModel


class SchedulingService(BaseSchedulingService):
    def __init__(self, driver: RelationalStorage):
        self.driver = driver

    def get(self, user_id: Union[UUID, str],
            schedule_id: Union[UUID, str]) -> Schedule:
        with orm_session() as session:
            schedule = ScheduleModel.load(
                user_id, schedule_id, session=session)
            if not schedule:
                return

            return Schedule(
                id=schedule.id,
                user_id=schedule.user_id,
                org_id=schedule.org_id,
                workspace_id=schedule.workspace_id,
                experiment_id=schedule.experiment_id,
                token_id=schedule.token_id,
                status=schedule.status.value,
                scheduled=schedule.scheduled,
                repeat=schedule.repeat,
                interval=schedule.interval,
                cron=schedule.cron,
                settings=schedule.settings,
                configuration=schedule.configuration,
                secrets=schedule.secrets,
                results=schedule.results
            )

    def create(self, user_id: Union[UUID, str], org_id: Union[UUID, str],
               workspace_id: Union[UUID, str], experiment_id: Union[UUID, str],
               token_id: Union[UUID, str], scheduled_at: str,
               interval: int = None, repeat: int = None, cron: str = None,
               settings: Any = None, configuration: Any = None,
               secrets: Any = None) -> Schedule:
        with orm_session() as session:
            schedule = ScheduleModel.create(
                user_id, org_id, workspace_id, experiment_id, token_id,
                scheduled_at, interval=interval, repeat=repeat, cron=cron,
                settings=settings, configuration=configuration,
                secrets=secrets, session=session)
            session.flush()

            return Schedule(
                id=schedule.id,
                user_id=schedule.user_id,
                org_id=schedule.org_id,
                workspace_id=schedule.workspace_id,
                experiment_id=schedule.experiment_id,
                token_id=schedule.token_id,
                status=schedule.status.value,
                scheduled=schedule.scheduled,
                repeat=schedule.repeat,
                interval=schedule.interval,
                cron=schedule.cron,
                settings=schedule.settings,
                configuration=schedule.configuration,
                secrets=schedule.secrets
            )

    def delete(self, schedule_id: Union[UUID, str]) -> NoReturn:
        with orm_session() as session:
            ScheduleModel.delete(schedule_id, session=session)

    def get_by_user(self, user_id: Union[UUID, str]) -> List[Schedule]:
        with orm_session() as session:
            schedules = []

            candidates = ScheduleModel.load_by_user(
                user_id, session=session)
            for schedule in candidates:
                schedules.append(
                    Schedule(
                        id=schedule.id,
                        user_id=schedule.user_id,
                        org_id=schedule.org_id,
                        workspace_id=schedule.workspace_id,
                        experiment_id=schedule.experiment_id,
                        token_id=schedule.token_id,
                        status=schedule.status.value,
                        scheduled=schedule.scheduled,
                        repeat=schedule.repeat,
                        interval=schedule.interval,
                        cron=schedule.cron,
                        settings=schedule.settings,
                        configuration=schedule.configuration,
                        secrets=schedule.secrets,
                        results=schedule.results
                    )
                )
            return schedules

    def job_started(self, schedule_id: Union[UUID, str],
                    job_id: Union[UUID, str]) -> NoReturn:
        with orm_session() as session:
            ScheduleModel.set_status(
                schedule_id, ScheduleStatus.pending, session=session)
            ScheduleModel.set_job_id(schedule_id, job_id, session=session)

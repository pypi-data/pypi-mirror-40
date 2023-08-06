import uuid
from uuid import UUID

from chaosplt_scheduling.storage.model import Schedule, ScheduleStatus
from chaosplt_relational_storage.db import orm_session


def test_save_schedule(user_id: UUID, org_id: UUID, workspace_id: UUID,
                       experiment_id: UUID, token_id: UUID, scheduled: str):
    with orm_session() as session:
        sched = Schedule.create(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            scheduled_at=scheduled,
            interval=None,
            cron=None,
            repeat=None,
            settings=None,
            configuration=None,
            secrets=None,
            session=session
        )
        session.commit()
        assert uuid.UUID(hex=sched.id.hex) == sched.id
        assert sched.status == ScheduleStatus.created


def test_get_schedule(user_id: UUID, org_id: UUID, workspace_id: UUID,
                      experiment_id: UUID, token_id: UUID, scheduled: str):
    with orm_session() as session:
        sched = Schedule.create(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            scheduled_at=scheduled,
            interval=None,
            cron=None,
            repeat=None,
            settings=None,
            configuration=None,
            secrets=None,
            session=session
        )
        session.commit()

        fetched_sched = Schedule.load(user_id, sched.id, session)
        assert sched == fetched_sched


def test_get_schedule_for_user(user_id: UUID, org_id: UUID, workspace_id: UUID,
                               experiment_id: UUID, token_id: UUID,
                               scheduled: str):
    with orm_session() as session:
        sched = Schedule.create(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            scheduled_at=scheduled,
            interval=None,
            cron=None,
            repeat=None,
            settings=None,
            configuration=None,
            secrets=None,
            session=session
        )
        session.commit()

        fetched_scheds = Schedule.load_by_user(user_id, session)
        assert len(fetched_scheds) == 1
        assert sched == fetched_scheds[0]


def test_delete_schedule(user_id: UUID, org_id: UUID, workspace_id: UUID,
                         experiment_id: UUID, token_id: UUID,
                         scheduled: str):
    with orm_session() as session:
        sched = Schedule.create(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            scheduled_at=scheduled,
            interval=None,
            cron=None,
            repeat=None,
            settings=None,
            configuration=None,
            secrets=None,
            session=session
        )
        session.commit()

        fetched_sched = Schedule.load(user_id, sched.id, session)
        assert sched == fetched_sched

        Schedule.delete(sched.id, session)
        fetched_sched = Schedule.load(user_id, sched.id, session)
        assert fetched_sched == None


def test_set_job_id(user_id: UUID, org_id: UUID, workspace_id: UUID,
                    experiment_id: UUID, token_id: UUID,
                    scheduled: str):
    with orm_session() as session:
        sched = Schedule.create(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            scheduled_at=scheduled,
            interval=None,
            cron=None,
            repeat=None,
            settings=None,
            configuration=None,
            secrets=None,
            session=session
        )
        session.commit()

        before_job_id = sched.job_id

        fetched_sched = Schedule.load(user_id, sched.id, session)
        assert sched == fetched_sched

        job_id = uuid.uuid4()
        Schedule.set_job_id(sched.id, job_id, session)
        session.commit()

        fetched_sched = Schedule.load(user_id, sched.id, session)
        assert before_job_id != fetched_sched.job_id


def test_set_status(user_id: UUID, org_id: UUID, workspace_id: UUID,
                    experiment_id: UUID, token_id: UUID,
                    scheduled: str):
    with orm_session() as session:
        sched = Schedule.create(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            scheduled_at=scheduled,
            interval=None,
            cron=None,
            repeat=None,
            settings=None,
            configuration=None,
            secrets=None,
            session=session
        )
        session.commit()

        before_status = sched.status

        fetched_sched = Schedule.load(user_id, sched.id, session)
        assert sched == fetched_sched

        job_id = uuid.uuid4()
        Schedule.set_status(sched.id, ScheduleStatus.completed, session)
        session.commit()

        fetched_sched = Schedule.load(user_id, sched.id, session)
        assert before_status != fetched_sched.status
        assert fetched_sched.status == ScheduleStatus.completed


def test_list_by_state(user_id: UUID, org_id: UUID, workspace_id: UUID,
                       experiment_id: UUID, token_id: UUID,
                       scheduled: str):
    with orm_session() as session:
        sched1 = Schedule.create(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            scheduled_at=scheduled,
            interval=None,
            cron=None,
            repeat=None,
            settings=None,
            configuration=None,
            secrets=None,
            session=session
        )
        sched2 = Schedule.create(
            user_id=user_id,
            org_id=org_id,
            workspace_id=workspace_id,
            experiment_id=experiment_id,
            token_id=token_id,
            scheduled_at=scheduled,
            interval=None,
            cron=None,
            repeat=None,
            settings=None,
            configuration=None,
            secrets=None,
            session=session
        )
        sched2.status = ScheduleStatus.retry
        session.commit()

        scheds = Schedule.list_by_state(ScheduleStatus.created, session)
        assert len(scheds) == 1
        assert scheds[0] == sched1

        scheds = Schedule.list_by_state(ScheduleStatus.retry, session)
        assert len(scheds) == 1
        assert scheds[0] == sched2

        scheds = Schedule.list_by_state(ScheduleStatus.completed, session)
        assert len(scheds) == 0

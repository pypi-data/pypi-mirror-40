from abc import ABC, abstractmethod
from typing import Any, List, NoReturn, Union
from uuid import UUID

from chaosplt_scheduling.model import Schedule

__all__ = ["BaseSchedulingService", "BaseSchedulingStorage"]


class BaseSchedulingService(ABC):
    @abstractmethod
    def get(self, user_id: Union[UUID, str],
            schedule_id: Union[UUID, str]) -> Schedule:
        """
        Lookup a schedule by its identifier for the given user
        """
        return self.load(user_id, schedule_id)

    @abstractmethod
    def create(self, user_id: Union[UUID, str], org_id: Union[UUID, str],
               workspace_id: Union[UUID, str], experiment_id: Union[UUID, str],
               token_id: Union[UUID, str], scheduled_at: str,
               interval: int = None, repeat: int = None, cron: str = None,
               settings: Any = None, configuration: Any = None,
               secrets: Any = None) -> Schedule:
        """
        Create a new schedule with the given context

        Return the new schedule
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, schedule_id: Union[UUID, str]) -> NoReturn:
        """
        Delete a schedule
        """
        raise NotImplementedError()

    @abstractmethod
    def get_by_user(self, user_id: Union[UUID, str]) -> List[Schedule]:
        """
        Get all schedules created by a given user
        """
        raise NotImplementedError()

    @abstractmethod
    def job_started(self, schedule_id: Union[UUID, str],
                    job_id: Union[UUID, str]) -> NoReturn:
        """
        Mark the job's status as started
        """
        raise NotImplementedError()


class BaseSchedulingStorage:
    def release(self) -> NoReturn:
        raise NotImplementedError()

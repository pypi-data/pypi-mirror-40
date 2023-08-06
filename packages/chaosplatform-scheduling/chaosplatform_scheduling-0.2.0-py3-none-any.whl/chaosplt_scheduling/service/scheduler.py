from datetime import datetime
from typing import Any

from chaosplt_grpc import remote_channel
from chaosplt_grpc.scheduler.client import schedule_experiment, \
    cancel_experiment

__all__ = ["SchedulerService"]


class SchedulerService:
    def __init__(self, config):
        grpc_config = config["grpc"]["scheduler"]
        self.scheduler_addr = grpc_config["address"]

    def release(self):
        pass

    def schedule(self, schedule_id: str, user_id: str, org_id: str,
                 workspace_id: str, experiment_id: str, token_id: str,
                 token: str, scheduled: datetime, experiment: Any,
                 interval: int, repeat: int, cron: str, settings: Any,
                 configuration: Any, secrets: Any) -> str:
        """
        Schedule a new execution with the given context

        Return the job identifier for the execution.
        """
        with remote_channel(self.scheduler_addr) as channel:
            return schedule_experiment(
                channel, schedule_id, user_id, org_id, workspace_id,
                experiment_id, token_id, token, scheduled, experiment,
                interval, repeat, cron, settings, configuration, secrets)

    def cancel(self, job_id: str):
        """
        Cancel the given job so that future executions do not take place.
        """
        with remote_channel(self.scheduler_addr) as channel:
            return cancel_experiment(channel, job_id)

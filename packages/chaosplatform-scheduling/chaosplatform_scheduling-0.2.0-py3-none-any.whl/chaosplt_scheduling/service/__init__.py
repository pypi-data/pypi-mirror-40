from typing import Any, Dict

import attr

from .scheduler import SchedulerService


__all__ = ["initialize_services", "shutdown_services", "Services"]


@attr.s
class Services:
    scheduler: object = attr.ib(default=None)


def initialize_services(services: Services, config: Dict[str, Any]):
    """
    Create and initialize services access:

    * scheduler
    """
    if not services.scheduler:
        services.scheduler = SchedulerService(config)


def shutdown_services(services: Services):
    """
    Release resources used by the services.

    They should not be assumed to be functional after this call.
    """
    if services.scheduler:
        services.scheduler.release()

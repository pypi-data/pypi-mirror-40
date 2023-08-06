from typing import Any, Dict, NoReturn

from chaosplt_relational_storage import get_storage, \
    configure_storage, release_storage
import pkg_resources

from .concrete import SchedulingService
from .interface import BaseSchedulingStorage

__all__ = ["initialize_storage", "shutdown_storage", "SchedulingStorage"]


class SchedulingStorage(BaseSchedulingStorage, SchedulingService):
    def __init__(self, config: Dict[str, Any]):
        BaseSchedulingStorage.__init__(self)

        driver = get_storage(config)
        configure_storage(driver)
        SchedulingService.__init__(self, driver)

    def release(self) -> NoReturn:
        """
        Release the resources used by the scheduling storage

        Do not use the storage after this method has been called.
        """
        release_storage(self.driver)


def initialize_storage(config: Dict[str, Any]) -> SchedulingStorage:
    """
    Initialize the storage.

    Look first for any plugin implementing the `'chaosplatform.storage'`
    entrypoint group and load it if any is found for the `"scheduling"` name.

    Otherwise, create an instance of `SchedulingStorage` from this module.
    """
    for plugin in pkg_resources.iter_entry_points('chaosplatform.storage'):
        if plugin.name == "scheduling":
            service_class = plugin.load()
            return service_class(config)

    return SchedulingStorage(config)


def shutdown_storage(storage: SchedulingStorage) -> NoReturn:
    """
    Release all resources used by the scheduling storage
    """
    storage.release()

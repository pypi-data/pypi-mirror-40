import os
import sys

from pkg_resources import Distribution, EntryPoint, iter_entry_points, \
    working_set

from chaosplt_scheduling.storage import initialize_storage, shutdown_storage


def test_loading_external_storage_implementation():
    try:
        distribution = Distribution(os.path.join(
                os.path.dirname(__file__), "fixtures"))
        entry_point = EntryPoint.parse(
            'scheduling = fake_storage:MySchedulingStorage', dist=distribution)
        distribution._ep_map = {
            'chaosplatform.storage': {'scheduling': entry_point}}
        working_set.add(distribution)

        storage = initialize_storage(config={"db":{"uri": "sqlite:///"}})
        assert storage.__class__.__name__ == "MySchedulingStorage"
        assert storage.some_flag == True

        shutdown_storage(storage)
        assert storage.some_flag == False

    finally:
        distribution._ep_map.clear()

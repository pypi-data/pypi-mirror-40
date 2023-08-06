import pytest

from chaosplt_scheduling.storage.interface import BaseSchedulingService

def test_cannot_instanciate_scheduling_interface():
    try:
        BaseSchedulingService()
    except TypeError as e:
        return
    else:
        pytest.fail("BaseSchedulingService should remain abstract")

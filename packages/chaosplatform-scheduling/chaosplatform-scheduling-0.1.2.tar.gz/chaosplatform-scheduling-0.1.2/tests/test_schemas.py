from collections import OrderedDict
from typing import Dict
from uuid import UUID

from chaosplt_scheduling.schemas import upload_scheduling_schema


def test_scheduling_request(scheduling: Dict[str, str]):
    s = upload_scheduling_schema.load(scheduling)
    assert str(s["org"]) == scheduling["org"]
    assert str(s["workspace"]) == scheduling["workspace"]
    assert str(s["token"]) == scheduling["token"]
    assert str(s["experiment"]) == scheduling["experiment"]
    assert "repeat" not in s
    assert "interval" not in s
    assert "cron" not in s
    assert "settings" not in s
    assert "configuration" not in s
    assert "secrets" not in s


def test_cron_scheduling_request(scheduling: Dict[str, str]):
    scheduling["cron"] = "* 8 * * *"
    s = upload_scheduling_schema.load(scheduling)
    assert str(s["org"]) == scheduling["org"]
    assert str(s["workspace"]) == scheduling["workspace"]
    assert str(s["token"]) == scheduling["token"]
    assert str(s["experiment"]) == scheduling["experiment"]
    assert s["cron"] == "* 8 * * *"
    assert "repeat" not in s
    assert "interval" not in s
    assert "settings" not in s
    assert "configuration" not in s
    assert "secrets" not in s


def test_cron_scheduling_with_repeat_request(scheduling: Dict[str, str]):
    scheduling["cron"] = "* 8 * * *"
    scheduling["repeat"] = 5
    s = upload_scheduling_schema.load(scheduling)
    assert str(s["org"]) == scheduling["org"]
    assert str(s["workspace"]) == scheduling["workspace"]
    assert str(s["token"]) == scheduling["token"]
    assert str(s["experiment"]) == scheduling["experiment"]
    assert s["cron"] == "* 8 * * *"
    assert s["repeat"] == 5
    assert "interval" not in s
    assert "settings" not in s
    assert "configuration" not in s
    assert "secrets" not in s


def test_interval_scheduling_request(scheduling: Dict[str, str]):
    scheduling["interval"] = 10
    s = upload_scheduling_schema.load(scheduling)
    assert str(s["org"]) == scheduling["org"]
    assert str(s["workspace"]) == scheduling["workspace"]
    assert str(s["token"]) == scheduling["token"]
    assert str(s["experiment"]) == scheduling["experiment"]
    assert s["interval"] == 10
    assert "repeat" not in s
    assert "cron" not in s
    assert "settings" not in s
    assert "configuration" not in s
    assert "secrets" not in s


def test_interval_with_repeat_scheduling_request(scheduling: Dict[str, str]):
    scheduling["interval"] = 10
    scheduling["repeat"] = 4
    s = upload_scheduling_schema.load(scheduling)
    assert str(s["org"]) == scheduling["org"]
    assert str(s["workspace"]) == scheduling["workspace"]
    assert str(s["token"]) == scheduling["token"]
    assert str(s["experiment"]) == scheduling["experiment"]
    assert s["interval"] == 10
    assert s["repeat"] == 4
    assert "cron" not in s
    assert "settings" not in s
    assert "configuration" not in s
    assert "secrets" not in s

import json

from corticalloop.types import RunRecord


def test_runrecord_json_serialization():
    record = RunRecord(task="x")
    payload = json.loads(record.to_json())
    assert payload["task"] == "x"
    assert "iterations" in payload

import datetime
import decimal
import json
import uuid

import pytest

from cms_forms.importer import TypeReference
from cms_forms.json import CustomJSONEncoder, CustomJSONDecoder


example_data = {
    "str": "",
    "int": 1,
    "float": 1.1,
    "true": True,
    "false": False,
    "none": None,
    "dict": {"extra_test": decimal.Decimal("1.1"), "extra_list": [decimal.Decimal("2.1"),],},
    "list": [{"extra_dict": decimal.Decimal("3.1"),}, decimal.Decimal("4.1"),],
    "datetime": datetime.datetime(2020, 1, 1, 1, 1, 1),
    "date": datetime.date(2020, 1, 1),
    "time": datetime.time(1, 1, 1),
    "timedelta": datetime.timedelta(days=1),
    "decimal": decimal.Decimal("11.1"),
    "uuid": uuid.UUID("7a8b6b6f-beda-4e42-be1a-60a718285d57"),
    "typereference": TypeReference(uuid.UUID),
    "type": datetime.datetime,
    "spoof1": {"__type__": "asdf"},
    "spoof2": {"__value__": "asdf"},
}
example_data_str = """
{
    "str": "",
    "int": 1,
    "float": 1.1,
    "true": true,
    "false": false,
    "none": null,
    "dict": {
        "extra_test": {"__type__": "decimal", "__value__": "1.1"},
        "extra_list": [
            {"__type__": "decimal", "__value__": "2.1"}
        ]
    },
    "list": [
        {
            "extra_dict": {"__type__": "decimal", "__value__": "3.1"}
        },
        {"__type__": "decimal", "__value__": "4.1"}
    ],
    "datetime": {"__type__": "datetime", "__value__": "2020-01-01T01:01:01"},
    "date": {"__type__": "date", "__value__": "2020-01-01"},
    "time": {"__type__": "time", "__value__": "01:01:01"},
    "timedelta": {"__type__": "timedelta", "__value__": 86400.0},
    "decimal": {"__type__": "decimal", "__value__": "11.1"},
    "uuid": {"__type__": "uuid", "__value__": "7a8b6b6f-beda-4e42-be1a-60a718285d57"},
    "typereference": {"__type__": "typereference", "__value__": "uuid.UUID"},
    "type": {"__type__": "type", "__value__": "datetime.datetime"},
    "spoof1": {"__type__": "asdf"},
    "spoof2": {"__value__": "asdf"}
}
"""
example_data_str_clean = json.dumps(json.loads(example_data_str))


class MyClass:
    pass


def test_json_encoder():
    res = json.dumps(example_data, cls=CustomJSONEncoder)
    assert res == example_data_str_clean
    assert json.dumps([1], cls=CustomJSONEncoder) == "[1]"
    with pytest.raises(TypeError):
        json.dumps([MyClass()], cls=CustomJSONEncoder)


def test_json_decoder():
    res = json.loads(example_data_str, cls=CustomJSONDecoder)
    assert res == example_data
    assert json.loads("[1]", cls=CustomJSONDecoder) == [1]

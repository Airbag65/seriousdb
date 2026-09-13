import pytest
from pathlib import Path
from seriousdb.configuration import (
    Configuration,
    MalformedConfigurationWarning,
    get_configuration,
)


def test_default():
    has = get_configuration(file_path="this.file.does.not.exits")
    want = Configuration()
    assert has == want


def test_malformed():
    test_config = {
        "port": 8888,
        "debug": False,
        "is_malformed": True,
        "db_file": "test.sdb",
    }
    with pytest.warns(MalformedConfigurationWarning):
        has = Configuration.from_json(test_config)
    assert has.port == 8888
    assert has.debug == False
    assert has.require_auth == False
    assert has.db_file == "test.sdb"


def test_correct_formated():
    test_config = {
        "port": 9999,
        "debug": False,
        "require_auth": True,
        "db_file": "test.sdb",
    }
    has = Configuration.from_json(test_config)
    assert has.port == 9999
    assert has.debug == False
    assert has.require_auth == True
    assert has.db_file == "test.sdb"


def test_correct_with_one_missing_field():
    test_config = {"debug": False, "require_auth": True, "db_file": "test.sdb"}
    has = Configuration.from_json(test_config)
    assert has.port == 8000
    assert has.debug == False
    assert has.require_auth == True
    assert has.db_file == "test.sdb"


def test_correct_with_mutliple_missing_fields():
    test_config = {"port": 9090}
    has = Configuration.from_json(test_config)
    assert has.port == 9090
    assert has.debug == True
    assert has.require_auth == False
    assert has.db_file == ".sdb"


def test_correct_with_empty_config():
    test_config = dict()
    has = Configuration.from_json(test_config)
    assert has.port == 8000
    assert has.debug == True
    assert has.require_auth == False
    assert has.db_file == ".sdb"


def test_partial_file_config():
    has = get_configuration("./tests/test.config.json")
    assert has.port == 9999
    assert has.debug == True
    assert has.require_auth == False
    assert has.db_file == ".sdb"

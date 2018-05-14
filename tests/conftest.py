import os

import pytest
from tinydb import TinyDB, Query

from tiny_thingy import Thingy


@pytest.fixture
def database():
    filename = "/tmp/tiny-thingy-tests.json"
    yield TinyDB(filename)
    os.remove(filename)


@pytest.fixture
def table(request, database):
    return database.table(request.node.name)


@pytest.fixture
def TestThingy(database, table):
    class TestThingy(Thingy):
        _database = database
        _table = table

    return TestThingy


@pytest.fixture
def q():
    return Query()

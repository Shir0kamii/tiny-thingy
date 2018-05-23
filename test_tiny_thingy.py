import os

import pytest
from tinydb import TinyDB

from tiny_thingy import Thingy, q


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


def test_thingy_database(TestThingy, database):
    assert TestThingy.database == database


def test_thingy_table(TestThingy, table):
    assert TestThingy.table == table


def test_thingy_names(database):
    class Foo(Thingy):
        pass

    with pytest.raises(AttributeError):
        Foo.database

    Foo._database = database
    assert Foo.database == database
    assert Foo.table == database.table("foo")
    assert Foo.table_name == "foo"


def test_table_name(table):
    class Foo(Thingy):
        _table = table

    assert Foo.table_name == table.name


def test_use_database():
    class Foo(Thingy):
        pass

    filename = "/tmp/test-tiny-thingy-use-database.json"
    Foo.use_database(filename)
    assert Foo.database is not None
    os.remove(filename)


def test_create(TestThingy, table):
    documents = [{"Test": 42}, {"foo": "bar"}, {"baz": "fool"}]
    for document in documents:
        TestThingy.create(document)
    assert table.all() == documents


def test_find(TestThingy, table):
    documents = [{"id": 42}, {"id": 32}, {"id": 13}]
    for document in documents:
        table.insert(document)
    assert len(TestThingy.find()) == 3
    assert len(TestThingy.find(q.id > 20)) == 2


def test_save(TestThingy, table):
    thingy = TestThingy(test=42)
    thingy.save()
    assert len(table) == 1
    thingy2 = TestThingy.find()[0]
    assert thingy2.doc_id == thingy.doc_id
    thingy.test = 101
    thingy.save()
    thingy2 = TestThingy.find()[0]
    assert thingy2.test == thingy.test


def test_find_one(TestThingy, table):
    assert TestThingy.find_one() is None
    TestThingy(test=42, foo="bar").save()
    thingy = TestThingy.find_one()
    assert isinstance(thingy, TestThingy)
    assert thingy.test == 42


def test_find_one_doc_id(TestThingy):
    assert TestThingy.find_one() is None
    TestThingy().save()
    thingy = TestThingy(lol=42, foo="bar").save()
    thingy = TestThingy.find_one(doc_id=thingy.doc_id)
    assert isinstance(thingy, TestThingy)
    assert thingy.lol == 42
    thingy2 = TestThingy.find_one(q.lol == 69, doc_id=thingy.doc_id)
    assert thingy2 is None


def test_count(TestThingy, table):
    documents = [{"id": 42}, {"id": 32}, {"id": 13}]
    for document in documents:
        table.insert(document)
    assert TestThingy.count() == 3

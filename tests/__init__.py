import pytest

from tiny_thingy import Thingy


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


def test_create(TestThingy, table):
    documents = [{"Test": 42}, {"foo": "bar"}, {"baz": "fool"}]
    for document in documents:
        TestThingy.create(document)
    assert table.all() == documents


def test_find(TestThingy, table, q):
    documents = [{"id": 42}, {"id": 32}, {"id": 13}]
    for document in documents:
        table.insert(document)
    assert len(TestThingy.find()) == 3
    assert len(TestThingy.find(q.id > 20)) == 2

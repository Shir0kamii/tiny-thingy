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

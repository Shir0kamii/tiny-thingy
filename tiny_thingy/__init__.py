from thingy import DatabaseThingy
from tinydb import TinyDB


class Thingy(DatabaseThingy):
    """Represents a JSON object in a table"""

    @classmethod
    def _get_table(cls, database, table_name):
        return database.table(table_name)

    @classmethod
    def _get_table_name(cls, table):
        return table.name

    @classmethod
    def create(cls, obj):
        return cls.table.insert(obj)

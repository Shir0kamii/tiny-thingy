from thingy import DatabaseThingy
from tinydb import TinyDB, Query
from tinydb.database import Document

q = Query()


class Thingy(DatabaseThingy):
    """Represents a JSON object in a table"""

    def __init__(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, Document):
                self.doc_id = arg.doc_id
        super().__init__(*args, **kwargs)

    @classmethod
    def _get_table(cls, database, table_name):
        return database.table(table_name)

    @classmethod
    def _get_table_name(cls, table):
        return table.name

    @classmethod
    def use_database(cls, filename):
        cls._database = TinyDB(filename)

    @classmethod
    def create(cls, obj):
        return cls.table.insert(obj)

    @classmethod
    def find(cls, query=None, doc_ids=None):
        if doc_ids is not None:
            return cls._find_by_id(query, doc_ids)
        if query is None:
            documents = cls.table.all()
        else:
            documents = cls.table.search(query)
        return [cls(doc) for doc in documents]

    @classmethod
    def _find_by_id(cls, query, doc_ids):
        def _filter(doc):
            return doc.doc_id in doc_ids
        documents = cls.find(_filter)
        if query is not None:
            documents = list(filter(query, documents))
        return documents

    @classmethod
    def find_one(cls, query=None, doc_id=None):
        if doc_id is not None:
            result = cls.find(query, doc_ids=[doc_id])
        else:
            result = cls.find(query)
        try:
            return next(iter(result))
        except StopIteration:
            return None

    @classmethod
    def count(cls):
        return len(cls.table)

    def save(self):
        data = self.__dict__.copy()
        doc_id = data.pop("doc_id", None)
        if doc_id is not None:
            self.get_table().update(data, doc_ids=[doc_id])
        else:
            self.doc_id = self.get_table().insert(data)
        return self


use_database = Thingy.use_database

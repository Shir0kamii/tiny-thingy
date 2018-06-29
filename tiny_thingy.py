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
        """Initialize a database for the class using the specified filename"""
        cls._database = TinyDB(filename)

    @classmethod
    def create(cls, obj):
        """Directly insert an object in the table"""
        return cls.table.insert(obj)

    @classmethod
    def find(cls, query=None, doc_ids=None):
        """Return a list of objects matching the query"""
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
        """Return a single object matching the query"""
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
        """Count the number of objects in the table"""
        return len(cls.table)

    @classmethod
    def remove(cls, query=None, doc_ids=None):
        """Remove the objects matching the query"""
        return cls.table.remove(query, doc_ids=doc_ids)

    @classmethod
    def inplace_update(cls, fields, query=None, doc_ids=None):
        """Directly update objects matching the query with given fields"""
        return cls.table.update(fields, query, doc_ids=doc_ids)

    def save(self):
        """Save the object in the table"""
        data = self.__dict__.copy()
        doc_id = data.pop("doc_id", None)
        if doc_id is not None:
            self.get_table().update(data, doc_ids=[doc_id])
        else:
            self.doc_id = self.get_table().insert(data)
        return self

    def delete(self):
        """Delete the object from the table"""
        self.remove(doc_ids=[self.doc_id])


use_database = Thingy.use_database

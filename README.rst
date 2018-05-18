Tiny-Thingy
###########

Tiny-Thingy is a wrapper around TinyDB_ that makes it more Pythonic.

Install
=======

.. code-block:: sh

    $ pip install tiny-thingy

Examples
========

First steps
-----------

Setup, insert and find thingies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from tiny_thingy import Thingy, use_database
    >>> use_database("/some/json/file/serving/as/database.json")

    >>> class Task(Thingy):
    ...     pass

    >>> task = Task({"name": "work on tiny-thingy"}).save()
    >>> Task.count()
    1
    >>> Task.find_one()
    Task({'doc_id': 1, 'name': 'work on tiny-thingy'})

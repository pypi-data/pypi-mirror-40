str_util
===============


String functions for Python 3, inspired by similar Lotus Domino @functions

Features

* Powerful functions to work with both strings and list of strings
* Fully documented: https://stringfunctions.readthedocs.io
* 98% coverage
* MIT License, source code: https://github.com/majkilde/stringfunctions


Installation
------------

Install the latest release from `PyPI <https://pypi.org/project/str_utils/>`_:

.. code-block:: sh

    pip install str_util

Usage
-----

All functions are available directly off the :code:`str_util` package. You may choose to import individual functions by name, or import all.

.. code-block:: python

    from str_util import word, is_string

    def foo(value):
        if is_string( value ):
            return word(value,1)
        return "not a string"


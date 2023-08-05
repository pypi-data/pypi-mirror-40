dict-converter
===============

A chain-line dict converter in Python 3

Example
-------

>>> from dict_converter import DictConverter
>>> a = {'a': 'a', 'b': 'b', 0: 0}
>>> DictConverter(a).add(0, lambda s: s + 1).add(['a', 'b'], str.upper).result()
{'a':'A','b':'B', 0:1}

Install
-------

.. code-block:: shell
pip install condition_chain

Author
------
Yixian Du (duyixian1234@outlook.com)
pybimaps - Python Bijective Maps
================================
|Build Status|

Various bijective maps in pure python, internally they use two dicts:

-  one 2 one: ``BijectiveMap``;

-  one 2 many: ``BijectiveListMap``, ``BijectiveSetMap``;

-  many 2 many: ``BijectiveSetSetMap``, ``BijectiveListSetMap``;

Dependencies
------------
Being written in pure python, ``pybimaps`` supports >=python-3.3, will probably work on >=python-2.7. and does not require any other dependency.


.. |Build Status| image:: https://travis-ci.org/waipu/pybimaps.svg
   :target: https://travis-ci.org/waipu/pybimaps

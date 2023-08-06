pytest-select
=============

|PyPI pyversions| |PyPI license| |PyPI version| |CircleCI build| |Codecov result|

.. |PyPI version| image:: https://img.shields.io/pypi/v/pytest-select.svg
   :target: https://pypi.org/project/pytest-select/
.. |PyPI license| image:: https://img.shields.io/pypi/l/pytest-select.svg
   :target: https://pypi.python.org/pypi/pytest-select/
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/pytest-select.svg
   :target: https://pypi.python.org/pypi/pytest-select/
.. |CircleCI build| image:: https://img.shields.io/circleci/project/github/ulope/pytest-select/master.svg?logo=circleci
   :target: https://circleci.com/gh/ulope/pytest-select/
.. |Codecov result| image:: https://img.shields.io/codecov/c/github/ulope/pytest-select/master.svg?logo=codecov
   :target: https://codecov.io/gh/ulope/pytest-select


This is a `pytest`_ plugin which allows to (de-)select tests by name from a list loaded from a file.

.. _pytest: https://pytest.org


Installation
------------

It's recommended to install this package from PyPI::

    pip install pytest-select


Usage
-----

This plugin adds new command line options to pytest:

- ``--select-from-file``
- ``--deselect-from-file``
- ``--select-fail-on-missing``

The first two both expect an argument that resolves to a UTF-8 encoded text file containing one test name per
line.

The third one changes the behaviour in case (de-)selected test names are missing from the to-be executed tests.
By default a warning is emitted and the remaining selected tests are executed as normal.
By using the ``--select-fail-on-missing`` flag this behaviour can be changed to instead abort execution in that case.

Test names are expected in the same format as seen in the output of
``pytest --collect-only --quiet`` for example.

Both plain test names or complete node ids (e.g. ``test_file.py::test_name``) are accepted.

Example::

    $~ cat selection.txt
    test_something
    test_parametrized[1]
    tests/test_foo.py::test_other

    $~ pytest --select-from-file selection.txt
    $~ pytest --deselect-from-file selection.txt


Development
-----------

This package uses Poetry_.
To setup a development environment install Poetry and then run::

    poetry install


.. _Poetry: https://poetry.eustace.io

Questions
---------

Why not use pytest's builtin ``-k`` option
******************************************

The ``-k`` selection mechanism is (currently) unable to deal with selecting multiple parametrized
tests and is also a bit fragile since it matches more than just the test name.
Additionally, depending on the number of tests, giving test names on the command line can overflow
the maximum command length.

What is this useful for
***********************

The author uses this plugin to `split tests across workers`_ on `Circle CI`_.

Example::

    pytest --collect-only --quiet | \
        grep '::' | \
        circleci tests split --split-by=timings --timings-type=testname > selected.txt
    pytest --select-from-file selected.txt

.. _Circle CI: https://circleci.com
.. _split tests across workers: https://circleci.com/docs/2.0/parallelism-faster-jobs/#splitting-test-files


Version History
---------------

- ``v0.1.2`` - 2019-01-18:
    - Add informational pytest header report output
- ``v0.1.1`` - 2018-12-10:
    - Add ``--select-fail-on-missing`` option
    - Add basic mutation testing
- ``v0.1.0post0`` - 2018-12-08:
    - Fix README
- ``v0.1.0`` - 2018-12-08:
    - Initial release

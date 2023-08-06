pimple
======

    Summarize your unit tests

.. image:: https://img.shields.io/badge/license-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

``pimple`` is a tool for compiling a summary of your unit tests.

Usage
-----

Install ``pimple`` from PyPI with::

    $ pip install pimple

Run pimple in your project directory with::

    $ python -m pimple tests/

(substitute the directory that contains your tests)

The ``testcase_summary.rst`` file can be found in the directory you run the script from.

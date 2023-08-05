========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/topock/badge/?style=flat
    :target: https://readthedocs.org/projects/topock
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/SmithSamuelM/topock.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/SmithSamuelM/topock

.. |version| image:: https://img.shields.io/pypi/v/topock.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/topock

.. |commits-since| image:: https://img.shields.io/github/commits-since/SmithSamuelM/topock/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/SmithSamuelM/topock/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/topock.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/topock

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/topock.svg
    :alt: Supported versions
    :target: https://pypi.org/project/topock

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/topock.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/topock


.. end-badges

Timeliness Ordered Proof of Common Knowledge

* Free software: Apache Software License 2.0

Installation
============

::

    pip install topock

Documentation
=============


https://topock.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

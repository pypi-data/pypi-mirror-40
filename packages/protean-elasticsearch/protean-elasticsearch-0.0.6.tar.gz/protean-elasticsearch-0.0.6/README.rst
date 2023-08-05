========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/protean-elasticsearch/badge/?style=flat
    :target: https://readthedocs.org/projects/protean-elasticsearch
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/protean-elasticsearch.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/protean-elasticsearch

.. |wheel| image:: https://img.shields.io/pypi/wheel/protean-elasticsearch.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/protean-elasticsearch

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/protean-elasticsearch.svg
    :alt: Supported versions
    :target: https://pypi.org/project/protean-elasticsearch

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/protean-elasticsearch.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/protean-elasticsearch


.. end-badges

Protean Elasticsearch Extension

* Free software: BSD 3-Clause License

Installation
============

::

    pip install protean-elasticsearch

Documentation
=============

https://protean-elasticsearch.readthedocs.io/

Development
===========

::

    pyenv virtualenv -p python3.6 3.6.5 protean-es-dev

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

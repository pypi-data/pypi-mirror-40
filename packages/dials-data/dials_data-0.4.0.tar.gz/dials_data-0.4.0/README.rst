=============================
DIALS Regression Data Manager
=============================

.. image:: https://img.shields.io/pypi/v/dials_data.svg
        :target: https://pypi.python.org/pypi/dials_data
        :alt: PyPI release

.. image:: https://img.shields.io/pypi/l/dials_data.svg
        :target: https://pypi.python.org/pypi/dials_data
        :alt: BSD license

.. image:: https://travis-ci.com/dials/data.svg?branch=master
        :target: https://travis-ci.com/dials/data
        :alt: Build status

.. image:: https://img.shields.io/pypi/pyversions/dials_data.svg
        :target: https://pypi.org/project/dials_data/
        :alt: Supported Python versions

.. image:: https://pyup.io/repos/github/dials/data/python-3-shield.svg
        :target: https://pyup.io/repos/github/dials/data/
        :alt: Python 3 ready

.. image:: https://pyup.io/repos/github/dials/data/shield.svg
        :target: https://pyup.io/repos/github/dials/data/
        :alt: Updates

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/ambv/black
        :alt: Code style: black

A python package providing data files used for regression tests in
DIALS_, dxtbx_, xia2_ and related packages.


Installation
------------

To install this package in a normal Python environment, run::

    install dials_data

To install in a DIALS installation you need to run::

    libtbx.pip install dials_data


Usage
-----

Tests that rely on the dials_data package will use it automatically
once it is installed. You can also access the regression data using
the command line interface::

    dials.data


How do I run tests?
^^^^^^^^^^^^^^^^^^^

Tests using the ``dials_data`` package are presumably written using pytest.
If they use the fixture provided by ``dials_data`` then you can run
the tests with::

    pytest --regression


How do I use this in my test?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If your test is written in pytest and you use the fixture provided by
``dials_data`` then you can use regression datasets in your test by
adding the ``dials_data`` fixture to your test, ie::

    def test_accessing_a_dataset(dials_data):
        location = dials_data("x4wide")

The fixture/variable ``dials_data`` in the test is a
``dials_data.download.DataFetcher`` instance, which can be called with
the name of the dataset you want to access (here: ``x4wide``). If the
files are not present on the machine then they will be downloaded.
If either the download fails or ``--regression`` is not specified then
the test is skipped.

The return value (``location``) is a ``py.path.local`` object pointing
to the directory containing the requested dataset.


How do I use this in my Python package?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming you are using ``pytest`` then simply add the following to a
file named ``conftest.py`` in the top level of your project::

    import pytest
    try:
        from dials_data import *
    except ImportError:
        @pytest.fixture
        def dials_data():
            pytest.skip("Test requires python package dials_data")


Where are the regression datasets stored?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order of evaluation:

* If the environment variable ``DIALS_DATA`` is set and exists or can be
  created then use that location
* If the file path ``/dls/science/groups/scisoft/DIALS/dials_data`` exists and is readable then
  use this location. This is a shared directory specific to Diamond Light Source
* If the environment variable ``LIBTBX_BUILD`` is set and the directory
  ``dials_data`` exists or can be created underneath that location then
  use that.
* Use ``~/.cache/dials_data`` if it exists or can be created
* Otherwise fail with a RuntimeError


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _DIALS: https://dials.github.io
.. _dxtbx: https://github.com/cctbx/cctbx_project/tree/master/dxtbx
.. _xia2: https://xia2.github.io

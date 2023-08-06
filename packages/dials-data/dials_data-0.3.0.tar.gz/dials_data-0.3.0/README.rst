=====================
DIALS Regression Data
=====================

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


Background
----------

Where is the regression data stored?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

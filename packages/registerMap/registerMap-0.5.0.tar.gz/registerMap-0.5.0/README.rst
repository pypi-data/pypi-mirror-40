registerMap
-----------

|pipeline| |coverage| |documentation|

.. |pipeline| image:: https://gitlab.com/registerMap/registerMap/badges/master/pipeline.svg
   :target: https://gitlab.com/registerMap/registerMap/commits/master
   :alt: pipeline status

.. |coverage| image:: https://gitlab.com/registerMap/registerMap/badges/master/coverage.svg
   :target: https://gitlab.com/registerMap/registerMap/commits/master
   :alt: coverage report

.. |documentation| image:: https://readthedocs.org/projects/registermap/badge/?version=latest
   :target: http://registermap.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

|pypiVersion|

|doi0.4.0| (v0.4.0)

.. |pypiVersion| image:: https://badge.fury.io/py/registerMap.svg
   :target: https://badge.fury.io/py/registerMap
   :alt: PyPI version


A Python 3 framework for creating and maintaining register maps for integrated circuit design and embedded
software development.

.. contents::

.. section-numbering::


Main Features
=============

* define a register map by the *relationships* and *order* of modules, registers and fields
* generate address of registers and modules automatically from relationships
* constrain registers and modules by size or address
* automatically manage registers that span multiple memory units
* arbitrary number of memory unit bits (but constant across the register map)
* arbitrary number of address bits (but constant across the register map)
* automatically avoid allocating register/module addresses to page registers


Installation
============

The simplest way to acquire ``registerMap`` is using ``pip``.

.. code-block:: bash

   pip install registerMap


Documentation
=============

Head over to readthedocs_

.. _readthedocs: http://registermap.readthedocs.io/


DOI Archive
===========

+-------+------------+
| 0.1.0 | |doi0.1.0| |
+-------+------------+
| 0.2.0 | |doi0.2.0| |
+-------+------------+
| 0.3.0 | |doi0.3.0| |
+-------+------------+
| 0.4.0 | |doi0.4.0| |
+-------+------------+

.. |doi0.1.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.322502.svg
   :target: https://doi.org/10.5281/zenodo.322502
   :alt: DOI 0.1.0

.. |doi0.2.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1098625.svg
   :target: https://doi.org/10.5281/zenodo.1098625
   :alt: DOI 0.2.0

.. |doi0.3.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1289354.svg
   :target: https://doi.org/10.5281/zenodo.1289354
   :alt: DOI 0.3.0

.. |doi0.4.0| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.1289364.svg
   :target: https://doi.org/10.5281/zenodo.1289364
   :alt: DOI 0.4.0

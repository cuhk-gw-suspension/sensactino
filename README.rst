|logo|

*Re-implementing Arduino serial monitor using Python*

|website| |release| |rtd| |license| |travis-ci| |codecov|

Sensactino
==========

A library for controlling sensors and actuator from python through arduino slaves.

**features**

* Control the output of actuator.
* Retrieve the readout from sensors.

**Documentation**: https://sensactino.readthedocs.io

**Repository**: https://github.com/cuhk-gw-suspension/sensactino

.. contents::
   :depth: 2

Getting Started
===============

Dependencies
------------

Required
^^^^^^^^
* NumPy
* pySerial

Optional
^^^^^^^^
* None.


Install from source
-------------------

.. code:: bash

   git clone https://github.com/cuhk-gw-suspension/sensactino.git
   cd sensactino
   pip install .

Basic Usage
-----------




How to Contribute
=================

Try out the package and file an issue if you find any!


For Developers
==============

Standards and Tools
-------------------
Please comply with the following standards/guides as much as possible.

Coding style
^^^^^^^^^^^^
- **PEP 8**: https://www.python.org/dev/peps/pep-0008/

CHANGELOG
^^^^^^^^^
- **Keep a Changelog**: https://keepachangelog.com/en/1.0.0/

Versioning
^^^^^^^^^^
- **Semantic Versioning**: https://semver.org/spec/v2.0.0.html

Packaging
^^^^^^^^^
- **PyPA**: https://www.pypa.io
- **python-packaging**: https://python-packaging.readthedocs.io

Documentation
^^^^^^^^^^^^^
- **NumPy docstrings**: https://numpydoc.readthedocs.io/en/latest/format.html
- **Sphinx**: https://www.sphinx-doc.org/
- **Read The Docs**: https://readthedocs.org/
- **Documenting Python Code: A Complete Guide**: https://realpython.com/documenting-python-code/

Cheat sheet
-----------

Sphinx
^^^^^^

Generate documentation base, in docs/,

.. code:: bash

   sphinx-quickstart

Select separate build and source files when prompted.

Preview documentation page with modified source, in docs/

.. code:: bash

   make html

Open index.html with a browser (if this was set as the first page).

.. |logo| image:: docs/source/_static/logo.svg
    :alt: Logo
    :target: https://github.com/cuhk-gw-suspension/serial-monitor

.. |website| image:: https://img.shields.io/badge/website-serial-monitor-blue.svg
    :alt: Website
    :target: https://github.com/cuhk-gw-suspension/serial-monitor

.. |release| image:: https://img.shields.io/github/v/release/cuhk-gw-suspension/serial-monitor?include_prereleases
   :alt: Release
   :target: https://github.com/cuhk-gw-suspension/serial-monitor/releases
..
  .. |rtd| image:: https://readthedocs.org/projects/serial-monitor/badge/?version=latest
     :alt: Read the Docs
     :target: https://serial-monitor.readthedocs.io/

  .. |license| image:: https://img.shields.io/github/license/cuhk-gw-suspension/serial-monitor
      :alt: License
      :target: https://github.com/cuhk-gw-suspension/serial-monitor/blob/master/LICENSE

  .. |travis-ci| image:: https://travis-ci.com/cuhk-gw-suspension/serial-monitor.svg?branch=master
      :alt: travis-ci
      :target: https://travis-ci.com/cuhk-gw-suspension/serial-monitor

  .. |codecov| image:: https://codecov.io/gh/cuhk-gw-suspension/serial-monitor/branch/master/graph/badge.svg?token=NMEBAYFE2N
      :alt: codecov
      :target: https://codecov.io/gh/cuhk-gw-suspension/serial-monitor

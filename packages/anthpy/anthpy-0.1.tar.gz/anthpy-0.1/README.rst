.. -*- mode: rst -*-

.. role:: bash(code)
   :language: bash

|Travis|_ |PyPi|_ |TestStatus|_ |PythonVersion|_

.. |Travis| image:: https://travis-ci.org/aagnone3/anthpy.svg?branch=master

.. |PyPi| image:: https://badge.fury.io/py/anthpy.svg
.. _PyPi: https://badge.fury.io/py/anthpy

.. |TestStatus| image:: https://travis-ci.org/aagnone3/anthpy.svg
.. _TestStatus: https://travis-ci.org/aagnone3/anthpy.svg

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/anthpy.svg
.. _PythonVersion: https://img.shields.io/pypi/pyversions/anthpy.svg

anthpy
================

Anthony's python utils

Documentation
-------------

Documentation can be found at the github pages here_

.. _here: https://aagnone3.github.io/anthpy/

Dependencies
~~~~~~~~~~~~

anthpy is tested to work under Python 2.x and 3.x.
See the requirements via the following command:

.. code-block:: bash

  cat requirements.txt

Installation
~~~~~~~~~~~~

anthpy is currently available on the PyPi's repository and you can
install it via `pip`:

.. code-block:: bash

  pip install -U anthpy

If you prefer, you can clone it and run the setup.py file. Use the following
commands to get a copy from GitHub and install all dependencies:

.. code-block:: bash

  git clone https://github.com/aagnone3/anthpy.git
  cd anthpy
  pip install .

Or install using pip and GitHub:

.. code-block:: bash

  pip install -U git+https://github.com/aagnone3/anthpy.git

Local Testing
~~~~~~~~~~~~~

.. code-block:: bash

  make test
  
Travis Testing
~~~~~~~~~~~~~~

The :bash:`Makefile`, :bash:`.travis.yml` file and :bash:`.ci` directory contain the structure necessary to have Travis_ test the repository upon all branch updates. Some additional steps, however, are needed:

- Enable the repository to be monitored by Travis via your Travis profile.
- Generate a Github app token, and assign it to the (private) environment variable :bash:`${GITHUB_TOKEN}` in the Travis environment.

.. _Travis: https://travis-ci.org/aagnone3/anthpy

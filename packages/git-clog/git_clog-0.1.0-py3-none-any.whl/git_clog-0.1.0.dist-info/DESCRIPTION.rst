Git colorlog
============

Introduction
------------

``git clog`` outputs the commit graph of the current Git repository and
colorizes commit symbols by interpreting the first six commit hash
digits as an RGB color value:

.. figure:: https://raw.githubusercontent.com/IngoHeimbach/git-clog/master/screenshot.png
   :alt: git clog screenshot

   git clog screenshot

**Important note**: You need a `terminal with true color
support <https://gist.github.com/XVilka/8346728>`__.

Installation and usage
----------------------

``git clog`` is `available on
PyPI <https://pypi.org/project/git-clog/>`__ and can be installed with
``pip``:

.. code:: bash

   python3 -m pip install git-clog

After the installation, call

.. code:: bash

   git clog

within a Git repository.



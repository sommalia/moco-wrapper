Installation
============

The moco-wrapper package is hosted on pypi and can be installed via pip.


.. code-block:: shell

      $ pip install moco-wrapper

.. note:: Depending on your system, you may need to use pip3 to install packages for Python 3.
.. note:: This package was only developed for Python 3. Using it with Python 2 will result in errors.


Installation in a virtual environment
-------------------------------------

.. code-block:: shell

      $ apt-get install python3-venv
      $ python3 -m venv venv
      $ source venv/bin/activate
      $ (venv) pip install moco-wrapper


Upgrading moco-wrapper
----------------------

The moco-wrapper can be updated by using pip

.. code-block:: shell

      $ pip install --upgrade moco-wrapper


Install from source
-------------------

For installation from source we recommend you install it into a virtual environment.


.. code-block:: shell
      
      $ sudo apt-get install python3 python3-venv git make
      $ python3 -m venv venv
      $ source venv/bin/activate
      $ (venv) git clone https://github.com/sommalia/moco-wrapper moco_wrapper
      $ (venv) cd moco_wrapper
      $ (venv) make install
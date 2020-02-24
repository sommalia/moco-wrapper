============
moco-wrapper
============


.. image:: https://img.shields.io/pypi/v/moco_wrapper.svg
        :target: https://pypi.python.org/pypi/moco_wrapper

.. image:: https://img.shields.io/travis/sommalia/moco-wrapper.svg
        :target: https://travis-ci.org/sommalia/moco-wrapper



The "moco-wrapper" is a python package that allows for simple access to Mocos API. 


Disclaimer (semi-serious)
-------------------------

This project is in no way finished, or polished. I am not responsible for any commercial, financial or emotional damage that may or may not be caused by using this project.

I am also not affiliated with the people behind moco. The package implements the api as described in its readme https://github.com/hundertzehn/mocoapp-api-docs.


API Documentation
-----------------

API Documentation can be found at here: https://moco-wrapper.readthedocs.io/en/latest/


Running the tests
-----------------

Tests can be run by executing the **tox** commend inside the root directory of the project.

.. code-block:: shell

        $ tox

This command will run all the tests.



Setting up integration tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the integration tests 2 environment variables are needed *mocotest_apikey* and *mocotest_domain*. Set them like this

.. code-block:: shell
        
        $ export mocotest_apikey="this is the api key"
        $ export mocotest_domain="testdomain"




License
-------

This project is licensed under the GNU Public License - see the `LICENSE`_  file for details


Credits
-------


This package was created with `Cookiecutter`_ and the `audreyr/cookiecutter-pypackage`_ project template.
This package tries to imitate the way that the `praw-package`_, for wrapping arount the reddit api, was structured



.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`praw-package`: https://github.com/praw-dev/praw
.. _`LICENSE`: https://github.com/sommalia/moco-wrapper/blob/master/LICENSE
.. _`moco-api-readme`: https://github.com/hundertzehn/mocoapp-api-docs




<<<<<<< HEAD
....
=======
>>>>>>> 4cf68b534f07f82bb03ddd8ba27d04aa204af982

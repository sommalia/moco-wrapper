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

I am also not affiliated with the people behind moco. The package implements the api as described in its readme https://github.com/hundertzehn/mocoapp-api-docs



Running the tests
-----------------

Tests can be run by executing the *tox* commend inside the root direcotry of this project

```
> tox
```

This command will run all the tests.

If you want to only run a specific set of tests, they are structured in the follwing 3 Folders.

* production (need configuration to run)
* integration (not implemented)
* unit


Setting up integration tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the integration tests 2 environment variables are needed *mocotest_apikey* and *mocotest_domain*. Set them like this

```
> export mocotest_apikey="this is the api key"
> export mocotest_domain="testdomain"
```



License
-------

This project is licensed under the GNU Public License - see the [LICENSE](LICENSE) file for details


Credits
-------


This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


This package tries to imitate the way that the praw-package, for wrapping arount the reddit api, was structured

.. praw: https://github.com/praw-dev/praw

....
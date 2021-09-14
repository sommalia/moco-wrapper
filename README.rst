============
moco-wrapper
============

.. image:: https://img.shields.io/pypi/v/moco_wrapper.svg
        :target: https://pypi.python.org/pypi/moco_wrapper

This is a client implementation of the moco api written in python3.

Installation
------------

From pypi
#########

The moco-wrapper package is available via `pip <https://pypi.org/project/moco-wrapper/>`_.

.. code-block:: shell

    $ pip3 install moco-wrapper

From Source
###########

If dont want to use pip you can clone this repository and install it from the source.

.. code-block:: shell

    $ git clone https://github.com/sommalia/moco-wrapper moco-wrapper
    $ cd ./moco-wrapper
    $ pip3 install -r requirements_dev.txt
    $ make install


Quickstart
----------

If you already have credentials or an api key you can instantiate your moco-wrapper object like so:

.. code-block:: python

    import moco_wrapper
    moco = moco_wrapper.Moco(auth={
        "api_key": "[MY API KEY]",
        "domain": "example" # domain of the moco webapp is example.mocoapp.com
    })

With the moco wrapper object you can now interact with moco.

.. code-block:: python

    # load a list of users
    users = moco.User.getlist()

    # load the second page of our list of users
    # requests with lists are paginated
    # default limit is 100 items per request
    users_page_two = moco.User.getlist(page=2)

    # create a project
    leader = moco.User.getlist()[0]
    customer = moco.Company.getlist(type="customer").getlist()[0]
    project = moco.Project.create(
        name = "my new project",
        currency = "EUR",
        leader_id = leader.id,
        customer_id = customer.id,
        finish_date = date(2020, 1, 1)
    )

    # update a contact
    moco.Contact.update(
        contact_id = 55123,
        lastname = "doe"
    )

    # add a task to a project
    task = moco.Task.create(
        project_id = project.id,
        name = "My new task"
    )

    # create a new customer
    new_customer = moco.Company.create(
        name = "my new customer company",
        company_type = moco_wrapper.models.company.CompanyType.CUSTOMER
    )

For an overview about all the things that can and cannot be done see
`The Moco Instance <https://moco-wrapper.readthedocs.io/en/latest/code_overview/moco_instance.html>`_.

Tests
-----

There are two types of tests in this repo. *unit*-tests with no side effects
and *integration*-tests that require an actual moco instance (if you want to recreate the cached responses).

Unit
####

These tests check whether all methods can be called correctly, use the
right HTTP method, have the right headers and format everything correctly for the API.
These tests have no side effects and can be run via pytest:

.. code-block:: shell

    $ python3 -m pytest tests/unit


Integration
###########

The second group of tests are the *integration* tests.
These tests use the betamax package, send actual requests to a moco instance and save the response locally (see tests/integration/cassettes/).
These tests can also be run via pytest:

.. code-block:: shell

    $ python3 -m pytest tests/integration

Recreating the tests results
****************************

If you want to recreate these tests make sure you have the following setup:

* A working, clean moco instance (eg. example.mocoapp.com)
* An api key
* Time to spare

After that you have to export the following variables

.. code-block:: shell

    $ export mocotest_apikey=[MY API KEY]
    $ export mocotest_domain=example
    $ export mocotest_delay=1 # enable delay between tests

The *mocotest_delay* variable will make sure that the api, does not rate limit our test-run
by waiting 5 seconds between the execution of each single test.

**Caution:** Make sure you run the integration tests (if you recreate the results) on a clean moco instance,
as some requests (delete. create and update requests) have side effects, that cannot be reversed easily.

Now that everything is set up we delete the saved responses and re-run the tests.

.. code-block:: shell

    $ rm tests/integration/cassettes/*.json
    $ python3 -m pytest tests/integration


Documentation
-------------

The full documentation for the moco-wrapper is located at `<https://moco-wrapper.readthedocs.io/>`_.


License
-------

This project is licensed under the GNU Public License - see the `LICENSE`_  file for details


Credits
-------

This package was created with `Cookiecutter`_ and the `audreyr/cookiecutter-pypackage`_ project template.
This package tries to imitate the way that the `praw-package`_, for wrapping around the reddit api, was structured

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`praw-package`: https://github.com/praw-dev/praw
.. _`LICENSE`: https://github.com/sommalia/moco-wrapper/blob/master/LICENSE
.. _`moco-api-readme`: https://github.com/hundertzehn/mocoapp-api-docs




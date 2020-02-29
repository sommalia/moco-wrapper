Quick Start
===========

First step is installing the package.

.. code-block:: shell

    $ pip install moco-wrapper


After that we need two things. The moco domain and the user api key.

Getting your moco domain is the easy part. From your full url just take your company specific part. For example if your moco appkication is found under https://testabcd.mocoapp.com we just use **testabcd** for creating our object.

Next we need an api key. You can find this key when logging into your user account, going to your user profile and copying the value under *your personal api key* from the tab integrations. (See https://github.com/hundertzehn/mocoapp-api-docs#authentication for more information)

Then we all the information we need to create the moco instance:

.. code-block:: python3

    >> from moco_wrapper import Moco
    >> wrapper = Moco(auth={"domain": "testabcd", "api_key": "your api key"})

After that we make a test call to the api.

.. code-block:: python3

    >> projects = wrapper.Project.getlist()
    >> print(projects)
    <ListingResponse, Status Code: 200, Data: [<moco_wrapper.models.objector_models.project.Project at ..]>






.. _authentication:

Authentication
==============

There are two ways of authenticating yourself with the moco api. Via api key and via your own user email and password.

Via api key
-----------

You can find your own api key under your user profile when you log into your account. 

.. code-block:: python

    from moco_wrapper import Moco

    wrapper = Moco(
        auth={
            "api_key": "[YOUR API KEY]"
            "domain": "testabcd" #your full domain would be testabcd.mocoapp.com
        }
    )


.. note::

    The api key is always associated with the user it belongs to. Things like activities and presecense always work in context of the current user.

.. note::

    This method is faster than authenticating via username and password because it skips the authentication requests (with an api key, you already are authenticated).


Via username and password
-------------------------

The second way you can authencate is via your own user information (username and password).

.. code-block:: python

    from moco_wrapper import Moco

    wrapper = Moco(
        auth={
            "email": "my-account-email@mycomapany.com",
            "password": "my account password",
            "domain": "testabcd" #full domain is testabcd.mocoapp.com
        }
    )


.. note::

    Note that you authenticate in this way an extra request will be sent, before you try to request any actual ressources of the api, for obtaining authentication.


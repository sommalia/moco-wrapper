Authentication
==============

For authentcating against the moco-api we always need the company specific domain part and an api key. The api key is always associated with the user it belongs to.

Currently the only method that can be used to create the moco-wrapper base instance is if the api key and the domain are both known.


.. code-block:: python

    import moco_wrapper as moco

    moco_istance = moco.Moco(
        domain="testabcd" # your full domain would be https://testabcd.mocoapp.com
        api_key="[YOUR API KEY]"
    )

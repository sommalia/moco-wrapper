Impersonation
=============

Things like :class:`moco_wrapper.models.Activity` and :class:`moco_wrapper.models.Presence` are always mapped to the user of the api key that was used. 

If you want to change that (for example when logging activities on behalf of someone else), you can impersontate them.

.. note::

    For impersonating other users your own user account must have the ``Staff`` permission. See https://github.com/hundertzehn/mocoapp-api-docs#impersonation.

You can start off the moco instance already impersonating a user:

.. code-block:: python

    from moco_wrapper import moco

    impersonate_as = 43
    m = Moco(
        ..,
        impersonate_user_id = impersonate_as
    )

    ## do something as someone else
    ##
    ##

    ## reset impersonation
    m.clear_impersonation()


Or you can use the impersonte method by itself.

.. code-block:: python

    from moco_wrapper import Moco

    m = Moco()

    ## do something as you
    ##
    ##

    impersonate_as = 43
    m.impersonate(impersonate_as)

    ## do something as someone else
    ##
    ##

    ## reset impersonation
    m.clear_impersonation()

.. seealso::

    :meth:`moco_wrapper.Moco.impersonate`, :meth:`moco_wrapper.Moco.clear_impersonation`.
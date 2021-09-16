from moco_wrapper.models import objector_models as obj


class PurchaseDraft(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "user" in kwargs.keys():
            u = obj.User(**kwargs["user"]);
            nk["user"] = u

        self.__dict__.update(nk)

from moco_wrapper.models import objector_models as obj

class Project(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "customer" in kwargs.keys() and kwargs["customer"] is not None:
            c = obj.Company(**kwargs["customer"])
            nk["customer"] = c

        self.__dict__.update(nk)
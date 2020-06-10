from moco_wrapper.models import objector_models as obj

class Purchase(object):
    def __init__(
        self,
        **kwargs
        ):

        nk = kwargs

        if "company" in kwargs.keys() and kwargs["company"] is not None:
            nk["company"] = obj.Company(**kwargs["company"]) 

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            nk["user"] = obj.User(**kwargs["user"])

        self.__dict__.update(nk)
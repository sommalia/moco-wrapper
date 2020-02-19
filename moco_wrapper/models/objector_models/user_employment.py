from moco_wrapper.models import objector_models as obj


class UserEmployment(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "from" in kwargs.keys():
            nk["from_date"] = kwargs["from"]
            del nk["from"]

        if "to" in kwargs.keys():
            nk["to_date"] = kwargs["to"]
            del nk["to"]

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = obj.User(**kwargs["user"])
            nk["user"] = u

        self.__dict__.update(nk)
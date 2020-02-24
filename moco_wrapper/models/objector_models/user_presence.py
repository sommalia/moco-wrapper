from moco_wrapper.models import objector_models as obj

class UserPresence(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "from" in kwargs.keys():
            nk["from_time"] = kwargs["from"]
            del nk["from"]

        if "to" in kwargs.keys():
            nk["to_time"] = kwargs["to"]
            del nk["to"]

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = obj.User(**kwargs["user"])
            nk["user"] = u


        self.__dict__.update(nk)
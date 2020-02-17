from .user import User

class Employment(object):
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
            u = User(**kwargs["user"])
            nk["user"] = u

        self.__dict__.update(nk)
from .user import User

class Comment(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = User(**kwargs["user"])
            nk["user"] = u

        self.__dict__.update(nk)
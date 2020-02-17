from .project import Project
from .deal import Deal

class Offer(object):
    def __init__(self, **kwargs):

        nk = kwargs
        if "project" in kwargs.keys() and kwargs["project"] is not None:
            p = Project(**kwargs["project"])
            nk["project"] = p

        if "deal" in kwargs.keys() and kwargs["deal"] is not None:
            d = Deal(**kwargs["deal"])
            nk["deal"] = d

        self.__dict__.update(nk)
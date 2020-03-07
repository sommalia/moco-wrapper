from moco_wrapper.models import objector_models as obj

class Offer(object):
    def __init__(self, **kwargs):

        nk = kwargs
        if "project" in kwargs.keys() and kwargs["project"] is not None:
            p = obj.Project(**kwargs["project"])
            nk["project"] = p

        if "deal" in kwargs.keys() and kwargs["deal"] is not None:
            d = obj.Deal(**kwargs["deal"])
            nk["deal"] = d

        self.__dict__.update(nk)
        
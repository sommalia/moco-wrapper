from moco_wrapper.models import objector_models as obj


class Deal(object):
    def __init__(self, **kwargs):

        nk = kwargs

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = obj.User(**kwargs["user"])
            nk["user"] = u
        
        if "category" in kwargs.keys() and kwargs["category"] is not None:
            cat = obj.DealCategory(**kwargs["category"])
            nk["category"] = cat

        if "company" in kwargs.keys() and kwargs["company"] is not None:
            com = obj.Company(**kwargs["company"])
            nk["company"] = com 

        self.__dict__.update(nk)
        
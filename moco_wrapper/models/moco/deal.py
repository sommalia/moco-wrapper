from .user import User
from .deal_category import DealCategory
from .company import Company

class Deal(object):
    def __init__(self, **kwargs):

        nk = kwargs

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = User(**kwargs["user"])
            nk["user"] = u
        
        if "category" in kwargs.keys() and kwargs["category"] is not None:
            cat = DealCategory(**kwargs["category"])
            nk["category"] = cat

        if "company" in kwargs.keys() and kwargs["company"] is not None:
            com = Company(**kwargs["company"])
            nk["company"] = com 

        self.__dict__.update(nk)
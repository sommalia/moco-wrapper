from moco_wrapper.models import objector_models as obj

class Activity(object):
    def __init__(
        self, 
        **kwargs
    ):
        nk = kwargs



        if "project" in kwargs.keys() and kwargs["project"] is not None:
            p = obj.Project(**kwargs["project"])
            nk["project"] = p

        if "task" in kwargs.keys() and kwargs["task"] is not None:
            t = obj.ProjectTask(**kwargs["task"])
            nk["task"] = t

        if "customer" in kwargs.keys() and kwargs["customer"] is not None:
            c = obj.Company(**kwargs["customer"])
            nk["customer"] = c

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = obj.User(**kwargs["user"])
            nk["user"] = u
    
        self.__dict__.update(nk)
        
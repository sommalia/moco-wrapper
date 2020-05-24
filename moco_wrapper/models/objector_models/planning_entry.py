from moco_wrapper.models import objector_models as obj


class PlanningEntry(object):
    def __init__(self, **kwargs):
        nk = kwargs

        if "project" in kwargs.keys() and kwargs["project"] is not None:
            p = obj.Project(**kwargs["project"])
            nk["project"] = p

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = obj.User(**kwargs["user"])
            nk["user"] = u

        self.__dict__.update(nk)

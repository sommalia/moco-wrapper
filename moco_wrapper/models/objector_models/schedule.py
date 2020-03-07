from moco_wrapper.models import objector_models as obj

class Schedule(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "assignment" in kwargs.keys() and kwargs["assignment"] is not None:
            a = ScheduleAssignment(**kwargs["assignment"])
            nk["assignment"] = a

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = obj.User(**kwargs["user"])
            nk["user"] = u

        self.__dict__.update(nk)

class ScheduleAssignment(object):
    def __init__(
        self,
        **kwargs
    ):
        self.__dict__.update(kwargs)
        
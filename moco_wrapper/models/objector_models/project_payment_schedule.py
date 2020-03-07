from moco_wrapper.models import objector_models as obj

class ProjectPaymentSchedule(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "project" in kwargs.keys() and kwargs["project"] is not None:
            p = obj.Project(**kwargs["project"])
            nk["project"] = p


        self.__dict__.update(nk)
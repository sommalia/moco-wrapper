from moco_wrapper.models import objector_models as obj

class ProjectReport(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "cost_by_task" in kwargs.keys() and kwargs["cost_by_task"] is not None:
            items = []
            for t in kwargs["cost_by_task"]:
                items.append(obj.Task(**t))
            nk["cost_by_task"] = items

        self.__dict__.update(nk)
            
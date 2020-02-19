from moco_wrapper.models import objector_models as obj

class Project(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "customer" in kwargs.keys() and kwargs["customer"] is not None:
            c = obj.Company(**kwargs["customer"])
            nk["customer"] = c

        if "leader" in kwargs.keys() and kwargs["leader"] is not None:
            u = obj.User(**kwargs["leader"])
            nk["leader"] = u

        if "contracts" in kwargs.keys() and kwargs["contracts"] is not None:
            items = []
            for c in kwargs["contracts"]:
                items.append(obj.ProjectContract(**c))
            nk["contracts"] = items

        if "tasks" in kwargs.keys() and kwargs["tasks"] is not None:
            items = []
            for t in kwargs["tasks"]:
                items.append(obj.ProjectTask(**t))
            nk["tasks"] = items

        self.__dict__.update(nk)
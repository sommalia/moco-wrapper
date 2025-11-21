from moco_wrapper.models import objector_models as obj


class ProjectGroup(object):
    def __init__(self, **kwargs):
        nk = kwargs

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = obj.User(**kwargs["user"])
            nk["user"] = u

        if "company" in kwargs.keys() and kwargs["company"] is not None:
            c = obj.Company(**kwargs["company"])
            nk["company"] = c

        if "projects" in kwargs.keys() and kwargs["projects"] is not None:
            items = []
            for c in kwargs["projects"]:
                items.append(obj.Project(**c))
            nk["projects"] = items

        self.__dict__.update(nk)

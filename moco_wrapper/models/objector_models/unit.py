from moco_wrapper.models import objector_models as obj


class Unit(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "users" in kwargs.keys() and kwargs["users"] is not None:
            items = []
            for u in kwargs["users"]:
                items.append(obj.User(**u))
            nk["users"] = items

        self.__dict__.update(nk)
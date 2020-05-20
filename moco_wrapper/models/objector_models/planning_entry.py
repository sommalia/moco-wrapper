from moco_wrapper.models import objector_models as obj


class PlanningEntry(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

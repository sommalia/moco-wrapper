from moco_wrapper.models import objector_models as obj


class Webhook(object):

    def __init__(self, **kwargs):

        nk = kwargs
        self.__dict__.update(nk)

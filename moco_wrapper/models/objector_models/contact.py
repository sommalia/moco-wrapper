from moco_wrapper.models import objector_models as obj

class Contact(object):
    def __init__(self, **kwargs):

        nk = kwargs

        if "company" in kwargs.keys() and kwargs["company"] is not None:
            c = obj.Company(**kwargs["company"])
            nk["company"] = c



        self.__dict__.update(nk)
        
from .company import Company

class Contact(object):
    def __init__(self, **kwargs):

        nk = kwargs

        if "company" in kwargs.keys() and kwargs["company"] is not None:
            c = Company(**kwargs["company"])
            nk["company"] = c



        self.__dict__.update(nk)
from moco_wrapper.models import objector_models as obj


class InvoicePayment(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        if "invoice" in kwargs.keys() and kwargs["invoice"] is not None:
            i = obj.Invoice(**kwargs["invoice"])
            nk["invoice"] = i

        self.__dict__.update(nk)
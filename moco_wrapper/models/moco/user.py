from .unit import Unit

class User(object):
    def __init__(
        self, 
        **kwargs
        ):
        
        nk = kwargs
        if "unit" in kwargs.keys():
            u = Unit(**kwargs["unit"])
            
            del nk["unit"]
            nk["unit"] = u

        self.__dict__.update(nk)
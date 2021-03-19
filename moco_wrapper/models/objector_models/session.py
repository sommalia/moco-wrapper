class SessionAuthentication(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs

        self.__dict__.update(nk)

class SessionVerification(object):
    def __init__(self):
        pass

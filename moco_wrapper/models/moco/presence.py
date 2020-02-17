class Presence(object):
    def __init__(
        self,
        **kwargs
    ):
        non_keyword_kwargs = kwargs

        if "from" in kwargs.keys():
            non_keyword_kwargs["from_time"] = kwargs["from"]
            del non_keyword_kwargs["from"]

        if "to" in kwargs.keys():
            non_keyword_kwargs["to_time"] = kwargs["to"]
            del non_keyword_kwargs["to"]


        self.__dict__.update(non_keyword_kwargs)
        print(non_keyword_kwargs)
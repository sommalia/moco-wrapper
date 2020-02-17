class Activity(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class DisregardedActivity(object):
    def __init__(self, ids: list):
        self.disregarded_ids = ids
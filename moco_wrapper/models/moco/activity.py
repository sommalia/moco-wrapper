from .project import Project
from .project_task import ProjectTask
from .company import Company
from .user import User

class Activity(object):
    def __init__(
        self, 
        **kwargs
    ):
        nk = kwargs

        if "project" in kwargs.keys() and kwargs["project"] is not None:
            p = Project(**kwargs["project"])
            nk["project"] = p

        if "task" in kwargs.keys() and kwargs["task"] is not None:
            t = ProjectTask(**kwargs["task"])
            nk["task"] = t

        if "customer" in kwargs.keys() and kwargs["customer"] is not None:
            c = Company(**kwargs["customer"])
            nk["customer"] = c

        if "user" in kwargs.keys() and kwargs["user"] is not None:
            u = User(**kwargs["user"])
            nk["user"] = u
    
        self.__dict__.update(nk)
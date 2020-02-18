from .project import Project
from .company import Company

class ProjectExpense(object):
    def __init__(
        self,
        **kwargs
    ):
        nk = kwargs
        
        if "project" in kwargs.keys() and kwargs["project"] is not None:
            p = Project(**kwargs["project"])
            nk["project"] = p

        if "company" in kwargs.keys() and kwargs["company"] is not None:
            c = Company(**kwargs["company"])
            nk["company"] = c

        self.__dict__.update(nk)
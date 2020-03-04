from .base import MWRAPResponse
from json import dumps

class ListingResponse(MWRAPResponse):
    """
    Class for handling http responses where the response body is a json list.

    Listings in Moco are usually paginated (if there are more than 100 items that fit your request).
    
    Example usage:

    .. code-block:: python

        from moco_wrapper import Moco

        m = Moco()
        all_projects = []

        project_list = m.Project.getlist()
        all_projects.extend(project_list.items)

        while not project_list.is_last:
            project_list = m.Project.getlist(page=project_list.next_page) 
            all_projects.extend(project_list.items)
         
    Or with a for loop:

    .. code-block:: python

        from moco_wrapper import Moco

        m = Moco
        all_projects = []

        project_list = m.Project.getlist()
        all_projects.extend(project_list.items)

        for i in range(2, project_list.last_page + 1): #first page alread queried
            project_list = m.Project.getlist(page=i) 
            all_projects.extend(project_list.items)
    """

    @property 
    def items(self) -> list:
        """
        Get the list of objects the response contains

        :type: list

        .. code-block:: python

            m = Moco()
            project_list = m.Project.getlist()

            for item in project_list.items:
                print(item)

        .. seealso:: 

            :attr:`data`
        """
        return self._data

    
    @property
    def current_page(self) -> int:
        """
        Returns the current page number

        :type: int  
        """
        return self._current_page

    @property 
    def page_size(self) -> int:
        """
        Returns the amount of items that are in the current page (usually 100)

        :type: int  
        """
        return self._page_size

    @property
    def total(self) -> int:
        """
        Returns the amount of items that are in the current (paginated) collection

        :type: int
        """
        return self._total

    @property
    def is_last(self) -> int:
        """
        Returns wether the current page is the last page

        :type: int  
        """
        return self._is_last

    @property
    def next_page(self) -> int:
        """
        Returns the next page number

        :type: int  

        .. note::

            Do not use this for checking if there is another page, use :meth:`.is_last`
        """
        return self._current_page + 1

    @property
    def last_page(self) -> bool:
        """
        Returns the last page number

        :type: bool  
        """
        last_page = int(self.total / self.page_size)
        if self.total % self.page_size == 0:
            return last_page
        else:
            return last_page + 1

    @property
    def data(self) -> list:
        """
        Returns the list of object the response contains

        :type: list

        .. seealso:: 

            :attr:`items`
        """
        return self._data
    

    def __init__(self, response):
        """
        Class constructor

        :param response: http response object
        """
        super(ListingResponse, self).__init__(response)

        #loop over every single item in the json dictionary and convert it into an object by itself
        json_content = response.json()
        items = []
        for json_item in json_content:
            items.append(json_item)

        self._data = items

        if "x-page" in response.headers.keys():
            self._current_page = int(response.headers["x-page"])
        else:
            self._current_page = 1

        if "x-total" in response.headers.keys():
            self._total = int(response.headers["x-total"])
        else:
            self._total = len(items)
        
        if  "x-per-page" in response.headers.keys():
            self._page_size = int(response.headers["x-per-page"])
        else:
            self._page_size = self._total

        #print(response.headers)

        if "Link" in response.headers.keys():
            link_parts =response.headers["Link"].split(",")
            rel = []
            #extract rels
            for link in link_parts:
                _rel = link.split("; rel=")[-1].strip().replace("\"", "")
                rel.append(_rel)

            self._is_last = "last" not in rel
        else:
            self._is_last = True


    def __str__(self):
         return "<ListingResponse, Status Code: {}, Data: {}>".format(self.response.status_code, str(self._data))

        
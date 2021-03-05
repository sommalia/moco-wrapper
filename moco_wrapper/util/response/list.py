from .base import MWRAPResponse
from json import dumps


class ListResponse(MWRAPResponse):
    """
    Class for handling responses where the response body is a json list.

    The difference to :class:`moco_wrapper.util.response.PagedListResponse` is that ListResponses are not paged.
    """

    def __init__(self, response):
        """
        Class constructor

        :param response: http response object
        """
        super(ListResponse, self).__init__(response)

        # loop over every single item in the json dictionary and convert it into an object by itself
        json_content = response.json()
        items = []
        for json_item in json_content:
            items.append(json_item)

        self._data = items

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
    def data(self) -> list:
        """
        Returns the list of object the response contains

        :type: list

        .. seealso::

            :attr:`items`
        """
        return self._data

    def __iter__(self):
        """
        Returns the iterator of the items list so we can loop over the response
        """
        return iter(self.items)

    def __getitem__(self, key):
        """
        Return the item of items with at key i

        :param key: Index
        :returns: item at key
        """
        return self.items[key]

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return "<ListResponse, Status Code: {}, Data: {}>".format(self.response.status_code, str(self._data))

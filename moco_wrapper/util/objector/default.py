from .base import BaseObjector

from moco_wrapper.util.response import EmptyResponse, JsonResponse, ListingResponse, ErrorResponse

from importlib import import_module

class DefaultObjector(BaseObjector):
    """
    This is the default class for handling the modification ob response objects that the requestor classes generated and were pushed to the objector.

    Successfull responses will have their data converted into actual python objects, while error responses will be converted into exceptions and raised at a later stage.

    .. note::

        If you do not want exceptions to be raised see :class:`moco_wrapper.util.objector.NoErrorObjector`

    """

    def __init__(self):
        self.module_path = "moco_wrapper.models.objector_models"

        self.class_map = {
            "projects": {
                "base": "Project",
                "tasks" : "ProjectTask",
                "archive": "Project",
                "unarchive": "Project",
                "assigned": "Project",
                "report": "ProjectReport",
                "contracts": "ProjectContract",
                "expenses": {
                    "base": "ProjectExpense",
                    "bulk": "ProjectExpense"
                },
                "recurring_expenses": "ProjectRecurringExpense",
                "payment_schedules": "ProjectPaymentSchedule",
            },
            "activities": {
                "base" : "Activity",
                "start_timer": "Activity",
                "stop_timer": "Activity",
                "disregard": None
            },
            "users": {
                "base" : "User",
                "presences": "UserPresence",
                "employments": "UserEmployment",
                "holidays": "UserHoliday"
            },
            "units": {
                "base": "Unit"
            },
            "offers": {
                "base": "Offer",
            },
            "invoices": {
                "base": "Invoice",
                "locked": "Invoice",
                "payments": {
                    "base": "InvoicePayment",
                    "bulk": "InvoicePayment"
                },
            },
            "deals": {
                "base": "Deal"
            },
            "deal_categories": {
                "base": "DealCategory"
            },
            "companies": {
                "base": "Company"
            },
            "contacts": {
                "base": "Contact",
                "people": "Contact"
            },
            "comments": {
                "base": "Comment",
                "bulk": "Comment",
            },
            "schedules": {
                "base": "Schedule"
            },
            "session": {
                "base" : "Session"
            },
            "purchases": {
                "base" : "Purchase",
                "categories": "PurchaseCategory"
            },
            "planning_entries": {
                "base": "PlanningEntry"
            }
        }
        """
        Dictionary used to find the appropriate classes from url-part-path created in :meth:`get_class_name_from_request_url`

        For example the path ``project=>tasks`` means ``ProjectTask`` is the responsible class. The dictionary contains the following:

        .. code-block:: python

            "projects": {
                "base" => "Project",
                "tasks" => "ProjectTask"
            }
        """

        self.error_module_path = "moco_wrapper.exceptions"

        self.error_class_map = {
            401 : "UnauthorizedException",
            403 : "ForbiddenException",
            404 : "NotFoundException",
            422 : "UnprocessableException",
            429 : "RateLimitException",
            500 : "ServerErrorException"
        }
        """
        Dictionary used to convert http status codes into the appropriate exceptions

        .. code-block:: python

            self.error_class_map = {
                404: "NotFoundException",
                ..
            }
        """


    def convert(self, requestor_response):
        """
        Converts the data of a response object (for example json) into a python object.

        :param requestor_response: response object (see :ref:`response`)
        :returns: modified response object

        .. note:: The data of an error resposne response (:class:`moco_wrapper.util.response.ErrorResponse`) will be converted into an actual exception that later can be raised

        .. note:: if the method :meth:`get_class_name_from_request_url` that is used to find the right class for conversion, returns ``None``, no conversion of objects will take place
        """
        http_response = requestor_response.response

        if isinstance(requestor_response, (JsonResponse, ListingResponse) ):
            class_name = self.get_class_name_from_request_url(http_response.request.url)

            if class_name is not None:
                class_ = getattr(
                    import_module(self.module_path),
                    class_name
                )


                if isinstance(requestor_response, JsonResponse):
                    obj = class_(**requestor_response.data)
                    requestor_response._data = obj
                elif isinstance(requestor_response, ListingResponse):
                    new_items = []

                    for item in requestor_response.items:
                        new_items.append(
                            class_(**item)
                        )

                    requestor_response._data = new_items

        elif isinstance(requestor_response, ErrorResponse):
            #convert the data for the error response into an actual exception
            class_name = self.get_error_class_name_from_response_status_code(http_response.status_code)

            if class_name is not None:
                class_ = getattr(
                    import_module(self.error_module_path),
                    class_name
                )

                #overwrite data of the error response with the actual exception
                obj = class_(http_response, requestor_response.data)
                requestor_response._data = obj

        return requestor_response

    def get_error_class_name_from_response_status_code(self, status_code) -> str:
        """
        Get the class name of the exception class based on the given http status code

        :param status_code: Http status code of the response

        :type status_code: int

        :returns: class name of the exception

        .. warning::

            The ``status_code`` parameter must be a key in :attr:`.error_class_map`

        """
        if status_code in self.error_class_map.keys():
            return self.error_class_map[status_code]

        #raise error if status code was not found
        raise ValueError("Objector could not find an error type, but it should, status_code: {}".format(status_code))


    def get_class_name_from_request_url(self, url) -> str:
        """
        Finds the class name by analysing the request url.

        :param url: url to analyse

        :type url: str


        This function works as follows:

        The url will look something like this ``https://test.mocoapp.com/api/v1/projects/1234/tasks?page=1``.
        We split the url on ``/api/v1/``.

            ``[https://test.mocoapp.com", "projects/1234/tasks?page=1"]``

        After that we throw away the first part and split the second part on the slash character:

            ``["projects", 1234, "tasks?page=1"]``

        Then we remove all query string parameters:

            ``["projects", 1234, "tasks"]``

        Then we remove all parts that are ids(digits):

            ``["projects", "tasks"]``

        Now that we have our path ``projects=>tasks``, we use the :attr:`class_map` to find the right classname.

        The map is a dictionary that looks something like this:

        .. code-block:: python

            class_map = {
                "activities" => {
                    "base" => "Activity"
                    "disregard" => None
                },
                "projects": {
                    "base" => "Project",
                    "tasks" => "ProjectTask"
                },
                "users" => { .. },
                "companies" => { .. }
            }

        We use the path we generated and walk our class_map until we get the entry at the end of the path. In our case that would be ``ProjectTask``. As this value is a string that is our final classname.

        .. note:: if the final value is a dictionary, the base case will be returned. For example if path was ``projects``, the value at the end of our path is a dictionary. If that is the case the *base* key will be used.
        """

        parts = url.split("/api/v1/")[-1].split("/")

        #remove ids and query string parameters
        parts = [x for x in parts if not x.isdigit()]
        if "?" in parts[-1]:
            parts[-1] = parts[-1].split("?")[0]


        #find classname by walking the classname
        #pop the first item from the stack
        #look into map if our item is a key of the map
        #set map to map[key]
        #repeat until stack is empty -> last value should be the class name
        current_map = self.class_map
        stack = [x for x in parts]
        while len(stack) > 0:
            key = stack.pop(0)
            if isinstance(current_map, dict) and key in current_map.keys():
                current_map = current_map[key]
            else:
                raise ValueError("Objector could not find a type, but it should, path: {}".format(">".join(parts)))


        if current_map is None:
            return None #no type conversion

        if isinstance(current_map, str):
            return current_map #current map is a specific class name

        if isinstance(current_map, dict):
            return current_map["base"] #more cases are present but we need the base case

from moco_wrapper.const import API_PATH
from moco_wrapper import models, util, exceptions
from moco_wrapper.util import requestor, objector

from requests import get, post, put, delete

class Moco(object):
    """
    Main Moco class for handling authentication, object conversion, requesting ressources with the moco api
    
    :param api_key: user specific api key
    :param domain: the subdomain part of your moco-url (if your full url is ``https://testabcd.mocoapp.com``, provide ``testabcd``)
    :param objector: objector object (see :ref:`objector`, default: :class:`moco_wrapper.util.objector.DefaultObjector`)
    :param requestor: requestor object (see :ref:`requestor`, default: :class:`moco_wrapper.util.requestor.DefaultRequestor`)
    :param impersonate_user_id: user id the client should impersonate (default: None, see https://github.com/hundertzehn/mocoapp-api-docs#impersonation)

    
    .. code-block:: python

        import moco_wrapper
        moco = moco_wrapper.Moco(
            api_key="<TOKEN>",
            domain="<DOMAIN>"
        )
    """
    def __init__(
        self, 
        api_key: str = None, 
        domain: str = None, 
        objector = objector.DefaultObjector(), 
        requestor = requestor.DefaultRequestor(),
        impersonate_user_id: int = None,
        **kwargs):

        self.api_key = api_key
        self.domain = domain

        self.Activity = models.Activity(self)
        self.Contact = models.Contact(self)
        self.Company = models.Company(self)
        self.Comment = models.Comment(self)
        self.Unit = models.Unit(self)

        self.User = models.User(self)
        self.UserPresence = models.UserPresence(self)
        self.UserHoliday = models.UserHoliday(self)
        self.UserEmployment = models.UserEmployment(self)
        
        self.Schedule = models.Schedule(self)

        self.Project = models.Project(self)
        self.ProjectContract = models.ProjectContract(self)
        self.ProjectExpense = models.ProjectExpense(self)
        self.ProjectTask = models.ProjectTask(self)
        self.ProjectRecurringExpense = models.ProjectRecurringExpense(self)

        self.Deal = models.Deal(self)
        self.DealCategory = models.DealCategory(self)

        self.Invoice = models.Invoice(self)
        self.InvoicePayment = models.InvoicePayment(self)
        self.Offer = models.Offer(self)
        

        self._requestor = requestor
        self._objector = objector

        #set default values if not already set
        if self._requestor is None:
            #default requestor is one that will fire 1 request every second
            self._requestor = util.requestor.DefaultRequestor()

        if self._objector is None:
            #default: no conversion on reponse objects
            self._objector = util.objector.DefaultObjector()

        self._impersonation_user_id = impersonate_user_id

    def request(self, method, path, params=None, data=None):
        """
        request the given ressource with the assigned requestor

        :param method: HTTP Method (eg. POST, GET, PUT, DELETE)
        :param path: path of the ressource (e.g. ``/projects``)
        :param params: url parameters (e.g. ``page=1``, query parameters)
        :param data: dictionary with data (http body) 

        The request will be given to the currently assinged requestor (see :ref:`requestor`).
        The response will then be given to the currently assinged objector (see :ref:`objector`)
        
        The *possibly* modified response will then be returned
        """

        full_path = self.full_domain + path
        response = None

        if method == "GET":
            response = self._requestor.get(full_path, params=params, data=data, headers=self.headers)
        elif method == "PUT":
            response = self._requestor.put(full_path, params=params, data=data, headers=self.headers)
        elif method == "POST":
            response = self._requestor.post(full_path, params=params, data=data, headers=self.headers)
        elif method == "DELETE":
            response = self._requestor.delete(full_path, params=params, data=data, headers=self.headers)
        elif method == "PATCH":
            response = self._requestor.patch(full_path, params=params, data=data, headers=self.headers)


        #push the response to the current objector
        result = self._objector.convert(response)

        #if the result is an exception we raise it, otherwise return it
        if isinstance(result, exceptions.MocoException):
            raise result
        else:
            return result


    def get(self, path, params=None, data=None):
        return self.request("GET", path, params=params, data=data)
        
    def post(self, path, params=None, data=None):
        return self.request("POST", path, params=params, data=data)

    def put(self, path, params=None, data=None):
        return self.request("PUT", path, params=params, data=data)

    def delete(self, path, params=None, data=None):
        return self.request("DELETE", path, params=params, data=data)

    def patch(self, path, params=None, data=None):
        return self.request("PATCH", path, params=params, data=data)


    def impersonate(self, user_id):
        """
        Impersontates the user with the supplied user id

        :param user_id: user id to impersonate

        .. seealso::
            
            :meth:`clear_impersonation` to end impersonation of ``user_id``

        """
        self._impersonation_user_id = user_id

    def clear_impersonation(self):
        """
        Ends impersonation

        .. seealso::

            :meth:`impersonate`

        """
        self._impersonation_user_id = None

    @property
    def headers(self):
        """
        Returns all http headers to be used by the assigned requestor
        """
        headers = {
            'Content-Type' : 'application/json',
            'Authorization': 'Token token={}'.format(self.api_key)
        }

        if self._impersonation_user_id is not None:
            headers["X-IMPERSONATE-USER-ID"] = str(self._impersonation_user_id)

        return headers

    @property
    def full_domain(self):
        """
        Returns the full url of the moco api

        .. code-block:: python

            >> m = Moco(domain="testabcd")
            >> print(m.full_domain)
            https://testabcd.mocoapp.com/api/v1

        """
        return "https://{}.mocoapp.com/api/v1".format(self.domain)

    @property
    def session(self):
        """
        Get the http.session object of the current requestor (None if the requestor does not have a session)
        """
        
        return self._requestor.session

    @property
    def objector(self):
        """
        Get the currently assigned objector object

        .. seealso::

            :ref:`objector`
        """
        return self._objector

    @property
    def requestor(self):
        """
        Get the currently assigned requestor object

        .. seealso::

            :ref:`requestor`
        """
        return self._requestor
    
    
    

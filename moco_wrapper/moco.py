# -*- coding: utf-8 -*-

from moco_wrapper import models, util
from .const import API_PATH

from requests import get, post, put, delete
from json import dumps

"""Main module."""
class Moco(object):
    """
    Main Moco class for handling authentication, object conversion, requesting ressources with the moco api

    .. code-block:: python

        import moco_wrapper
        moco = moco_wrapper.Moco(
            api_key="<TOKEN>",
            domain="<DOMAIN>"
        )
    
    :param api_key: user specific api key
    :param domain: your company specific moco domain part (if your full domain is https://testabcd.mocoapp.com, provide testabcd)
    :param objector: objector (see util.objector)
    :param requestor: requestor (see util.requestor) 
    :param impersonate_user_id: user id the client should impersonate (default none, see https://github.com/hundertzehn/mocoapp-api-docs#impersonation)
    """
    def __init__(
        self, 
        api_key = None, 
        domain = None, 
        objector = util.objector.DefaultObjector(), 
        requestor = util.requestor.DefaultRequestor(),
        impersonate_user_id = None,
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

    def request(self, method, path, params=None, data=None, current_try=1):
        """Send a request to an URL with the specified params and data
        :returns an object that was returns by the objetor currently assigned to the moco warpper object
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
        return self._objector.convert(response)


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
        """
        self._impersonation_user_id = user_id

    def clear_impersonation(self):
        """
        Clears impersonation
        """
        self._impersonation_user_id = None

    @property
    def headers(self):
        headers = {
            'Content-Type' : 'application/json',
            'Authorization': 'Token token={}'.format(self.api_key)
        }

        if self._impersonation_user_id is not None:
            headers["X-IMPERSONATE-USER-ID"] = self._impersonation_user_id

        return headers

    @property
    def full_domain(self):
        return "https://{}.mocoapp.com/api/v1".format(self.domain)

    @property
    def session(self):
        """
        Get the http.session object of the current requestor

        :returns: requestors session object (None if the requestor does not have a session)
        """
        
        return self._requestor.session

    @property
    def objector(self):
        """
        Get the currently assigned objector object

        :returns: the currently assigned objector
        """
        return self._objector
    
    

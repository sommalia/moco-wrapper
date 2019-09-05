# -*- coding: utf-8 -*-

from . import models
from requests import get, post, put, delete
from json import dumps
from .const import API_PATH

"""Main module."""
class Moco(object):
    """The Moco class provides access to moco's api

    .. code-block:: python

    import moco_wrapper
    moco = moco_wrapper.Moco(email='EMAIL_ADDRESS', password='PASSWORD', api_key='API_KEY', domain='DOMAIN')

    """
    def __init__(self, api_key = None, domain = None):
        self.api_key = api_key
        self.domain = domain

        #init contacts model

        self.Contact = models.Contact(self)
        self.Company = models.Company(self)
        self.Unit = models.Unit(self)
        self.Project = models.Project(self)
        self.ProjectContract = models.ProjectContract(self)

    def request(self, method, path, params=None, data=None):
        """Send a request to an URL with the specified params and data"""
        if method == "GET":
            return self.get(path, params=params, data=data)
        elif method == "PUT":
            return self.put(path, params=params, data=data)
        elif method == "POST":
            return self.post(path, params=params, data=data)
        elif method == "DELETE":
            return self.delete(path, params=params, data=data)
        
    def get(self, path, params=None, data=None):
        response = get(self.full_domain + path, json=data, headers=self.headers, params=params)
        return response
        
    def post(self, path, params=None, data=None):
        response = post(self.full_domain + path, json=data, headers=self.headers, params=params)
        return response

    def put(self, path, params=None, data=None):
        response = put(self.full_domain + path, json=data, headers=self.headers, params=params)
        return response

    def delete(self, path, params=None, data=None):
        response = delete(self.full_domain + path, json=data, headers=self.headers, params=params)
        return response

    @property
    def headers(self):
        headers = {
            'Content-Type' : 'application/json',
            'Authorization': 'Token token={}'.format(self.api_key)
        }
        return headers

    @property
    def full_domain(self):
        return "https://{}.mocoapp.com/api/v1".format(self.domain)

    
    

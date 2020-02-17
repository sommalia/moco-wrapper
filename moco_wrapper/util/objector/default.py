from .base import BaseObjector

from moco_wrapper.models.moco.activity import Activity
from moco_wrapper.util.response import EmptyResponse, JsonResponse, ListingResponse

from importlib import import_module

class DefaultObjector(BaseObjector):
    def __init__(self):
        self.module_path = "moco_wrapper.models.moco"
    

    def convert(self, wrapper_response):
        http_response = wrapper_response.response

       
        if isinstance(wrapper_response, JsonResponse):
            class_name = self._get_class_name_from_request_url(http_response.request.url)
            class_ = getattr(import_module("moco_wrapper.models.moco"), class_name)
            
            obj = class_(**wrapper_response.data)
            wrapper_response._data = obj
        elif isinstance(wrapper_response, EmptyResponse):
            pass # do nothing reponse.data is None
        elif isinstance(wrapper_response, ListingResponse):
            class_name = self._get_class_name_from_request_url(http_response.request.url)
            class_ = getattr(import_module("moco_wrapper.models.moco"), class_name)

            new_items = []
            for old_item in wrapper_response.items:
                if isinstance(old_item, dict):
                    new_items.append(class_(**old_item))

            if len(new_items) > 0:
                wrapper_response._data = new_items
        
        return wrapper_response

    def _get_class_name_from_request_url(self, url):
        parts = url.split("/api/v1/")[-1].split("/")
        
        #remove ids from parts
        parts = [x for x in parts if not x.isdigit()]
        if "?" in parts[-1]:
            parts[-1] = parts[-1].split("?")[0]

        if len(parts) == 1:
            #single part
            s_part = parts[0]
            if s_part == "projects":
                return "Project"
            elif s_part == "users":
                return "User"
            elif s_part == "units":
                return "Unit"
            elif s_part == "offers":
                return "Offer"
            elif s_part == "invoices":
                return "Invoice"
            elif s_part == "deals":
                return "Deal"
            elif s_part == "deal_categories":
                return "DealCategory"
            elif s_part == "companies":
                return "Company"
            elif s_part == "activities":
                return "Activity"

        if len(parts) == 2:
            first, sec = parts

            if first == "projects" and sec == "tasks":
                return "ProjectTask"
            elif first == "projects" and sec in ["archive", "unarchive", "report", "assigned"]:
                return "Project"
            elif first == "users" and sec == "presences":
                return "Presence"
            elif first == "contacts" and sec == "people":
                return "Contact"
            elif first == "activities" and sec in ["start_timer", "stop_timer"]:
                return "Activity"
            elif first == "activities" and sec in ["disregard"]:
                return "DisregardedActivity"
            elif first == "invoices" and sec == "locked":
                return "Invoice"



        print (parts)
        exit(1) 
        
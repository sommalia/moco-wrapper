from .base import BaseObjector

from moco_wrapper.models.moco.activity import Activity
from moco_wrapper.util.response import EmptyResponse, JsonResponse, ListingResponse

from importlib import import_module

class DefaultObjector(BaseObjector):
    def __init__(self):
        self.module_path = "moco_wrapper.models.moco"
    
        self.class_map = {
            "projects": {
                "base": "Project",
                "tasks" : "ProjectTask",
                "archive": "Project",
                "unarchive": "Project",
                "assigned": "Project",
                "report": "Project"
            },
            "activities": {
                "base" : "Activity",
                "start_timer": "Activity",
                "stop_timer": "Activity",
                "disregard": None
            },
            "users": {
                "base" : "User",
                "presences": "Presence",
                "employments": "Employment",
                "holidays": "Holiday"
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
                "payments": "InvoicePayment",
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
            }
        }


    def convert(self, wrapper_response):
        http_response = wrapper_response.response

        if isinstance(wrapper_response, JsonResponse) or isinstance(wrapper_response, ListingResponse):
            class_name = self._get_class_name_from_request_url(http_response.request.url)

            if class_name is not None:
                class_ = getattr(
                    import_module(self.module_path),
                    class_name
                )

                
                if isinstance(wrapper_response, JsonResponse):
                    obj = class_(**wrapper_response.data)
                    wrapper_response._data = obj
                elif isinstance(wrapper_response, ListingResponse):
                    new_items = []

                    for item in wrapper_response.items:
                        new_items.append(
                            class_(**item)
                        )

                    wrapper_response._data = new_items

        return wrapper_response

    def _get_class_name_from_request_url(self, url):
        """
        finds the class name by analysing the request url

        :param url: url to analyse

        the url will look something like this https://test.mocoapp.com/api/v1/projects/1234/tasks?page=1
        we split the url on the api part and slashes ["projects", 1234, "tasks?page=1"]
        the we remove id parts and query string parameters ["projects", "tasks"]
        then with the class map we find the corresponding class name to return

        "projects" : {
            "tasks" : "ProjectTask"
        }

        "ProjectTask will get returned"
        """
        
        parts = url.split("/api/v1/")[-1].split("/")
        
        #remove ids and query string parameters
        parts = [x for x in parts if not x.isdigit()]
        if "?" in parts[-1]:
            parts[-1] = parts[-1].split("?")[0]

        #append base case if url contains no secondary type
        if len(parts) == 1:
            parts.append("base")

        general_type, sub_type = parts

        if general_type in self.class_map.keys():
            if sub_type in self.class_map[general_type].keys():
                return self.class_map[general_type][sub_type]    
        
        #return None by default (no conversion of objects will take place)
        
        print("Objector could not find a type, but should")
        print(parts)
        exit(1)
        return None

        


        
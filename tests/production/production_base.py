import pytest   
import json
import os

from moco_wrapper.moco_wrapper import Moco

class ProductionTest(object):

    def setup(self):
        self.setup_moco()

    def setup_moco(self):
        #read local config  
        config = None

        self.api_key = ""
        self.domain = ""


        config_path = os.path.join(os.path.dirname(__file__), "config.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)

            self.api_key = config["api_key"]
            self.domain = config["domain"]

        self._moco = Moco(api_key=self.api_key, domain=self.domain)

    @property
    def moco(self):
        return self._moco
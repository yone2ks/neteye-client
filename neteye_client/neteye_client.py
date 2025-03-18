import requests

from neteye_client.base import RestClient
from neteye_client.node.node import node
from neteye_client.interface.interface import interface

class NeteyeClient(RestClient):
    def __init__(self, url):
        self.node = node(self)
        self.interface = interface(self)
        super().__init__(url)

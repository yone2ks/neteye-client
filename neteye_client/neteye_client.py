import requests
from neteye_client.node import Node


class NeteyeClient:
    def __init__(self, url):
        self.url = url

    def get(self, path):
        return requests.get(url=f"{self.url}{path}").json()

    def post(self, path, data):
        return requests.post(url=f"{self.url}{path}", data=data)
    
    def put(self, path, data):
        return requests.put(url=f"{self.url}{path}", data=data) 
    
    def delete(self, path):
        return requests.delete(url=f"{self.url}{path}") 
    
    def get_node(self, id):
        path = f"{Node.NODE_PATH}/{id}"
        return Node.from_dict(self.get(path))
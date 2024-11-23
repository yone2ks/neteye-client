import requests


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
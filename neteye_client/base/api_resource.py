from typing import Optional

from .rest_client import RestClient

class APIResource():
    def __init__(self, client):
        self.client = client
        super().__init__()
        
    def get(self, id: Optional[str] = None):
        if id is None:
            data = self.client.get(self.PATH)
            return [self.MODEL.from_dict(item) for item in data]
        else:
            data = self.client.get(f"{self.PATH}/{id}")
            return self.MODEL.from_dict(data)
    
    def create(self, data):
        data = self.client.post(self.PATH, data)
        return self.MODEL.from_dict(data)
    
    def update(self, id, data):
        data = self.client.put(f"{self.PATH}/{id}", data)
        return self.MODEL.from_dict(data)
    
    def delete(self, id):
        data = self.client.delete(f"{self.PATH}/{id}")
        return self.MODEL.from_dict(data)
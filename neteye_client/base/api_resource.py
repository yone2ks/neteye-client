from typing import Optional

from .rest_client import RestClient

class APIResource():
    def __init__(self, client):
        self.client = client
        super().__init__()
        
    def get(self, id: Optional[str] = None):
        if id is None:
            response = self.client.get(self.PATH)
            return [self.MODEL.from_dict(item) for item in response]
        else:
            response = self.client.get(f"{self.PATH}/{id}")
            return self.MODEL.from_dict(response)
    
    def create(self, data):
        if data.get('id'):
            del data['id']
        response = self.client.post(self.PATH, data)
        return self.MODEL.from_dict(response)
    
    def update(self, id, data):
        response = self.client.put(f"{self.PATH}/{id}", data)
        return self.MODEL.from_dict(response)
    
    def delete(self, id):
        response = self.client.delete(f"{self.PATH}/{id}")
        return response
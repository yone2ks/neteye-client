import requests
from urllib.parse import urljoin
class RestClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        headers = {
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(headers)

    def get(self, path, params=None):
        url = urljoin(self.base_url, path)
        response = self.session.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def post(self, path, data=None):
        url = urljoin(self.base_url, path)
        response = self.session.post(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def put(self, path, data):
        url = urljoin(self.base_url, path)
        response = self.session.put(url, json=data, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
    
    def delete(self, path):
        url = urljoin(self.base_url, path)
        response = self.session.delete(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

from typing import Optional, List, Union
from ipaddress import IPv4Address
import re

from .rest_client import RestClient, APIError

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

    def create(self, data: Union[dict, object]):
        """Create a new resource."""
        if hasattr(data, 'to_dict'):
            data = data.to_dict()

        if isinstance(data, dict) and data.get('id'):
            del data['id']

        if hasattr(self, 'MODEL'):
            self._validate_data(data)

        try:
            response = self.client.post(self.PATH, data)
            return self.MODEL.from_dict(response)
        except APIError as e:
            if e.status_code == 400:
                raise APIError(f"Validation failed for {self.MODEL.__name__}: {e.message}", e.status_code)
            else:
                raise
        except ValueError as e:
            raise APIError(f"Client validation failed: {str(e)}", 400)

    def update(self, id: str, data: Union[dict, object]):
        """Update an existing resource."""
        if not id:
            raise ValueError("ID cannot be empty")

        if hasattr(data, 'to_dict'):
            data = data.to_dict()

        response = self.client.put(f"{self.PATH}/{id}", data)
        return self.MODEL.from_dict(response)

    def delete(self, id: str):
        """Delete a resource by ID."""
        if not id:
            raise ValueError("ID cannot be empty")

        response = self.client.delete(f"{self.PATH}/{id}")
        return response

    def _validate_data(self, data: dict):
        """Validate resource data using the resource's VALIDATOR function."""
        # Access via class __dict__ to avoid Python descriptor binding (VALIDATOR is a plain
        # function, not a staticmethod, so self.VALIDATOR would incorrectly bind self as first arg)
        validator = type(self).__dict__.get('VALIDATOR')
        if validator:
            validator(data)

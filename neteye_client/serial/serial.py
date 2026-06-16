from dataclasses import dataclass
from typing import Optional

from neteye_client.base import APIResource


@dataclass
class Serial:

    id: Optional[str] = None
    node_id: Optional[str] = None
    serial_number: str = ''
    product_id: str = ''
    description: str = ''

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            node_id=data.get('node_id'),
            serial_number=data.get('serial_number', ''),
            product_id=data.get('product_id', ''),
            description=data.get('description', ''),
        )

    def to_dict(self):
        required_fields = {
            'node_id': self.node_id,
            'serial_number': self.serial_number,
        }

        optional_fields = {
            'id': self.id,
            'product_id': self.product_id,
            'description': self.description,
        }

        data = required_fields.copy()

        for key, value in optional_fields.items():
            if value:
                data[key] = value

        return data


class serial(APIResource):
    PATH = '/api/serials'
    MODEL = Serial

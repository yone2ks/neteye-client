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
            if value is not None and value != '':
                data[key] = value

        return data


def _validate_serial_data(data: dict) -> None:
    required_fields = ['node_id', 'serial_number']

    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Required field '{field}' is missing or empty")

    serial_number = data.get('serial_number', '').strip()
    if not serial_number or len(serial_number) < 3:
        raise ValueError("Serial number must be at least 3 characters long")


class serial(APIResource):
    PATH = '/api/serials'
    MODEL = Serial
    VALIDATOR = _validate_serial_data

    def filter_by_serial_number(self, serial_number: str):
        path = f"{self.PATH}/filter?field=serial_number&filter_str={serial_number}"
        response = self.client.get(path)
        return [self.MODEL.from_dict(item) for item in response]

    def filter_by_product_id(self, product_id: str):
        path = f"{self.PATH}/filter?field=product_id&filter_str={product_id}"
        response = self.client.get(path)
        return [self.MODEL.from_dict(item) for item in response]

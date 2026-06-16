from dataclasses import dataclass
from typing import Optional

from neteye_client.base import APIResource


@dataclass
class Cable:

    id: Optional[str] = None
    a_interface_id: Optional[str] = None
    b_interface_id: Optional[str] = None
    cable_type: str = ''
    link_speed: str = ''
    description: str = ''

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            a_interface_id=data.get('a_interface_id'),
            b_interface_id=data.get('b_interface_id'),
            cable_type=data.get('cable_type', ''),
            link_speed=data.get('link_speed', ''),
            description=data.get('description', ''),
        )

    def to_dict(self):
        required_fields = {
            'a_interface_id': self.a_interface_id,
            'b_interface_id': self.b_interface_id,
        }

        optional_fields = {
            'id': self.id,
            'cable_type': self.cable_type,
            'link_speed': self.link_speed,
            'description': self.description,
        }

        data = required_fields.copy()

        for key, value in optional_fields.items():
            if value is not None and value != '':
                data[key] = value

        return data


def _validate_cable_data(data: dict) -> None:
    required_fields = ['a_interface_id', 'b_interface_id']

    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Required field '{field}' is missing or empty")

    if data.get('a_interface_id') == data.get('b_interface_id'):
        raise ValueError("Cannot connect an interface to itself")


class cable(APIResource):
    PATH = '/api/cables'
    MODEL = Cable
    VALIDATOR = _validate_cable_data

    def filter_by_cable_type(self, cable_type: str):
        path = f"{self.PATH}/filter?field=cable_type&filter_str={cable_type}"
        response = self.client.get(path)
        return [self.MODEL.from_dict(item) for item in response]

    def filter_by_link_speed(self, link_speed: str):
        path = f"{self.PATH}/filter?field=link_speed&filter_str={link_speed}"
        response = self.client.get(path)
        return [self.MODEL.from_dict(item) for item in response]

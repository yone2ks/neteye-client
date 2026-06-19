from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Optional

from neteye_client.base import APIResource


@dataclass
class Interface():

    id: Optional[str] = None
    name: str = ''
    description: str = ''
    ip_address: str = ''
    mask: str = ''
    speed: str = ''
    duplex: str = ''
    mtu: int = 1500
    status: str = ''
    node_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            name=data.get('name', ''),
            description=data.get('description', ''),
            ip_address=data.get('ip_address', ''),
            mask=data.get('mask', ''),
            speed=data.get('speed', ''),
            duplex=data.get('duplex', ''),
            mtu=data.get('mtu', 1500),
            status=data.get('status', ''),
            node_id=data.get('node_id'),
        )

    def to_dict(self):
        required_fields = {
            'name': self.name,
            'node_id': self.node_id,
        }

        optional_fields = {
            'id': self.id,
            'description': self.description,
            'ip_address': self.ip_address,
            'mask': self.mask,
            'speed': self.speed,
            'duplex': self.duplex,
            'mtu': self.mtu,
            'status': self.status,
        }

        data = required_fields.copy()

        for key, value in optional_fields.items():
            if value is not None and value != '':
                data[key] = value

        return data


def _validate_interface_data(data: dict) -> None:
    required_fields = ['name', 'node_id']

    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Required field '{field}' is missing or empty")

    mtu = data.get('mtu')
    if mtu is not None:
        if not isinstance(mtu, int) or mtu < 68 or mtu > 9000:
            raise ValueError(f"MTU must be an integer between 68 and 9000, got: {mtu}")

    ip_address = data.get('ip_address')
    if ip_address and ip_address.strip():
        try:
            IPv4Address(ip_address)
        except Exception:
            raise ValueError(f"Invalid IP address format: {ip_address}")

    status = data.get('status')
    if status:
        valid_statuses = ['up', 'down', 'admin-down', 'testing']
        if status.lower() not in valid_statuses:
            raise ValueError(f"Invalid status '{status}'. Valid values: {valid_statuses}")

    duplex = data.get('duplex')
    if duplex:
        valid_duplex = ['full', 'half', 'auto']
        if duplex.lower() not in valid_duplex:
            raise ValueError(f"Invalid duplex '{duplex}'. Valid values: {valid_duplex}")


class interface(APIResource):
    PATH = '/api/interfaces'
    MODEL = Interface
    VALIDATOR = _validate_interface_data

    def get_by_node(self, node_id: str):
        data = self.client.get(f"{self.PATH}/filter?field=node_id&filter_str={node_id}")
        return [self.MODEL.from_dict(item) for item in data]

    def filter_by_ip_address(self, ip_address: str):
        path = f"{self.PATH}/filter?field=ip_address&filter_str={ip_address}"
        response = self.client.get(path)
        return [self.MODEL.from_dict(item) for item in response]

    def filter_by_name(self, name: str):
        path = f"{self.PATH}/filter?field=name&filter_str={name}"
        response = self.client.get(path)
        return [self.MODEL.from_dict(item) for item in response]

    def filter_by_status(self, status: str):
        path = f"{self.PATH}/filter?field=status&filter_str={status}"
        response = self.client.get(path)
        return [self.MODEL.from_dict(item) for item in response]

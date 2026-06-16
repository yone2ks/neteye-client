import re
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Optional

from neteye_client.base import APIResource


@dataclass
class Arp:

    id: Optional[str] = None
    interface_id: Optional[str] = None
    ip_address: str = ''
    mac_address: str = ''
    protocol: str = ''
    arp_type: str = ''
    vendor: str = ''

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            interface_id=data.get('interface_id'),
            ip_address=data.get('ip_address', ''),
            mac_address=data.get('mac_address', ''),
            protocol=data.get('protocol', ''),
            arp_type=data.get('arp_type', ''),
            vendor=data.get('vendor', ''),
        )

    def to_dict(self):
        required_fields = {
            'interface_id': self.interface_id,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
        }

        optional_fields = {
            'id': self.id,
            'protocol': self.protocol,
            'arp_type': self.arp_type,
            'vendor': self.vendor,
        }

        data = required_fields.copy()

        for key, value in optional_fields.items():
            if value:
                data[key] = value

        return data


def _validate_arp_data(data: dict) -> None:
    required_fields = ['interface_id', 'ip_address', 'mac_address']

    for field in required_fields:
        if not data.get(field):
            raise ValueError(f"Required field '{field}' is missing or empty")

    try:
        IPv4Address(data['ip_address'])
    except Exception:
        raise ValueError(f"Invalid IP address format: {data['ip_address']}")

    mac_address = data.get('mac_address', '').strip()
    if mac_address:
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        if not re.match(mac_pattern, mac_address):
            raise ValueError(f"Invalid MAC address format: {mac_address}")


class arp(APIResource):
    PATH = '/api/arp_entries'
    MODEL = Arp
    VALIDATOR = _validate_arp_data

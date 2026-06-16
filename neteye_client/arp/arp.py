from dataclasses import dataclass
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


class arp(APIResource):
    PATH = '/api/arp_entries'
    MODEL = Arp

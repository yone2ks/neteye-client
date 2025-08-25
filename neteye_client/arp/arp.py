from dataclasses import dataclass

from neteye_client.base import APIResource


@dataclass
class Arp:

    id: str = None
    node_id: str = None
    ip_address: str = ''
    mac_address: str = ''

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            node_id=data.get('node_id'),
            ip_address=data.get('ip_address', ''),
            mac_address=data.get('mac_address', ''),
        )

    def to_dict(self):
        return {
            'id': self.id,
            'node_id': self.node_id,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address,
        }


class arp(APIResource):
    PATH = '/api/arps'
    MODEL = Arp

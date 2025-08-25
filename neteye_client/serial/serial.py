from dataclasses import dataclass

from neteye_client.base import APIResource


@dataclass
class Serial:

    id: str = None
    node_id: str = None
    serial: str = ''

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            node_id=data.get('node_id'),
            serial=data.get('serial', ''),
        )

    def to_dict(self):
        return {
            'id': self.id,
            'node_id': self.node_id,
            'serial': self.serial,
        }


class serial(APIResource):
    PATH = '/api/serials'
    MODEL = Serial

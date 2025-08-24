from dataclasses import dataclass

from neteye_client.base import APIResource


@dataclass
class Cable:
    PATH = '/api/cables'

    id: str
    src_node_id: str
    src_interface_id: str
    dst_node_id: str
    dst_interface_id: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            src_node_id=data.get('src_node_id'),
            src_interface_id=data.get('src_interface_id'),
            dst_node_id=data.get('dst_node_id'),
            dst_interface_id=data.get('dst_interface_id'),
        )

    def to_dict(self):
        return {
            'id': self.id,
            'src_node_id': self.src_node_id,
            'src_interface_id': self.src_interface_id,
            'dst_node_id': self.dst_node_id,
            'dst_interface_id': self.dst_interface_id,
        }


class cable(APIResource):
    PATH = '/api/cables'
    MODEL = Cable

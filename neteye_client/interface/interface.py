from dataclasses import dataclass
from ipaddress import IPv4Address

from neteye_client.base import APIResource

@dataclass
class Interface():

    id: str = None
    name: str = ''
    description: str = ''
    ip_address: str = ''
    mask: str = ''
    speed: str = ''
    duplex: str = ''
    mtu: int = 1500
    status: str = ''
    node_id: str = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            id = data.get('id'),
            name = data.get('name', ''),
            description = data.get('description', ''),
            ip_address = data.get('ip_address', ''),
            mask = data.get('mask', ''),
            speed = data.get('speed', ''),
            duplex = data.get('duplex', ''),
            mtu = data.get('mtu', 1500),
            status = data.get('status', ''),
            node_id = data.get('node_id'),
        )
        
    def to_dict(self):
        # 必須フィールド（バリデーションと一致）
        required_fields = {
            'name': self.name,
            'node_id': self.node_id
        }
        
        # オプションフィールド
        optional_fields = {
            'id': self.id,
            'description': self.description,
            'ip_address': self.ip_address,
            'mask': self.mask,
            'speed': self.speed,
            'duplex': self.duplex,
            'mtu': self.mtu,  # デフォルト値も含める
            'status': self.status
        }
        
        # 必須フィールドは常に含める
        data = required_fields.copy()
        
        # オプションフィールドは値が存在する場合のみ追加
        for key, value in optional_fields.items():
            if value:
                data[key] = value
                
        return data

class interface(APIResource):
    PATH = '/api/interfaces'
    MODEL = Interface

    def get_by_node(self, node_id):
        data = self.client.get(f"{self.PATH}/filter?field=node_id&filter_str={node_id}")
        return [self.MODEL.from_dict(item) for item in data]
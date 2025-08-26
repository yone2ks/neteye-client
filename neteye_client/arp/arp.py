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
        # 必須フィールド（バリデーションと一致）
        required_fields = {
            'node_id': self.node_id,
            'ip_address': self.ip_address,
            'mac_address': self.mac_address
        }
        
        # オプションフィールド
        optional_fields = {
            'id': self.id
        }
        
        # 必須フィールドは常に含める
        data = required_fields.copy()
        
        # オプションフィールドは値が存在する場合のみ追加
        for key, value in optional_fields.items():
            if value:
                data[key] = value
                
        return data


class arp(APIResource):
    PATH = '/api/arps'
    MODEL = Arp

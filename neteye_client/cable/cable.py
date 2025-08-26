from dataclasses import dataclass

from neteye_client.base import APIResource


@dataclass
class Cable:

    id: str = None
    src_node_id: str = None
    src_interface_id: str = None
    dst_node_id: str = None
    dst_interface_id: str = None

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
        # 必須フィールド（バリデーションと一致）
        required_fields = {
            'src_node_id': self.src_node_id,
            'src_interface_id': self.src_interface_id,
            'dst_node_id': self.dst_node_id,
            'dst_interface_id': self.dst_interface_id
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


class cable(APIResource):
    PATH = '/api/cables'
    MODEL = Cable

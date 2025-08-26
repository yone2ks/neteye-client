from dataclasses import dataclass
from ipaddress import IPv4Address

from neteye_client.base import APIResource


@dataclass
class Node():

    id: str = None
    hostname: str = ''
    description: str = ''
    ip_address: IPv4Address = IPv4Address('0.0.0.0')
    port: int = 22
    device_type: str = 'autodetect'
    scrapli_driver: str = 'not supported'
    napalm_driver: str = 'not supported'
    ntc_template_platform: str = ''
    model: str = ''
    os_type: str = ''
    os_version: str = ''
    username: str = ''
    password: str = ''
    enable: str = ''
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id = data.get('id'),
            hostname = data.get('hostname', ''),
            description = data.get('description', ''),
            ip_address = IPv4Address(data.get('ip_address', '0.0.0.0')),
            port = data.get('port', 22),
            device_type = data.get('device_type', 'autodetect'),
            scrapli_driver = data.get('scrapli_driver', 'not supported'),
            napalm_driver = data.get('napalm_driver', 'not supported'),
            ntc_template_platform = data.get('ntc_template_platform', ''),
            model = data.get('model', ''),
            os_type = data.get('os_type', ''),
            os_version = data.get('os_version', ''),
            username = data.get('username', ''),
            password = data.get('password', ''),
            enable = data.get('enable', '')
        )

    def to_dict(self):
        # 必須フィールドの定義（バリデーションと一致させる）
        required_fields = {
            'hostname': self.hostname,
            'ip_address': str(self.ip_address),
            'port': self.port
        }
        
        # オプションフィールドの定義（デフォルト値は含める）
        optional_fields = {
            'id': self.id,
            'description': self.description,
            'device_type': self.device_type,  # デフォルト値も含める
            'scrapli_driver': self.scrapli_driver,  # デフォルト値も含める
            'napalm_driver': self.napalm_driver,  # デフォルト値も含める
            'ntc_template_platform': self.ntc_template_platform,
            'model': self.model,
            'os_type': self.os_type,
            'os_version': self.os_version,
            'username': self.username,
            'password': self.password,
            'enable': self.enable
        }
        
        # 必須フィールドは常に含める（バリデーションと一致）
        data = required_fields.copy()
        
        # オプションフィールドは値が存在する場合のみ追加
        for key, value in optional_fields.items():
            if value:
                data[key] = value
        
        return data


class node(APIResource):
    PATH = '/api/nodes'
    MODEL = Node

    def command(self, id: str, command: str):
        command_path = command.replace(' ', '+')
        path = f"{self.PATH}/{id}/command/{command_path}"
        response = self.client.get(path)
        return response

    def raw_command(self, id: str, command: str):
        command_path = command.replace(' ', '+')
        path = f"{self.PATH}/{id}/raw_command/{command_path}"
        response = self.client.get(path)
        return response

    def import_node_from_id(self, id: str):
        path = f"{self.PATH}/import_node_from_id/{id}"
        response = self.client.get(path)
        return response

    def import_node(self, id: str):
        path = f"{self.PATH}/{id}/import/node"
        response = self.client.post(path)
        return response

    def import_serial(self, id: str):
        path = f"{self.PATH}/{id}/import/serial"
        response = self.client.post(path)
        return response

    def import_interface(self, id: str):
        path = f"{self.PATH}/{id}/import/interface"
        response = self.client.post(path)
        return response

    def import_arp_entry(self, id: str):
        path = f"{self.PATH}/{id}/import/arp_entry"
        response = self.client.post(path)
        return response

    def import_all_data(self, id: str):
        path = f"{self.PATH}/{id}/import/all_data"
        response = self.client.post(path)
        return response
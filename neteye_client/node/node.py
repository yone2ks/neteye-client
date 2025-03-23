from dataclasses import dataclass
from ipaddress import IPv4Address

from neteye_client.base import APIResource


@dataclass
class Node():

    id: str = None
    hostname: str = ''
    ip_address: IPv4Address = IPv4Address('0.0.0.0')
    port: int = 22
    device_type: str = 'autodetect'
    scrapli_driver: str = 'not supported'
    napalm_driver: str = 'not supported'
    ntc_template_platform: str = ''
    model: str = ''
    os_type: str = ''
    os_version: str = ''
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id = data.get('id'),
            hostname = data.get('hostname'),
            ip_address = IPv4Address(data.get('ip_address')),
            port = data.get('port'),
            device_type = data.get('device_type'),
            scrapli_driver = data.get('scrapli_driver'),
            napalm_driver = data.get('napam_driver'),
            ntc_template_platform = data.get('ntc_template_platform'),
            model = data.get('model'),
            os_type = data.get('os_type'),
            os_version = data.get('os_version'),
        )

    def to_dict(self):
        return {
            'id': self.id,
            'hostname': self.hostname,
            'ip_address': str(self.ip_address),
            'port': self.port,
            'device_type': self.device_type,
            'scrapli_driver': self.scrapli_driver,
            'napalm_driver': self.napalm_driver,
            'ntc_template_platform': self.ntc_template_platform,
            'model': self.model,
            'os_type': self.os_type,
            'os_version': self.os_version,
        }


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
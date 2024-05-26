from dataclasses import dataclass
from ipaddress import IPv4Address
@dataclass
class Node:
    NODE_PATH = '/nodes'

    id: str
    hostname: str
    ip_address: IPv4Address
    port: int
    device_type: str
    scrapli_driver: str
    naplam_driver: str
    ntc_template_platform: str
    model: str
    os_type: str
    os_version: str
    
    @classmethod
    def from_dict(cls, data):
        retrun cls(
            id = data.get('id'),
            hostname = data.get('hostname'),
            ip_address = IPv4Address(data.get('ip_address')),
            port = data.get('port'),
            device_type = data.get('device_type'),
            scrapli_driver = data.get('scrapli_driver'),
            naplam_driver = data.get('naplam_driver'),
            ntc_template_platform = data.get('ntc_template_platform'),
            model = data.get('model'),
            os_type = data.get('os_type'),
            os_version = data.get('os_version'),
        )

    @classmethod
    def to_dict(cls):
        return {
            'id': self.id,
            'hostname': self.hostname,
            'ip_address': str(self.ip_address),
            'port': self.port,
            'device_type': self.device_type,
            'scrapli_driver': self.scrapli_driver,
            'naplam_driver': self.naplam_driver,
            'ntc_template_platform': self.ntc_template_platform,
            'model': self.model,
            'os_type': self.os_type,
            'os_version': self.os_version,
        }
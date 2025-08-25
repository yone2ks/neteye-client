from typing import Optional, List, Union
from ipaddress import IPv4Address
import re

from .rest_client import RestClient, APIError

class APIResource():
    def __init__(self, client):
        self.client = client
        super().__init__()
        
    def get(self, id: Optional[str] = None):
        if id is None:
            response = self.client.get(self.PATH)
            return [self.MODEL.from_dict(item) for item in response]
        else:
            response = self.client.get(f"{self.PATH}/{id}")
            return self.MODEL.from_dict(response)
    
    def create(self, data: Union[dict, object]):
        """Create a new resource.
        
        Args:
            data: Dictionary of resource data or a model instance
            
        Returns:
            Created resource instance
            
        Raises:
            APIError: If creation fails
        """
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
        
        # Remove id if present (server will assign)
        if isinstance(data, dict) and data.get('id'):
            del data['id']
            
        # Validate required fields based on resource type
        if hasattr(self, 'MODEL'):
            self._validate_data(data)
            
        try:
            response = self.client.post(self.PATH, data)
            return self.MODEL.from_dict(response)
        except APIError as e:
            # Add more context to the error
            if e.status_code == 400:
                raise APIError(f"Validation failed for {self.MODEL.__name__}: {e.message}", e.status_code)
        except ValueError as e:
            # Convert validation errors to APIError for consistency
            raise APIError(f"Client validation failed: {str(e)}", 400)
    
    def update(self, id: str, data: Union[dict, object]):
        """Update an existing resource.
        
        Args:
            id: Resource ID to update
            data: Dictionary of resource data or a model instance
            
        Returns:
            Updated resource instance
            
        Raises:
            APIError: If update fails
        """
        if not id:
            raise ValueError("ID cannot be empty")
            
        if hasattr(data, 'to_dict'):
            data = data.to_dict()
            
        response = self.client.put(f"{self.PATH}/{id}", data)
        return self.MODEL.from_dict(response)
    
    def delete(self, id: str):
        """Delete a resource by ID.
        
        Args:
            id: Resource ID to delete
            
        Returns:
            Delete response
            
        Raises:
            APIError: If deletion fails
        """
        if not id:
            raise ValueError("ID cannot be empty")
            
        response = self.client.delete(f"{self.PATH}/{id}")
        return response
    
    def _validate_data(self, data: dict):
        """Validate resource data before creation based on resource type.
        
        Args:
            data: Resource data dictionary
            
        Raises:
            ValueError: If validation fails
        """
        model_name = self.MODEL.__name__
        
        if model_name == 'Node':
            self._validate_node_data(data)
        elif model_name == 'Interface':
            self._validate_interface_data(data)
        elif model_name == 'Arp':
            self._validate_arp_data(data)
        elif model_name == 'Serial':
            self._validate_serial_data(data)
        elif model_name == 'Cable':
            self._validate_cable_data(data)
        # Add more resource types as needed
    
    def _validate_node_data(self, data: dict):
        """Validate Node data before creation.
        
        Args:
            data: Node data dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ['hostname', 'ip_address', 'port']
        
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Required field '{field}' is missing or empty")
        
        # Validate IP address format
        try:
            if isinstance(data['ip_address'], str):
                IPv4Address(data['ip_address'])
        except Exception:
            raise ValueError(f"Invalid IP address format: {data['ip_address']}")
            
        # Validate port range
        port = data.get('port')
        if not isinstance(port, int) or port < 1 or port > 65535:
            raise ValueError(f"Port must be an integer between 1 and 65535, got: {port}")
    
    def _validate_interface_data(self, data: dict):
        """Validate Interface data before creation.
        
        Args:
            data: Interface data dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ['name', 'node_id']
        
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Required field '{field}' is missing or empty")
        
        # Validate MTU range if provided
        mtu = data.get('mtu')
        if mtu is not None:
            if not isinstance(mtu, int) or mtu < 68 or mtu > 9000:
                raise ValueError(f"MTU must be an integer between 68 and 9000, got: {mtu}")
        
        # Validate IP address format if provided
        ip_address = data.get('ip_address')
        if ip_address and ip_address.strip():
            try:
                IPv4Address(ip_address)
            except Exception:
                raise ValueError(f"Invalid IP address format: {ip_address}")
        
        # Validate status values if provided
        status = data.get('status')
        if status:
            valid_statuses = ['up', 'down', 'admin-down', 'testing']
            if status.lower() not in valid_statuses:
                raise ValueError(f"Invalid status '{status}'. Valid values: {valid_statuses}")
        
        # Validate duplex values if provided
        duplex = data.get('duplex')
        if duplex:
            valid_duplex = ['full', 'half', 'auto']
            if duplex.lower() not in valid_duplex:
                raise ValueError(f"Invalid duplex '{duplex}'. Valid values: {valid_duplex}")
    
    def _validate_arp_data(self, data: dict):
        """Validate ARP data before creation.
        
        Args:
            data: ARP data dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ['node_id', 'ip_address', 'mac_address']
        
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Required field '{field}' is missing or empty")
        
        # Validate IP address format
        try:
            IPv4Address(data['ip_address'])
        except Exception:
            raise ValueError(f"Invalid IP address format: {data['ip_address']}")
        
        # Validate MAC address format (basic check)
        mac_address = data.get('mac_address', '').strip()
        if mac_address:
            # Basic MAC address format check (XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)
            import re
            mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
            if not re.match(mac_pattern, mac_address):
                raise ValueError(f"Invalid MAC address format: {mac_address}")
    
    def _validate_serial_data(self, data: dict):
        """Validate Serial data before creation.
        
        Args:
            data: Serial data dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ['node_id', 'serial']
        
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Required field '{field}' is missing or empty")
        
        # Validate serial number format (basic check)
        serial = data.get('serial', '').strip()
        if not serial or len(serial) < 3:
            raise ValueError("Serial number must be at least 3 characters long")
    
    def _validate_cable_data(self, data: dict):
        """Validate Cable data before creation.
        
        Args:
            data: Cable data dictionary
            
        Raises:
            ValueError: If validation fails
        """
        required_fields = ['src_node_id', 'src_interface_id', 'dst_node_id', 'dst_interface_id']
        
        for field in required_fields:
            if not data.get(field):
                raise ValueError(f"Required field '{field}' is missing or empty")
        
        # Validate that source and destination are different
        if data.get('src_node_id') == data.get('dst_node_id') and data.get('src_interface_id') == data.get('dst_interface_id'):
            raise ValueError("Source and destination cannot be the same interface")
        
        # Validate that we don't have a cable connecting to itself
        if data.get('src_interface_id') == data.get('dst_interface_id'):
            raise ValueError("Cannot connect an interface to itself")
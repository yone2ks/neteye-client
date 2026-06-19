"""Model roundtrip and validation unit tests (no network required)."""
import pytest
from ipaddress import IPv4Address

from neteye_client.node.node import Node, _validate_node_data
from neteye_client.interface.interface import Interface, _validate_interface_data
from neteye_client.arp.arp import Arp, _validate_arp_data
from neteye_client.serial.serial import Serial, _validate_serial_data
from neteye_client.cable.cable import Cable, _validate_cable_data


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------

class TestNodeModel:
    def test_roundtrip_full(self):
        data = {
            "id": "n-1",
            "hostname": "r1",
            "ip_address": "192.0.2.1",
            "port": 22,
            "device_type": "cisco_ios",
            "description": "core router",
        }
        node = Node.from_dict(data)
        assert node.hostname == "r1"
        assert node.ip_address == IPv4Address("192.0.2.1")
        result = node.to_dict()
        assert result["hostname"] == "r1"
        assert result["ip_address"] == "192.0.2.1"
        assert result["port"] == 22

    def test_to_dict_excludes_empty_optional(self):
        node = Node(hostname="r1", ip_address=IPv4Address("10.0.0.1"), port=22)
        result = node.to_dict()
        assert "id" not in result
        assert "username" not in result

    def test_to_dict_includes_non_none_optional(self):
        node = Node(hostname="r1", ip_address=IPv4Address("10.0.0.1"), port=22, description="test")
        result = node.to_dict()
        assert result["description"] == "test"


class TestNodeValidation:
    def test_valid(self):
        _validate_node_data({"hostname": "r1", "ip_address": "192.0.2.1", "port": 22})

    def test_missing_hostname(self):
        with pytest.raises(ValueError, match="hostname"):
            _validate_node_data({"ip_address": "192.0.2.1", "port": 22})

    def test_invalid_ip(self):
        with pytest.raises(ValueError, match="IP address"):
            _validate_node_data({"hostname": "r1", "ip_address": "not-an-ip", "port": 22})

    def test_invalid_port_out_of_range(self):
        with pytest.raises(ValueError, match="Port"):
            _validate_node_data({"hostname": "r1", "ip_address": "192.0.2.1", "port": 99999})

    def test_invalid_port_zero(self):
        with pytest.raises(ValueError, match="Port"):
            _validate_node_data({"hostname": "r1", "ip_address": "192.0.2.1", "port": 0})


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

class TestInterfaceModel:
    def test_roundtrip(self):
        data = {
            "id": "i-1",
            "name": "Gi0/0",
            "node_id": "n-1",
            "ip_address": "192.0.2.10",
            "mtu": 1500,
            "status": "up",
        }
        iface = Interface.from_dict(data)
        assert iface.name == "Gi0/0"
        result = iface.to_dict()
        assert result["name"] == "Gi0/0"
        assert result["mtu"] == 1500

    def test_to_dict_mtu_zero_included(self):
        """mtu=0 is not None, so it should be included in to_dict()."""
        iface = Interface(name="lo", node_id="n-1", mtu=0)
        result = iface.to_dict()
        assert "mtu" in result
        assert result["mtu"] == 0


class TestInterfaceValidation:
    def test_valid(self):
        _validate_interface_data({"name": "Gi0/0", "node_id": "n-1"})

    def test_missing_name(self):
        with pytest.raises(ValueError, match="name"):
            _validate_interface_data({"node_id": "n-1"})

    def test_invalid_mtu(self):
        with pytest.raises(ValueError, match="MTU"):
            _validate_interface_data({"name": "Gi0/0", "node_id": "n-1", "mtu": 50})

    def test_invalid_status(self):
        with pytest.raises(ValueError, match="status"):
            _validate_interface_data({"name": "Gi0/0", "node_id": "n-1", "status": "unknown"})

    def test_invalid_duplex(self):
        with pytest.raises(ValueError, match="duplex"):
            _validate_interface_data({"name": "Gi0/0", "node_id": "n-1", "duplex": "super"})


# ---------------------------------------------------------------------------
# ARP
# ---------------------------------------------------------------------------

class TestArpModel:
    def test_roundtrip(self):
        data = {
            "id": "a-1",
            "interface_id": "i-1",
            "ip_address": "192.0.2.10",
            "mac_address": "aa:bb:cc:dd:ee:ff",
            "vendor": "Cisco",
        }
        arp = Arp.from_dict(data)
        assert arp.interface_id == "i-1"
        assert arp.vendor == "Cisco"
        result = arp.to_dict()
        assert result["interface_id"] == "i-1"
        assert result["mac_address"] == "aa:bb:cc:dd:ee:ff"
        assert "node_id" not in result

    def test_to_dict_excludes_empty_optional(self):
        arp = Arp(interface_id="i-1", ip_address="192.0.2.1", mac_address="aa:bb:cc:dd:ee:ff")
        result = arp.to_dict()
        assert "id" not in result
        assert "vendor" not in result


class TestArpValidation:
    def test_valid(self):
        _validate_arp_data({
            "interface_id": "i-1",
            "ip_address": "192.0.2.10",
            "mac_address": "aa:bb:cc:dd:ee:ff",
        })

    def test_missing_interface_id(self):
        with pytest.raises(ValueError, match="interface_id"):
            _validate_arp_data({"ip_address": "192.0.2.10", "mac_address": "aa:bb:cc:dd:ee:ff"})

    def test_invalid_mac(self):
        with pytest.raises(ValueError, match="MAC address"):
            _validate_arp_data({
                "interface_id": "i-1",
                "ip_address": "192.0.2.10",
                "mac_address": "zz:zz:zz:zz:zz:zz",
            })

    def test_mac_with_dash_separator(self):
        _validate_arp_data({
            "interface_id": "i-1",
            "ip_address": "192.0.2.10",
            "mac_address": "aa-bb-cc-dd-ee-ff",
        })


# ---------------------------------------------------------------------------
# Serial
# ---------------------------------------------------------------------------

class TestSerialModel:
    def test_roundtrip(self):
        data = {"id": "s-1", "node_id": "n-1", "serial_number": "FTX1234ABCD", "product_id": "C9300"}
        s = Serial.from_dict(data)
        assert s.serial_number == "FTX1234ABCD"
        assert s.product_id == "C9300"
        result = s.to_dict()
        assert result["serial_number"] == "FTX1234ABCD"
        assert "serial" not in result

    def test_to_dict_excludes_empty_optional(self):
        s = Serial(node_id="n-1", serial_number="SN123")
        result = s.to_dict()
        assert "id" not in result
        assert "product_id" not in result


class TestSerialValidation:
    def test_valid(self):
        _validate_serial_data({"node_id": "n-1", "serial_number": "FTX1234"})

    def test_missing_serial_number(self):
        with pytest.raises(ValueError, match="serial_number"):
            _validate_serial_data({"node_id": "n-1"})

    def test_serial_too_short(self):
        with pytest.raises(ValueError, match="at least 3 characters"):
            _validate_serial_data({"node_id": "n-1", "serial_number": "AB"})


# ---------------------------------------------------------------------------
# Cable
# ---------------------------------------------------------------------------

class TestCableModel:
    def test_roundtrip(self):
        data = {
            "id": "c-1",
            "a_interface_id": "i-1",
            "b_interface_id": "i-2",
            "cable_type": "copper",
            "link_speed": "1G",
        }
        cable = Cable.from_dict(data)
        assert cable.a_interface_id == "i-1"
        assert cable.cable_type == "copper"
        result = cable.to_dict()
        assert result["b_interface_id"] == "i-2"
        assert "src_node_id" not in result
        assert "dst_node_id" not in result

    def test_to_dict_excludes_empty_optional(self):
        cable = Cable(a_interface_id="i-1", b_interface_id="i-2")
        result = cable.to_dict()
        assert "id" not in result
        assert "cable_type" not in result


class TestCableValidation:
    def test_valid(self):
        _validate_cable_data({"a_interface_id": "i-1", "b_interface_id": "i-2"})

    def test_missing_a_interface(self):
        with pytest.raises(ValueError, match="a_interface_id"):
            _validate_cable_data({"b_interface_id": "i-2"})

    def test_self_loop(self):
        with pytest.raises(ValueError, match="Cannot connect"):
            _validate_cable_data({"a_interface_id": "i-1", "b_interface_id": "i-1"})

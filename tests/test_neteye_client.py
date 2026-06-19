import types
import pytest
import requests
from ipaddress import IPv4Address

from neteye_client.neteye_client import NeteyeClient
from neteye_client.node.node import Node
from neteye_client.interface.interface import Interface
from neteye_client.base.rest_client import APIError


class DummyResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if not (200 <= self.status_code < 300):
            raise requests.exceptions.HTTPError(response=self)

    def json(self):
        return self._payload


def make_session(monkeypatch):
    class DummySession:
        def __init__(self):
            self.headers = {}
            self.last = {}
            self.auth = None

        def post(self, url, data=None, json=None, timeout=None):
            self.last = {"method": "POST", "url": url, "json": json, "data": data}
            response_data = DummySession.responses.get(("POST", url), {})
            if isinstance(response_data, DummyResponse):
                return response_data
            return DummyResponse(response_data)

        def get(self, url, params=None, timeout=None):
            self.last = {"method": "GET", "url": url, "params": params}
            response_data = DummySession.responses.get(("GET", url), {})
            if isinstance(response_data, DummyResponse):
                return response_data
            return DummyResponse(response_data)

        def put(self, url, json=None, timeout=None):
            self.last = {"method": "PUT", "url": url, "json": json}
            return DummyResponse(DummySession.responses.get(("PUT", url), json))

        def delete(self, url, timeout=None):
            self.last = {"method": "DELETE", "url": url}
            return DummyResponse(DummySession.responses.get(("DELETE", url), {}))

    DummySession.responses = {}

    def fake_session(*args, **kwargs):
        return DummySession()

    monkeypatch.setattr("requests.Session", fake_session)
    return DummySession


def test_auth(monkeypatch):
    DummySession = make_session(monkeypatch)
    base = "http://localhost:5001"
    c = NeteyeClient(base)

    # Mock API responses
    login_url = f"{base}/api/auth/login"
    logout_url = f"{base}/api/auth/logout"
    me_url = f"{base}/api/auth/me"

    user_payload = {
        "id": 1,
        "email": "test@example.com",
        "username": "testuser",
        "active": True,
        "roles": ["user"],
    }

    # Setup responses for mocked session
    DummySession.responses[("POST", login_url)] = user_payload
    DummySession.responses[("POST", logout_url)] = {"message": "Successfully logged out"}
    DummySession.responses[("GET", me_url)] = user_payload

    # 1. Test successful login
    assert not c.is_authenticated()
    user = c.login("test@example.com", "password")
    assert user["email"] == "test@example.com"
    assert c.is_authenticated()
    assert c.get_current_user()["username"] == "testuser"

    # 2. Test logout
    c.logout()
    # After logout, /api/auth/me returns 401 → get_current_user() returns None
    DummySession.responses[("GET", me_url)] = DummyResponse({}, 401)
    assert not c.is_authenticated()
    assert c.get_current_user() is None

    # 3. Test login failure
    DummySession.responses[("POST", login_url)] = DummyResponse(
        {"message": "Invalid credentials"}, status_code=400
    )
    with pytest.raises(APIError, match="Invalid credentials"):
        c.login("test@example.com", "wrongpassword")


def test_node_get_all(monkeypatch):
    DummySession = make_session(monkeypatch)
    base = "http://localhost:5001/"
    list_payload = [
        {
            "id": "1",
            "hostname": "r1",
            "ip_address": "192.0.2.1",
            "port": 22,
            "device_type": "autodetect",
            "scrapli_driver": "not supported",
            "napalm_driver": "not supported",
        }
    ]
    url = base + "api/nodes"
    DummySession.responses[("GET", url)] = list_payload

    c = NeteyeClient(base)
    nodes = c.node.get()
    assert isinstance(nodes, list)
    assert isinstance(nodes[0], Node)
    assert nodes[0].hostname == "r1"


def test_node_get_single(monkeypatch):
    DummySession = make_session(monkeypatch)
    base = "http://localhost:5001/"
    item = {
        "id": "n-1",
        "hostname": "r2",
        "ip_address": "192.0.2.2",
        "port": 22,
        "device_type": "autodetect",
        "scrapli_driver": "not supported",
        "napalm_driver": "not supported",
    }
    url = base + "api/nodes/n-1"
    DummySession.responses[("GET", url)] = item

    c = NeteyeClient(base)
    node = c.node.get("n-1")
    assert isinstance(node, Node)
    assert node.id == "n-1"
    assert node.ip_address == IPv4Address("192.0.2.2")


def test_node_create_update_delete(monkeypatch):
    DummySession = make_session(monkeypatch)
    base = "http://localhost:5001/"
    create_url = base + "api/nodes"
    update_url = base + "api/nodes/n-1"
    delete_url = update_url

    created = {
        "id": "n-1",
        "hostname": "r3",
        "ip_address": "192.0.2.3",
        "port": 22,
        "device_type": "autodetect",
        "scrapli_driver": "not supported",
        "napalm_driver": "not supported",
    }
    updated = {**created, "hostname": "r3-new"}
    DummySession.responses[("POST", create_url)] = created
    DummySession.responses[("PUT", update_url)] = updated
    DummySession.responses[("DELETE", delete_url)] = {"ok": True}

    c = NeteyeClient(base)

    node = c.node.create({"hostname": "r3", "ip_address": "192.0.2.3", "port": 22})
    assert node.id == "n-1"

    node2 = c.node.update("n-1", {"hostname": "r3-new"})
    assert node2.hostname == "r3-new"

    resp = c.node.delete("n-1")
    assert resp == {"ok": True}


def test_node_import_routes(monkeypatch):
    DummySession = make_session(monkeypatch)
    base = "http://localhost:5001/"
    c = NeteyeClient(base)

    # stub responses
    DummySession.responses[("GET", base + "api/nodes/import_node_from_id/n-1")] = {"ok": True, "ep": "import_node_from_id"}
    DummySession.responses[("POST", base + "api/nodes/n-1/import/node")] = {"ok": True, "ep": "import_node"}
    DummySession.responses[("POST", base + "api/nodes/n-1/import/interface")] = {"ok": True, "ep": "import_interface"}
    DummySession.responses[("POST", base + "api/nodes/n-1/import/serial")] = {"ok": True, "ep": "import_serial"}
    DummySession.responses[("POST", base + "api/nodes/n-1/import/arp_entry")] = {"ok": True, "ep": "import_arp_entry"}
    DummySession.responses[("POST", base + "api/nodes/n-1/import/all_data")] = {"ok": True, "ep": "import_all_data"}

    resp = c.node.import_node_from_id("n-1")
    assert isinstance(resp, dict)
    assert resp.get("ep") == "import_node_from_id"
    assert c.node.import_node("n-1")["ep"] == "import_node"
    assert c.node.import_interface("n-1")["ep"] == "import_interface"
    assert c.node.import_serial("n-1")["ep"] == "import_serial"
    assert c.node.import_arp_entry("n-1")["ep"] == "import_arp_entry"
    assert c.node.import_all_data("n-1")["ep"] == "import_all_data"


def test_serial_arp_cable_clients(monkeypatch):
    DummySession = make_session(monkeypatch)
    base = "http://localhost:5001/"
    c = NeteyeClient(base)

    # serials
    serials_url = base + "api/serials"
    DummySession.responses[("GET", serials_url)] = [
        {"id": "s1", "node_id": "n-1", "serial_number": "FTX1234"}
    ]
    serials = c.serial.get()
    assert isinstance(serials, list)
    assert serials[0].to_dict()["serial_number"] == "FTX1234"

    # arps
    arps_url = base + "api/arp_entries"
    DummySession.responses[("GET", arps_url)] = [
        {"id": "a1", "interface_id": "i-1", "ip_address": "192.0.2.10", "mac_address": "aa:bb:cc:dd:ee:ff"}
    ]
    arps = c.arp.get()
    assert arps[0].to_dict()["mac_address"] == "aa:bb:cc:dd:ee:ff"
    assert arps[0].interface_id == "i-1"

    # cables
    cables_url = base + "api/cables"
    DummySession.responses[("GET", cables_url)] = [
        {"id": "c1", "a_interface_id": "i1", "b_interface_id": "i9", "cable_type": "copper"}
    ]
    cables = c.cable.get()
    assert cables[0].to_dict()["b_interface_id"] == "i9"
    assert cables[0].cable_type == "copper"


def test_interface_get_and_filter(monkeypatch):
    DummySession = make_session(monkeypatch)
    base = "http://localhost:5001/"

    # list all
    list_url = base + "api/interfaces"
    DummySession.responses[("GET", list_url)] = [
        {"id": "i1", "name": "Gi0/0", "description": "", "ip_address": "192.0.2.10", "mask": "255.255.255.0", "speed": "1000", "duplex": "full", "mtu": 1500, "status": "up", "node_id": "n-1"}
    ]

    # filter by node
    filter_url = base + "api/interfaces/filter?field=node_id&filter_str=n-1"
    DummySession.responses[("GET", filter_url)] = DummySession.responses[("GET", list_url)]

    c = NeteyeClient(base)
    all_interfaces = c.interface.get()
    assert isinstance(all_interfaces[0], Interface)
    by_node = c.interface.get_by_node("n-1")
    assert len(by_node) == 1
    assert by_node[0].node_id == "n-1"

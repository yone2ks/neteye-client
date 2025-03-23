from neteye_client import node, interface
from neteye_client.node.node import Node
from neteye_client.interface.interface import Interface

from neteye_client.neteye_client import NeteyeClient

neteye_client = NeteyeClient("http://localhost:5001")
nodes = neteye_client.node.get()
print("Existing nodes:")
for node in nodes:
    print(node.to_dict())

interfaces = neteye_client.interface.get()
#node = neteye_client.node.get("1023432c-558f-47d2-8db8-643a293146a0")
# response = neteye_client.node.command(node.id, "show version")
# raw_response = neteye_client.node.raw_command(node.id, "show version")
# import_response = neteye_client.node.import_node_from_id("1023432c-558f-47d2-8db8-643a293146a0")

#node_client = node.Client("http://localhost:5001")
#add_node = Node(
#    hostname="test",
#    ip_address="192.168.0.1")
add_node = {
    'hostname': 'test100',
    'ip_address': '192.168.0.1',
    'port': 22
}
#print(add_node.to_dict())

print("\nTrying to create new node:")
print(add_node)

response = neteye_client.node.create(add_node)
print("\nResponse:")
print(response)
#print([node.to_dict() for node in nodes])
#print([interface.to_dict() for interface in interfaces])
#print(node)
#print(response)
#print(raw_response)
#print(import_response)
#interface_client = interface.Client("http://localhost:5001")
#interface = interface_client.get("bd67a90f-ed7e-4753-95da-bc9318829a15")
#print(interface)

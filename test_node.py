from neteye_client import node, interface
from neteye_client.node.node import Node
from neteye_client.interface.interface import Interface

from neteye_client.neteye_client import NeteyeClient

neteye_client = NeteyeClient("http://localhost:5001")
nodes = neteye_client.node.get()
interfaces = neteye_client.interface.get()
#node = neteye_client.node.get("1023432c-558f-47d2-8db8-643a293146a0")
# response = neteye_client.node.command(node.id, "show version")
# raw_response = neteye_client.node.raw_command(node.id, "show version")
# import_response = neteye_client.node.import_node_from_id("1023432c-558f-47d2-8db8-643a293146a0")

#node_client = node.Client("http://localhost:5001")
print([node.to_dict() for node in nodes])
print([interface.to_dict() for interface in interfaces])
#print(node)
#print(response)
#print(raw_response)
#print(import_response)
#interface_client = interface.Client("http://localhost:5001")
#interface = interface_client.get("bd67a90f-ed7e-4753-95da-bc9318829a15")
#print(interface)

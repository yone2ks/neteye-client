from neteye_client.node.client import Client
from neteye_client.node.node import Node

client = Client("http://192.168.55.130:5000")
node = client.get("c911f9e5-3235-43d6-abf9-293c8ae10e08")
print(node)

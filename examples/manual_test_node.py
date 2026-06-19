#!/usr/bin/env python3
"""Script to manually verify the connection to a live server.

Set the following environment variables before running:
  export NETEYE_URL=http://localhost:5001
  export NETEYE_EMAIL=your_email@example.com
  export NETEYE_PASSWORD=your_password
"""

import os
from ipaddress import IPv4Address

from neteye_client.neteye_client import NeteyeClient
from neteye_client.node.node import Node

NETEYE_URL = os.environ.get("NETEYE_URL", "http://localhost:5001")
NETEYE_EMAIL = os.environ["NETEYE_EMAIL"]
NETEYE_PASSWORD = os.environ["NETEYE_PASSWORD"]

client = NeteyeClient(NETEYE_URL, timeout=10)
client.login(NETEYE_EMAIL, NETEYE_PASSWORD)

node = Node(
    hostname="test_node",
    ip_address=IPv4Address("192.168.1.1"),
    port=22,
)

client.node.create(node)

nodes = client.node.get()
print(nodes[0].hostname)

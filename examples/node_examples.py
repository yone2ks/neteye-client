#!/usr/bin/env python3
"""Example code for managing Node resources with neteye_client.

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


def get_client() -> NeteyeClient:
    client = NeteyeClient(NETEYE_URL)
    client.login(NETEYE_EMAIL, NETEYE_PASSWORD)
    return client


def add_node_example():
    """Example of adding a Node with all fields specified."""
    client = get_client()

    new_node = Node(
        hostname="router-0001",
        description="Main router for network",
        ip_address=IPv4Address("192.168.1.1"),
        port=22,
        device_type="cisco_ios",
        scrapli_driver="cisco_iosxe",
        napalm_driver="ios",
        ntc_template_platform="cisco_ios",
        model="ISR4321",
        os_type="IOS",
        os_version="15.7(3)M4a",
        username=os.environ.get("NODE_USERNAME", "admin"),
        password=os.environ.get("NODE_PASSWORD", ""),
        enable=os.environ.get("NODE_ENABLE", ""),
    )

    try:
        created_node = client.node.create(new_node)
        print(f"Node created successfully: {created_node.hostname} (ID: {created_node.id})")
        return created_node
    except Exception as e:
        print(f"Failed to create Node: {e}")
        return None


def add_minimal_node():
    """Example of adding a Node with only required fields."""
    client = get_client()

    minimal_node = Node(
        hostname="minimal-router",
        ip_address=IPv4Address("192.168.1.100"),
        port=22,
    )

    print(f"Payload: {minimal_node.to_dict()}")

    try:
        created_node = client.node.create(minimal_node)
        print(f"Minimal Node created successfully: {created_node.hostname} (ID: {created_node.id})")
        return created_node
    except Exception as e:
        print(f"Failed to create Node: {e}")
        return None


def add_node_with_dict():
    """Example of adding a Node using a plain dict."""
    client = get_client()

    node_data = {
        "hostname": "dict-router",
        "ip_address": "192.168.1.102",
        "port": 22,
    }

    try:
        created_node = client.node.create(node_data)
        print(f"Node created successfully from dict: {created_node.hostname} (ID: {created_node.id})")
        return created_node
    except Exception as e:
        print(f"Failed to create Node: {e}")
        return None


def get_all_nodes():
    """Example of fetching all Nodes."""
    client = get_client()

    try:
        nodes = client.node.get()
        print(f"Fetched {len(nodes)} Node(s)")
        for node in nodes:
            print(f"- {node.hostname} ({node.ip_address}) - ID: {node.id}")
        return nodes
    except Exception as e:
        print(f"Failed to fetch Nodes: {e}")
        return []


def filter_nodes_example():
    """Example of filtering Nodes."""
    client = get_client()

    print("=== Node filtering examples ===")

    try:
        print("\n1. Filter by hostname (router):")
        for node in client.node.filter_by_hostname("router"):
            print(f"  - {node.hostname} ({node.ip_address})")

        print("\n2. Filter by IP address (192.168.1):")
        for node in client.node.filter_by_ip_address("192.168.1"):
            print(f"  - {node.hostname} ({node.ip_address})")

        print("\n3. Filter by device type (cisco_ios):")
        for node in client.node.filter_by_device_type("cisco_ios"):
            print(f"  - {node.hostname} ({node.device_type})")

        print("\n4. Filter by OS type (IOS):")
        for node in client.node.filter_by_os_type("IOS"):
            print(f"  - {node.hostname} ({node.os_type})")

    except Exception as e:
        print(f"Filter error: {e}")


if __name__ == "__main__":
    print("=== Node operation examples ===")

    print("\n1. Add a single Node (all fields):")
    add_node_example()

    print("\n2. Add a minimal Node (required fields only):")
    add_minimal_node()

    print("\n3. Add a Node using a dict:")
    add_node_with_dict()

    print("\n4. Get all Nodes:")
    get_all_nodes()

    print("\n5. Filter Nodes:")
    filter_nodes_example()

#!/usr/bin/env python3
"""Demonstration of the client-side validation system.

Set the following environment variables before running:
  export NETEYE_URL=http://localhost:5001
  export NETEYE_EMAIL=your_email@example.com
  export NETEYE_PASSWORD=your_password
"""

import os
from ipaddress import IPv4Address

from neteye_client.neteye_client import NeteyeClient
from neteye_client.node.node import Node
from neteye_client.interface.interface import Interface
from neteye_client.arp.arp import Arp
from neteye_client.serial.serial import Serial
from neteye_client.cable.cable import Cable

NETEYE_URL = os.environ.get("NETEYE_URL", "http://localhost:5001")
NETEYE_EMAIL = os.environ["NETEYE_EMAIL"]
NETEYE_PASSWORD = os.environ["NETEYE_PASSWORD"]


def get_client() -> NeteyeClient:
    client = NeteyeClient(NETEYE_URL)
    client.login(NETEYE_EMAIL, NETEYE_PASSWORD)
    return client


def demo_node_validation():
    client = get_client()
    print("=== Node validation demo ===")

    print("\n1. Valid Node creation:")
    try:
        created = client.node.create(Node(
            hostname="valid-node-01",
            ip_address=IPv4Address("192.168.10.1"),
            port=22,
        ))
        print(f"  Success: {created.hostname}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n2. Empty hostname:")
    try:
        client.node.create({"hostname": "", "ip_address": "192.168.10.2", "port": 22})
    except Exception as e:
        print(f"  Expected error: {e}")

    print("\n3. Invalid IP address:")
    try:
        client.node.create({"hostname": "test", "ip_address": "invalid.ip", "port": 22})
    except Exception as e:
        print(f"  Expected error: {e}")

    print("\n4. Port out of range:")
    try:
        client.node.create({"hostname": "test", "ip_address": "192.168.10.3", "port": 70000})
    except Exception as e:
        print(f"  Expected error: {e}")


def demo_interface_validation():
    client = get_client()
    print("\n=== Interface validation demo ===")

    nodes = client.node.get()
    if not nodes:
        print("  No test Node available")
        return
    test_node_id = nodes[0].id

    print("\n1. Valid Interface creation:")
    try:
        created = client.interface.create(Interface(
            name="GigabitEthernet0/1",
            ip_address="192.168.20.1",
            mask="255.255.255.0",
            mtu=1500,
            status="up",
            duplex="full",
            node_id=test_node_id,
        ))
        print(f"  Success: {created.name}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n2. Invalid MTU (10000):")
    try:
        client.interface.create({"name": "gi0/2", "node_id": test_node_id, "mtu": 10000})
    except Exception as e:
        print(f"  Expected error: {e}")

    print("\n3. Invalid status:")
    try:
        client.interface.create({"name": "gi0/3", "node_id": test_node_id, "status": "broken"})
    except Exception as e:
        print(f"  Expected error: {e}")


def demo_arp_validation():
    client = get_client()
    print("\n=== ARP validation demo ===")

    interfaces = client.interface.get()
    if not interfaces:
        print("  No test Interface available")
        return
    test_interface_id = interfaces[0].id

    print("\n1. Valid ARP creation:")
    try:
        created = client.arp.create(Arp(
            interface_id=test_interface_id,
            ip_address="192.168.30.1",
            mac_address="00:11:22:33:44:55",
        ))
        print(f"  Success: {created.ip_address} -> {created.mac_address}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n2. Invalid MAC address:")
    try:
        client.arp.create({
            "interface_id": test_interface_id,
            "ip_address": "192.168.30.2",
            "mac_address": "invalid-mac",
        })
    except Exception as e:
        print(f"  Expected error: {e}")


def demo_serial_validation():
    client = get_client()
    print("\n=== Serial validation demo ===")

    nodes = client.node.get()
    if not nodes:
        print("  No test Node available")
        return
    test_node_id = nodes[0].id

    print("\n1. Valid Serial creation:")
    try:
        created = client.serial.create(Serial(
            node_id=test_node_id,
            serial_number="ABC123456789",
        ))
        print(f"  Success: {created.serial_number}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n2. Serial number too short (2 characters):")
    try:
        client.serial.create({"node_id": test_node_id, "serial_number": "AB"})
    except Exception as e:
        print(f"  Expected error: {e}")


def demo_cable_validation():
    client = get_client()
    print("\n=== Cable validation demo ===")

    interfaces = client.interface.get()
    if len(interfaces) < 2:
        print("  Need at least 2 test Interfaces")
        return

    print("\n1. Valid Cable creation:")
    try:
        created = client.cable.create(Cable(
            a_interface_id=interfaces[0].id,
            b_interface_id=interfaces[1].id,
            cable_type="copper",
        ))
        print(f"  Success: {created.id}")
    except Exception as e:
        print(f"  Error: {e}")

    print("\n2. Connecting an interface to itself:")
    try:
        client.cable.create({
            "a_interface_id": interfaces[0].id,
            "b_interface_id": interfaces[0].id,
        })
    except Exception as e:
        print(f"  Expected error: {e}")


def demo_validation_summary():
    print("\n=== Validation summary ===")
    summary = {
        "Node":      ["hostname, ip_address, port (required)", "IPv4 format", "Port range 1-65535"],
        "Interface": ["name, node_id (required)", "MTU 68-9000", "status: up/down/admin-down/testing", "duplex: full/half/auto"],
        "ARP":       ["interface_id, ip_address, mac_address (required)", "IPv4 format", "MAC: XX:XX:XX:XX:XX:XX"],
        "Serial":    ["node_id, serial_number (required)", "Serial number must be 3+ characters"],
        "Cable":     ["a_interface_id, b_interface_id (required)", "Cannot self-loop"],
    }
    for resource, rules in summary.items():
        print(f"\n{resource}:")
        for rule in rules:
            print(f"  - {rule}")


if __name__ == "__main__":
    print("Validation system demo")
    print("=" * 60)

    demo_node_validation()
    demo_interface_validation()
    demo_arp_validation()
    demo_serial_validation()
    demo_cable_validation()
    demo_validation_summary()

    print("\n" + "=" * 60)
    print("Demo complete")

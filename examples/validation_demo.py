#!/usr/bin/env python3
"""バリデーションシステムのデモンストレーション。

使用前に環境変数を設定してください:
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
    print("=== Node バリデーションデモ ===")

    print("\n1. 正常な Node 作成:")
    try:
        created = client.node.create(Node(
            hostname="valid-node-01",
            ip_address=IPv4Address("192.168.10.1"),
            port=22,
        ))
        print(f"  ✓ 成功: {created.hostname}")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    print("\n2. 空のホスト名:")
    try:
        client.node.create({"hostname": "", "ip_address": "192.168.10.2", "port": 22})
    except Exception as e:
        print(f"  ✓ 期待されたエラー: {e}")

    print("\n3. 無効な IP アドレス:")
    try:
        client.node.create({"hostname": "test", "ip_address": "invalid.ip", "port": 22})
    except Exception as e:
        print(f"  ✓ 期待されたエラー: {e}")

    print("\n4. 範囲外のポート番号:")
    try:
        client.node.create({"hostname": "test", "ip_address": "192.168.10.3", "port": 70000})
    except Exception as e:
        print(f"  ✓ 期待されたエラー: {e}")


def demo_interface_validation():
    client = get_client()
    print("\n=== Interface バリデーションデモ ===")

    nodes = client.node.get()
    if not nodes:
        print("  テスト用 Node が存在しません")
        return
    test_node_id = nodes[0].id

    print("\n1. 正常な Interface 作成:")
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
        print(f"  ✓ 成功: {created.name}")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    print("\n2. 無効な MTU (10000):")
    try:
        client.interface.create({"name": "gi0/2", "node_id": test_node_id, "mtu": 10000})
    except Exception as e:
        print(f"  ✓ 期待されたエラー: {e}")

    print("\n3. 無効なステータス:")
    try:
        client.interface.create({"name": "gi0/3", "node_id": test_node_id, "status": "broken"})
    except Exception as e:
        print(f"  ✓ 期待されたエラー: {e}")


def demo_arp_validation():
    client = get_client()
    print("\n=== ARP バリデーションデモ ===")

    interfaces = client.interface.get()
    if not interfaces:
        print("  テスト用 Interface が存在しません")
        return
    test_interface_id = interfaces[0].id

    print("\n1. 正常な ARP 作成:")
    try:
        created = client.arp.create(Arp(
            interface_id=test_interface_id,
            ip_address="192.168.30.1",
            mac_address="00:11:22:33:44:55",
        ))
        print(f"  ✓ 成功: {created.ip_address} -> {created.mac_address}")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    print("\n2. 無効な MAC アドレス:")
    try:
        client.arp.create({
            "interface_id": test_interface_id,
            "ip_address": "192.168.30.2",
            "mac_address": "invalid-mac",
        })
    except Exception as e:
        print(f"  ✓ 期待されたエラー: {e}")


def demo_serial_validation():
    client = get_client()
    print("\n=== Serial バリデーションデモ ===")

    nodes = client.node.get()
    if not nodes:
        print("  テスト用 Node が存在しません")
        return
    test_node_id = nodes[0].id

    print("\n1. 正常な Serial 作成:")
    try:
        created = client.serial.create(Serial(
            node_id=test_node_id,
            serial_number="ABC123456789",
        ))
        print(f"  ✓ 成功: {created.serial_number}")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    print("\n2. 短すぎるシリアル番号 (2文字):")
    try:
        client.serial.create({"node_id": test_node_id, "serial_number": "AB"})
    except Exception as e:
        print(f"  ✓ 期待されたエラー: {e}")


def demo_cable_validation():
    client = get_client()
    print("\n=== Cable バリデーションデモ ===")

    interfaces = client.interface.get()
    if len(interfaces) < 2:
        print("  テスト用 Interface が 2 つ以上必要です")
        return

    print("\n1. 正常な Cable 作成:")
    try:
        created = client.cable.create(Cable(
            a_interface_id=interfaces[0].id,
            b_interface_id=interfaces[1].id,
            cable_type="copper",
        ))
        print(f"  ✓ 成功: {created.id}")
    except Exception as e:
        print(f"  ✗ エラー: {e}")

    print("\n2. 同一インターフェース接続:")
    try:
        client.cable.create({
            "a_interface_id": interfaces[0].id,
            "b_interface_id": interfaces[0].id,
        })
    except Exception as e:
        print(f"  ✓ 期待されたエラー: {e}")


def demo_validation_summary():
    print("\n=== バリデーションサマリー ===")
    summary = {
        "Node":      ["hostname, ip_address, port (必須)", "IPv4 形式", "ポート範囲 1-65535"],
        "Interface": ["name, node_id (必須)", "MTU 68-9000", "status: up/down/admin-down/testing", "duplex: full/half/auto"],
        "ARP":       ["interface_id, ip_address, mac_address (必須)", "IPv4 形式", "MAC: XX:XX:XX:XX:XX:XX"],
        "Serial":    ["node_id, serial_number (必須)", "シリアル番号 3文字以上"],
        "Cable":     ["a_interface_id, b_interface_id (必須)", "自己ループ不可"],
    }
    for resource, rules in summary.items():
        print(f"\n{resource}:")
        for rule in rules:
            print(f"  - {rule}")


if __name__ == "__main__":
    print("バリデーションシステム デモ")
    print("=" * 60)

    demo_node_validation()
    demo_interface_validation()
    demo_arp_validation()
    demo_serial_validation()
    demo_cable_validation()
    demo_validation_summary()

    print("\n" + "=" * 60)
    print("デモ完了")

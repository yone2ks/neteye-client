#!/usr/bin/env python3
"""neteye_client を使用して Node を操作するサンプルコード。

使用前に環境変数を設定してください:
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
    """Node を全フィールド指定で追加する例。"""
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
        print(f"Node追加成功: {created_node.hostname} (ID: {created_node.id})")
        return created_node
    except Exception as e:
        print(f"Node追加エラー: {e}")
        return None


def add_minimal_node():
    """必須フィールドのみで Node を追加する例。"""
    client = get_client()

    minimal_node = Node(
        hostname="minimal-router",
        ip_address=IPv4Address("192.168.1.100"),
        port=22,
    )

    print(f"送信データ: {minimal_node.to_dict()}")

    try:
        created_node = client.node.create(minimal_node)
        print(f"最小限 Node 追加成功: {created_node.hostname} (ID: {created_node.id})")
        return created_node
    except Exception as e:
        print(f"Node 追加エラー: {e}")
        return None


def add_node_with_dict():
    """辞書形式で Node を追加する例。"""
    client = get_client()

    node_data = {
        "hostname": "dict-router",
        "ip_address": "192.168.1.102",
        "port": 22,
    }

    try:
        created_node = client.node.create(node_data)
        print(f"辞書形式 Node 追加成功: {created_node.hostname} (ID: {created_node.id})")
        return created_node
    except Exception as e:
        print(f"Node 追加エラー: {e}")
        return None


def get_all_nodes():
    """全 Node を取得する例。"""
    client = get_client()

    try:
        nodes = client.node.get()
        print(f"取得した Node 数: {len(nodes)}")
        for node in nodes:
            print(f"- {node.hostname} ({node.ip_address}) - ID: {node.id}")
        return nodes
    except Exception as e:
        print(f"Node 取得エラー: {e}")
        return []


def filter_nodes_example():
    """Node をフィルタリングする例。"""
    client = get_client()

    print("=== Node フィルタリング例 ===")

    try:
        print("\n1. ホスト名でフィルタ (router):")
        for node in client.node.filter_by_hostname("router"):
            print(f"  - {node.hostname} ({node.ip_address})")

        print("\n2. IP アドレスでフィルタ (192.168.1):")
        for node in client.node.filter_by_ip_address("192.168.1"):
            print(f"  - {node.hostname} ({node.ip_address})")

        print("\n3. デバイスタイプでフィルタ (cisco_ios):")
        for node in client.node.filter_by_device_type("cisco_ios"):
            print(f"  - {node.hostname} ({node.device_type})")

        print("\n4. OS タイプでフィルタ (IOS):")
        for node in client.node.filter_by_os_type("IOS"):
            print(f"  - {node.hostname} ({node.os_type})")

    except Exception as e:
        print(f"フィルタエラー: {e}")


if __name__ == "__main__":
    print("=== Node 操作サンプル ===")

    print("\n1. 単一 Node 追加（全フィールド）:")
    add_node_example()

    print("\n2. 最小限 Node 追加（必須フィールドのみ）:")
    add_minimal_node()

    print("\n3. 辞書形式で Node 追加:")
    add_node_with_dict()

    print("\n4. 全 Node 取得:")
    get_all_nodes()

    print("\n5. Node フィルタリング:")
    filter_nodes_example()

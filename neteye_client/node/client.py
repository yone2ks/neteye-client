from neteye_client.neteye_client import NeteyeClient
from neteye_client.node.node import Node


class Client:
    def __init__(self, url: str):
        self.client = NeteyeClient(url)

    def get(self, node_id: str) -> Node:
        """
        Retrieves a Node object with the specified ID.
        """
        path = f"{Node.NODE_PATH}/{node_id}"
        node_data = self.client.get(path)
        return Node.from_dict(node_data)

    def create(self, node: Node) -> Node:
        """
        Creates a new Node object.
        """
        node_data = node.to_dict()
        created_node_data = self.client.post(Node.NODE_PATH, data=node_data)
        return Node.from_dict(created_node_data)

    def update(self, node: Node) -> Node:
        """
        Updates an existing Node object.
        """
        path = f"{Node.NODE_PATH}/{node.id}"
        node_data = node.to_dict()
        updated_node_data = self.client.put(path, data=node_data)
        return Node.from_dict(updated_node_data)

    def delete(self, node_id: str) -> None:
        """
        Deletes a Node object with the specified ID.
        """
        path = f"{Node.NODE_PATH}/{node_id}"
        self.client.delete(path)

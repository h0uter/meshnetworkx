import json
import pickle
import time
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import zenoh
from humid import hfid

PREFIX = "graph"


def totopic(key: str):
    return f"{PREFIX}/{key}"


class GraphZ:
    def __init__(self):
        """
        Initializes the GraphZ object and connects to the Zenoh router.
        """
        cfg = zenoh.Config()

        # tell zenoh to connect to local router, cause multicast scouting does not work in docker outside of linux host.
        cfg.insert_json5("connect/endpoints", json.dumps(["tcp/localhost:7447"]))

        self._z = zenoh.open(cfg)

    @staticmethod
    def from_networkx(g: nx.Graph) -> "GraphZ":
        """
        Creates a GraphZ object from a NetworkX graph.

        Args:
            g: A NetworkX graph.

        Returns:
            A GraphZ object.
        """
        raise NotImplementedError()
        return GraphZ()

    def to_networkx(self) -> nx.Graph:
        """
        Converts the GraphZ object to a NetworkX graph.

        Returns:
            A NetworkX graph.
        """
        g = nx.Graph()

        for node, data in self.nodes(data=True):
            g.add_node(node, **data)

        return g

    def add_node(self, node: Any, **attr) -> None:
        """
        Adds a node to the GraphZ object.

        Args:
            node: The node to add.
            attr: Additional attributes for the node.
        """
        # TODO: handle node already exists

        data_dict = {}
        data_dict.update(attr)

        data_bytes = pickle.dumps((type(node), data_dict))
        self._z.put(totopic(node), data_bytes)
        time.sleep(0.01)

    def add_nodes_from(self, nodes: list[Any], **attr) -> None:
        """Add nodes from a list of nodes.

        Args:
            nodes: The nodes to add.
            **attr: The attributes to add to the nodes.
        """
        for node in nodes:
            self.add_node(node, **attr)

    def remove_nodes_from(self, nodes: list[Any]) -> None:
        for node in nodes:
            self.remove_node(node)

    def remove_node(self, node: Any) -> None:
        self._z.delete(totopic(node))
        time.sleep(0.01)

    def has_node(self, node: Any) -> bool:
        """
        Checks if a node exists in the GraphZ object.

        Args:
            node: The node to check.

        Returns:
            True if the node exists, False otherwise.
        """
        return node in self.nodes()

    def nodes(self, data: bool = False) -> list[Any] | list[tuple[Any, Any]]:
        """
        Returns a list of nodes in the GraphZ object.

        Args:
            data: If True, returns a list of tuples containing nodes and their data. If False, returns a list of nodes.

        Returns:
            A list of nodes or a list of tuples containing nodes and their data.
        """
        nodes = []
        replies = self._z.get(f"{PREFIX}/**", handler=zenoh.handlers.DefaultHandler())
        for reply in replies:
            reply: zenoh.Reply
            # the last part is the node name
            node = str(reply.ok.key_expr).split("/")[-1]
            node_type, node_data = pickle.loads(reply.ok.payload.to_bytes())
            node = node_type(node)
            if data:
                nodes.append((node, node_data))
            else:
                nodes.append(node)

        return nodes

    def clear(self) -> None:
        """
        Clears all nodes from the GraphZ object.
        """
        for node in self.nodes():
            self.remove_node(node)

    def close(self) -> None:
        """
        Closes the connection to the Zenoh router.
        """
        self._z.close()

    def __iter__(self):
        """
        Returns an iterator over the nodes in the GraphZ object.

        Returns:
            An iterator over the nodes.
        """
        return iter(self.nodes())

    def draw(self, block: bool = True) -> None:
        """
        Draws the GraphZ object using NetworkX.

        Args:
            block: If True, blocks the drawing window. If False, does not block.
        """
        nxg = self.to_networkx()
        nx.draw(nxg)
        plt.show(block=block)


def main():
    print("running nx example!!!")
    print()

    zg = GraphZ()
    for _ in range(10):
        zg.add_node(hfid(), color="red")

    time.sleep(1)

    print(f"plotting {zg}")
    print("")
    zg.draw()

    print("clearing graph")
    print("")
    zg.clear()

    time.sleep(1)

    print(f"plotting {zg}")
    print("")
    zg.draw()


if __name__ == "__main__":
    main()

import json
import pickle
import time
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import zenoh
from humid import hfid

PREFIX = "graph"
WAIT_TIME = 0.0001

class ZNetworkXError(Exception):
    """General exception for ZNetworkX errors."""

    pass


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
        nodes = list(g.nodes)

        zg = GraphZ()
        zg.add_nodes_from(nodes)

        return GraphZ()

    def to_networkx(self) -> nx.Graph:
        """
        Converts the GraphZ object to a NetworkX graph.

        Returns:
            A NetworkX graph.
        """
        g = nx.Graph()

        for node, data in self.nodes(data=True).items():
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
        try_str(node)

        data_dict = {}
        data_dict.update(attr)

        data_bytes = pickle.dumps(data_dict)
        self._z.put(totopic(node), data_bytes)
        # TODO: instead wait till we can read it back
        time.sleep(WAIT_TIME)

    def add_edge(self, u: Any, v: Any, **attr) -> None:
        """
        Adds an edge to the GraphZ object.

        Args:
            u: The source node.
            v: The target node.
            attr: Additional attributes for the edge.
        """
        try_str(u)
        try_str(v)

        # check if the nodes exist, else create them
        if not self.has_node(u):
            self.add_node(u)
        if not self.has_node(v):
            self.add_node(v)

        data_dict = {}
        data_dict.update(attr)
        data_bytes = pickle.dumps(data_dict)

        key = f"{u}/to/{v}" if u < v else f"{v}/to/{u}"
        self._z.put(totopic(key), data_bytes)
        # TODO: instead wait till we can read it back
        time.sleep(WAIT_TIME)

    def remove_edge(self, u: Any, v: Any) -> None:
        """
        Removes an edge from the GraphZ object.

        Args:
            u: The source node.
            v: The target node.
        """
        try_str(u)
        try_str(v)

        key = f"{u}/to/{v}" if u < v else f"{v}/to/{u}"
        self._z.delete(totopic(key))
        time.sleep(WAIT_TIME)

    @property
    def adj(self):
        """
        Returns the adjacency list of the GraphZ object.

        Returns:
            The adjacency list.
        """
        adj = {}
        replies = self._z.get(
            totopic("*/to/*"), handler=zenoh.handlers.DefaultHandler()
        )

        for reply in replies:
            reply: zenoh.Reply

            data = pickle.loads(reply.ok.payload.to_bytes())
            print("data", data)

            # the last part is the node name
            u = str(reply.ok.key_expr).split("/")[-1]
            v = str(reply.ok.key_expr).split("/")[-3]

            # add the edge to the adjacency list
            if u not in adj:
                adj[u] = {}
            adj[u][v] = {}
            if v not in adj:
                adj[v] = {}
            adj[v][u] = {}

        return adj

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
        # check if the node exists
        if not self.has_node(node):
            raise ZNetworkXError(f"Node {node} does not exist")


        self._z.delete(totopic(node))
        self._z.delete(totopic(f"{node}/to/*"))
        self._z.delete(totopic(f"*/to/{node}"))
        time.sleep(WAIT_TIME)

    def has_node(self, node: Any) -> bool:
        """
        Checks if a node exists in the GraphZ object.

        Args:
            node: The node to check.

        Returns:
            True if the node exists, False otherwise.
        """
        try_str(node)
        return str(node) in self.nodes()

    def nodes(self, data: bool = False) -> dict[Any, Any] | set[Any]:
        """
        Returns a list of nodes in the GraphZ object.

        Args:
            data: If True, returns a list of tuples containing nodes and their data. If False, returns a list of nodes.

        Returns:
            A list of nodes or a list of tuples containing nodes and their data.
        """
        nodes = set()
        if data:
            nodes = {}

        replies = self._z.get(f"{PREFIX}/*", handler=zenoh.handlers.DefaultHandler())
        for reply in replies:
            reply: zenoh.Reply
            # the last part is the node name
            node = str(reply.ok.key_expr).split("/")[-1]
            node_data = pickle.loads(reply.ok.payload.to_bytes())

            if isinstance(nodes, dict):
                nodes[node] = node_data
            elif isinstance(nodes, set):
                nodes.add(node)

        return nodes

    def clear(self) -> None:
        """
        Clears all nodes from the GraphZ object.
        """
        # for node in self.nodes():
        #     self.remove_node(node)

        self._z.delete(totopic("**"))

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


def try_str(key: Any):
    if key is None:
        raise ValueError("Item cannot be None.")
    try:
        str(key)
    except Exception as e:
        raise ZNetworkXError(f"Item '{key}' cannot be converted to string.") from e


if __name__ == "__main__":
    main()

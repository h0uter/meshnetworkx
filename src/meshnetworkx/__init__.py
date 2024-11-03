"""Provides the GraphZ class for storing a NetworkX graph in Zenoh."""

import json
import pickle
import time
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import zenoh

PREFIX = "graph"
WAIT_TIME = 0.0001


class MeshNetworkXError(Exception):
    """General exception for MeshNetworkX errors."""

    pass


def _totopic(key: str):
    return f"{PREFIX}/{key}"


class NodeView:
    """Provides a read only view for accessing node data in a dictionary-like manner."""

    def __init__(self, node_data: dict[Any, Any]):
        """Initializes the NodeView object with node data.

        Args:
            node_data: A dictionary containing node data.
        """
        self._node_data = node_data  # Dictionary to store node data

    def __getitem__(self, key: Any):
        """Allow dictionary-like access."""
        return self._node_data[key]

    def __setitem__(self, key: Any, value: Any):
        """Prevent assignment to the NodeView."""
        raise TypeError("NodeView object does not support item assignment")

    def __call__(self, data: bool = False):
        """Method-like access with optional arguments."""
        if data:
            return self._node_data.items()  # Return nodes with data
        return self._node_data.keys()  # Return just node identifiers


class Graph:
    """Represents a NetworkX graph stored in Zenoh."""

    def __init__(self):
        """Initializes the GraphZ object and connects to the Zenoh router."""
        cfg = zenoh.Config()

        # tell zenoh to connect to local router,
        # cause multicast scouting does not work in docker outside of linux host.
        cfg.insert_json5("connect/endpoints", json.dumps(["tcp/localhost:7447"]))

        self._z = zenoh.open(cfg)

    @staticmethod
    def from_networkx(g: nx.Graph) -> "Graph":
        """Creates a GraphZ object from a NetworkX graph.

        Args:
            g: A NetworkX graph.

        Returns:
            A GraphZ object.
        """
        nodes = list(g.nodes)

        zg = Graph()
        zg.add_nodes_from(nodes)

        # TODO: also convert node data
        # TODO: also convert edges
        # TODO: also convert edge data

        return zg

    def to_networkx(self) -> nx.Graph:
        """Converts the GraphZ object to a NetworkX graph.

        Returns:
            A NetworkX graph.
        """
        g = nx.Graph()

        for node, data in self.nodes(data=True):
            g.add_node(node, **data)

        return g

    def add_node(self, node: Any, **attr) -> None:
        """Adds a node to the GraphZ object.

        Args:
            node: The node to add.
            attr: Additional attributes for the node.
        """
        _try_str(node)
        # if self.has_node(node):
        #     raise MeshNetworkXError(f"Node {node} already exists")

        data_dict = {}
        data_dict.update(attr)

        data_bytes = pickle.dumps(data_dict)
        self._z.put(_totopic(node), data_bytes)
        # TODO: instead wait till we can read it back
        time.sleep(WAIT_TIME)

    def add_edge(self, u: Any, v: Any, **attr) -> None:
        """Adds an edge to the GraphZ object.

        Args:
            u: The source node.
            v: The target node.
            attr: Additional attributes for the edge.
        """
        _try_str(u)
        _try_str(v)

        # check if the nodes exist, else create them
        if not self.has_node(u):
            self.add_node(u)
        if not self.has_node(v):
            self.add_node(v)

        data_dict = {}
        data_dict.update(attr)
        data_bytes = pickle.dumps(data_dict)

        key = f"{u}/to/{v}" if u < v else f"{v}/to/{u}"
        self._z.put(_totopic(key), data_bytes)
        # TODO: instead wait till we can read it back
        time.sleep(WAIT_TIME)

    def remove_edge(self, u: Any, v: Any) -> None:
        """Removes an edge from the GraphZ object.

        Args:
            u: The source node.
            v: The target node.
        """
        _try_str(u)
        _try_str(v)

        key = f"{u}/to/{v}" if u < v else f"{v}/to/{u}"
        self._z.delete(_totopic(key))
        time.sleep(WAIT_TIME)

    @property
    def adj(self) -> dict[Any, dict[Any, dict[Any, Any]]]:
        """Returns the adjacency list of the GraphZ object.

        Returns:
            The adjacency list.
        """
        adj = {}
        replies = self._z.get(
            _totopic("*/to/*"), handler=zenoh.handlers.DefaultHandler()
        )

        for reply in replies:
            reply: zenoh.Reply

            if reply.err:
                raise MeshNetworkXError(f"Error: {reply.err.payload.to_string()}")

            if reply.ok:
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
        """Removes nodes from the GraphZ object.

        Args:
            nodes: The nodes to remove.
        """
        for node in nodes:
            self.remove_node(node)

    def remove_node(self, node: Any) -> None:
        """Removes a node from the GraphZ object.

        Args:
            node: The node to remove.
        """
        # check if the node exists
        if not self.has_node(node):
            raise MeshNetworkXError(f"Node {node} does not exist")

        self._z.delete(_totopic(node))
        self._z.delete(_totopic(f"{node}/to/*"))
        self._z.delete(_totopic(f"*/to/{node}"))
        time.sleep(WAIT_TIME)

    def has_node(self, node: Any) -> bool:
        """Checks if a node exists in the GraphZ object.

        Args:
            node: The node to check.

        Returns:
            True if the node exists, False otherwise.
        """
        _try_str(node)
        return str(node) in self.nodes()

    # def nodes(self, data: bool = False) -> dict[Any, Any] | set[Any]:
    @property
    def nodes(self) -> NodeView:
        """Returns a list of nodes in the GraphZ object.

        Args:
            data: If True, returns a list of tuples containing nodes and their data.
            If False, returns a list of nodes.

        Returns:
            A list of nodes or a list of tuples containing nodes and their data.
        """
        nodes = {}

        replies = self._z.get(_totopic("*"), handler=zenoh.handlers.DefaultHandler())
        for reply in replies:
            reply: zenoh.Reply
            if not reply.ok:
                raise MeshNetworkXError(f"Error: {reply.err.payload.to_string()}")

            # the last part is the node name
            node = str(reply.ok.key_expr).split("/")[-1]
            node_data = pickle.loads(reply.ok.payload.to_bytes())

            nodes[node] = node_data

        return NodeView(nodes)

    def clear(self) -> None:
        """Clears all nodes from the GraphZ object."""
        self._z.delete(_totopic("**"))
        time.sleep(WAIT_TIME)

    def close(self) -> None:
        """Closes the connection to the Zenoh router."""
        self._z.close()

    def __iter__(self):
        """Returns an iterator over the nodes in the GraphZ object.

        Returns:
            An iterator over the nodes.
        """
        return iter(self.nodes())

    def draw(self, block: bool = True) -> None:
        """Draws the GraphZ object using NetworkX.

        Args:
            block: If True, blocks the drawing window. If False, does not block.
        """
        nxg = self.to_networkx()
        nx.draw(nxg)
        plt.show(block=block)


def _try_str(key: Any) -> str:
    if key is None:
        raise TypeError("Item cannot be None.")

    try:
        key_str = str(key)
    except Exception as e:
        raise MeshNetworkXError(f"Item '{key}' cannot be converted to string.") from e

    ILLEGAL_CHARS = ["/", "*", "?", ":", "|", "\\", "<", ">", '"', " "]

    if any(char in key_str for char in ILLEGAL_CHARS):
        raise MeshNetworkXError(f"Item '{key}' contains illegal characters.")

    return key_str

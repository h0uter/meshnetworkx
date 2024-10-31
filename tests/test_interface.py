import networkx as nx
import pytest

from networkedx.main import GraphZ

# Define a whitelist of interface elements differences that can be ignored
WHITELIST = {
    "methods": [
        "subgraph",
        "get_edge_data",
        "__networkx_backend__",
        "__getitem__",
        "adjlist_inner_dict_factory",
        "to_directed_class",
        "__networkx_cache__",
        "add_edges_from",
        "graph",
        "edge_attr_dict_factory",
        "edge_subgraph",
        "add_edge",
        "nbunch_iter",
        "__contains__",
        "__iter__",
        "is_multigraph",
        "add_weighted_edges_from",
        "adj",
        "to_directed",
        "neighbors",
        "degree",
        "number_of_nodes",
        "has_edge",
        "__len__",
        "remove_nodes_from",
        "edges",
        "graph_attr_dict_factory",
        "node_dict_factory",
        "clear_edges",
        "size",
        "remove_edge",
        "to_undirected",
        "number_of_edges",
        "update",
        "adjacency",
        "adjlist_outer_dict_factory",
        "name",
        "to_undirected_class",
        "node_attr_dict_factory",
        "add_nodes_from",
        "copy",
        "has_node",
        "is_directed",
        "order",
        "remove_edges_from",
        "_adj",
        "_node",
    ],
    "attributes": [
        "__networkx_cache__",
        "graph",
        "adj",
        "__networkx_backend__",
        "name",
        "_adj",
        "_node",
    ],
}


def log_differences(differences, element_type):
    if differences:
        print(f"Differences in {element_type}:")
        for diff in differences:
            print(f" - {diff}")


def test_graph_interface():
    nx_graph = nx.Graph()
    graphz_graph = GraphZ()

    # Check if both have the same methods
    nx_methods = set(dir(nx_graph))
    graphz_methods = set(dir(graphz_graph))

    method_differences = (nx_methods - graphz_methods) - set(WHITELIST["methods"])
    log_differences(method_differences, "methods")
    assert (
        not method_differences
    ), "Graphz interface does not match NetworkX Graph interface"

    # Check if both have the same attributes
    nx_attrs = {attr for attr in nx_methods if not callable(getattr(nx_graph, attr))}
    graphz_attrs = {
        attr for attr in graphz_methods if not callable(getattr(graphz_graph, attr))
    }

    attr_differences = (nx_attrs - graphz_attrs) - set(WHITELIST["attributes"])
    log_differences(attr_differences, "attributes")
    assert (
        not attr_differences
    ), "Graphz attributes do not match NetworkX Graph attributes"


def test_graph_methods():
    nx_graph = nx.Graph()
    graphz_graph = GraphZ()

    for method in dir(nx_graph):
        if callable(getattr(nx_graph, method)) and method not in WHITELIST["methods"]:
            assert hasattr(graphz_graph, method), f"Graphz is missing method: {method}"


def test_graph_attributes():
    nx_graph = nx.Graph()
    graphz_graph = GraphZ()

    for attr in dir(nx_graph):
        if (
            not callable(getattr(nx_graph, attr))
            and attr not in WHITELIST["attributes"]
        ):
            assert hasattr(graphz_graph, attr), f"Graphz is missing attribute: {attr}"

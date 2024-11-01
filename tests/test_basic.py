import time

import networkx as nx
import pytest

import networkedx.main as znx


@pytest.fixture
def graphz():
    # Fixture to create and teardown GraphZ instance
    g = znx.GraphZ()
    yield g
    g.clear()
    g.close()


def test_add_node(graphz):
    # Test adding a node to the graph
    graphz.add_node("node1", color="blue")
    nodes = graphz.nodes()
    assert "node1" in nodes


def test_add_node_hardcore(graphz):
    G = graphz
    G.add_node(0)

    # TODO: enable adj
    # assert G.adj == {0: {}}

    # test add attributes
    G.add_node(1, c="red")
    G.add_node(2, c="blue")
    G.add_node(3, c="red")
    assert G.nodes(data=True)[1]["c"] == "red"
    assert G.nodes(data=True)[2]["c"] == "blue"
    assert G.nodes(data=True)[3]["c"] == "red"
    # test updating attributes
    G.add_node(1, c="blue")
    G.add_node(2, c="red")
    G.add_node(3, c="blue")
    assert G.nodes(data=True)[1]["c"] == "blue"
    assert G.nodes(data=True)[2]["c"] == "red"
    assert G.nodes(data=True)[3]["c"] == "blue"


@pytest.mark.skip("Real nx interface does not have G.nodes()[1]")
def test_add_node_hardcore_correct(graphz):
    G = graphz
    G.add_node(0)

    # TODO: enable adj
    # assert G.adj == {0: {}}

    # test add attributes
    G.add_node(1, c="red")
    G.add_node(2, c="blue")
    G.add_node(3, c="red")
    assert G.nodes[1]["c"] == "red"
    assert G.nodes[2]["c"] == "blue"
    assert G.nodes[3]["c"] == "red"
    # test updating attributes
    G.add_node(1, c="blue")
    G.add_node(2, c="red")
    G.add_node(3, c="blue")
    assert G.nodes[1]["c"] == "blue"
    assert G.nodes[2]["c"] == "red"
    assert G.nodes[3]["c"] == "blue"


def test_add_nodes_from(graphz):
    G = graphz
    G.add_nodes_from(list("ABCDEFGHIJKL"))
    assert G.has_node("L")
    G.remove_nodes_from(["H", "I", "J", "K", "L"])
    G.add_nodes_from([1, 2, 3, 4])
    assert sorted(G.nodes(), key=str) == [
        1,
        2,
        3,
        4,
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
    ]
    # test __iter__
    assert sorted(G, key=str) == [1, 2, 3, 4, "A", "B", "C", "D", "E", "F", "G"]


def test_add_node_with_attributes(graphz):
    # Test adding a node with attributes
    graphz.add_node("node2", color="green", weight=5)
    nodes = graphz.nodes(data=True)
    assert any(
        node == "node2" and data["color"] == "green" and data["weight"] == 5
        for node, data in nodes.items()
    )


def test_remove_node(graphz):
    # Test removing a node
    graphz.add_node("node3")
    graphz.remove_node("node3")
    nodes = graphz.nodes()
    assert "node3" not in nodes


def test_remove_node_hardcore(graphz):
    G = graphz
    G.add_node(0)
    G.remove_node(0)
    # assert G.adj == {1: {2: {}}, 2: {1: {}}}
    with pytest.raises(znx.ZNetworkXError):
        G.remove_node(-1)


def test_clear(graphz):
    # Test clearing all nodes
    graphz.add_node("node4")
    graphz.add_node("node5")
    graphz.clear()
    nodes = graphz.nodes()
    assert len(nodes) == 0


def test_to_networkx(graphz):
    # Test converting to NetworkX graph
    graphz.add_node("node6", color="yellow")
    graphz.add_node("node7", color="red")
    g = graphz.to_networkx()
    assert isinstance(g, nx.Graph)
    assert "node6" in g.nodes
    assert g.nodes["node6"]["color"] == "yellow"
    assert "node7" in g.nodes
    assert g.nodes["node7"]["color"] == "red"


def test_nodes_without_data(graphz):
    # Test getting nodes without attributes
    graphz.add_node("node8")
    graphz.add_node("node9")
    nodes = graphz.nodes()
    assert "node8" in nodes
    assert "node9" in nodes


def test_nodes_with_data(graphz):
    # Test getting nodes with attributes
    graphz.add_node("node10", color="orange")
    graphz.add_node("node11", color="purple")
    nodes = graphz.nodes(data=True)
    assert any(
        node == "node10" and data["color"] == "orange" for node, data in nodes.items()
    )
    assert any(
        node == "node11" and data["color"] == "purple" for node, data in nodes.items()
    )

def test_nx_to_zgraph_to_nx_nodes_only():
    """Test converting a NetworkX graph to a GraphZ instance and back to NetworkX."""
    G = nx.Graph()
    G.add_nodes_from(list("ABCDEFGHIJKL"))
    Z = znx.GraphZ.from_networkx(G)

    G2 = Z.to_networkx()

    assert sorted(G.nodes()) == sorted(G2.nodes())


@pytest.mark.skip("Not implemented")
def test_duplicate_node_warning():
    """How do we handle adding a node with a key that already exists?"""
    graphz.add_node("node10", color="orange")
    graphz.add_node("node10", color="purple")
    assert False

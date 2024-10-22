import networkx as nx
import pytest

from networkedx.main import GraphZ 


@pytest.fixture
def graphz():
    # Fixture to create and teardown GraphZ instance
    g = GraphZ()
    yield g
    g.clear()
    g.close()


def test_add_node(graphz):
    # Test adding a node to the graph
    graphz.add_node("node1", color="blue")
    nodes = graphz.nodes()
    assert "node1" in nodes


def test_add_node_with_attributes(graphz):
    # Test adding a node with attributes
    graphz.add_node("node2", color="green", weight=5)
    nodes = graphz.nodes(data=True)
    assert any(
        node == "node2" and data["color"] == "green" and data["weight"] == 5
        for node, data in nodes
    )


def test_remove_node(graphz):
    # Test removing a node
    graphz.add_node("node3")
    graphz.remove_node("node3")
    nodes = graphz.nodes()
    assert "node3" not in nodes


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
    assert any(node == "node10" and data["color"] == "orange" for node, data in nodes)
    assert any(node == "node11" and data["color"] == "purple" for node, data in nodes)

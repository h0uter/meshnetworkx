"""This module contains basic tests for the GraphZ class."""

import time

import networkx as nx
import pytest

import meshnetworkx as mnx


@pytest.fixture
def graphz():
    """Fixture to create and teardown GraphZ instance."""
    # Fixture to create and teardown GraphZ instance
    g = mnx.Graph()
    yield g
    g.clear()
    g.close()


def test_add_node(graphz):
    """Test adding a node to the graph."""
    # Test adding a node to the graph
    graphz.add_node("node1", color="blue")
    nodes = graphz.nodes()
    assert "node1" in nodes


@pytest.mark.skip("Real nx interface does not have G.nodes()[1]")
def test_add_node_hardcore(graphz):
    """Test adding nodes with various attributes and updating them."""
    G = graphz
    G.add_node(0)

    # TODO: enable adj
    # assert G.adj == {0: {}}

    # test add attributes
    G.add_node(1, c="red")
    G.add_node(2, c="blue")
    G.add_node(3, c="red")
    assert G.nodes(data=True)["1"]["c"] == "red"
    assert G.nodes(data=True)["2"]["c"] == "blue"
    assert G.nodes(data=True)["3"]["c"] == "red"
    # test updating attributes
    G.add_node(1, c="blue")
    G.add_node(2, c="red")
    G.add_node(3, c="blue")
    assert G.nodes(data=True)["1"]["c"] == "blue"
    assert G.nodes(data=True)["2"]["c"] == "red"
    assert G.nodes(data=True)["3"]["c"] == "blue"


def test_add_node_hardcore_correct(graphz):
    """Test adding nodes with various attributes and updating them correctly."""
    G = graphz
    G.add_node(0)

    # TODO: enable adj
    # assert G.adj == {0: {}}

    # test add attributes
    G.add_node(1, c="red")
    G.add_node(2, c="blue")
    G.add_node(3, c="red")
    assert G.nodes["1"]["c"] == "red"
    assert G.nodes["2"]["c"] == "blue"
    assert G.nodes["3"]["c"] == "red"
    # test updating attributes
    G.add_node(1, c="blue")
    G.add_node(2, c="red")
    G.add_node(3, c="blue")
    assert G.nodes["1"]["c"] == "blue"
    assert G.nodes["2"]["c"] == "red"
    assert G.nodes["3"]["c"] == "blue"


def test_add_nodes_from(graphz):
    """Test adding nodes from a list and removing some of them."""
    G = graphz
    G.add_nodes_from(list("ABCDEFGHIJKL"))
    assert G.has_node("L")
    G.remove_nodes_from(["H", "I", "J", "K", "L"])
    G.add_nodes_from([1, 2, 3, 4])
    assert sorted(G.nodes(), key=str) == [
        "1",
        "2",
        "3",
        "4",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
    ]
    # test __iter__
    assert sorted(G, key=str) == ["1", "2", "3", "4", "A", "B", "C", "D", "E", "F", "G"]


def test_add_node_with_attributes(graphz):
    """Test adding a node with attributes."""
    # Test adding a node with attributes
    WEIGHT = 5
    graphz.add_node("node2", color="green", weight=WEIGHT)
    nodes = graphz.nodes(data=True)
    assert any(
        node == "node2" and data["color"] == "green" and data["weight"] == WEIGHT
        for node, data in nodes
    )


def test_remove_node(graphz):
    """Test removing a node from the graph."""
    # Test removing a node
    graphz.add_node("node3")
    nodes = graphz.nodes()
    assert "node3" in nodes

    graphz.remove_node("node3")
    nodes = graphz.nodes()
    assert "node3" not in nodes


def test_remove_node_hardcore(graphz):
    """Test removing a node with edges from the graph."""
    G = graphz
    G.add_edge(1, 2)
    assert G.adj == {"1": {"2": {}}, "2": {"1": {}}}
    G.add_node(0)
    G.remove_node(0)
    assert G.adj == {"1": {"2": {}}, "2": {"1": {}}}
    with pytest.raises(mnx.MeshNetworkXError):
        G.remove_node(-1)


def test_clear(graphz):
    """Test clearing all nodes from the graph."""
    # Test clearing all nodes
    graphz.add_node("node4")
    graphz.add_node("node5")
    graphz.clear()
    nodes = graphz.nodes()
    assert len(nodes) == 0


def test_to_networkx(graphz):
    """Test converting GraphZ instance to NetworkX graph."""
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
    """Test getting nodes without attributes."""
    # Test getting nodes without attributes
    graphz.add_node("node8")
    graphz.add_node("node9")
    nodes = graphz.nodes()
    assert "node8" in nodes
    assert "node9" in nodes


def test_nodes_with_data(graphz):
    """Test getting nodes with attributes."""
    # Test getting nodes with attributes
    graphz.add_node("node10", color="orange")
    graphz.add_node("node11", color="purple")
    nodes = graphz.nodes(data=True)
    assert any(node == "node10" and data["color"] == "orange" for node, data in nodes)
    assert any(node == "node11" and data["color"] == "purple" for node, data in nodes)


def test_nx_to_zgraph_to_nx_nodes_only():
    """Test converting a NetworkX graph to a GraphZ instance and back to NetworkX."""
    G = nx.Graph()
    G.add_nodes_from(list("ABCDEFGHIJKL"))
    Z = mnx.Graph.from_networkx(G)

    G2 = Z.to_networkx()

    assert sorted(G.nodes()) == sorted(G2.nodes())


@pytest.mark.skip("Not implemented")
def test_duplicate_node_warning():
    """How do we handle adding a node with a key that already exists?"""
    graphz.add_node("node10", color="orange")
    graphz.add_node("node10", color="purple")
    raise AssertionError()


def test_add_edge(graphz):
    """Test adding an edge to the graph."""
    G = graphz
    G.add_edge(0, 1)
    assert G.adj == {"0": {"1": {}}, "1": {"0": {}}}
    G = graphz
    G.add_edge(*(0, 1))
    assert G.adj == {"0": {"1": {}}, "1": {"0": {}}}
    G = graphz
    with pytest.raises(ValueError):
        G.add_edge(None, "anything")


def test_remove_edge(graphz):
    """Test removing an edge from the graph."""
    G = graphz
    G.add_edge(1, 2, weight=3)
    assert G.adj == {"1": {"2": {}}, "2": {"1": {}}}
    G.remove_edge(1, 2)
    assert G.adj == {}


def test_remove_edge_2(graphz):
    """Test removing an edge from the graph with multiple edges."""
    G = graphz
    G.add_edge(1, 2, weight=3)
    assert G.adj == {"1": {"2": {}}, "2": {"1": {}}}
    G.add_edge(0, 1, weight=2)
    assert G.adj == {"0": {"1": {}}, "1": {"2": {}, "0": {}}, "2": {"1": {}}}
    G.remove_edge(0, 1)
    assert G.adj == {"1": {"2": {}}, "2": {"1": {}}}


@pytest.mark.skip("TODO")
def test_add_edges_from(self):
    """Test adding edges from a list with various attributes."""
    G = self.Graph()
    G.add_edges_from([(0, 1), (0, 2, {"weight": 3})])
    assert G.adj == {
        0: {1: {}, 2: {"weight": 3}},
        1: {0: {}},
        2: {0: {"weight": 3}},
    }
    G = self.Graph()
    G.add_edges_from([(0, 1), (0, 2, {"weight": 3}), (1, 2, {"data": 4})], data=2)
    assert G.adj == {
        0: {1: {"data": 2}, 2: {"weight": 3, "data": 2}},
        1: {0: {"data": 2}, 2: {"data": 4}},
        2: {0: {"weight": 3, "data": 2}, 1: {"data": 4}},
    }

    with pytest.raises(nx.NetworkXError):
        G.add_edges_from([(0,)])  # too few in tuple
    with pytest.raises(nx.NetworkXError):
        G.add_edges_from([(0, 1, 2, 3)])  # too many in tuple
    with pytest.raises(TypeError):
        G.add_edges_from([0])  # not a tuple
    with pytest.raises(ValueError):
        G.add_edges_from([(None, 3), (3, 2)])  # None cannot be a node


# @pytest.mark.skip("TODO")
# def test_remove_edge(self):
#     G = self.K3.copy()
#     G.remove_edge(0, 1)
#     assert G.adj == {0: {2: {}}, 1: {2: {}}, 2: {0: {}, 1: {}}}
#     with pytest.raises(nx.NetworkXError):
#         G.remove_edge(-1, 0)


@pytest.mark.skip("TODO")
def test_remove_edges_from(self):
    """Test removing edges from the graph."""
    G = self.K3.copy()
    G.remove_edges_from([(0, 1)])
    assert G.adj == {0: {2: {}}, 1: {2: {}}, 2: {0: {}, 1: {}}}
    G.remove_edges_from([(0, 0)])  # silent fail


@pytest.mark.skip("TODO")
def test_clear_orig(self):
    """Test clearing the graph and its attributes."""
    G = self.K3.copy()
    G.graph["name"] = "K3"
    G.clear()
    assert list(G.nodes) == []
    assert G.adj == {}
    assert G.graph == {}


# @pytest.mark.skip("TODO")
def test_removing_node_removes_edge(graphz):
    """Test removing a node also removes its edges."""
    G = graphz
    G.add_edge(1, 2, weight=3)
    assert G.adj == {"1": {"2": {}}, "2": {"1": {}}}
    G.add_edge(0, 1, weight=2)
    assert G.adj == {"0": {"1": {}}, "1": {"2": {}, "0": {}}, "2": {"1": {}}}
    G.remove_node(0)
    time.sleep(1)
    assert G.adj == {"1": {"2": {}}, "2": {"1": {}}}


def test_node_view_assignment_raises_error(graphz):
    """Test that assigning to the node view raises an error."""
    G = graphz
    G.add_node(1, color="red")

    with pytest.raises(TypeError):
        G.nodes[1] = "foo"


@pytest.mark.skip("TODO: node data is still unprotected since it is a regular dict.")
def test_node_view_data_assignment_raises_error(graphz):
    """Test that assigning to the node view raises an error."""
    G = graphz
    G.add_node(1, color="red")

    # fails
    with pytest.raises(TypeError):
        G.nodes["1"]["color"] = "green"

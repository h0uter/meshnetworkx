"""This module contains tests while running in multiple processes."""

import multiprocessing as mp

from test_basic import mnx_graph

import meshnetworkx as mnx


def _start_and_write_graph():
    g = mnx.Graph()

    g.add_node("a", color="red")

    g.close()


def test_subprocess_communication(mnx_graph):
    """Test communication in a subprocess."""
    p = mp.Process(target=_start_and_write_graph)
    p.start()
    p.join()

    assert mnx_graph.has_node("a")
    assert mnx_graph.nodes["a"]["color"] == "red"


def _start_and_add_multiple_nodes():
    g = mnx.Graph()

    g.add_node("a", color="red")
    g.add_node("b", color="blue")
    g.add_node("c", color="green")

    g.close()


def test_subprocess_multiple_nodes(mnx_graph):
    """Test adding multiple nodes in a subprocess."""
    p = mp.Process(target=_start_and_add_multiple_nodes)
    p.start()
    p.join()

    assert mnx_graph.has_node("a")
    assert mnx_graph.has_node("b")
    assert mnx_graph.has_node("c")
    assert mnx_graph.nodes["a"]["color"] == "red"
    assert mnx_graph.nodes["b"]["color"] == "blue"
    assert mnx_graph.nodes["c"]["color"] == "green"


def _start_and_remove_node():
    g = mnx.Graph()

    g.remove_node("a")

    g.close()


def test_subprocess_remove_node(mnx_graph):
    """Test removing a node in a subprocess."""
    mnx_graph.add_node("a", color="red")

    p = mp.Process(target=_start_and_remove_node)
    p.start()
    p.join()

    assert not mnx_graph.has_node("a")

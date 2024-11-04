"""This module contains pytest fixtures for testing meshnetworkx."""

import pytest

import meshnetworkx as mnx


@pytest.fixture
def mnx_graph():
    """Fixture to create and teardown GraphZ instance."""
    # Fixture to create and teardown GraphZ instance
    g = mnx.Graph()

    yield g

    g.clear()
    g.close()

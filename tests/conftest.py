"""This module contains pytest fixtures for testing meshnetworkx."""

import pytest

import meshnetworkx as mx


@pytest.fixture
def mnx_graph():
    """Fixture to create and teardown GraphZ instance."""
    g = mx.GraphZ()

    # This should not be necessary,
    # but just in case a previous test did not cleanup properly
    g.clear()

    yield g

    g.clear()
    g.close()

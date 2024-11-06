"""This module demonstrates a simple NiceGUI application with a mesh network graph."""

import random

from humid import hfid
from nicegui import app, run, ui

import meshnetworkx as mx

ui.label("Hi world")

M = mx.GraphZ()

ui.button("shutdown", on_click=app.shutdown)

ui.button("clear", on_click=M.clear)


def _add_node():
    some_color = random.choice(["red", "blue", "green"])

    M.add_node(hfid(), color=some_color)


ui.button("add Node", on_click=_add_node)


def _add_n_nodes():
    N = 50000
    for _ in range(N):
        _add_node()


ui.button("add N Nodes", on_click=_add_n_nodes)


nr_nodes = ui.label("nr_nodes")
info = ui.label("info")


async def _read_graph():
    def wrap():
        return M.nodes(data=True)

    nodes = await run.io_bound(wrap)
    nr_nodes.set_text(f"Got {len(nodes)} nodes")
    info.set_text(str(nodes))


ui.timer(0.3, _read_graph)


def _cleanup():
    M.clear()
    M.close()


app.on_shutdown(_cleanup)

ui.run()

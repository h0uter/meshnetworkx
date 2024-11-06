"""This module demonstrates a simple NiceGUI application with a mesh network graph."""

from humid import hfid
from nicegui import app, ui

import meshnetworkx as mx

M = mx.GraphZ()

nr_nodes = ui.label("nr_nodes")
info = ui.label("info")


def _add_node(i=1):
    M.add_node(hfid(), pos=(i, i))


def _add_n_nodes():
    N = 50
    for i in range(N):
        _add_node(i)


with ui.row():
    ui.button("shutdown", on_click=app.shutdown, color="negative")
    ui.button("clear", on_click=M.clear)
    ui.button("add Node", on_click=_add_node)
    ui.button("add N Nodes", on_click=_add_n_nodes)


with ui.scene(height=700).classes("w-full") as scene:
    pass


async def _read_graph():
    nodes = M.nodes(data=True)
    nr_nodes.set_text(f"Got {len(nodes)} nodes")
    # info.set_text(str(nodes))
    scene.clear()

    for _, data in nodes:
        x, y = data["pos"]
        scene.sphere().move(x, y, 0).material(color="red")


ui.timer(0.3, _read_graph)


def _cleanup():
    M.clear()
    M.close()


app.on_shutdown(_cleanup)

ui.run()

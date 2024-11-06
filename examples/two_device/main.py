"""This module demonstrates a simple NiceGUI application with a mesh network graph."""

from humid import hfid
from nicegui import app, run, ui

import meshnetworkx as mx

N_NODES = 500
M = mx.GraphZ()


nr_nodes = ui.label("nr_nodes")


def _add_node(i=1):
    M.add_node(hfid(), pos=(i, i))


def _add_n_nodes():
    for i in range(N_NODES):
        _add_node(i)


with ui.row().classes("w-full"):
    ui.button("clear", on_click=M.clear)
    ui.button("add Node", on_click=_add_node)
    ui.button(f"add {N_NODES} Nodes", on_click=_add_n_nodes)
    ui.space()
    ui.button("shutdown", on_click=app.shutdown, color="negative")


with ui.scene(height=700).classes("w-full") as scene:
    pass


async def _read_graph():
    # FIXME: still delay upon clearing graph

    def wrap():
        return M.nodes(data=True)

    # nodes = M.nodes(data=True)
    nodes = await run.io_bound(wrap)
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

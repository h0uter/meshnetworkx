"""This module demonstrates a simple NiceGUI application with a mesh network graph."""

import os
import pickle

from humid import hfid
from nicegui import app, run, ui

import meshnetworkx as mx

N_NODES = 5000
M = mx.GraphZ()

RENDERED_POINTS: dict[tuple[float, float], ui.scene.sphere] = {}

nr_nodes = ui.label("nr_nodes")
MACHINE = os.getenv("MACHINE", "1")

ui.page_title(f"Machine {MACHINE}")

M.subscribe("hello", lambda _: print("hello received"))


def _add_node(i=1):
    NUMBER = 50
    div = i // NUMBER
    remaining = i % NUMBER
    x = div if MACHINE == "1" else -div
    M.add_node(hfid(), pos=(x, remaining))
    if i == 1:
        ui.notify(f"Added node {i}")


def _add_n_nodes():
    for i in range(N_NODES):
        _add_node(i)


def _clear_rendered_points():
    RENDERED_POINTS.clear()
    scene.clear()


def _say_hello():
    M.publish("hello", pickle.dumps("hello"))


with ui.row().classes("w-full"):
    ui.button("say hello", on_click=_say_hello)
    ui.button("clear GraphZ", on_click=M.clear)
    ui.button("add Node", on_click=_add_node)
    ui.button(f"add {N_NODES} Nodes", on_click=_add_n_nodes)
    ui.button("clear rendered points", on_click=_clear_rendered_points)
    ui.space()
    ui.button("shutdown", on_click=app.shutdown, color="negative")


with ui.scene(height=700).classes("w-full") as scene:
    pass


def _draw_pointcloud(nodes):
    points = []
    for _, data in nodes:
        x, y = data["pos"]

        points.append((x, y, 0))
    colors = [(255, 0, 0)] * len(points)
    scene.point_cloud(points, colors)


def _draw(nodes):
    read = set()
    for _, data in nodes:
        x, y = data["pos"]
        read.add((x, y))
    diff = read - RENDERED_POINTS.keys()
    sdiff = sorted(diff)
    # for x, y in read - RENDERED_POINTS.keys():
    for x, y in sdiff:
        color = "red" if MACHINE == "1" else "blue"
        actor = scene.sphere(radius=0.2).move(x, y, 0).material(color=color)
        RENDERED_POINTS[(x, y)] = actor

    for x, y in RENDERED_POINTS.keys() - read:
        actor = RENDERED_POINTS.pop((x, y))
        actor.delete()


async def _read_graph():
    # FIXME: still delay upon clearing graph

    def wrap():
        return M.nodes(data=True)

    # nodes = M.nodes(data=True)
    nodes = await run.io_bound(wrap)
    nr_nodes.set_text(f"Got {len(nodes)} nodes")
    # info.set_text(str(nodes))
    # scene.clear()

    await run.io_bound(_draw, nodes)

    ui.notify("Graph updated")


ui.timer(1, _read_graph)
ui.timer(1, lambda: ui.notify("tick"))


def _cleanup():
    M.clear()
    M.close()


app.on_shutdown(_cleanup)

port = 8080 if MACHINE == "1" else 8081
ui.run(port=port)

"""This module demonstrates a simple NiceGUI application with a mesh network graph."""

import random
import string

from nicegui import app, run, ui

import meshnetworkx as mx

ui.label("Hi world")

M = mx.GraphZ()


ui.button("clear", on_click=M.clear)


def _add_node():
    some_letter = random.choice(string.ascii_letters)
    some_color = random.choice(["red", "blue", "green"])

    M.add_node(some_letter, color=some_color)


ui.button("add Node", on_click=_add_node)

info = ui.label("info")


async def _read_graph():
    def wrap():
        return M.nodes(data=True)

    nodes = await run.io_bound(wrap)
    info.set_text(str(nodes))


ui.timer(0.3, _read_graph)


def _cleanup():
    M.clear()
    M.close()


app.on_shutdown(_cleanup)

ui.run()

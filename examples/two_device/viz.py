"""This module demonstrates a simple NiceGUI application with a mesh network graph."""

import random
import string

from nicegui import ui

import meshnetworkx as mx

ui.label("Hi world")

M = mx.Graph()


ui.button("clear", on_click=M.clear)


def _add_node():
    some_letter = random.choice(string.ascii_letters)
    some_color = random.choice(["red", "blue", "green"])

    M.add_node(some_letter, color=some_color)


ui.button("add Node", on_click=_add_node)

info = ui.label("info")


def _read_graph():
    info.set_text(str(M.nodes(data=True)))


ui.timer(0.1, _read_graph)

ui.run()

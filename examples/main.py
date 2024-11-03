"""A simple example that creates a graph, adds nodes to it, and then clears it."""

import time

from humid import hfid

import meshnetworkx as mnx


def main():
    """Simple example that creates a graph and adds nodes to it, then clears it."""
    print("running nx example!!!")
    print()

    zg = mnx.Graph()
    for _ in range(10):
        zg.add_node(hfid(), color="red")

    time.sleep(1)

    print(f"plotting {zg}")
    print("")
    zg.draw()

    print("clearing graph")
    print("")
    zg.clear()

    time.sleep(1)

    print(f"plotting {zg}")
    print("")
    zg.draw()


if __name__ == "__main__":
    main()

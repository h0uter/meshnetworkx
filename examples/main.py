import time

from humid import hfid

import networkedx as znx


def main():
    """Simple example that creates a graph and adds nodes to it, then clears it."""
    print("running nx example!!!")
    print()

    zg = znx.GraphZ()
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

import pickle
import time
from typing import Any

import matplotlib.pyplot as plt
import networkx as nx
import zenoh
from humid import hfid

PREFIX = "graph"


def totopic(key: str):
    return f"{PREFIX}/{key}"


class GraphZ:
    def __init__(self):
        cfg = zenoh.Config()
        self._z = zenoh.open(cfg)

    @staticmethod
    def from_networkx(g: nx.Graph) -> "GraphZ":
        raise NotImplementedError()
        return GraphZ()

    def to_networkx(self) -> nx.Graph:
        g = nx.Graph()

        for node, data in self.nodes(data=True):
            g.add_node(node, **data)

        return g

    def add_node(self, node: Any, **attr) -> None:
        data_dict = {}
        data_dict.update(attr)
        data_bytes = pickle.dumps(data_dict)
        self._z.put(totopic(node), data_bytes)

    def remove_node(self, node: Any) -> None:
        self._z.delete(totopic(node))

    def nodes(self, data: bool = False) -> list[Any] | list[tuple[Any, Any]]:
        nodes = []
        replies = self._z.get(f"{PREFIX}/**", handler=zenoh.handlers.DefaultHandler())
        for reply in replies:
            reply: zenoh.Reply
            node = str(reply.ok.key_expr).split("/")[-1]
            print(node)
            if data:
                node_data = pickle.loads(reply.ok.payload.to_bytes())
                nodes.append((node, node_data))
            else:
                nodes.append(node)

        return nodes

    def clear(self) -> None:
        for node in self.nodes():
            self.remove_node(node)

    def close(self) -> None:
        self._z.close()


def main():
    print("running nx example!!!")
    print()

    zg = GraphZ()
    for _ in range(10):
        zg.add_node(hfid(), color="red")

    time.sleep(1)
    gg = zg.to_networkx()

    print(f"plotting {gg}")
    nx.draw(gg)
    plt.show()

    zg.clear()
    print("cleared graph")
    time.sleep(1)

    gg = zg.to_networkx()
    nx.draw(gg)
    plt.show()


if __name__ == "__main__":
    main()

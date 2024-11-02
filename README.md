# networkedx

## Quickstart

- run  `zenohd -c .zenoh_docker/zenoh-myhome.json5` to create a storage
- or `docker compose up zenoh-host` to create a storage.

then run the following `pip install -e .` to install the package.

Then run an example with `python examples/main.py`

## Why?

- If you model your application domain as a graph, this package makes it easy to run on multiple devices and automatically sync the graph between them.
- It is an abstraction on top of the Zenoh protocol, which is a very efficient protocol for IoT applications.
- It is a drop-in replacement for networkx, so you can use all the networkx methods on the graph.

## How?

- The graph is stored in a zenoh storage, which is a key-value store.
- The nodes and edges are stored as keys in the zenoh storage.
- The graph is synced between devices using zenoh Storages.

## Example

```python
import networkedx as znx

G = znx.Graph()
G.add_node(1, data="data")
G.add_edge(1, 2, data="data")
print(G.nodes(data=True))
>>> [(1, {'data': 'data'}), (2, {})]

```

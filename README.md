<a name="readme-top"></a>
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

<!-- PROJECT LOGO -->

<br />
<div align="center">
    <div align="center">
    <img src="./docs/assets/logo_no_bg.png" alt="alt text" width="250" height="whatever">
    </div>
  <h3 align="center">MeshNetworkX</h3>

  <p align="center">
    Networkx Graphs synced across devices using Zenoh.
    <br />
    <!-- <a href="https://h0uter.github.io/humid"><strong>Explore the docs »</strong></a> -->
    <br />
    <br />
    <a href="https://github.com/h0uter/meshnetworkx/issues/new?labels=bug&title=New+bug+report">Report Bug</a>
    ·
    <a href="https://github.com/h0uter/meshnetworkx/issues/new?labels=enhancement&title=New+feature+request">Request Feature</a>
  </p>
</div>

## Quickstart

- run  `zenohd -c .zenoh_docker/zenoh-myhome.json5` to create a storage
- or `docker compose up zenoh-host` to create a storage.

then run the following `pip install -e ".[examples]"` to install the package.

Then run an example with `python examples/main.py`

## Why?

- If you model your application domain as a graph, this package makes it easy to run on multiple devices and automatically sync the graph between them.
- It is a drop-in replacement for networkx, so you can use all the networkx methods on the graph.

## How?

- It is an abstraction on top of the Zenoh protocol, which is a very efficient protocol for IoT applications.
- The graph is stored in a zenoh storage, which is a key-value store.
- The nodes and edges are stored as keys in the zenoh storage.
- The graph is synced between devices using zenoh Storages. This protocol automagically orchestrates allignment between storages, even if the network becomes partitioned and then later reconnects.

## Example

Assuming:

- you have two devices, and you want to create a graph on one device and access it on the other device.
- you have a zenoh storage running on both devices.
- Both devices can find each other using zenoh discovery (local network or using a Zenoh Router).

On device one:

```python
import meshnetworkx as mnx

G = znx.Graph()
G.add_node(1, color="red")
G.add_edge(1, 2, color="pink")

```

After that on device two:

```python
import meshnetworkx as mnx

G = znx.Graph()
print(G.nodes(data=True))
>>> [(1, {'color': 'red'}), (2, {})]

print(G.edges(data=True))
>>> [(1, 2, {'color': 'pink'})]
```

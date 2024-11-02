<a name="readme-top"></a>
[![text](https://img.shields.io/pypi/v/humid?logo=python&logoColor=%23cccccc)](https://pypi.org/project/humid/)
[![Downloads](https://static.pepy.tech/badge/humid)](https://pepy.tech/project/humid)
![tests](https://github.com/h0uter/humid/workflows/Test/badge.svg)
[![PDM](https://camo.githubusercontent.com/2f56a2dc4c9b19beec5347774a078871a81e00d624a51fe9cc20a8ae8ac4e957/68747470733a2f2f696d672e736869656c64732e696f2f656e64706f696e743f75726c3d687474707325334125324625324663646e2e6a7364656c6976722e6e6574253246676825324670646d2d70726f6a6563742532462e67697468756225324662616467652e6a736f6e)](https://pdm-project.org/en/latest/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

<!-- PROJECT LOGO -->

<br />
<div align="center">
    <div align="center">
    <!-- <img src=".readme/the logo.png" alt="alt text" width="250" height="whatever"> -->
    <img src="./.readme/zenoh-nx.png" alt="alt text" width="250" height="whatever">
    </div>
  <!-- <h3 align="center">humid</h3> -->

  <p align="center">
    Networkx Graphs synced across devices using Zenoh.
    <br />
    <!-- <a href="https://h0uter.github.io/humid"><strong>Explore the docs »</strong></a> -->
    <br />
    <br />
    <a href="https://github.com/h0uter/networkedx/issues/new?labels=bug&title=New+bug+report">Report Bug</a>
    ·
    <a href="https://github.com/h0uter/networkedx/issues/new?labels=enhancement&title=New+feature+request">Request Feature</a>
  </p>
</div>

<!-- # networkedx -->

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
- The graph is synced between devices using zenoh Storages. This protocol automagically orchestrates allignment between storages, even if the network becomes partitioned and then later reconnects.

## Example

Assuming:

- you have two devices, and you want to create a graph on one device and access it on the other device.
- you have a zenoh storage running on both devices.
- Both devices can find each other using zenoh discovery (local network or using a Zenoh Router).

On device one:

```python
import networkedx as znx

G = znx.Graph()
G.add_node(1, data="data")
G.add_edge(1, 2, data="data")

```

After that on device two:

```python
import networkedx as znx

G = znx.Graph()
print(G.nodes(data=True))
>>> [(1, {'data': 'data'}), (2, {})]

print(G.edges(data=True))
>>> [(1, 2, {'data': 'data'})]
```

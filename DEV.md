# Development notes

## TODO

- [x] how to encode edges as keyexpr?
  - "from/to/edge_id" for a directed multi graph

- check this for basic graph interface: <https://github.com/networkx/networkx/blob/main/networkx/classes/graph.py>
- [x] how to get the G.nodes[1] and G.nodes(data=True) to work at the same time?

## use allignment

<https://zenoh.io/blog/2022-11-29-zenoh-alignment/>

## requirements

- need to be able to handle high level methods
  - [ ] make inventory of methods.
- need to be able to quickly search the graph
  - for nodes
  - for edges

## differences with networkx

- nodes and edges cannot be any object, they have to be convertable to string.

## name ideas

- nx-zenoh
- znetworkx
- zenoh-nx
- zenoh-networkx
- zgraph

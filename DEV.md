# Development notes

## TODO

- [x] how to encode edges as keyexpr?
  - "from/to/edge_id" for a directed multi graph
- [ ] check this for basic graph interface: <https://github.com/networkx/networkx/blob/main/networkx/classes/graph.py>
- [x] how to get the G.nodes[1] and G.nodes(data=True) to work at the same time?
- [x] rename the package to `meshnetworkx`
- [ ] finish implementing edges
- [ ] setup performance test using online broker and vizualisation.
  - [ ] create two line graphs and see how fast they sync.  


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
- **znetworkx** <- this is the best one
- zenoh-nx
- zenoh-networkx
- zgraph
- networkz
- zenohx
- zenoh-graph
- zenoh-graphx

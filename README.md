# networkedx

- run  `zenohd -c .zenoh_docker/zenoh-myhome.json5` to create a storage
- or `docker compose up zenoh-host` to create a storage.

## TODO

- how to encode edges as keyexpr?
  - "from/to/edge_id" for a directed multi graph

- check this for basic graph interface: https://github.com/networkx/networkx/blob/main/networkx/classes/graph.py

## use allignment

https://zenoh.io/blog/2022-11-29-zenoh-alignment/

## requirements

- need to be able to handle high level methods 
  - [ ] make inventory of methods.
- need to be able to quickly search the graph
  - for nodes
  - for edges
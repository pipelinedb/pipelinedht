# PipelineDHT
A simple distributed hash table

### Overview

In this project you'll be implementing a distributed hash table in Python (or the language of your choice). The 
hash table will be spread across  multiple processes, and will expose all of its public functionality via an HTTP 
API. Processes can communicate with each other using a protocol of your choosing. The hash table's keyspace will be
partitioned evenly across all nodes (processes), but any node can process a request for any key (although it may
have to re-route the request).

### Resources

* [Distributed hash tables](http://en.wikipedia.org/wiki/Distributed_hash_table) - Don't worry if this overview of distributed hash tables seems a little dense. It's there if you need it, but this project will keep things pretty simple.
* [Consistent hashing](https://en.wikipedia.org/wiki/Consistent_hashing) - A hashing scheme that tries to minimize the cost of rebalancing a resizable hash table.
* [Flask](http://flask.pocoo.org/docs/0.10) - Each process in the distributed hash table will run a Flask HTTP server, so you'll need to install Flask if you don't already have it. You can ignore this if you plan on implementing the DHT in a different language.

### Functionality

The distributed hash table will expose all of its public functionality via HTTP. This includes the standard hash table `get`, `put`, and `delete` calls, as well as two operational functions: `join` and `leave`. For the sake of testing two other calls, `db` and `peers`, are also supported.

#### get / put / delete / db

Functionally, `get`, `put`, and `delete` are identical to the analagous calls on a regular hash table. However, for
the purposes of our distributed hash table, each of these calls will need to operate on the process that is
currently responsible for the given key. That is, a node receiving a `get`, `put`, or `delete` request may need to
re-route the request to the node that actually contains the key in question. For example, if a DHT process is
running at `localhost:9876`, you could use these calls as:

    # curl -X PUT http://localhost:9876/db/key -d "value"
    # curl -X GET http://localhost:9876/db/key
    value
    # curl -X DELETE http://localhost:9876/db/key
    # curl -X GET http://localhost:9876/db/key

`db` should only return the list of keys that the DHT process being queries is responsible for, *not* all the keys
in the DHT.

    # curl -X PUT http://localhost:9876/db/key1 -d "value1"
    # curl -X PUT http://localhost:9876/db/key2 -d "value2"
    # curl -X GET http://localhost:9876/db
    # key1
    # key2

#### join / leave / peers

`join` and `leave` will add and remove a node to the distributed hash table, respectively. `join` takes a list of
peers to join to, and `leave` should remove itself from the list of peers stored by each node currently running in
the distributed hash table. These calls will involve rebalancing the DHT's data so that it is evenly distributed
across all nodes after one has been added or removed.

For the sake of simplicity, concurrent requests to `join` or `leave` will never be made on the DHT. Furthermore, no
`put`, `get` or `delete` requests will be made while a `join` or `leave` request is in progress. If two independent
DHT processes are running at `localhost:9876` and `localhost:9876`, you could do:

    # curl -X GET http://localhost:9876/dht/peers
    peer1
    # curl -X GET http://localhost:9877/dht/peers
    peer2
    # curl -X POST http://localhost:9876/dht/join -d "peer2:localhost:9877"
    # curl -X GET http://localhost:9876/dht/peers
    peer1
    peer2
    # curl -X GET http://localhost:9877/dht/peers
    peer2
    peer1
    # curl -X GET http://localhost:9877/dht/leave
    # curl -X GET http://localhost:9876/dht/peers
    peer1
    # curl -X GET http://localhost:9877/dht/peers
    peer2

### Skeleton

This repository contains a skeleton for the distributed hash table implementation to use as a starting point:

* [server.py](https://github.com/pipelinedb/pipelinedht/blob/master/dht/server.py) - Public [RESTful interface](http://en.wikipedia.org/wiki/Representational_state_transfer) documented above that is exposed by each DHT process.
* [runserver.py](https://github.com/pipelinedb/pipelinedht/blob/master/runserver.py) - Script to run a DHT process with its HTTP server on a given host and port.
* [tests](https://github.com/pipelinedb/pipelinedht/tree/master/tests) - Test harness to verify your [server](https://github.com/pipelinedb/pipelinedht/blob/master/dht/server.py) implementation. The [runtests.py](https://github.com/pipelinedb/pipelinedht/blob/master/runtests.py) script can be used to run all the tests.
* [DHTNode](https://github.com/pipelinedb/pipelinedht/blob/master/tests/__init__.py#L14) - An object wrapper around managing a DHT process and making requests to it, which probably is easier to use than cURL.

### Notes

It's fine if you don't fully implement the given interface in the time you've been allotted. More importantly, you
should focus on fully implemeting as many functions as possible. That is, half of the functions fully implemented
is better than all of the functions half implemented. **And most importantly of all, have fun!**

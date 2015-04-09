# PipelineDHT
A simple distributed hash table

### Overview

In this project you'll be implementing a distributed hash table in Python. The hashtable will be spread across
multiple processes, and will expose all of its public functionality via an HTTP API. Processes can communicate with
each other using a protocol of your choosing. The hashtable's keyspace will be partitioned evenly across all nodes (processes), although any
node can process a request for any key (although it may have to re-route the request).

### Resources

* [Distributed hashtables](http://en.wikipedia.org/wiki/Distributed_hash_table) - Don't worry if this overview of distributed hashtables seems a little dense. It's there if you need it, but this project will keep things pretty simple.
* [Flask](http://flask.pocoo.org/docs/0.10) - Each process in the distributed hashtable will run a Flask HTTP server, so you'll need to install Flask if you don't already have it.

### Functionality

The distributed hashtable will expose all of its public functionality via HTTP. This includes the standard hashtable `get`, `put`, and `delete` calls, as well as two operational functions: `join` and `leave`. For example, if a process is running at `localhost:9876`, you could use `curl` to use the distributed hashtable.

    # curl --data 'value' http://localhost:9876/db/put/key
    # curl http://localhost:9876/db/get/key
    value
    
#### get / put / delete

Functionally, `get`, `put`, and `delete` are identical to the analagous calls on a regular hashtable. However, for the purposes of our distributed hashtable, each of these calls will need to operate on the process that is currently responsible for the given key. That is, a node receiving a `get`, `put`, or `delete` request may need to re-route the request to the node that actuall contains the key in question.

#### join / leave

`join` and `leave` will add and remove a node to the distributed hashtable, respectively. `join` takes a list of peers to join to, and `leave` should remove itself from the list of peers stored by each node currently running in the distributed hashtable.

### Skeleton

This repository contains a skeleton for the distributed hashtable implementation to use as a starting point:

* [server](https://github.com/pipelinedb/pipelinedht/blob/master/dht/server.py) - Public HTTP interface that will be exposed by each DHT process.
* [runserver](https://github.com/pipelinedb/pipelinedht/blob/master/runserver.py) - Script to run a DHT process with its HTTP server on a given host and port.
* [tests](https://github.com/pipelinedb/pipelinedht/tree/master/tests) - Test harness to verify your [server](https://github.com/pipelinedb/pipelinedht/blob/master/dht/server.py) implementation. 

### Notes

It's fine if you don't fully implement the given interface in the time you've been allotted. More importantly, you should focus on fully implemeting as many functions as possible. That is, half of the functions fully implemented is better than all of the functions half implemented. **And most importantly of all, have fun!**

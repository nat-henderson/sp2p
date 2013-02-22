SP2P, the simple peer-to-peer network, is trying to be the simplest possible implementation of a p2p network.

As such, it's not a purely p2p network; it's got 'privileged clients' which are in charge of knowing things like where stuff is.

The goal is for the job of these privileged clients to eventually be distributed, but that's not in v1.

v1 features:

privileged client:
    runs a database with three tables, Users, Files, and Owners.
    answers queries on /search/<query> with a list of places to find that stuff and hashes.
    accepts connections on /signin/username/secret and registers the user.
    accepts connections to /register/filename/hash and registers the owner.
    written in python using SQLAlchemy and Flask

client:
    accepts connections on some port, and a file path, and writes that file to the wire.
    sends requests to its favorite privileged client (specified on login) for some filename.
    displays results to the user
    allows the user to select a connection to make.
    written in Java

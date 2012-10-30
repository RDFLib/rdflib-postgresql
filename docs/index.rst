.. _rdflib_postgresql.PostgreSQL: RDFLib, stores, PostgreSQL.

|today|

=============================================================
PostgreSQL :: a formula-aware Store based on AbstractSQLStore
=============================================================

PostgreSQL store formula-aware implementation. It stores its triples in the
following partitions (per AbstractSQLStore):

* Asserted non rdf:type statements
* Asserted rdf:type statements (in a table which models Class membership). The motivation for this partition is primarily query speed and scalability as most graphs will always have more rdf:type statements than others
* All Quoted statements

In addition it persists namespace mappings in a separate table

Example
========
.. code-block:: python

    from rdflib import plugin, Graph, URIRef
    from rdflib.store import Store, VALID_STORE, NO_STORE

    # Set database DSN, follow the format below, see psycopg2
    # documentation for details ...
    # http://initd.org/psycopg/docs/module.html#psycopg2.connect
    dsn = "user=gjh password=50uthf0rk host=localhost dbname=test"

    # Set a store identifier, can also be a URI, if preferred.
    store_id = "my_rdf_store_12"

    # Set a default graph uri as an identifier for the Graph
    graph_uri = "http://bel-epa.com/data"

    # Set up the PostgreSQL plugin. You may have to install the python
    # psycopg2 library
    store = plugin.get('PostgreSQL', Store)(identifier=store_id)

    # Open a previously created store or create it if it doesn't yet exist.
    rt = store.open(dsn)
    if rt == NO_STORE:
        # There is no underlying PostgreSQL infrastructure, create it
        store.open(dsn, create=True)
    else:
        assert rt == VALID_STORE, "There underlying store is corrupted"

    # Create a Graph
    g = Graph(store, identifier=URIRef(graph_uri))

    # And now ...    
    # g
    # <Graph identifier=http://bel-epa.com/data (<class 'rdflib.graph.Graph'>)>

    # g.store
    # <Parititioned PostgreSQL N3 Store>


Module API
++++++++++

.. currentmodule:: rdflib_postgresql.PostgreSQL

:mod:`rdflib_postgresql.PostgreSQL`
----------------------------------------
.. automodule:: rdflib_postgresql.PostgreSQL
.. autoclass:: PostgreSQL
   :members:
.. autofunction:: ParseConfigurationString
.. autofunction:: GetConfigurationString
.. autofunction:: unionSELECT


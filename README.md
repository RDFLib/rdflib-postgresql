PostgreSQL :: a formula-aware RDFLib Store based on AbstractSQLStore

PostgreSQL RDFLib Store, formula-aware implementation. It stores its
triples in the following partitions (per AbstractSQLStore):

* Asserted non rdf:type statements
* Asserted rdf:type statements (in a table which models Class membership).
  The motivation for this partition is primarily query speed and scalability
  as most graphs will always have more rdf:type statements than others
* All Quoted statements

In addition it persists namespace mappings in a separate table

Requires RDFLib 3.

Install with:

    $ pip install rdflib_sparqlstore

Basic usage:

    >>> from rdflib import Graph, URIRef
    >>> configString = "user=postgresql dbname=rdflibpostgresql_test"
    >>> g = Graph('PostgreSQL', identifier=URIRef("http://example.com/g43"))
    >>> g.open(configString, create=True)
    1
    >>> print(g)
    <http://example.com/g43> a rdfg:Graph;rdflib:storage 
                        [a rdflib:Store;rdfs:label 'PostgreSQL'].
    >>> print(g.store)
    <Parititioned PostgreSQL N3 Store>
    >>> print(g.identifier)
    http://example.com/g43
    >>> g.close()
    >>> 

[![Build Status](https://travis-ci.org/gjhiggins/rdflib-postgresql.png?branch=master)](https://travis-ci.org/gjhiggins/rdflib-postgresql)

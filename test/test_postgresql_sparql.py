import unittest
import os
from nose.exc import SkipTest
from rdflib import Namespace, plugin, URIRef
from rdflib.store import Store, NO_STORE, VALID_STORE
from rdflib.graph import Graph


default_graph_uri = "http://example.com/"

configString = os.environ.get(
  'DBURI',
  'postgresql+psycopg2://postgres@localhost/rdflibpostgresql_test')

pgstore = plugin.get('PostgreSQL', Store)(identifier="rdflibtest")
graph = Graph(store=pgstore,
              identifier=URIRef(default_graph_uri))
rt = graph.open(configString, create=False)
if rt == NO_STORE:
    graph.open(configString, create=True)
else:
    assert rt == VALID_STORE, "The underlying store is corrupt"
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
graph.bind("dc", "http://http://purl.org/dc/elements/1.1/")
graph.bind("foaf", str(FOAF))
datasize = '5ktriples'
datafile = os.path.join(
    os.path.dirname(__file__), 'sp2b/' + datasize + '.n3')
graph.parse(location=datafile, format="n3")


def tearDown(self):
    self.graph.destroy(configString)
    try:
        self.graph.close()
    except:
        pass


class TestPostgreSQLSPARQL(unittest.TestCase):
    graph = graph
    performancetest = True

    def test_sparql_q01(self):
        qs = """\
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX bench:   <http://localhost/vocabulary/bench/>
        PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>

        SELECT ?yr
        WHERE {
          ?journal rdf:type bench:Journal .
          ?journal dc:title "Journal 1 (1940)"^^xsd:string .
          ?journal dcterms:issued ?yr
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q02(self):
        qs = """\
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX swrc:    <http://swrc.ontoware.org/ontology#>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX bench:   <http://localhost/vocabulary/bench/>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>

        SELECT ?inproc ?author ?booktitle ?title
               ?proc ?ee ?page ?url ?yr ?abstract
        WHERE {
          ?inproc rdf:type bench:Inproceedings .
          ?inproc dc:creator ?author .
          ?inproc bench:booktitle ?booktitle .
          ?inproc dc:title ?title .
          ?inproc dcterms:partOf ?proc .
          ?inproc rdfs:seeAlso ?ee .
          ?inproc swrc:pages ?page .
          ?inproc foaf:homepage ?url .
          ?inproc dcterms:issued ?yr
          OPTIONAL {
            ?inproc bench:abstract ?abstract
          }
        }
        ORDER BY ?yr
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q03a(self):
        raise SkipTest("q03a fails")
        qs = """\
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX swrc:  <http://swrc.ontoware.org/ontology#>

        SELECT ?article
        WHERE {
          ?article rdf:type bench:Article .
          ?article ?property ?value
          FILTER (?property=swrc:pages)
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q03b(self):
        raise SkipTest("q03b fails")
        qs = """\
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX swrc:  <http://swrc.ontoware.org/ontology#>

        SELECT ?article
        WHERE {
          ?article rdf:type bench:Article .
          ?article ?property ?value
          FILTER (?property=swrc:month)
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q03c(self):
        raise SkipTest("q03c fails")
        qs = """\
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX swrc:  <http://swrc.ontoware.org/ontology#>
        PREFIX bench: <http://localhost/vocabulary/bench/>

        SELECT ?article
        WHERE {
          ?article rdf:type bench:Article .
          ?article ?property ?value
          FILTER (?property=swrc:isbn)
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q04(self):
        raise SkipTest("q04 interminable")
        qs = """\
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX bench:   <http://localhost/vocabulary/bench/>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX swrc:    <http://swrc.ontoware.org/ontology#>

        SELECT DISTINCT ?name1 ?name2
        WHERE {
          ?article1 rdf:type bench:Article .
          ?article2 rdf:type bench:Article .
          ?article1 dc:creator ?author1 .
          ?author1 foaf:name ?name1 .
          ?article2 dc:creator ?author2 .
          ?author2 foaf:name ?name2 .
          ?article1 swrc:journal ?journal .
          ?article2 swrc:journal ?journal
          FILTER (?name1<?name2)
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q05a(self):
        raise SkipTest("q05a interminable")
        qs = """\
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX dc:    <http://purl.org/dc/elements/1.1/>

        SELECT DISTINCT ?person ?name
        WHERE {
          ?article rdf:type bench:Article .
          ?article dc:creator ?person .
          ?inproc rdf:type bench:Inproceedings .
          ?inproc dc:creator ?person2 .
          ?person foaf:name ?name .
          ?person2 foaf:name ?name2
          FILTER (?name=?name2)
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q05b(self):
        qs = """\
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX dc:    <http://purl.org/dc/elements/1.1/>

        SELECT DISTINCT ?person ?name
        WHERE {
          ?article rdf:type bench:Article .
          ?article dc:creator ?person .
          ?inproc rdf:type bench:Inproceedings .
          ?inproc dc:creator ?person .
          ?person foaf:name ?name
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q06(self):
        raise SkipTest("q06 interminable")
        qs = """\
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>

        SELECT ?yr ?name ?document
        WHERE {
          ?class rdfs:subClassOf foaf:Document .
          ?document rdf:type ?class .
          ?document dcterms:issued ?yr .
          ?document dc:creator ?author .
          ?author foaf:name ?name
          OPTIONAL {
            ?class2 rdfs:subClassOf foaf:Document .
            ?document2 rdf:type ?class2 .
            ?document2 dcterms:issued ?yr2 .
            ?document2 dc:creator ?author2
            FILTER (?author=?author2 && ?yr2<?yr)
          } FILTER (!bound(?author2))
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q07(self):
        raise SkipTest("q07 interminable")
        qs = """\
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?title
        WHERE {
          ?class rdfs:subClassOf foaf:Document .
          ?doc rdf:type ?class .
          ?doc dc:title ?title .
          ?bag2 ?member2 ?doc .
          ?doc2 dcterms:references ?bag2
          OPTIONAL {
            ?class3 rdfs:subClassOf foaf:Document .
            ?doc3 rdf:type ?class3 .
            ?doc3 dcterms:references ?bag3 .
            ?bag3 ?member3 ?doc
            OPTIONAL {
              ?class4 rdfs:subClassOf foaf:Document .
              ?doc4 rdf:type ?class4 .
              ?doc4 dcterms:references ?bag4 .
              ?bag4 ?member4 ?doc3
            } FILTER (!bound(?doc4))
          } FILTER (!bound(?doc3))
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q08(self):
        raise SkipTest("q08 interminable")
        qs = """\
        PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc:   <http://purl.org/dc/elements/1.1/>

        SELECT DISTINCT ?name
        WHERE {
          ?erdoes rdf:type foaf:Person .
          ?erdoes foaf:name "Paul Erdoes"^^xsd:string .
          {
            ?document dc:creator ?erdoes .
            ?document dc:creator ?author .
            ?document2 dc:creator ?author .
            ?document2 dc:creator ?author2 .
            ?author2 foaf:name ?name
            FILTER (?author!=?erdoes &&
                    ?document2!=?document &&
                    ?author2!=?erdoes &&
                    ?author2!=?author)
          } UNION {
            ?document dc:creator ?erdoes.
            ?document dc:creator ?author.
            ?author foaf:name ?name
            FILTER (?author!=?erdoes)
          }
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q09(self):
        qs = """\
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT DISTINCT ?predicate
        WHERE {
          {
            ?person rdf:type foaf:Person .
            ?subject ?predicate ?person
          } UNION {
            ?person rdf:type foaf:Person .
            ?person ?predicate ?object
          }
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q10(self):
        qs = """\
        PREFIX person: <http://localhost/persons/>

        SELECT ?subject ?predicate
        WHERE {
          ?subject ?predicate person:Paul_Erdoes
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q11(self):
        qs = """\
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?ee
        WHERE {
          ?publication rdfs:seeAlso ?ee
        }
        ORDER BY ?ee
        LIMIT 10
        OFFSET 50
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q12a(self):
        qs = """\
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX dc:    <http://purl.org/dc/elements/1.1/>

        ASK {
          ?article rdf:type bench:Article .
          ?article dc:creator ?person1 .
          ?inproc  rdf:type bench:Inproceedings .
          ?inproc  dc:creator ?person2 .
          ?person1 foaf:name ?name1 .
          ?person2 foaf:name ?name2
          FILTER (?name1=?name2)
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q12b(self):
        raise SkipTest("q12b interminable")
        qs = """\
        PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc:   <http://purl.org/dc/elements/1.1/>

        ASK {
          ?erdoes rdf:type foaf:Person .
          ?erdoes foaf:name "Paul Erdoes"^^xsd:string .
          {
            ?document dc:creator ?erdoes .
            ?document dc:creator ?author .
            ?document2 dc:creator ?author .
            ?document2 dc:creator ?author2 .
            ?author2 foaf:name ?name
            FILTER (?author!=?erdoes &&
                    ?document2!=?document &&
                    ?author2!=?erdoes &&
                    ?author2!=?author)
          } UNION {
            ?document dc:creator ?erdoes .
            ?document dc:creator ?author .
            ?author foaf:name ?name
            FILTER (?author!=?erdoes)
          }
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

    def test_sparql_q12c(self):
        qs = """\
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX person: <http://localhost/persons/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        ASK {
          person:John_Q_Public rdf:type foaf:Person.
        }
        """
        res = self.graph.query(qs)
        assert len(list(res)) is not 0

if __name__ == '__main__':
    unittest.main()

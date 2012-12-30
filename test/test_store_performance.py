import unittest
import gc
import os
import itertools
from time import time
from random import random
from rdflib import Graph
from rdflib import URIRef


def random_uri():
    return URIRef("%s" % random())


class StoreTestCase(unittest.TestCase):
    """
    Test case for testing store performance... probably should be
    something other than a unit test... but for now we'll add it as a
    unit test.
    """
    store = 'IOMemory'
    path = None
    storetest = True
    performancetest = True

    def setUp(self):
        self.gcold = gc.isenabled()
        gc.collect()
        gc.disable()

        self.graph = Graph(store=self.store)
        from test_postgresql import configString
        from rdflib_postgresql.PostgreSQL import PostgreSQL
        path = configString
        PostgreSQL().destroy(path)
        self.path = path
        self.graph.open(self.path, create=True)
        self.input = Graph()

    def tearDown(self):
        self.graph.close()
        if self.gcold:
            gc.enable()
        # TODO: delete a_tmp_dir
        self.graph.close()

    def testTime(self):
        # number = 1
        print('"%s": [' % self.store)
        for i in ['500triples', '1ktriples', '2ktriples',
                  '3ktriples', '5ktriples', '10ktriples',
                  '25ktriples']:
            inputloc = os.getcwd() + '/test/sp2b/%s.n3' % i
            res = self._testInput(inputloc)
            print("%s," % res.strip())
        print("],")

    def _testInput(self, inputloc):
        number = 1
        store = self.graph
        self.input.parse(location=inputloc, format="n3")

        def add_from_input():
            for t in self.input:
                store.add(t)
        it = itertools.repeat(None, number)
        t0 = time()
        for _i in it:
            add_from_input()
        t1 = time()
        return "%.3g " % (t1 - t0)


class PostgreSQLStoreTestCase(StoreTestCase):
    store = "PostgreSQL"

    def setUp(self):
        self.store = "PostgreSQL"
        self.path = \
            "user=postgresql dbname=rdflibpostgresql_test"
        StoreTestCase.setUp(self)

if __name__ == '__main__':
    unittest.main()

from nose import SkipTest
import unittest
import test_graph
import test_context
from test_n3_2 import testN3Store
from rdflib.graph import Graph

configString="user=gjh,password=50uthf0rk,host=localhost,db=test"

class PostgreSQLGraphTestCase(test_graph.GraphTestCase):
    store_name = "PostgreSQL"
    storetest = True
    path = configString
    create = True

    def testStatementNode(self):
        raise SkipTest("RDF Statements not supported in AbstractSQLStore")

class PostgreSQLContextTestCase(test_context.ContextTestCase):
    store_name = "PostgreSQL"
    storetest = True
    path = configString
    create = True

    def testLenInMultipleContexts(self):
        raise SkipTest("Known issue.")

    def testConjunction(self):
        raise SkipTest("Known issue.")

class PostgreSQLStoreTests(unittest.TestCase):
    storetest = True
    store_name = "PostgreSQL"
    path = configString
    create = True

    def setUp(self):
        self.graph = Graph(store=self.store_name)
        self.graph.open(self.path, create=self.create)

    def tearDown(self):
        self.graph.destroy(self.path)
        self.graph.close()
        import os
        if hasattr(self,'path') and self.path is not None:
            if os.path.exists(self.path):
                if os.path.isdir(self.path):
                    for f in os.listdir(self.path): os.unlink(self.path+'/'+f)
                    os.rmdir(self.path)
                elif len(self.path.split(':')) == 1:
                    os.unlink(self.path)
                else:
                    os.remove(self.path)

    def test_PostgreSQL_testN3_store(self):
        testN3Store('PostgreSQL',configString)

if __name__ == '__main__':
    unittest.main()

# To enable profiling data, use nose's built-in hookup with hotshot:
# nosetests --with-profile --profile-stats-file stats.pf test/test_postgresql
# Also see Tarek Ziade's gprof2dot explorations:
# http://tarekziade.wordpress.com/2008/08/25/visual-profiling-with-nose-and-gprof2dot/

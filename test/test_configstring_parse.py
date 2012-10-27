import unittest
from rdflib_postgresql.PostgreSQL import ParseConfigurationString
from rdflib_postgresql.PostgreSQL import GetConfigurationString


class PostgreSQLStoreConfigTests(unittest.TestCase):
    storetest = True
    store_name = "PostgreSQL"
    create = True
    configString = \
        "user=dog59 password=secret host=localhost port=5432 dbname=test"

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_PostgreSQL_getconfig(self):
        dsn = "port=5432 host=localhost password=secret user=dog59 dbname=test"
        res = GetConfigurationString(self.configString)
        assert set(res.split()) == set(dsn.split())

    def test_PostgreSQL_parseconfig(self):
        kvDict = dict(
            user="dog59", password="secret",
            host="localhost", port=5432, dbname="test")
        res = ParseConfigurationString(self.configString)
        assert res == kvDict, repr(res)


if __name__ == '__main__':
    unittest.main()

# To enable profiling data, use nose's built-in hookup with hotshot:
# nosetests --with-profile --profile-stats-file stats.pf test/test_postgresql
# Also see Tarek Ziade's gprof2dot explorations:
# http://tarekziade.wordpress.com/2008/08/25/visual-profiling-with-nose-and-gprof2dot/

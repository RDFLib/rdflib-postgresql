from setuptools import setup

setup(
    name = 'rdflib-postgresql',
    version = '0.1',
    description = "rdflib extension adding PostgreSQL as back-end store",
    author = "Graham Higgins",
    author_email = "gjhiggins@gmail.com",
    url = "http://github.com/RDFLib/rdflib-postgresql",
    py_modules = ["rdflib_postgresql"],
    test_suite = "test",
    install_requires = ["rdflib>=3.0", "rdfextras>=0.1", "psycopg2"],
    entry_points = {
    	'rdf.plugins.store': [
            'SQLite = rdfextras.store.PostgreSQL:PostgreSQL',
        ],
    }

)

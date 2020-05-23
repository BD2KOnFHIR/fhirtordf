
import unittest

from rdflib import URIRef

from fhirtordf.rdfsupport.namespaces import SCT


class Issue12TestCase(unittest.TestCase):
    def test_sct_namespace(self):
        self.assertEqual(URIRef("http://snomed.info/id/177460008"), SCT.C177460008)
        self.assertEqual(URIRef("http://snomed.info/id/177460008"), SCT[177460008])


if __name__ == '__main__':
    unittest.main()

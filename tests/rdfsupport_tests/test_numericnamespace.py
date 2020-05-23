
import unittest

from rdflib import URIRef


class NumericNamespaceTestCase(unittest.TestCase):
    def eval(self, item: URIRef, val: str):
        self.assertTrue(isinstance(item, URIRef))
        self.assertEqual(val, str(item))

    def test(self):
        from fhirtordf.rdfsupport.numericnamespace import NumericNamespace
        SCT = NumericNamespace("http://snomed.info/id/")
        self.eval(SCT.C74400008, "http://snomed.info/id/74400008")

    def test_comparisons(self):
        from fhirtordf.rdfsupport.numericnamespace import NumericNamespace
        SCT = NumericNamespace("http://snomed.info/id/")
        self.assertEqual(SCT.C74400008, SCT.C74400008)
        self.assertNotEqual(SCT.C74400008, SCT.C74400009)
        self.assertEqual(SCT.C74400008, URIRef("http://snomed.info/id/74400008"))
        self.assertEqual(URIRef("http://snomed.info/id/74400008"), SCT.C74400008)
        self.assertTrue(SCT.C74400008 in {SCT.C12345, URIRef("http://snomed.info/id/74400008")})
        self.assertTrue(SCT.C74400008 in {SCT.C12345, SCT.C74400008})


if __name__ == '__main__':
    unittest.main()

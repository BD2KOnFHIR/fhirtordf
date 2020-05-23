
import unittest

from rdflib import URIRef


class DottedNamespaceTestCase(unittest.TestCase):
    def eval(self, item: URIRef, val: str):
        self.assertTrue(isinstance(item, URIRef))
        self.assertEqual(val, str(item))

    def test(self):
        from fhirtordf.rdfsupport.dottednamespace import DottedNamespace
        fhir = DottedNamespace("http://hl7.org/fhir/")
        self.eval(fhir.Patient, "http://hl7.org/fhir/Patient")
        self.eval(fhir.Patient.status, "http://hl7.org/fhir/Patient.status")
        self.eval(fhir.Patient.status.code.value, "http://hl7.org/fhir/Patient.status.code.value")

    def test_comparisons(self):
        from fhirtordf.rdfsupport.namespaces import FHIR
        self.assertEqual(FHIR.nodeRole, FHIR.nodeRole)
        self.assertEqual(URIRef("http://hl7.org/fhir/nodeRole"), URIRef("http://hl7.org/fhir/nodeRole"))
        self.assertEqual(FHIR.nodeRole, URIRef("http://hl7.org/fhir/nodeRole"))
        self.assertEqual(URIRef("http://hl7.org/fhir/nodeRole"), FHIR.nodeRole)

        self.assertTrue(FHIR.nodeRole in {FHIR['index'], URIRef("http://hl7.org/fhir/nodeRole"), FHIR['id']})
        self.assertTrue(URIRef("http://hl7.org/fhir/nodeRole") in {FHIR.index, FHIR.nodeRole, FHIR['id']})
        self.assertTrue(FHIR.nodeRole in {FHIR['index'], FHIR.nodeRole, FHIR['id']})

    def test_index_failure(self):
        from fhirtordf.rdfsupport.namespaces import FHIR
        self.assertEqual(str(FHIR.index), "http://hl7.org/fhir/index")
        self.assertEqual(str(FHIR.id), "http://hl7.org/fhir/id")

if __name__ == '__main__':
    unittest.main()

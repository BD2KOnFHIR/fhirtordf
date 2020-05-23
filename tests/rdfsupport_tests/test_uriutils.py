
import unittest

from rdflib import URIRef, Namespace

from fhirtordf.rdfsupport.namespaces import FHIR
from fhirtordf.rdfsupport.uriutils import parse_fhir_resource_uri


class URIUtilsTestCase(unittest.TestCase):
    def test_uri_to_ide_and_source(self):
        r = parse_fhir_resource_uri(URIRef("http://hl7.org/fhir/Patient/f201"))
        self.assertEqual('f201', r.resource)
        self.assertEqual(FHIR, r.namespace)
        self.assertEqual(FHIR.Patient, r.resource_type)

        EX = Namespace("http://example.org/some/path/")
        r = parse_fhir_resource_uri("http://example.org/some/path/Observation/O123")
        self.assertEqual('O123', r.resource)
        self.assertEqual(EX, r.namespace)
        self.assertEqual(FHIR.Observation, r.resource_type)

        r = parse_fhir_resource_uri("http://example.org/some/path/Observation/O123/_history/stuff")
        self.assertEqual('O123', r.resource)
        self.assertEqual(EX, r.namespace)
        self.assertEqual(FHIR.Observation, r.resource_type)

        r = parse_fhir_resource_uri("http://example.org/some/path/Penguin/ABCD")
        self.assertEqual('ABCD', r.resource)
        self.assertEqual(EX.Penguin, r.namespace)
        self.assertEqual(None, r.resource_type)



if __name__ == '__main__':
    unittest.main()

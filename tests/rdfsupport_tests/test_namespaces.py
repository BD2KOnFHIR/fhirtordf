
import unittest

from rdflib import URIRef, RDF, OWL, RDFS, XSD

from fhirtordf.rdfsupport.namespaces import FHIR, namespace_for, W5, V2, V3, SCT, LOINC, RXNORM


class NamespacesTestCase(unittest.TestCase):
    def test_namespace_for(self):
        self.assertEqual("fhir", namespace_for(FHIR))
        self.assertEqual("owl", namespace_for(OWL))
        self.assertEqual("rdfs", namespace_for(RDFS))
        self.assertEqual("rdf", namespace_for(RDF))
        self.assertEqual("xsd", namespace_for(XSD))
        self.assertEqual("w5", namespace_for(W5))
        self.assertEqual("v2", namespace_for(V2))
        self.assertEqual("v3", namespace_for(V3))
        self.assertEqual("sct", namespace_for(SCT))
        self.assertEqual("loinc", namespace_for(LOINC))
        self.assertEqual("rxnorm", namespace_for(RXNORM))
        self.assertEqual("v2", namespace_for(URIRef("http://hl7.org/fhir/v2/")))

        self.assertEqual("fhir", namespace_for("http://hl7.org/fhir/"))
        self.assertEqual("ns1", namespace_for("http://example.org/"))
        self.assertEqual("ns1", namespace_for("http://example.org/"))
        self.assertEqual("ns2", namespace_for("http://example.com/"))


if __name__ == '__main__':
    unittest.main()

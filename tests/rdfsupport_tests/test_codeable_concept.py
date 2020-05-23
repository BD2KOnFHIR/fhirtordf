
import unittest

import os
from rdflib import Graph, URIRef

from fhirtordf.rdfsupport.namespaces import FHIR


class CodeableConceptCodeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..', 'data'))

    def test_two_entries(self):
        from fhirtordf.rdfsupport.fhirgraphutils import codeable_concept_code
        from fhirtordf.rdfsupport.fhirgraphutils import CodeableConcept

        g = Graph()
        g.load(os.path.join(self.base_dir, "patient-example-f201-roel.ttl"), format="turtle")
        codes = sorted(codeable_concept_code(g, URIRef(FHIR['Patient/f201']), FHIR.Patient.maritalStatus))
        self.assertEqual([
            CodeableConcept("http://hl7.org/fhir/v3/MaritalStatus", "M"),
            CodeableConcept("http://snomed.info/sct", "36629006", URIRef("http://snomed.info/id/36629006"))], codes)

    def test_filters(self):
        from fhirtordf.rdfsupport.fhirgraphutils import codeable_concept_code
        from fhirtordf.rdfsupport.fhirgraphutils import CodeableConcept

        g = Graph()
        g.load(os.path.join(self.base_dir, "patient-example-f201-roel.ttl"), format="turtle")
        codes = sorted(codeable_concept_code(g, URIRef(FHIR['Patient/f201']), FHIR.Patient.maritalStatus,
                                             "http://snomed.info/sct"))
        self.assertEqual([CodeableConcept("http://snomed.info/sct", "36629006",
                                          URIRef("http://snomed.info/id/36629006"))], codes)
        codes = sorted(codeable_concept_code(g, URIRef(FHIR['Patient/f201']), FHIR.Patient.maritalStatus,
                                             "http://loinc.org"))
        self.assertEqual([], codes)

    def test_empty(self):
        from fhirtordf.rdfsupport.fhirgraphutils import codeable_concept_code

        g = Graph()
        g.load(os.path.join(self.base_dir, "patient-example-f201-roel-edited.ttl"), format="turtle")
        codes = sorted(codeable_concept_code(g, URIRef(FHIR['Patient/f201']), FHIR.Patient.maritalStatus))
        self.assertEqual([], codes)

if __name__ == '__main__':
    unittest.main()

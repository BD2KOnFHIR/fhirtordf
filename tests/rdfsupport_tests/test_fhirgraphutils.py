import os
import unittest
from datetime import date, datetime

from isodate import FixedOffset
from rdflib import Graph, URIRef, Literal

from fhirtordf.rdfsupport.namespaces import FHIR

ACT_V3_CODESYSTEM = 'http://terminology.hl7.org/CodeSystem/v3-ActCode'

class FHIRGraphUtilsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..', 'data'))

    def test_value(self):
        from fhirtordf.rdfsupport.fhirgraphutils import value
        g = Graph()
        g.load(os.path.join(self.base_dir, "account-example.ttl"), format="turtle")
        s = FHIR['Account/example']
        self.assertEqual("example", value(g, s, FHIR.Resource.id))
        self.assertEqual(Literal("example"), value(g, s, FHIR.Resource.id, True))
        self.assertEqual(FHIR.treeRoot, value(g, s, FHIR.nodeRole))
        period = g.value(s, FHIR.Account.servicePeriod)
        self.assertIsNotNone(period)
        self.assertEqual(date(2016, 1, 1), value(g, period, FHIR.Period.start))
        period_end = g.value(period, FHIR.Period.end)
        self.assertIsNotNone(period_end)
        self.assertEqual(date(2016, 6, 30), value(g, period_end, FHIR.value))
        self.assertIsNone(value(g, s, FHIR.Account.type))
        self.assertIsNone(value(g, s, FHIR.foo))

    def test_extension(self):
        from fhirtordf.rdfsupport.fhirgraphutils import extension
        g = Graph()
        g.load(os.path.join(self.base_dir, "patient-example.ttl"), format="turtle")
        s = FHIR['Patient/example']
        birthdate = g.value(s, FHIR.Patient.birthDate)
        birthtime = extension(g, birthdate, URIRef("http://hl7.org/fhir/StructureDefinition/patient-birthTime"))
        self.assertEqual(datetime(1974, 12, 25, 14, 35, 45, 0, FixedOffset(-5)), birthtime)
        self.assertTrue(isinstance(
            extension(g, birthdate,
                      URIRef("http://hl7.org/fhir/StructureDefinition/patient-birthTime"), True),
            Literal))

    def test_code(self):
        from fhirtordf.rdfsupport.fhirgraphutils import code
        g = Graph()
        g.load(os.path.join(self.base_dir, "account-example.ttl"), format="turtle")
        s = FHIR['Account/example']
        self.assertEqual("PBILLACCT", code(g, s, FHIR.Account.type))
        self.assertEqual("PBILLACCT", code(g, s, FHIR.Account.type, ACT_V3_CODESYSTEM))
        self.assertIsNone(code(g, s, FHIR.Account.type, "http://hl7.org/fhir/v3/foo"))

    def test_concept_uri(self):
        from fhirtordf.rdfsupport.fhirgraphutils import concept_uri
        g = Graph()
        g.load(os.path.join(self.base_dir, "account-example.ttl"), format="turtle")
        s = FHIR['Account/example']
        self.assertEqual(URIRef("http://terminology.hl7.org/CodeSystem/v3-ActCode/PBILLACCT"),
                         concept_uri(g, s, FHIR.Account.type))
        self.assertEqual(URIRef("http://terminology.hl7.org/CodeSystem/v3-ActCode/PBILLACCT"),
                         concept_uri(g, s, FHIR.Account.type, "http://terminology.hl7.org/CodeSystem/v3-ActCode"))
        self.assertIsNone(concept_uri(g, s, FHIR.Account.type, "http://hl7.org/fhir/v3/foo"))

    def test_link(self):
        from fhirtordf.rdfsupport.fhirgraphutils import link
        g = Graph()
        g.load(os.path.join(self.base_dir, "observation-example-bmd.ttl"), format="turtle")
        s = FHIR['Observation/bmd']
        uri, typ = link(g, s, FHIR.Observation.subject)
        self.assertEqual(FHIR["Patient/pat2"], uri)
        self.assertEqual(FHIR.Patient, typ)
        uri, typ = link(g, s, FHIR.Observation.subject2)
        self.assertIsNone(uri)
        self.assertIsNone(typ)


if __name__ == '__main__':
    unittest.main()

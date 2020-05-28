import unittest

from rdflib import URIRef, Graph

from fhirtordf.fhir.fhirmetavoc import FHIRMetaVoc
from fhirtordf.loaders.fhirjsonloader import fhir_json_to_rdf
from tests.utils import USE_BUILD_SERVER
from tests.utils.base_test_case import test_fhir_server
from tests.utils.output_redirector import OutputRedirector


class LibraryTestCase(unittest.TestCase, OutputRedirector):
    def test_basics(self):
        # TODO: The test below fails.  See: https://github.com/fhircat/FHIRCat/issues/36
        print("http://hl7.org/fhir/Observation/vitals-panel test skipped -- See: FHIRCat issue #36 for details")
        # g = fhir_json_to_rdf("http://hl7.org/fhir/Observation/vitals-panel")
        g = fhir_json_to_rdf("http://hl7.org/fhir/observation-example-vitals-panel.json")
        self.assertEqual(['http://hl7.org/fhir/Observation/blood-pressure',
                          'http://hl7.org/fhir/Observation/body-temperature',
                          'http://hl7.org/fhir/Observation/heart-rate',
                          'http://hl7.org/fhir/Observation/respiratory-rate',
                          'http://hl7.org/fhir/Observation/vitals-panel',
                          'http://hl7.org/fhir/Observation/vitals-panel.ttl',
                          'http://hl7.org/fhir/Patient/example'],
                         sorted(str(s) for s in set(g.subjects()) if isinstance(s, URIRef)))

        mv = FHIRMetaVoc()
        self.assertTrue(mv.from_cache)

        print("http://hl7.org/fhir/DiagnosticReport/f201 test skipped -- See: FHIRCat issue #36 for details")
        # g = fhir_json_to_rdf("http://hl7.org/fhir/DiagnosticReport/f201")
        g = fhir_json_to_rdf("http://hl7.org/fhir/diagnosticreport-example-f201-brainct.json", target_graph=g, metavoc=mv)
        self.assertEqual({URIRef('http://hl7.org/fhir/Observation/blood-pressure'),
                          URIRef('http://hl7.org/fhir/Observation/heart-rate'),
                          URIRef('http://hl7.org/fhir/DiagnosticReport/f201.ttl'),
                          URIRef('http://hl7.org/fhir/Patient/example'),
                          URIRef('http://hl7.org/fhir/Observation/body-temperature'),
                          URIRef('http://hl7.org/fhir/Observation/respiratory-rate'),
                          URIRef('http://hl7.org/fhir/Observation/vitals-panel.ttl'),
                          URIRef('http://hl7.org/fhir/Patient/f201'),
                          URIRef('http://hl7.org/fhir/DiagnosticReport/f201'),
                          URIRef('http://hl7.org/fhir/Organization/f203'),
                          URIRef('http://hl7.org/fhir/Observation/vitals-panel')},
                         set(s for s in g.subjects() if isinstance(s, URIRef)))

    def test_subjects(self):
        from fhirtordf.fhirtordf import main
        output = self._push_stdout()
        if USE_BUILD_SERVER:
            args = '-i {}/observation-example-vitals-panel.json'.format(test_fhir_server)
        else:
            args = "-i {}/Observation/vitals-panel".format(test_fhir_server)
        main(args.split())
        self._pop_stdout()
        g = Graph()
        g.parse(data=output.getvalue(), format="turtle")
        self.assertEqual({URIRef('http://hl7.org/fhir/Observation/respiratory-rate'),
                          URIRef('http://hl7.org/fhir/Observation/body-temperature'),
                          URIRef('http://hl7.org/fhir/Patient/example'),
                          URIRef('http://hl7.org/fhir/Observation/vitals-panel.ttl'),
                          URIRef('http://hl7.org/fhir/Observation/blood-pressure'),
                          URIRef('http://hl7.org/fhir/Observation/heart-rate'),
                          URIRef('http://hl7.org/fhir/Observation/vitals-panel')},
                         set(s for s in g.subjects() if isinstance(s, URIRef)))


if __name__ == '__main__':
    unittest.main()

import os
import unittest

from rdflib import Graph

from fhirtordf.loaders.fhirjsonloader import fhir_json_to_rdf
from fhirtordf.rdfsupport.rdfcompare import rdf_compare_split
from tests import FHIR_R4_TTL
from tests.issue_tests import ISSUE_TEST_DATA_DIR


class MedicationStatementIssue(unittest.TestCase):

    def test_statement(self):

        test_json = os.path.join(ISSUE_TEST_DATA_DIR, 'issue_15.json')
        mvg = Graph()
        mvg.load(FHIR_R4_TTL, format="turtle")
        g = fhir_json_to_rdf(test_json, metavoc=mvg)
        expected_graph = Graph()
        g.load(os.path.join(ISSUE_TEST_DATA_DIR, 'issue_15.ttl'), format="turtle")
        expected, actual = rdf_compare_split(expected_graph, g, ignore_owl_version=False, ignore_type_arcs=False)
        self.assertEqual('', expected)
        self.assertEqual('', actual)


if __name__ == '__main__':
    unittest.main()

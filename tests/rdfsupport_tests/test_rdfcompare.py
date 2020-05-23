
import unittest

from fhirtordf.rdfsupport.namespaces import FHIR


class RDFCompareTestCase(unittest.TestCase):
    def test_subj_pred_to_uri(self):
        from fhirtordf.rdfsupport.rdfcompare import subj_pred_idx_to_uri
        self.assertEqual(FHIR['Patient/f001.Patient.identifier_0'],
                         subj_pred_idx_to_uri(FHIR['Patient/f001'], FHIR.Patient.identifier, 0))
        self.assertEqual(FHIR['Patient/f001.Patient.active'],
                         subj_pred_idx_to_uri(FHIR['Patient/f001'], FHIR.Patient.active))

if __name__ == '__main__':
    unittest.main()

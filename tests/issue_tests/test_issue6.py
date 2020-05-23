
import unittest

import os


class InstanceNumTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tests.utils.base_test_case import FHIRGraph
        cls.fhir_ontology = FHIRGraph()
        cls.test_input_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'data')

    @unittest.expectedFailure
    def test_careplan_instancenum(self):
        # This is creating the correct parsing for this resource.  Once the FHIR resource is fixed, we should
        # pull this
        from fhirtordf.loaders.fhircollectionloader import FHIRCollection

        collection = FHIRCollection(self.fhir_ontology,
                                    os.path.join(self.test_input_directory, 'synthea_data',
                                                 'CarePlan.json'),
                                    "http://standardhealthrecord.org/fhir/")
        for entry in collection.entries:
            print(entry)
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()

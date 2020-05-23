import os
import unittest

from tests.utils.base_test_case import make_and_clear_directory


class FHIRCollectionTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tests.utils.base_test_case import FHIRGraph
        cls.fhir_ontology = FHIRGraph()
        cls.test_input_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'data')
        cls.test_output_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data_out')

    def test_synthea_collection(self):
        from fhirtordf.loaders.fhircollectionloader import FHIRCollection

        output_dir = os.path.join(self.test_output_directory, 'synthea_data', 'ttl')
        make_and_clear_directory(output_dir)

        collection = FHIRCollection(self.fhir_ontology,
                                    os.path.join(self.test_input_directory, 'synthea_data', 'Adams301_Keyshawn30_74.json'),
                                    "http://standardhealthrecord.org/fhir/")
        generated_files = []
        for entry in collection.entries:
            output_fname = os.path.join(output_dir, entry.resource_type, entry.resource_id + ".ttl")
            os.makedirs(os.path.join(output_dir, entry.resource_type), exist_ok=True)
            with open(output_fname, 'w') as output:
                output.write(str(entry))

            generated_files.append(
                os.path.join(entry.resource_type,
                             (entry.resource_id
                              if entry.resource_type not in ["CarePlan", "MedicationRequest"] else "<UUID>") + ".ttl"))

        self.assertEqual([
             'Patient/526238ef-dec3-401d-a1c1-2974962df23f.ttl',
             'Organization/9c00d82c-8deb-4e3c-80ee-2e9221addbc0.ttl',
             'Encounter/ff4f9269-5036-45dc-b0fb-d8133ae13c76.ttl',
             'Condition/9eba3a2a-b040-4697-8b46-41f87f3bbe71.ttl',
             'Condition/e69d5da5-4408-44e5-9ed0-2e93aacae4fa.ttl',
             'Condition/ccbc87d7-8439-4558-9672-7d58c56aa56c.ttl',
             'Condition/0b901fad-ecc3-4135-9ee8-ff4534010c44.ttl',
             'Observation/1d52ae90-6721-476c-ad4c-ec978eac4a34.ttl',
             'DiagnosticReport/4d7445b4-d001-4679-8053-d564fddbb973.ttl',
             'CarePlan/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl',
             'MedicationRequest/<UUID>.ttl'], generated_files)
        print("\n*****> Check outputs in {}".format(output_dir))

    def test_smartonfhir_collection(self):
        """ Pull a sample of the smartonfhir observation data and generate the results in """
        from fhirtordf.loaders.fhircollectionloader import FHIRCollection

        output_dir = os.path.join(self.test_output_directory, 'smartonfhir_testdata', 'obs_sample')
        make_and_clear_directory(output_dir)
        collection = \
            FHIRCollection(self.fhir_ontology,
                           os.path.join(self.test_input_directory,  'smartonfhir_testdata', 'json', 'obs_sample.json'),
                           "https://sb-fhir-dstu2.smarthealthit.org/api/smartdstu2/open/")
        generated_files = []
        for entry in collection.entries:
            os.makedirs(os.path.join(output_dir, entry.resource_type), exist_ok=True)
            with open(os.path.join(output_dir, entry.resource_type, entry.resource_id + '.ttl'), 'w') as output:
                output.write(str(entry))
            generated_files.append(os.path.join(entry.resource_type, entry.resource_id + ".ttl"))
        self.assertEqual(
            ['Observation/SMART-Observation-5-smokingstatus.ttl',
             'Observation/SMART-Observation-6-smokingstatus.ttl',
             'Observation/SMART-Observation-18-smokingstatus.ttl',
             'Observation/SMART-Observation-1098667-gestage.ttl',
             'Observation/SMART-Observation-1681-lab.ttl',
             'Observation/SMART-Observation-1682-lab.ttl',
             'Observation/SMART-Observation-1683-lab.ttl',
             'Observation/SMART-Observation-1684-lab.ttl',
             'Observation/SMART-Observation-1685-lab.ttl'], generated_files)
        print("\n*****> Check outputs in {}".format(output_dir))


if __name__ == '__main__':
    unittest.main()

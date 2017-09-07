# Copyright (c) 2017, Mayo Clinic
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
#     list of conditions and the following disclaimer.
#
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
#     Neither the name of the Mayo Clinic nor the names of its contributors
#     may be used to endorse or promote products derived from this software
#     without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
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

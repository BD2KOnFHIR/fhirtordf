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

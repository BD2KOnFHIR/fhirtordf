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

from jsonasobj import load

from fhirtordf.rdfsupport.prettygraph import PrettyGraph
from fhirtordf.rdfsupport.rdfcompare import rdf_compare, rdf_compare_split


class FhirDataLoaderTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tests.utils.base_test_case import FHIRGraph
        cls.fhir_ontology = FHIRGraph()
        cls.base_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'data')

    def do_test(self, fname):
        from fhirtordf.loaders.fhirresourceloader import FHIRResource

        json_file = fname + ".json"
        turtle_file = fname + ".ttl"

        target = FHIRResource(self.fhir_ontology, os.path.join(self.base_dir, json_file), "http://hl7.org/fhir/")
        turtle_fname = os.path.join(self.base_dir, turtle_file)
        source = PrettyGraph()
        source.load(turtle_fname, format="turtle")
        self.maxDiff = None
        self.assertEqual(*rdf_compare_split(source, target.graph, ignore_owl_version=False))

    def test_observation_example_bmd(self):
        self.do_test('observation-example-bmd')

    def test_account_example(self):
        # Note: trailing slash deliberately omitted to test FHIRResource constructor
        # Note: The latest FHIR RDF no longer generates type arcs for FHIR RDF.  We've edited one in manually for this
        #       example.
        self.do_test('account-example')

    def test_observation_example_f001_glucose(self):
        self.do_test('observation-example-f001-glucose')

    def test_data_entry(self):
        save_output = False
        from fhirtordf.loaders.fhirresourceloader import FHIRResource
        with open(os.path.join(self.base_dir, 'synthea_data', 'Adams301_Keyshawn30_74.json')) as f:
            collection = load(f)
        source = FHIRResource(self.fhir_ontology,
                              None,
                              "http://standardhealthrecord.org/fhir/", data=collection.entry[0].resource)
        turtle_fname = os.path.join(self.base_dir, 'synthea_data', 'Adams301_Keyshawn30_74_entry0.ttl')
        if save_output:
            with open(turtle_fname, 'w') as output:
                output.write(str(source))
        target = PrettyGraph()
        target.load(turtle_fname, format="turtle")
        # Note: This will fail if we use the pure turtle serializer (vs our changes in this package)
        self.maxDiff = None
        self.assertEqual('', rdf_compare(source.graph, target, ignore_owl_version=True))
        self.assertFalse(save_output, "Update output file always fails")


if __name__ == '__main__':
    unittest.main()

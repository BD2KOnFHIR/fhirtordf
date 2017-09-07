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

from rdflib import Graph, URIRef

from fhirtordf.rdfsupport.rdfcompare import rdf_compare

# If true, we're updating the target. Will always return a fail
save_output = False


class JSONToRDFTestCase(unittest.TestCase):

    def test_patient_example(self):
        from fhirtordf.fhirtordf import fhirtordf

        test_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'data')
        infname = os.path.join(test_directory, "patient-example.json")
        testfname = os.path.join(test_directory, "patient-example.ttl")
        if save_output:
            outfname = testfname
        else:
            outfname = os.path.join(test_directory, "patient-example-out.ttl")
        args = "-i {} -o {} -s".format(infname, outfname)
        self.assertTrue(fhirtordf(args.split()))
        self.assertFalse(save_output, "Test file: {} generated".format(outfname))
        out_graph = Graph()
        out_graph.load(outfname, format="turtle")
        test_graph = Graph()
        test_graph.load(testfname, format="turtle")
        comp_result = rdf_compare(test_graph, out_graph, ignore_owl_version=True, ignore_type_arcs=True)
        if len(comp_result):
            print(comp_result)
        self.assertTrue(len(comp_result) == 0)

    def test_fhir_files(self):
        from fhirtordf.fhirtordf import fhirtordf

        fnames = ['activitydefinition-example',
                  'activitydefinition-medicationorder-example',
                  'capabilitystatement-base',
                  'careplan-example-f001-heart',
                  'claim-example',
                  'patient-example']

        for fname in fnames:
            in_url = "http://build.fhir.org/{}.json".format(fname)
            test_url = "http://build.fhir.org/{}.ttl".format(fname)
            test_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')
            outfname = os.path.join(test_directory, "{}.ttl".format(fname))
            args = "-i {} -o {} -s".format(in_url, outfname)
            self.assertTrue(fhirtordf(args.split()))
            out_graph = Graph()
            out_graph.load(outfname, format="turtle")
            test_graph = Graph()
            test_graph.load(test_url, format="turtle")
            comp_result = rdf_compare(test_graph, out_graph, ignore_owl_version=True, ignore_type_arcs=True)
            if len(comp_result):
                print(comp_result)
            self.assertTrue(len(comp_result) == 0)

    def test_continuations(self):
        from fhirtordf.fhirtordf import fhirtordf

        test_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')
        outfname = os.path.join(test_directory, "patlist1.ttl")
        url = "http://fhirtest.uhn.ca/baseDstu3/Patient?_format=json&gender=male"
        args = "-i {} -o {} -nc".format(url, outfname)
        self.assertTrue(fhirtordf(args.split()))
        out_graph = Graph()
        out_graph.load(outfname, format="turtle")
        self.assertTrue(len([s for s in set(out_graph.subjects()) if isinstance(s, URIRef)]) < 50)
        args = "-i {} -o {}".format(url, outfname)
        self.assertTrue(fhirtordf(args.split()))
        out_graph = Graph()
        out_graph.load(outfname, format="turtle")
        self.assertTrue(len([s for s in set(out_graph.subjects()) if isinstance(s, URIRef)]) > 3000)


if __name__ == '__main__':
    unittest.main()

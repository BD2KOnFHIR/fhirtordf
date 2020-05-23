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
        from fhirtordf.fhirtordf import fhirtordf
        output = self._push_stdout()
        if USE_BUILD_SERVER:
            args = '-i {}/observation-example-vitals-panel.json'.format(test_fhir_server)
        else:
            args = "-i {}/Observation/vitals-panel".format(test_fhir_server)
        fhirtordf(args.split())
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

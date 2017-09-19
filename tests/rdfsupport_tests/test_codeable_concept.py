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
from rdflib import Graph, URIRef

from fhirtordf.rdfsupport.namespaces import FHIR


class CodeableConceptCodeTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..', 'data'))

    def test_two_entries(self):
        from fhirtordf.rdfsupport.fhirgraphutils import codeable_concept_code
        from fhirtordf.rdfsupport.fhirgraphutils import CodeableConcept

        g = Graph()
        g.load(os.path.join(self.base_dir, "patient-example-f201-roel.ttl"), format="turtle")
        codes = sorted(codeable_concept_code(g, URIRef(FHIR['Patient/f201']), FHIR.Patient.maritalStatus))
        self.assertEqual([
            CodeableConcept("http://hl7.org/fhir/v3/MaritalStatus", "M"),
            CodeableConcept("http://snomed.info/sct", "36629006", URIRef("http://snomed.info/id/36629006"))], codes)

    def test_filters(self):
        from fhirtordf.rdfsupport.fhirgraphutils import codeable_concept_code
        from fhirtordf.rdfsupport.fhirgraphutils import CodeableConcept

        g = Graph()
        g.load(os.path.join(self.base_dir, "patient-example-f201-roel.ttl"), format="turtle")
        codes = sorted(codeable_concept_code(g, URIRef(FHIR['Patient/f201']), FHIR.Patient.maritalStatus,
                                             "http://snomed.info/sct"))
        self.assertEqual([CodeableConcept("http://snomed.info/sct", "36629006",
                                          URIRef("http://snomed.info/id/36629006"))], codes)
        codes = sorted(codeable_concept_code(g, URIRef(FHIR['Patient/f201']), FHIR.Patient.maritalStatus,
                                             "http://loinc.org"))
        self.assertEqual([], codes)

    def test_empty(self):
        from fhirtordf.rdfsupport.fhirgraphutils import codeable_concept_code

        g = Graph()
        g.load(os.path.join(self.base_dir, "patient-example-f201-roel-edited.ttl"), format="turtle")
        codes = sorted(codeable_concept_code(g, URIRef(FHIR['Patient/f201']), FHIR.Patient.maritalStatus))
        self.assertEqual([], codes)

if __name__ == '__main__':
    unittest.main()

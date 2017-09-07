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

from rdflib import URIRef


class DottedNamespaceTestCase(unittest.TestCase):
    def eval(self, item: URIRef, val: str):
        self.assertTrue(isinstance(item, URIRef))
        self.assertEqual(val, str(item))

    def test(self):
        from fhirtordf.rdfsupport.dottednamespace import DottedNamespace
        fhir = DottedNamespace("http://hl7.org/fhir/")
        self.eval(fhir.Patient, "http://hl7.org/fhir/Patient")
        self.eval(fhir.Patient.status, "http://hl7.org/fhir/Patient.status")
        self.eval(fhir.Patient.status.code.value, "http://hl7.org/fhir/Patient.status.code.value")

    def test_comparisons(self):
        from fhirtordf.rdfsupport.namespaces import FHIR
        self.assertEqual(FHIR.nodeRole, FHIR.nodeRole)
        self.assertEqual(URIRef("http://hl7.org/fhir/nodeRole"), URIRef("http://hl7.org/fhir/nodeRole"))
        self.assertEqual(FHIR.nodeRole, URIRef("http://hl7.org/fhir/nodeRole"))
        self.assertEqual(URIRef("http://hl7.org/fhir/nodeRole"), FHIR.nodeRole)

        self.assertTrue(FHIR.nodeRole in {FHIR['index'], URIRef("http://hl7.org/fhir/nodeRole"), FHIR['id']})
        self.assertTrue(URIRef("http://hl7.org/fhir/nodeRole") in {FHIR.index, FHIR.nodeRole, FHIR['id']})
        self.assertTrue(FHIR.nodeRole in {FHIR['index'], FHIR.nodeRole, FHIR['id']})

    def test_index_failure(self):
        from fhirtordf.rdfsupport.namespaces import FHIR
        self.assertEqual(str(FHIR.index), "http://hl7.org/fhir/index")
        self.assertEqual(str(FHIR.id), "http://hl7.org/fhir/id")

if __name__ == '__main__':
    unittest.main()

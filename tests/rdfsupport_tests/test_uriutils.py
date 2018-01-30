# Copyright (c) 2018, Mayo Clinic
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

from rdflib import URIRef, Namespace

from fhirtordf.rdfsupport.namespaces import FHIR
from fhirtordf.rdfsupport.uriutils import parse_fhir_resource_uri


class URIUtilsTestCase(unittest.TestCase):
    def test_uri_to_ide_and_source(self):
        r = parse_fhir_resource_uri(URIRef("http://hl7.org/fhir/Patient/f201"))
        self.assertEqual('f201', r.resource)
        self.assertEqual(FHIR, r.namespace)
        self.assertEqual(FHIR.Patient, r.resource_type)

        EX = Namespace("http://example.org/some/path/")
        r = parse_fhir_resource_uri("http://example.org/some/path/Observation/O123")
        self.assertEqual('O123', r.resource)
        self.assertEqual(EX, r.namespace)
        self.assertEqual(FHIR.Observation, r.resource_type)

        r = parse_fhir_resource_uri("http://example.org/some/path/Observation/O123/_history/stuff")
        self.assertEqual('O123', r.resource)
        self.assertEqual(EX, r.namespace)
        self.assertEqual(FHIR.Observation, r.resource_type)

        r = parse_fhir_resource_uri("http://example.org/some/path/Penguin/ABCD")
        self.assertEqual('ABCD', r.resource)
        self.assertEqual(EX.Penguin, r.namespace)
        self.assertEqual(None, r.resource_type)



if __name__ == '__main__':
    unittest.main()

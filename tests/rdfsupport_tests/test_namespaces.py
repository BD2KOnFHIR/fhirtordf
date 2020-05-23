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

from rdflib import URIRef, RDF, OWL, RDFS, XSD

from fhirtordf.rdfsupport.namespaces import FHIR, namespace_for, W5, V2, V3, SCT, LOINC, RXNORM


class NamespacesTestCase(unittest.TestCase):
    def test_namespace_for(self):
        self.assertEqual("fhir", namespace_for(FHIR))
        self.assertEqual("owl", namespace_for(OWL))
        self.assertEqual("rdfs", namespace_for(RDFS))
        self.assertEqual("rdf", namespace_for(RDF))
        self.assertEqual("xsd", namespace_for(XSD))
        self.assertEqual("w5", namespace_for(W5))
        self.assertEqual("v2", namespace_for(V2))
        self.assertEqual("v3", namespace_for(V3))
        self.assertEqual("sct", namespace_for(SCT))
        self.assertEqual("loinc", namespace_for(LOINC))
        self.assertEqual("rxnorm", namespace_for(RXNORM))
        self.assertEqual("v2", namespace_for(URIRef("http://hl7.org/fhir/v2/")))

        self.assertEqual("fhir", namespace_for("http://hl7.org/fhir/"))
        self.assertEqual("ns1", namespace_for("http://example.org/"))
        self.assertEqual("ns1", namespace_for("http://example.org/"))
        self.assertEqual("ns2", namespace_for("http://example.com/"))


if __name__ == '__main__':
    unittest.main()

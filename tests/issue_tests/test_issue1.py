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

from jsonasobj import loads
from rdflib import URIRef

from fhirtordf.rdfsupport.namespaces import FHIR
from tests.utils.base_test_case import FHIRGraph

data = """{
  "resourceType": "EligibilityResponse",
  "id": "E2500",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\\"http://www.w3.org/1999/xhtml\\">A human-readable rendering of the EligibilityResponse.</div>"
  },
  "identifier": [
    {
      "system": "http://www.BenefitsInc.com/fhir/eligibilityresponse",
      "value": "881234"
    }
  ],
  "status": "active",
  "created": "2014-08-16",
  "request": {
    "reference": "http://www.BenefitsInc.com/fhir/eligibility/225476332402"
  },
  "outcome": "complete",
  "disposition": "Policy is currently in-force.",
  "insurer": {
    "reference": "Organization/2"
  },
  "inforce": true
}"""


class Issue1TestCase(unittest.TestCase):
    def test_reference(self):
        test_json = loads(data)
        from fhirtordf.loaders.fhirresourceloader import FHIRResource
        test_rdf = FHIRResource(FHIRGraph(), None, "http://hl7.org/fhir", test_json)
        g = test_rdf.graph
        subj = URIRef("http://hl7.org/fhir/EligibilityResponse/E2500")
        self.assertEqual("http://www.BenefitsInc.com/fhir/eligibility/225476332402",
                         str(g.value(g.value(subj, FHIR.EligibilityResponse.request), FHIR.link)))


if __name__ == '__main__':
    unittest.main()

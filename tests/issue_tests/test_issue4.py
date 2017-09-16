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
from rdflib import URIRef, Literal, XSD

from fhirtordf.rdfsupport.namespaces import FHIR
from tests.utils.base_test_case import FHIRGraph

json_data = """{
  "resourceType": "VisionPrescription",
  "id": "33123",
  "text": {
    "status": "generated",
    "div": "(cut)"
  },
   "dispense": [
    {
      "product": {
        "coding": [
          {
            "system": "http://hl7.org/fhir/ex-visionprescriptionproduct",
            "code": "lens"
          }
        ]
      },
      "eye": "right",
      "sphere": -2.00,
      "prism": 0.5,
      "base": "down",
      "add": 2.00
    }
  ]
}
  """


class Issue4TestCase(unittest.TestCase):
    def test_decimal(self):
        test_json = loads(json_data)
        from fhirtordf.loaders.fhirresourceloader import FHIRResource
        test_rdf = FHIRResource(FHIRGraph(), None, "http://hl7.org/fhir", test_json)
        g = test_rdf.graph
        # rdflib supports decimal precision if you create the data as a string.
        self.assertNotEqual(Literal("2.00", datatype=XSD.decimal), Literal("2.0", datatype=XSD.decimal))
        self.assertEqual(Literal(2.00), Literal(2.0))

        # FHIR requires that *all* decimals use the first form.  While the diopter example above
        # would work, issues arise in situations where numbers really ARE decimal...
        self.assertEqual(Literal("2.00", datatype=XSD.decimal),
                         g.value(
                             g.value(
                                 g.value(URIRef("http://hl7.org/fhir/VisionPrescription/33123"),
                                         FHIR.VisionPrescription.dispense),
                                 FHIR.VisionPrescription.dispense.add), FHIR.value))

if __name__ == '__main__':
    unittest.main()

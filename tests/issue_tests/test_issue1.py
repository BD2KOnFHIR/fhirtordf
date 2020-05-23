
import unittest

from jsonasobj import loads
from rdflib import URIRef

from fhirtordf.fhir.fhirmetavoc import FHIRMetaVoc
from fhirtordf.rdfsupport.namespaces import FHIR
from tests.utils.base_test_case import FHIRGraph, test_fhir_server

data = """{
  "resourceType": "CoverageEligibilityResponse",
  "id": "E2500",
  "text": {
    "status": "generated",
    "div": "<div xmlns=\\"http://www.w3.org/1999/xhtml\\">A human-readable rendering of the CoverageEligibilityResponse.</div>"
  },
  "identifier": [
    {
      "system": "http://www.BenefitsInc.com/fhir/coverageeligibilityresponse",
      "value": "881234"
    }
  ],
  "status": "active",
  "purpose": [
    "validation"
  ],
  "patient": {
    "reference": "Patient/pat1"
  },
  "created": "2014-08-16",
  "request": {
    "reference": "http://www.BenefitsInc.com/fhir/coverageeligibilityrequest/225476332402"
  },
  "outcome": "complete",
  "disposition": "Policy is currently in-force.",
  "insurer": {
    "reference": "Organization/2"
  },
  "insurance": [
    {
      "coverage": {
        "reference": "Coverage/9876B1"
      },
      "inforce": true
    }
  ]
}"""


class Issue1TestCase(unittest.TestCase):
    def test_reference(self):
        test_json = loads(data)
        from fhirtordf.loaders.fhirresourceloader import FHIRResource
        fmv_loc = "http://build.fhir.org/fhir.ttl"

        test_rdf = FHIRResource(FHIRMetaVoc(fmv_loc).g, None, "http://hl7.org/fhir", test_json)
        g = test_rdf.graph
        subj = URIRef("http://hl7.org/fhir/CoverageEligibilityResponse/E2500")
        self.assertEqual("http://www.BenefitsInc.com/fhir/coverageeligibilityrequest/225476332402",
                         str(g.value(g.value(subj, FHIR.CoverageEligibilityResponse.request), FHIR.link)))


if __name__ == '__main__':
    unittest.main()

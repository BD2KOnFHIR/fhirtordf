
import unittest

from jsonasobj import loads
from rdflib import URIRef

from tests.utils.base_test_case import FHIRGraph

json_data = """{
  "resourceType": "Bundle",
  "id": "bundle-example",
  "meta": {
    "lastUpdated": "2014-08-18T01:43:30Z"
  },
  "type": "searchset",
  "total": 3,
  "link": [
    {
      "relation": "self",
      "url": "https://example.com/base/MedicationRequest?patient=347&_include=MedicationRequest.medication"
    },
    {
      "relation": "next",
      "url": "https://example.com/base/MedicationRequest?patient=347&searchId=ff15fd40-ff71-4b48-b366-09c706bed9d0&page=2"
    }
  ],
  "entry": [
    {
      "fullUrl": "https://example.com/base/MedicationRequest/3123",
      "resource": {
        "resourceType": "MedicationRequest",
        "id": "3123",
        "text": {
          "status": "generated",
          "div": "(cut)"
        },
        "intent": "order"
      }
    }
  ]
}"""


class Issue5TestCase(unittest.TestCase):
    def test_decimal(self):
        test_json = loads(json_data)
        from fhirtordf.loaders.fhirresourceloader import FHIRResource
        test_rdf = FHIRResource(FHIRGraph(), None, "http://hl7.org/fhir", test_json, add_ontology_header=False)
        g = test_rdf.graph
        self.assertEqual({URIRef('http://hl7.org/fhir/Bundle/bundle-example'),
                          URIRef('https://example.com/base/MedicationRequest/3123')},
                         set(s for s in g.subjects() if isinstance(s, URIRef)))


if __name__ == '__main__':
    unittest.main()

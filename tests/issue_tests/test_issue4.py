
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
    # This hasn't been fixed -- failure is expected
    @unittest.expectedFailure
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

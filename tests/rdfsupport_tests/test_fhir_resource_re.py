
import unittest


from fhirtordf.rdfsupport.fhirresourcere import FHIR_RESOURCE_RE, FHIR_RE_BASE, FHIR_RE_RESOURCE, FHIR_RE_VERSION


class FHIRResourceRETestCase(unittest.TestCase):
    def test(self):
        fhir_re = FHIR_RESOURCE_RE
        self.assertIsNotNone(fhir_re.match("http://fhir.org/hl7/Patient/sample12345"))
        self.assertIsNone(fhir_re.match("http://fhir.org/hl7/Patient"))
        self.assertIsNotNone(fhir_re.match("Account/example"))
        self.assertIsNone(fhir_re.match("Account"))
        self.assertIsNone(fhir_re.match("http://fhir.org/hl7/Zatient/sample12345"))
        self.assertIsNotNone(fhir_re.match("http://fhir.org/hl7/Patient/sample12345/_history/3"))
        self.assertIsNone(fhir_re.match("http://fhir.org/hl7/Patient/sample_12345"))
        self.assertIsNotNone(fhir_re.match("http://fhir.org/hl7/Patient/" + 'a' * 64))
        self.assertIsNone(fhir_re.match("http://fhir.org/hl7/Patient/" + 'a' * 65))

    def test_indices(self):
        fhir_re = FHIR_RESOURCE_RE
        v = fhir_re.match("http://fhir.org/hl7/Patient/sample12345")
        self.assertEqual('http://fhir.org/hl7/', v.group(FHIR_RE_BASE))
        self.assertEqual('Patient', v.group(FHIR_RE_RESOURCE))
        self.assertIsNone(v.group(FHIR_RE_VERSION))

        v = fhir_re.match("Patient/sample12345")
        self.assertIsNone(v.group(FHIR_RE_BASE))
        self.assertEqual('Patient', v.group(FHIR_RE_RESOURCE))
        self.assertIsNone(v.group(FHIR_RE_VERSION))

        v = fhir_re.match("http://fhir.org/hl7/Patient/sample12345/_history/sample12345v3.17")
        self.assertEqual('http://fhir.org/hl7/', v.group(FHIR_RE_BASE))
        self.assertEqual('Patient', v.group(FHIR_RE_RESOURCE))
        self.assertEqual('sample12345v3.17', v.group(FHIR_RE_VERSION))


if __name__ == '__main__':
    unittest.main()

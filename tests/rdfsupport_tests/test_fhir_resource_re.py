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

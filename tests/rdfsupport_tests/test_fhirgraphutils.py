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
import os
import unittest
from datetime import date, datetime

from isodate import FixedOffset
from rdflib import Graph, URIRef, Literal

from fhirtordf.rdfsupport.namespaces import FHIR

ACT_V3_CODESYSTEM = 'http://terminology.hl7.org/CodeSystem/v3-ActCode'

class FHIRGraphUtilsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_dir = os.path.abspath(os.path.join(os.path.split(__file__)[0], '..', 'data'))

    def test_value(self):
        from fhirtordf.rdfsupport.fhirgraphutils import value
        g = Graph()
        g.load(os.path.join(self.base_dir, "account-example.ttl"), format="turtle")
        s = FHIR['Account/example']
        self.assertEqual("example", value(g, s, FHIR.Resource.id))
        self.assertEqual(Literal("example"), value(g, s, FHIR.Resource.id, True))
        self.assertEqual(FHIR.treeRoot, value(g, s, FHIR.nodeRole))
        period = g.value(s, FHIR.Account.servicePeriod)
        self.assertIsNotNone(period)
        self.assertEqual(date(2016, 1, 1), value(g, period, FHIR.Period.start))
        period_end = g.value(period, FHIR.Period.end)
        self.assertIsNotNone(period_end)
        self.assertEqual(date(2016, 6, 30), value(g, period_end, FHIR.value))
        self.assertIsNone(value(g, s, FHIR.Account.type))
        self.assertIsNone(value(g, s, FHIR.foo))

    def test_extension(self):
        from fhirtordf.rdfsupport.fhirgraphutils import extension
        g = Graph()
        g.load(os.path.join(self.base_dir, "patient-example.ttl"), format="turtle")
        s = FHIR['Patient/example']
        birthdate = g.value(s, FHIR.Patient.birthDate)
        birthtime = extension(g, birthdate, URIRef("http://hl7.org/fhir/StructureDefinition/patient-birthTime"))
        self.assertEqual(datetime(1974, 12, 25, 14, 35, 45, 0, FixedOffset(-5)), birthtime)
        self.assertTrue(isinstance(
            extension(g, birthdate,
                      URIRef("http://hl7.org/fhir/StructureDefinition/patient-birthTime"), True),
            Literal))

    def test_code(self):
        from fhirtordf.rdfsupport.fhirgraphutils import code
        g = Graph()
        g.load(os.path.join(self.base_dir, "account-example.ttl"), format="turtle")
        s = FHIR['Account/example']
        self.assertEqual("PBILLACCT", code(g, s, FHIR.Account.type))
        self.assertEqual("PBILLACCT", code(g, s, FHIR.Account.type, ACT_V3_CODESYSTEM))
        self.assertIsNone(code(g, s, FHIR.Account.type, "http://hl7.org/fhir/v3/foo"))

    def test_concept_uri(self):
        from fhirtordf.rdfsupport.fhirgraphutils import concept_uri
        g = Graph()
        g.load(os.path.join(self.base_dir, "account-example.ttl"), format="turtle")
        s = FHIR['Account/example']
        self.assertEqual(URIRef("http://terminology.hl7.org/CodeSystem/v3-ActCode/PBILLACCT'"),
                         concept_uri(g, s, FHIR.Account.type))
        self.assertEqual(URIRef("http://terminology.hl7.org/CodeSystem/v3-ActCode/PBILLACCT"),
                         concept_uri(g, s, FHIR.Account.type, "http://terminology.hl7.org/CodeSystem/v3-ActCode"))
        self.assertIsNone(concept_uri(g, s, FHIR.Account.type, "http://hl7.org/fhir/v3/foo"))

    def test_link(self):
        from fhirtordf.rdfsupport.fhirgraphutils import link
        g = Graph()
        g.load(os.path.join(self.base_dir, "observation-example-bmd.ttl"), format="turtle")
        s = FHIR['Observation/bmd']
        uri, typ = link(g, s, FHIR.Observation.subject)
        self.assertEqual(FHIR["Patient/pat2"], uri)
        self.assertEqual(FHIR.Patient, typ)
        uri, typ = link(g, s, FHIR.Observation.subject2)
        self.assertIsNone(uri)
        self.assertIsNone(typ)


if __name__ == '__main__':
    unittest.main()

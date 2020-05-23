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

import os
from jsonasobj import loads
from rdflib import Graph

from fhirtordf.rdfsupport.rdfcompare import rdf_compare_split
from tests.utils.base_test_case import FHIRGraph

data = """{
  "resourceType": "Bundle",
  "id": "b248b1b2-1686-4b94-9936-37d7a5f94b51",
  "meta": {
    "lastUpdated": "2012-05-29T23:45:32Z"
  },
  "type": "collection",
  "entry": [
    {
      "fullUrl": "http://hl7.org/fhir/Patient/1",
      "resource": {
        "resourceType": "Patient",
        "id": "1",
        "meta": {
          "lastUpdated": "2012-05-29T23:45:32Z"
        },
        "text": {
          "status": "generated",
          "div": ""
        },
        "identifier": [
          {
            "type": {
              "coding": [
                {
                  "system": "http://hl7.org/fhir/v2/0203",
                  "code": "SS"
                }
              ]
            },
            "system": "http://hl7.org/fhir/sid/us-ssn",
            "value": "444222222"
          }
        ]
      }
    }
  ]
}"""

expected = """@prefix fhir: <http://hl7.org/fhir/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix v2-0203: <http://hl7.org/fhir/v2/0203> .
@prefix w5: <http://hl7.org/fhir/w5#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://hl7.org/fhir/Bundle/b248b1b2-1686-4b94-9936-37d7a5f94b51> a fhir:Bundle ;
    fhir:nodeRole fhir:treeRoot ;
    fhir:Bundle.entry [
        fhir:Bundle.entry.fullUrl [
            fhir:value "http://hl7.org/fhir/Patient/1"
        ] ;
        fhir:Bundle.entry.resource <http://hl7.org/fhir/Patient/1> ;
        fhir:index "0"^^xsd:integer
    ] ;
    fhir:Bundle.type [
        fhir:value "collection"
    ] ;
    fhir:Resource.id [
        fhir:value "b248b1b2-1686-4b94-9936-37d7a5f94b51"
    ] ;
    fhir:Resource.meta [
        fhir:Meta.lastUpdated [
            fhir:value "2012-05-29T23:45:32+00:00"^^xsd:dateTime
        ]
    ] .

<http://hl7.org/fhir/Bundle/b248b1b2-1686-4b94-9936-37d7a5f94b51.ttl> a owl:Ontology ;
    owl:imports fhir:fhir.ttl .

<http://hl7.org/fhir/Patient/1> a fhir:Patient ;
    fhir:DomainResource.text [
        fhir:Narrative.div "" ;
        fhir:Narrative.status [
            fhir:value "generated"
        ]
    ] ;
    fhir:Patient.identifier [
        fhir:index "0"^^xsd:integer ;
        fhir:Identifier.system [
            fhir:value "http://hl7.org/fhir/sid/us-ssn"
        ] ;
        fhir:Identifier.type [
            fhir:CodeableConcept.coding [
                a <http://hl7.org/fhir/v2/0203/SS> ;
                fhir:index "0"^^xsd:integer ;
                fhir:Coding.code [
                    fhir:value "SS"
                ] ;
                fhir:Coding.system [
                    fhir:value "http://hl7.org/fhir/v2/0203"
                ]
            ]
        ] ;
        fhir:Identifier.value [
            fhir:value "444222222"
        ]
    ] ;
    fhir:Resource.id [
        fhir:value "1"
    ] ;
    fhir:Resource.meta [
        fhir:Meta.lastUpdated [
            fhir:value "2012-05-29T23:45:32+00:00"^^xsd:dateTime
        ]
    ] .
"""


class Issue2TestCase(unittest.TestCase):
    def test_reference(self):
        test_json = loads(data)
        from fhirtordf.loaders.fhirresourceloader import FHIRResource
        test_rdf = FHIRResource(FHIRGraph(), None, "http://hl7.org/fhir", test_json)
        g = test_rdf.graph
        expected_graph = Graph()
        expected, actual = rdf_compare_split(expected_graph, test_rdf.graph, ignore_owl_version=True, ignore_type_arcs=True)
        self.assertEqual('', expected)
        self.assertEqual('', actual)


if __name__ == '__main__':
    unittest.main()

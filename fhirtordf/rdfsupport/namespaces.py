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

from rdflib import Namespace, OWL, RDFS, RDF, XSD, URIRef

from fhirtordf.rdfsupport.dottednamespace import DottedNamespace

# TODO: Determine what these various namespaces should actually be
W5 = DottedNamespace("http://hl7.org/fhir/w5#")
FHIR = DottedNamespace("http://hl7.org/fhir/")
LOINC = Namespace("http://loinc.org/owl#")
SNOMEDCT = Namespace("http://snomed.info/id/")
RXNORM = Namespace("http://www.nlm.nih.gov/research/umls/rxnorm")
V3 = Namespace("http://hl7.org/fhir/v3/")
V2 = Namespace("http://hl7.org/fhir/v2/")
SCT = Namespace("http://snomed.info/id/")

namespaces = {"fhir": FHIR,
              "owl": OWL,
              "rdfs": RDFS,
              "rdf": RDF,
              "xsd": XSD,
              "w5": W5,
              "v2": V2,
              "v3": V3,
              "sct": SCT}


class AnonNS:
    _nsnum = 0

    def __init__(self):
        self._nsnum += 1
        self.ns = 'ns{}'.format(self._nsnum)


def namespace_for(uri: URIRef) -> str:
    """
    Reverse namespace lookup.  Note that returned namespace may not be unique
    :param uri: namespace URI
    :return: namespace
    """
    if uri not in namespaces:
        namespaces[AnonNS()] = uri
    return [k for k, v in namespaces.items() if uri == v][0]

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
from datetime import datetime, date
from typing import Union, Optional, Tuple, List

from rdflib import Graph, BNode, Literal, RDF
from rdflib.term import Identifier, URIRef, Node
from rdflib.exceptions import UniquenessError

from fhirtordf.rdfsupport.namespaces import FHIR


def value(g: Graph, subject: Node, predicate: URIRef, asLiteral=False) -> \
        Union[None, BNode, URIRef, str, date, bool, datetime, int, float]:

    values = list(set(g.objects(subject, predicate)))
    if len(values) == 0:
        return None

    if all(isinstance(v, BNode) for v in values) and predicate != FHIR.value:
        vv = list(set(g.value(v, FHIR.value) for v in values))
        if len(vv) > 1:
            raise UniquenessError("Non-unique values for {} {} : [{}]".format(subject, predicate, ', '.join(vv)))
        return vv[0].toPython() if not asLiteral else vv[0]
    else:
        if len(values) > 1:
            raise UniquenessError("Non-unique values for {} {} : [{}]".format(subject, predicate, ', '.join(values)))
        return values[0].toPython() if isinstance(values[0], Literal) and not asLiteral else values[0]


def extension(g: Graph, node: Identifier, extension_predicate: Union[URIRef, str], asLiteral=False) -> \
        Union[None, BNode, date, bool, datetime, int, float]:
    ext_pred = str(extension_predicate)
    for ext in g.objects(node, FHIR.Element.extension):
        if value(g, ext, FHIR.Extension.url) == ext_pred:
            for p, o in g.predicate_objects(ext):
                # TODO: Think this through -- do we need something in the RDF
                if 'Extension.value' in str(p):
                    return value(g, ext, p, asLiteral)
    return None


def code(g: Graph, subject: Node, predicate: URIRef, system: Optional[Union[URIRef, str]]=None,
         asLiteral: bool=False) -> Union[Node, str, None]:
    c = g.value(subject, predicate)
    if c:
        for coding in g.objects(c, FHIR.CodeableConcept.coding):
            if not system or str(system) == value(g, coding, FHIR.Coding.system):
                return value(g, coding, FHIR.Coding.code, asLiteral=asLiteral)
    return None


def concept_uri(g: Graph, subject: Node, predicate: URIRef, system: Optional[Union[URIRef, str]]=None) ->\
        Union[URIRef, None]:
    c = g.value(subject, predicate)
    if c:
        for coding in g.objects(c, FHIR.CodeableConcept.coding):
            if not system or str(system) == value(g, coding, FHIR.Coding.system):
                return value(g, coding, RDF.type, asLiteral=True)
    return None


def link(g: Graph, subject: Node, predicate: URIRef) -> Tuple[Optional[URIRef], Optional[URIRef]]:
    """
    Return the link URI and link type for subject and predicate
    :param g: graph context
    :param subject: subject of linke
    :param predicate: link predicate
    :return: URI and optional type URI.  URI is None if not a link
    """
    link_node = g.value(subject, predicate)
    if link_node:
        l = g.value(link_node, FHIR.link)
        if l:
            typ = g.value(l, RDF.type)
            return l, typ
    return None, None


class CodeableConcept:
    def __init__(self, system: str, code_: str, uri: Optional[URIRef]=None):
        self.system = system
        self.code = code_
        self.uri = uri

    def __lt__(self, other):
        return repr(self) < repr(other)

    def __eq__(self, other):
        return repr(self) == repr(other)

    def __repr__(self):
        return "({}, {}, {})".format(self.system, self.code, self.uri)

    def __str__(self):
        return 'CodeableConcept("{}", "{}", {})'.format(self.system, self.code,
                                                        'URIRef("{}")'.format(self.uri) if self.uri else "None")


def codeable_concept_code(g: Graph, subject: Node, predicate: URIRef, system: Optional[str]=None) \
        -> List[CodeableConcept]:
    """
    Return a list of CodeableConcept entries for the supplied subject and predicate in graph g
    :param g: graph containing the data
    :param subject: subject
    :param predicate: predicate
    :param system: coding system.  If present, only concepts in this system will be returned
    :return: system, code and optional URI of matching concept(s)
    """
    # EXAMPLE:
    # fhir:Patient.maritalStatus [
    #    fhir:CodeableConcept.coding [
    #      fhir:index 0;
    #      a sct:36629006;
    #      fhir:Coding.system [ fhir:value "http://snomed.info/sct" ];
    #      fhir:Coding.code [ fhir:value "36629006" ];
    #      fhir:Coding.display [ fhir:value "Legally married" ]
    #    ], [
    #      fhir:index 1;
    #      fhir:Coding.system [ fhir:value "http://hl7.org/fhir/v3/MaritalStatus" ];
    #      fhir:Coding.code [ fhir:value "M" ]
    #    ]
    # ];
    rval = []
    coded_entry = g.value(subject, predicate, any=False)
    if coded_entry:
        for codeable_concept in list(g.objects(coded_entry, FHIR.CodeableConcept.coding)):
            coding_system = value(g, codeable_concept, FHIR.Coding.system)
            coding_code = value(g, codeable_concept, FHIR.Coding.code)
            if coding_system and coding_code and (system is None or system == coding_system):
                rval.append(CodeableConcept(coding_system, coding_code, g.value(codeable_concept, RDF.type, any=False)))
    return rval

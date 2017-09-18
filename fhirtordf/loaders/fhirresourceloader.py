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

import re
import urllib
from typing import Union, List, Optional, Dict
from urllib.parse import urlencode
from uuid import uuid4

from jsonasobj.jsonobj import JsonObj, load, JsonObjTypes
from rdflib import Graph, OWL, RDF, URIRef, Namespace
from rdflib.term import Node, BNode, Literal

from fhirtordf.fhir.fhirmetavoc import FHIRMetaVocEntry
from fhirtordf.rdfsupport.fhirgraphutils import value
from fhirtordf.rdfsupport.namespaces import FHIR, LOINC, SNOMEDCT, namespaces
from fhirtordf.rdfsupport.fhirresourcere import FHIR_RESOURCE_RE, FHIR_RE_BASE, FHIR_RE_RESOURCE, \
    REPLACED_NARRATIVE_TEXT
from fhirtordf.rdfsupport.prettygraph import PrettyGraph


def loinc_uri(_: str, code: str, nsmap: Dict[str, Namespace]) -> Optional[URIRef]:
    nsmap.setdefault('loinc', LOINC)
    return LOINC[code]


def snomed_uri(_: str, code: str, nsmap: Dict[str, Namespace]) -> Optional[URIRef]:
    nsmap.setdefault('sct', SNOMEDCT)
    return SNOMEDCT[code] if code.isdigit() else None


def hl7_v3_uri(system: str, code: str, nsmap: Dict[str, Namespace]) -> Optional[URIRef]:
    nsmap.setdefault('v3-' + system.replace('http://hl7.org/fhir/v3/', ''), Namespace(system))
    return URIRef(system + '/' + code)


def hl7_v2_uri(system: str, code: str, nsmap: Dict[str, Namespace]) -> Optional[URIRef]:
    nsmap.setdefault('v2-' + system.replace('http://hl7.org/fhir/v2/', ''), Namespace(system))
    return URIRef(system + '/' + code)


def hl7_fhir_uri(system: str, code: str, nsmap: Dict[str, Namespace]) -> Optional[URIRef]:
    nsmap.setdefault(system.replace('http://hl7.org/fhir/', '').replace('/', '_'), Namespace(system))
    return URIRef(system + '/' + code)


# Map from FHIR codesystem URI to generator
codesystem_maps = {"http://loinc.org": loinc_uri,
                   "http://snomed.info/sct": snomed_uri,
                   re.compile(r"http://hl7.org/fhir/v3/*"): hl7_v3_uri,
                   re.compile(r"http://hl7.org/fhir/v2/*"): hl7_v2_uri,
                   re.compile(r"http://hl7.org/fhir/[a-z-]+"): hl7_fhir_uri}


class FHIRResource:
    """ A FHIR RDF representation of a FHIR JSON resource """
    def __init__(self, vocabulary: Graph, json_fname: Optional[str], base_uri: str,
                 data: Optional[JsonObj]=None, target: Optional[Graph]=None, add_ontology_header: bool=True,
                 replace_narrative_text: bool=False, is_root=True, resource_uri: Optional[URIRef]=None):
        """
        Construct an RDF representation
        :param vocabulary: FHIR Metadata Vocabulary (fhir.ttl)
        :param json_fname: URI or file name of resource to convert
        :param base_uri: base of resource URI -- will be combined with the resource id to generate the actual URI
        :param data: if present load this data rather than json_fname
        :param target: target graph -- used for collections, bundles, etc.
        :param add_ontology_header: Add the OWL ontology header to the output
        :param replace_narrative_text: Replace long narrative text section with boilerplate
        :param is_root: True means this is a root node, False a component
        :param resource_uri: If present, this becomes the resource subject
        """
        if json_fname:
            self.root = load(json_fname)
        elif data:
            self.root = data
        else:
            assert False, "Either a json file name or actual data image must be supplied"
        self._base_uri = base_uri + ('/' if base_uri[-1] not in '/#' else '')
        if 'resourceType' not in self.root:
            raise ValueError("{} is not a FHIR resource".format(json_fname))
        if resource_uri:
            self._resource_uri = resource_uri
        else:
            if 'id' not in self.root:
                self.root.id = str(uuid4())
            self._resource_uri = URIRef(self._base_uri + self.root.resourceType + '/' + self.root.id)
        self._meta = FHIRMetaVocEntry(vocabulary, FHIR[self.root.resourceType])
        self._g = PrettyGraph() if target is None else target
        self._vocabulary = vocabulary
        self._addl_namespaces = dict()
        self._add_ontology_header = add_ontology_header
        self._replace_narrative_text = replace_narrative_text
        self.generate(is_root)

    @property
    def resource_id(self) -> Optional[str]:
        return value(self._g, self._resource_uri, FHIR.Resource.id)

    @property
    def resource_type(self) -> str:
        return self.root.resourceType

    @property
    def graph(self):
        return self._g

    def add_prefixes(self, nsmap: Dict[str, Namespace]) -> None:
        """
        Add the required prefix definitions
        :return:
        """
        [self._g.bind(e[0], e[1]) for e in nsmap.items()]

    def add_ontology_definition(self) -> None:
        ont_uri = URIRef(str(self._resource_uri) + ".ttl")
        self.add(ont_uri, RDF.type, OWL.Ontology)\
            .add(ont_uri, OWL.imports, FHIR['fhir.ttl'])
        if 'meta' in self.root and 'versionId' in self.root.meta:
            self.add(ont_uri, OWL.versionIRI, URIRef(str(ont_uri) + '/_history/' + self.root.meta.versionId))

    def add(self, subj: Node, pred: URIRef, obj: Node) -> "FHIRResource":
        """
        Shortcut to rdflib add function
        :param subj:
        :param pred:
        :param obj:
        :return: self for chaining
        """
        self._g.add((subj, pred, obj))
        return self

    def add_value_node(self, subj: Node, pred: URIRef, val: Union[JsonObj, str, List],
                       valuetype: Optional[URIRef]= None) -> None:
        """
        Expand val according to the range of pred and add it to the graph
        :param subj: graph subject
        :param pred: graph predicate
        :param val: JSON representation of target object
        :param valuetype: predicate type if it can't be directly determined
        """
        pred_type = self._meta.predicate_type(pred) if not valuetype else valuetype
        # Transform generic resources into specific types
        if pred_type == FHIR.Resource:
            pred_type = FHIR[val.resourceType]

        val_meta = FHIRMetaVocEntry(self._vocabulary, pred_type)
        for k, p in val_meta.predicates().items():
            if k in val:
                self.add_val(subj, p, val, k)
                if pred == FHIR.CodeableConcept.coding:
                    self.add_type_arc(subj, val)
            elif k == "value" and val_meta.predicate_type(p) == FHIR.Element:
                # value / Element is the wild card combination -- if there is a "value[x]" in val, emit it where the
                # type comes from 'x'
                for vk in val._as_dict.keys():
                    if vk.startswith(k):
                        self.add_val(subj, FHIR['Extension.' + vk], val, vk, self._meta.value_predicate_to_type(vk))
            else:
                # Can have an extension only without a primary value
                self.add_extension_val(subj, val, k, p)

    def add_reference(self, subj: Node, val: str) -> None:
        """
        Add a fhir:link and RDF type arc if it can be determined
        :param subj: reference subject
        :param val: reference value
        """
        match = FHIR_RESOURCE_RE.match(val)
        ref_uri_str = res_type = None
        if match:
            ref_uri_str = val if match.group(FHIR_RE_BASE) else (self._base_uri + urllib.parse.quote(val))
            res_type = match.group(FHIR_RE_RESOURCE)
        elif '://' in val:
            ref_uri_str = val
            res_type = "Resource"
        elif self._base_uri and not val.startswith('#') and not val.startswith('/'):
            ref_uri_str = self._base_uri + urllib.parse.quote(val)
            res_type = val.split('/', 1)[0] if '/' in val else "Resource"
        if ref_uri_str:
            ref_uri = URIRef(ref_uri_str)
            self.add(subj, FHIR.link, ref_uri)
            self.add(ref_uri, RDF.type, FHIR[res_type])

    def add_type_arc(self, subj: Node, val: JsonObj) -> None:
        if "system" in val and "code" in val:
            for k in codesystem_maps.keys():
                if (isinstance(k, str) and k == val.system) or (not isinstance(k, str) and k.match(val.system)):
                    type_uri = codesystem_maps[k](val.system, urllib.parse.quote(val.code), self._addl_namespaces)
                    if type_uri:
                        self.add(subj, RDF.type, type_uri)
                    break

    def node_subject(self, list_idx: int, subj: Node, pred: URIRef, node: JsonObj) -> Node:
        if pred == FHIR.Bundle.entry:
            entry = BNode()
            self.add(entry, FHIR.index, Literal(list_idx))
            self.add_val(entry, FHIR.Bundle.entry.fullUrl, node, 'fullUrl')
            self.add(entry, FHIR.Bundle.entry.resource, URIRef(node.fullUrl))
            self.add(subj, pred, entry)
            return URIRef(node.fullUrl)
        else:
            return BNode()

    def add_val(self, subj: Node, pred: URIRef, json_obj: JsonObj, json_key: str,
                valuetype: Optional[URIRef] = None) -> Optional[BNode]:
        """
        Add the RDF representation of val to the graph as a target of subj, pred.  Note that FHIR lists are
        represented as a list of BNODE objects with a fhir:index discrimanant
        :param subj: graph subject
        :param pred: predicate
        :param json_obj: object containing json_key
        :param json_key: name of the value in the JSON resource
        :param valuetype: value type if NOT determinable by predicate
        :return: value node if target is a BNode else None
        """
        if json_key not in json_obj:
            print("Expecting to find object named '{}' in JSON:".format(json_key))
            print(json_obj._as_json_dumps())
            print("entry skipped")
            return None
        val = json_obj[json_key]
        if isinstance(val, List):
            list_idx = 0
            for lv in val:
                entry_bnode = BNode()
                # TODO: this is getting messy. Refactor and clean this up
                if pred == FHIR.Bundle.entry:
                    entry_subj = URIRef(lv.fullUrl)
                    self.add(entry_bnode, FHIR.index, Literal(list_idx))
                    self.add_val(entry_bnode, FHIR.Bundle.entry.fullUrl, lv, 'fullUrl')
                    self.add(entry_bnode, FHIR.Bundle.entry.resource, entry_subj)
                    self.add(subj, pred, entry_bnode)
                    entry_mv = FHIRMetaVocEntry(self._vocabulary, FHIR.BundleEntryComponent)
                    for k, p in entry_mv.predicates().items():
                        if k not in ['resource', 'fullUrl'] and k in lv:
                            print("---> adding {}".format(k))
                            self.add_val(subj, p, lv, k)
                    FHIRResource(self._vocabulary, None,  self._base_uri, lv.resource, self._g,
                                 False, self._replace_narrative_text, False, resource_uri=entry_subj)
                else:
                    self.add(entry_bnode, FHIR.index, Literal(list_idx))
                    if isinstance(lv, JsonObj):
                        self.add_value_node(entry_bnode, pred, lv, valuetype)
                    else:
                        vt = self._meta.predicate_type(pred)
                        atom_type = self._meta.primitive_datatype_nostring(vt) if vt else None
                        self.add(entry_bnode, FHIR.value, Literal(lv, datatype=atom_type))
                    self.add(subj, pred, entry_bnode)
                list_idx += 1
        else:
            vt = self._meta.predicate_type(pred) if not valuetype else valuetype
            if self._meta.is_atom(pred):
                if self._replace_narrative_text and pred == FHIR.Narrative.div and len(val) > 120:
                    val = REPLACED_NARRATIVE_TEXT
                self.add(subj, pred, Literal(val))
            else:
                v = BNode()
                if self._meta.is_primitive(vt):
                    self.add(v, FHIR.value, Literal(str(val), datatype=self._meta.primitive_datatype_nostring(vt, val)))
                else:
                    self.add_value_node(v, pred, val, valuetype)
                self.add(subj, pred, v)
                if pred == FHIR.Reference.reference:
                    self.add_reference(subj, val)
                self.add_extension_val(v, json_obj, json_key)
                return v
        return None

    def add_extension_val(self,
                          subj: Node,
                          json_obj:
                          Union[JsonObj, List[JsonObjTypes]],
                          key: str,
                          pred: Optional[URIRef] = None) -> None:
        """
        Add any extensions for the supplied object. This can be called in following situations:
        1) Single extended value 
                "key" : (value),
                "_key" : {
                    "extension": [
                       {
                        "url": "http://...",
                        "value[x]": "......" 
                       }
                    ]
                }
        2) Single extension only
                "_key" : {
                    "extension": [
                       {
                        "url": "http://...",
                        "value[x]": "......" 
                       }
                    ]
                }
        3) Multiple extended values:
                (TBD)
                
        4) Multiple extensions only
                "_key" : [
                  { 
                    "extension": [
                       {
                        "url": "http://...",
                        "value[x]": "......" 
                       }
                    ]
                  }
                ]
                    
        :param subj: Node containing subject
        :param json_obj: Object (potentially) containing "_key"
        :param key: name of element that is possibly extended (as indicated by "_" prefix)
        :param pred: predicate for the contained elements. Only used in situations 3) (?) and 4 
        """
        extendee_name = "_" + key
        if extendee_name in json_obj:
            if not isinstance(subj, BNode):
                raise NotImplementedError("Extension to something other than a simple BNode")
            if isinstance(json_obj[extendee_name], list):
                if not pred:
                    raise NotImplemented("Case 3 not implemented")
                entry_idx = 0
                for extension in json_obj[extendee_name]:
                    entry = BNode()
                    self.add(entry, FHIR.index, Literal(entry_idx))
                    self.add_val(entry, FHIR.Element.extension, extension, 'extension')
                    self.add(subj, pred, entry)
                    entry_idx += 1
            elif 'fhir_comments' in json_obj[extendee_name] and len(json_obj[extendee_name]) == 1:
                # TODO: determine whether and how fhir comments should be represented in RDF.
                # for the moment we just drop them
                print("fhir_comment ignored")
                print(json_obj[extendee_name]._as_json_dumps())
                pass
            else:
                self.add_val(subj, FHIR.Element.extension, json_obj[extendee_name], 'extension')

    def add_resource(self, subj: URIRef, json_obj: JsonObj):
        self.add(subj, RDF.type, FHIR[json_obj.resourceType])
        for k, p in self._meta.predicates().items():
            if k in json_obj:
                self.add_val(subj, p, json_obj, k)

    def generate(self, is_root: bool) -> Graph:
        if is_root:
            self.add_prefixes(namespaces)
            if self._add_ontology_header:
                self.add_ontology_definition()
            self.add(self._resource_uri, FHIR.nodeRole, FHIR.treeRoot)
        self.add_resource(self._resource_uri, self.root)
        self.add_prefixes(self._addl_namespaces)
        return self._g

    def __str__(self):
        return self._g.serialize().decode()

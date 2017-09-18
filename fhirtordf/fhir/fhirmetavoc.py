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
"""
FHIR Metadata Vocabulary -- a representation for the metadata about a FHIR class URI.
"""
from typing import Union, Dict, Optional
from rdflib import Graph, URIRef, RDFS, RDF, OWL, XSD

from fhirtordf.fhir.signature import signature
from fhirtordf.rdfsupport.namespaces import FHIR, W5
from fhirtordf.fhir.picklejar import picklejar


class FHIRMetaVocEntry:
    # True means use gYear, gYearMonth, date and datetime
    # False means use OWL dates (datetime)
    fhir_dates = True

    # FHIR doesn't attach the anyURI to an oid
    fhir_oids = True

    """
    FHIR metadata vocbulary for a given subject
    """
    def __init__(self, ontology: Graph, subject: Union[str, URIRef]):
        """
        Represent FHIR metadata for subject
        :param ontology: FHIR "ontology" (fhir.ttl)
        :param subject: name or URI of subject in ontology
        """
        self._o = ontology
        self._subj = subject if isinstance(subject, URIRef) else URIRef(FHIR[subject])

    @staticmethod
    def _to_str(uri: URIRef) -> str:
        """
        Convert a FHIR style URI into a tag name to be used to retrieve data from a JSON representation
        Example: http://hl7.org/fhir/Provenance.agent.whoReference --> whoReference
        :param uri: URI to convert
        :return: tag name
        """
        local_name = str(uri).replace(str(FHIR), '')
        return local_name.rsplit('.', 1)[1] if '.' in local_name else local_name

    def predicates(self) -> Dict[str, URIRef]:
        """
        Return the tag names and corresponding URI's for all properties that can be associated with subject
        :return: Map from tag name (JSON object identifier) to corresponding URI
        """
        rval = dict()
        for parent in self._o.objects(self._subj, RDFS.subClassOf):
            if isinstance(parent, URIRef) and not str(parent).startswith(str(W5)):
                rval.update(**FHIRMetaVocEntry(self._o, parent).predicates())
        for s in self._o.subjects(RDFS.domain, self._subj):
            rval[self._to_str(s)] = s
        return rval

    def predicate_type(self, pred: URIRef) -> URIRef:
        """
        Return the type of pred
        :param pred: predicate to map
        :return:
        """
        return self._o.value(pred, RDFS.range)

    def has_type(self, t: URIRef) -> bool:
        return (t, None, None) in self._o

    def is_valid(self, t: URIRef) -> bool:
        """
        Raise an exception if 't' is unrecognized
        :param t: metadata URI
        """
        if not self.has_type(t):
            raise TypeError("Unrecognized FHIR type: {}".format(t))
        return True

    def is_primitive(self, t: URIRef) -> bool:
        """
        Determine whether type "t" is a FHIR primitive type
        :param t: type to test
        :return:
        """
        return FHIR.Primitive in self._o.objects(t, RDFS.subClassOf)

    def value_predicate_to_type(self, value_pred: str) -> URIRef:
        """
        Convert a predicate in the form of "fhir:[...].value[type] to fhir:type, covering the downshift on the
        first character if necessary
        :param value_pred: Predicate associated with the value
        :return: corresponding type or None if not found
        """
        if value_pred.startswith('value'):
            vp_datatype = value_pred.replace('value', '')
            if vp_datatype:
                if self.has_type(FHIR[vp_datatype]):
                    return FHIR[vp_datatype]
                else:
                    vp_datatype = vp_datatype[0].lower() + vp_datatype[1:]
                    if self.has_type(FHIR[vp_datatype]):
                        return FHIR[vp_datatype]
        if self.is_valid(FHIR[value_pred]):
            return FHIR[value_pred]

    def is_atom(self, pred: URIRef) -> bool:
        """
        Determine whether predicate is an 'atomic' type -- i.e it doesn't use a FHIR value representation
        :param pred: type to test
        :return:
        """
        if not self.has_type(pred):
            if '.value' in str(pred):               # synthetic values (valueString, valueDate, ...)
                return False
            else:
                raise TypeError("Unrecognized FHIR predicate: {}".format(pred))
        return pred == FHIR.nodeRole or OWL.DatatypeProperty in set(self._o.objects(pred, RDF.type))

    def primitive_datatype(self, t: URIRef) -> Optional[URIRef]:
        """
        Return the data type for primitive type t, if any
        :param t: type
        :return: corresponding data type
        """
        for sco in self._o.objects(t, RDFS.subClassOf):
            sco_type = self._o.value(sco, RDF.type)
            sco_prop = self._o.value(sco, OWL.onProperty)
            if sco_type == OWL.Restriction and sco_prop == FHIR.value:
                return self._o.value(sco, OWL.allValuesFrom)
        return None

    def primitive_datatype_nostring(self, t: URIRef, v: Optional[str] = None) -> Optional[URIRef]:
        """
        Return the data type for primitive type t, if any, defaulting string to no type
        :param t: type
        :param v: value - for munging dates if we're doing FHIR official output
        :return: corresponding data type
        """
        vt = self.primitive_datatype(t)
        if self.fhir_dates and vt == XSD.dateTime and v:
            return XSD.gYear if len(v) == 4 else XSD.gYearMonth if len(v) == 7 \
                else XSD.date if (len(v) == 10 or (len(v) > 10 and v[10] in '+-')) else XSD.dateTime
        # For some reason the oid datatype is represented as a string as well
        if self.fhir_oids and vt == XSD.anyURI:
            vt = None
        return None if vt == XSD.string else vt


class FHIRMetaVoc:

    def __init__(self, mv_file_loc: str="http://build.fhir.org/fhir.ttl", fmt: str="turtle", cache_mv_file=True):
        """
        Load a FHIR Metadata Vocabulary image
        :param mv_file_loc: file name or URI of fhir.ttl image
        :param fmt: format of image
        :param cache_mv_file: True means cache an image in ~/.cache/.  False means no cache
        """
        self.g = picklejar().get(mv_file_loc, signature(mv_file_loc)) if cache_mv_file else None
        if not self.g:
            self.from_cache = False
            self.g = Graph()
            self.g.load(mv_file_loc, format=fmt)
            if cache_mv_file:
                picklejar().add(mv_file_loc, signature(mv_file_loc), self.g)
        else:
            self.from_cache = True

    def entry_for(self, subject: Union[str, URIRef]) -> FHIRMetaVocEntry:
        return FHIRMetaVocEntry(self.g, subject)

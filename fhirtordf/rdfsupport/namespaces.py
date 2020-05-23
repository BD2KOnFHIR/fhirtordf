from typing import Union

from rdflib import Namespace, OWL, RDFS, RDF, XSD, URIRef

from fhirtordf.rdfsupport.dottednamespace import DottedNamespace

# TODO: Determine what these various namespaces should actually be
from fhirtordf.rdfsupport.numericnamespace import NumericNamespace

W5 = DottedNamespace("http://hl7.org/fhir/w5#")
FHIR = DottedNamespace("http://hl7.org/fhir/")
LOINC = Namespace("http://loinc.org/rdf#")
SNOMEDCT = Namespace("http://snomed.info/id/")
RXNORM = Namespace("http://www.nlm.nih.gov/research/umls/rxnorm/")
V3 = Namespace("http://hl7.org/fhir/v3/")
V2 = Namespace("http://hl7.org/fhir/v2/")
SCT = NumericNamespace("http://snomed.info/id/")

namespaces = {"fhir": str(FHIR),
              "owl": str(OWL),
              "rdfs": str(RDFS),
              "rdf": str(RDF),
              "xsd": str(XSD),
              "w5": str(W5),
              "v2": str(V2),
              "v3": str(V3),
              "sct": str(SCT),
              "loinc": str(LOINC),
              "rxnorm": str(RXNORM)}


class AnonNS:
    _nsnum = 0

    def __init__(self):
        AnonNS._nsnum += 1
        self.ns = 'ns{}'.format(self._nsnum)


def namespace_for(uri: Union[URIRef, Namespace, str]) -> str:
    """
    Reverse namespace lookup.  Note that returned namespace may not be unique
    :param uri: namespace URI
    :return: namespace
    """
    uri = str(uri)
    if uri not in namespaces.values():
        namespaces[AnonNS().ns] = uri
    return [k for k, v in namespaces.items() if uri == v][0]

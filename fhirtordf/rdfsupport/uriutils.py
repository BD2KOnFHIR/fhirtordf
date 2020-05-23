from typing import Tuple, NamedTuple, Union, Optional

from rdflib import URIRef

from fhirtordf.rdfsupport.fhirresourcere import FHIR_RESOURCE_RE, FHIR_RE_ID, FHIR_RE_BASE, FHIR_RE_RESOURCE
from fhirtordf.rdfsupport.namespaces import FHIR


class FHIR_RESOURCE(NamedTuple):
    namespace: Optional[URIRef]
    resource_type: Optional[URIRef]
    resource: str


def parse_fhir_resource_uri(uri: Union[URIRef, str]) -> FHIR_RESOURCE:
    """
    Use the FHIR Regular Expression for Resource URI's to determine the namespace and type
    of a given URI.  As an example, "http://hl7.org/fhir/Patient/p123" maps to the tuple
    ``('Patient', 'http://hl7.org/fhir')

    :param uri:  URI to parse
    :return: FHIR_RESOURCE (namespace, type, resource)
    """
    uri_str = str(uri)
    m = FHIR_RESOURCE_RE.match(uri_str)
    if m:
        return FHIR_RESOURCE(URIRef(m.group(FHIR_RE_BASE)), FHIR[m.group(FHIR_RE_RESOURCE)], m.group(FHIR_RE_ID))
    else:
        # Not in the FHIR format - we can only do namespace and name
        namespace, name = uri_str.rsplit('#', 1) if '#' in uri_str \
            else uri_str.rsplit('/', 1) if '/' in uri_str else (None, uri_str)

        return FHIR_RESOURCE(URIRef(namespace), None, name)

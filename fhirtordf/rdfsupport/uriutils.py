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

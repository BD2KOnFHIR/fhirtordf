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
from typing import Tuple

from rdflib import URIRef

from i2fhirb2.fhir.fhirspecific import FHIR_RESOURCE_RE, FHIR_RE_ID, FHIR_RE_BASE, FHIR_RE_RESOURCE


def uri_to_ide_and_source(uri: URIRef, include_resource: bool=False) -> Tuple[str, str]:
    """
    Convert a  URI into a identifier/ identifier source tuple
    :param uri:  URI
    :param include_resource: If true, resource type becomes part of the identifier
    :return: ide, ide_source
    """
    uri_str = str(uri)
    m = FHIR_RESOURCE_RE.match(uri_str)
    if m:
        ide = ((m.group(FHIR_RE_RESOURCE) + '/') if include_resource else '') + m.group(FHIR_RE_ID)
        ide_source = m.group(FHIR_RE_BASE)
    else:
        # Assume no history entry if not FHIR format...
        ide_source, ide = uri_str.rsplit('#', 1) if '#' in uri_str \
            else uri_str.rsplit('/', 1) if '/' in uri_str else ('UNKNOWN', uri_str)
    return ide, ide_source

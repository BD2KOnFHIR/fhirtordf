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

from rdflib import Namespace, URIRef


class DottedNamespace(Namespace):
    """
    An RDF namespace that supports the FHIR dotted notation (e.g. fhir:Patient.status)
    """
    def __new__(cls, value):
        return Namespace.__new__(cls, value)

    def __getattribute__(self, item: str) -> "DottedURIRef":
        if item == 'index':
            return DottedURIRef(str(self) + item)
        else:
            return super().__getattribute__(item)

    def __getattr__(self, item: str) -> "DottedURIRef":
        return DottedURIRef(str(self) + item)

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class DottedURIRef(URIRef):
    """
    A URIRef that supports the FHIR dotted notation
    """
    def __new__(cls, value, base=None):
        return URIRef.__new__(cls, value, base)

    def __getattr__(self, item: str) -> "DottedURIRef":
        return DottedURIRef(str(self) + '.' + item)

    def __eq__(self, other):
        if isinstance(self, URIRef) and isinstance(other, URIRef):
            return str(self) == str(other)
        else:
            return False

    def __hash__(self):
        fqn = URIRef.__module__ + '.' + URIRef.__name__
        return hash(fqn) ^ hash(str(self))

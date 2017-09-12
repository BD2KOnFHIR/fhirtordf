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
from typing import Optional, List

from jsonasobj import JsonObj, load
from rdflib import Graph

from fhirtordf.loaders.fhirresourceloader import FHIRResource


class FHIRCollection:
    """ FHIR JSON collection to RDF conversion utility.  This tool takes a collection of json "entry" elements
     and generates a list of FHIRResource elements from the entries in the collection.  The JSON file itself can have
     an optional collection header.
     """
    def __init__(self, vocabulary: Graph, json_fname: Optional[str], base_uri: str, data: Optional[JsonObj] = None,
                 add_ontology_header: Optional[bool] = True, replace_narrative_text: Optional[bool] = False,
                 target: Optional[Graph] = None):
        """
        Convert a JSON collection into RDF.
        :param vocabulary: fhir metadata vocabulary
        :param json_fname: name or URI of the FHIR json collection to convert
        :param base_uri: URI to use as a base for identifiers
        :param data: JsonObj to use if json fname is not present
        :param add_ontology_header: Include the OWL:Ontology declaration
        :param replace_narrative_text: Replace long narrative text with REPLACED_NARRATIVE_TEXT
        :param target: Target graph -- load everything into this if present
        """
        collection = load(json_fname) if json_fname else data

        self.entries = []           # type: List[FHIRResource]
        for entry in collection.entry:
            if 'resource' in entry:
                self.entries.append(FHIRResource(vocabulary, None, base_uri, data=entry.resource,
                                                 add_ontology_header=add_ontology_header,
                                                 replace_narrative_text=replace_narrative_text, target=target))

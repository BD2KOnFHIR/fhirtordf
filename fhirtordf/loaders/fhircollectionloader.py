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

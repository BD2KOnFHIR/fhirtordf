from typing import Optional, Union

from jsonasobj import load, JsonObj
from rdflib import Graph, URIRef

from fhirtordf.fhir.fhirmetavoc import FHIRMetaVoc
from fhirtordf.loaders.fhircollectionloader import FHIRCollection
from fhirtordf.loaders.fhirresourceloader import FHIRResource


def fhir_json_to_rdf(json_fname: str,
                     base_uri: str = "http://hl7.org/fhir/",
                     target_graph: Optional[Graph] = None,
                     add_ontology_header: bool = True,
                     do_continuations: bool = True,
                     replace_narrative_text: bool = False,
                     metavoc: Optional[Union[Graph, FHIRMetaVoc]] = None) -> Graph:
    """
    Convert a FHIR JSON resource image to RDF
    :param json_fname: Name or URI of the file to convert
    :param base_uri: Base URI to use for relative references.
    :param target_graph:  If supplied, add RDF to this graph. If not, start with an empty graph.
    :param add_ontology_header:  True means add owl:Ontology declaration to output
    :param do_continuations: True means follow continuation records on bundles and queries
    :param replace_narrative_text: True means replace any narrative text longer than 120 characters with
                '<div xmlns="http://www.w3.org/1999/xhtml">(removed)</div>'
    :param metavoc: FHIR Metadata Vocabulary (fhir.ttl) graph
    :return: resulting graph
    """

    def check_for_continuation(data_: JsonObj) -> Optional[str]:
        if do_continuations and 'link' in data_ and isinstance(data_.link, list):
            for link_e in data_.link:
                if 'relation' in link_e and link_e.relation == 'next':
                    return link_e.url
        return None

    if target_graph is None:
        target_graph = Graph()

    if metavoc is None:
        metavoc = FHIRMetaVoc().g
    elif isinstance(metavoc, FHIRMetaVoc):
        metavoc = metavoc.g

    page_fname = json_fname
    while page_fname:
        data = load(page_fname)
        if 'resourceType' in data and data.resourceType != 'Bundle':
            FHIRResource(metavoc, None, base_uri, data, target=target_graph, add_ontology_header=add_ontology_header,
                         replace_narrative_text=replace_narrative_text)
            page_fname = check_for_continuation(data)
        elif 'entry' in data and isinstance(data.entry, list) and 'resource' in data.entry[0]:
            FHIRCollection(metavoc, None, base_uri, data, target=target_graph,
                           add_ontology_header=add_ontology_header if 'resourceType' in data else False,
                           replace_narrative_text=replace_narrative_text)
            page_fname = check_for_continuation(data)
        else:
            page_fname = None
            target_graph = None
    return target_graph

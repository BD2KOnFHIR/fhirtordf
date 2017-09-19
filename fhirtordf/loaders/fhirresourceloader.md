# fhirresourceloader.py
This package does all the heavy lifting when converting FHIR JSON into FHIR RDF. 
## Summary
The `FHIRResource` class takes the following arguments:
* `vocabulary` - an RDF graph containing an image of the FHIR Metadata Vocabulary (fhir.ttl)
* `json_fname` - (optional) the URI or name of a FHIR Resource in JSON format.  If not present, the image of an already parsed JSON object is supplied in the `data` parameter.
* `base_uri` - the base URI for the resource represented by the JSON file. This URI becomes the base for any [FHIR References](http://hl7.org/fhir/references.html) in the resource(s).
* `data` - (optional) a [`JsonAsObj`](https://github.com/hsolbrig/jsonasobj) image of a FHIR JSON resource.
* `target` - (optional) the RDF graph in which the converted resources are stored.  This parameter allows multiple resources (including embedded resources) to be stored as a single graph.  If omitted, a new target graph will be created.
* `add_ontology_header` - A boolean parameter.  If `True`, an `owl:Ontology` assertion will be added to the output graph.
* `replace_narrative_text` - A boolean parameter. If `True` instances of
`fhir:Narrative.div` will be replaced by [`REPLACED_NARRATIVE_TEXT`](../fhir/fhirspecific.py) if the text is longer than 120 characters.

## Methods
### `resource_id`
The string representation of the resource URI for this resource.  This becomes the `encounter_ide / encounter_ide_source` entries in the `encounter_mapping` table
### `resource_type`
The value of the JSON `"resourceType"` entry.
### `graph`
The target RDF graph
### `add_prefixes(nsmap)`
Add `@prefix` declarations for the set of prefix / (RDF) Namespace items supplied in nsmap
### `add_ontology_definition()`
Generate and add an `owl:Ontology` declaration for the resource.  This takes the form:
```text
    [resource_id] a owl:Ontology;
        owl:imports fhir:fhir.ttl;
        owl:versionIRI [resource_id]/_history/[version_id].
```
Note that the versionIRI will be added only in the case that the resource 
contains a `"meta"` object which carries a '"versionId"'.  As an example, the resource (http://hl7.org/fhir/Bundle/lri-example.json), which contains:
```json
{
  "resourceType": "Bundle",
  "id": "lri-example",
  "meta": {
    "versionId": "1",
    "lastUpdated": "2017-06-27T00:52:51Z"
  },
  ...
```
Would generate the following ontology header:
```text
<http://hl7.org/fhir/Bundle/lri-example.ttl> a owl:Ontology;
  owl:imports fhir:fhir.ttl;
  owl:versionIRI <http://build.fhir.org/Bundle/lri-example/_history/1> .
```
### add(subj, pred, obj)
Shortcut to the [rdflib](https://rdflib.readthedocs.io/en/stable/) graph add function. This is here because the rdflib function requires a tuple and programmers always forget it.

### add_value_node(subj, pred, val, valuetype)

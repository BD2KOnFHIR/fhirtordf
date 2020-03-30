# FHIR JSON to RDF conversion utility

A tool to convert FHIR Resources from the JSON format to their equivalent in the FHIR RDF format.  This tool can be used to convert FHIR queries, bundles and individual FHIR resources.  It can be used to load an `rdflib` instance of the resource(s) for further processing and/or to create RDF output files.


[![PyPi](https://version-image.appspot.com/pypi/?name=fhirtordf)](https://pypi.python.org/pypi/fhirtordf)

[![Pyversions](https://img.shields.io/pypi/pyversions/fhirtordf.svg)](https://pypi.python.org/pypi/fhirtordf)

## Warning!!!
The FHIR R4 Build (http://hl7.org/fhir) no longer has the FHIR Structured Vocabulary (fhir.ttl), which makes R4 conversions
exceedingly difficult.  Anywhere that the text `http://hl7.org/fhir/fhir.ttl` appears below, you will need to use a local
copy of fhir.ttl, which can be found in [tests/data/fhir_metadata_vocabulary/fhir.ttl]()

## History
* 1.0.0 - Initial Drop
* 1.1.0 - Remove uri_to_ide_and_source method from uriutils and add parse_fhir_resource_uri 
* 1.2.0 - Fix error in LOINC namespace. FHIR uses http://loinc.org/rdf# (not good but...)
* 1.2.1 - Fix issue #12 - SCT is a numeric namespace

## Example:

```text
> fhirtordf -i http://hl7.org/fhir/Patient/f201 -nn
@prefix fhir: <http://hl7.org/fhir/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sct: <http://snomed.info/id/> .
@prefix v2-0131: <http://hl7.org/fhir/v2/0131> .
@prefix v3-MaritalStatus: <http://hl7.org/fhir/v3/MaritalStatus> .
@prefix v3-RoleCode: <http://hl7.org/fhir/v3/RoleCode> .
@prefix w5: <http://hl7.org/fhir/w5#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<http://hl7.org/fhir/Patient/f201> a fhir:Patient ;
    fhir:nodeRole fhir:treeRoot ;
    fhir:DomainResource.text [
        fhir:Narrative.div "<div xmlns=\"http://www.w3.org/1999/xhtml\">(removed)</div>" ;
        fhir:Narrative.status [
            fhir:value "generated"
        ]
    ] ;
    fhir:Patient.active [
        fhir:value "true"^^xsd:boolean
    ] ;
    fhir:Patient.address [
        fhir:index "0"^^xsd:integer ;
        fhir:Address.city [
            fhir:value "Amsterdam"
        ] ;
        fhir:Address.country [
            fhir:value "NLD"
        ] ;
        fhir:Address.line [
            fhir:index "0"^^xsd:integer ;
    ...

```

## Installation

### Requirements
This package requires [python](https://www.python.org/) 3. It has been developed and tested with [python 3.6.1](https://www.python.org/downloads/release/python-361/).

### Create a virtual environment (optional)
The [`virtualenv`](https://virtualenv.pypa.io/en/stable/) package allows you to load local libraries in a sandbox, which minimizes the possibility of version collisions. 
  1) Install [`virtualenv`](https://virtualenv.pypa.io/en/stable/) if needed:

```text
> virtualenv --version
-bash: virtualenv: command not found    <-- If you get this message ...
> pip install virtualenv                <-- ... install virtualenv
   ...
> virtualenv --version
15.1.0
>
```
    
2) Activate the virtual environment
```text
    > virtualenv venv -p python3
    Running virtualenv with interpreter /Library/Frameworks/Python.framework/Versions/3.6/bin/python3
    Using base prefix '/Library/Frameworks/Python.framework/Versions/3.6'
       ...
    > . venv/bin/activate
    (venv) > 
```

The `(venv)` at the prompt is a visual indicator that the virtual environment is in place.  You can revert to the default python environment at any type by:
```text
 (venv) > deactivate
 >
```

### Install the `fhirtordf` package

#### Option 1: Installation using [pip](https://pip.pypa.io/en/stable/)
```text
(venv) > pip install fhirtordf
...
(venv) >
(venv) > firtordf -v
FHIR to RDF Conversion Tool -- Version 0.1.0
(venv) >
```

#### Option 2: Installation from github image
```text
(venv) get clone https://github.com/BD2KOnFHIR/fhirtordf.git
...
(venv) > cd fhirtordf
(venv) > pip install -e .      <-- Don't forget the '.'
```

Installation can be tested with:
```text
(venv) > fhirtordf -v
FHIR to RDF Conversion Tool -- Version 0.1.0    <-- actual version number will vary
```

## FHIR to RDF Command Line Tool
The `fhirtordf` command line tool can:
* Convert a list of FHIR DSTU2 or STU3 JSON resources, bundles or collections to their RDF equivalents.  The input(s) can be URL's, files or both.
* Convert a (possibly nested) directory of JSON resources into their RDF equivalent, saving the output as a (possibly nested) directory of output files or as a single aggregate output file.

### Parameters
* **`-h, --help`**: show this help message and exit
* **`-i [INFILE [INFILE ...]], --infile [INFILE [INFILE ...]]`**: List of Input file(s) or url(s).  If not supplied, all files ending in ".json" in `INDIR` will be processed.
* **`-id INDIR, --indir INDIR`**: Source directory.  If `INFILE`(s) are named, they will be relative to this directory.  If no files are supplied all ".json" files within this directory and its subdirectory will be processed.
* **`-o [OUTFILE [OUTFILE ...]], --outfile [OUTFILE [OUTFILE ...]]`**: List of output RDF files.  
* **`-od OUTDIR, --outdir OUTDIR`**: Target directory.  Output RDF file(s) will be recorded in this directory.
* **`-f, --flatten`**: Flatten the output directory.  Default is to preserve the nested heirarchy of the input directory
* **`-s, --stoponerror`**: Stop on processing error.  Default is to continue processing if errors are encountered
* **`-v, --version`**: print the version identifier of the `fhirtordf` converter
* **`-u URIBASE, --uribase URIBASE`**: Base URI for the output RDF identifiers (default: http://hl7.org/fhir/)
* **`-mv METADATAVOC, --metadatavoc METADATAVOC`**: Location of the FHIR metadata vocabulary (fhir.ttl) (default: )
* **`-no, --noontology`**: Do not emit the OWL ontology declaration for the target resources.
* **`-nn, --nonarrative`**: Remove the content of the `fhir:narrative` text if it is greater than ?? bytes in length
* **`-nc, --nocontinuation`**: Don't follow FHIR navigation next page links.  Normally the service will load all of the pages in a resource 
* **`--nocache `**: Load the FHIR Metadata Vocabulary (fhir.ttl) from the `METADATVOC` location.
* **`--fmvcache FMVCACHE`**: Location of the FMB cache. (default: `$HOME/.cache`)
* **`--maxsize MAXSIZE`**: Maximum sensible file size in KB. 0 means no size check (default: 800)
* **`-sd, --skipdirs`**: List of directory patterns to skip.  Example: `-sd /v2 v3/ foo` will not process files in any directory that begins with 'v2', ends with 'v3' or contains 'foo'.  Directories whose names begin with an underscore ('_') are always skpped.
* **`-sf, --skipfns`**: List of file name patterns to skip.  Example: `-sf .cs. .vs` will not process any files whose names contain '.cs.' or '.vs'. All files whose names that do not end with '.json' will be skipped. 
* **`--format FORMAT`**: Output file format.  Posssible formats include:

| Format | DESCRIPTION | OUTPUT FILE SUFFIX | NOTES |
| ------ | ----------- | ----- | ----- |
| json-ld | [JSON for Linking Data](https://json-ld.org/) | .json-ld | Will be considerably more useful if and when we include a FHIR context |
| n3 | [Notation3 (N3)](https://www.w3.org/TeamSubmission/n3/) | .n3 | |
| nt</br>nt11</br>ntriples | [N-Triples 1.1](https://www.w3.org/TeamSubmission/n3/) | .nt | Line-based syntax | |
| xml | [XML Syntax](https://www.w3.org/TR/rdf-syntax-grammar/) | .xml | RDF Triples in XML |
| pretty-xml | [XML Syntax](https://www.w3.org/TR/rdf-syntax-grammar/) | .xml | Nested RDF -- BNodes factored out |
| trig | [RDF Dataset Language](https://www.w3.org/TR/trig/) | .trig | |
| ttl</br>turtle | [Terse RDF Triple Language](https://www.w3.org/TeamSubmission/turtle/) | .ttl | (default) |



## Examples
### Transform a FHIR resource and emit on stdout
`(venv) >fhirtordf -i http://hl7.org/fhir/Patient/f201`

### Merge two FHIR resources and emit result on stdout
`(venv) >fhirtordf -i http://hl7.org/fhir/Patient/f201 http://hl7.org/fhir/Patient/pat1`

### Merge two FHIR resources and save the result in t1.ttl
`(venv) >fhirtordf -i http://hl7.org/fhir/Patient/f201 http://hl7.org/fhir/Patient/pat1 -o t1.ttl`
`(venv) >fhirtordf -i http://hl7.org/fhir/Patient/f201 http://hl7.org/fhir/Patient/pat1 > t1.ttl`

### Run a query on a FHIR server and save the output resources as individual files
`(venv) >firtordf -i http://hl7.org/fhir/Patient/f201 http://hl7.org/fhir/Patient/pat1 test.json -od testdir`

This creates three files:
* `testdir/_url1.ttl` -- f201
* `testdir/_url2.ttl` -- pat1
* `testdir/test.ttl` -- test.json

### Recursively convert all `.json` files in the FHIR publication directory, ignoring v2, v3 and various test files
`(venv) >fhirtordf -id FHIR/build/publish -od test/publish -sd /v2/ /v3/ -sf .cs. .vs. .profile. .canonical. .schema. .diff.`

The above command will convert all .json files in the `FHIR/build/publish` directory converting the output to the nested equivalent in the `test/publish` target.  It will not conver the contents of directories named 'v2' or 'v3' and files that contain '.cs.', '.vs.', etc.

Note: The conversion utility will never convert files whose names begin with '.' or '\_' and will ignore all directories whose names begin with '\_'.

### Recursively convert all `.json` files in the FHIR publication directory, ignoring v2, v3 and various test files
`(venv) >fhirtordf -id FHIR/build/publish -od test/publish -sd /v2/ /v3/ -sf .cs. .vs. .profile. .canonical. .schema. .diff. -of master.ttl`

This will do the same thing as the previous command, with the exception that all of the output RDF will be merged int a single output file named `master.ttl`

## Use as a python library
The `fhirrtordf` package can be used to create an `rdflib Graph` from one or more FHIR JSON resources. Example:
```python
from rdflib import URIRef
from fhirtordf.loaders.fhirjsonloader import fhir_json_to_rdf

g = fhir_json_to_rdf("http://hl7.org/fhir/Observation/vitals-panel")
print([str(s) for s in set(g.subjects()) if isinstance(s, URIRef)])

# ['http://hl7.org/fhir/Observation/blood-pressure',
#  'http://hl7.org/fhir/Observation/body-temperature',
#  'http://hl7.org/fhir/Observation/heart-rate',
#  'http://hl7.org/fhir/Observation/respiratory-rate',
#  'http://hl7.org/fhir/Observation/vitals-panel',
#  'http://hl7.org/fhir/Observation/vitals-panel.ttl',
#  'http://hl7.org/fhir/Patient/example']

```

Signature:
```python
from typing import Optional, Union
from rdflib import Graph
from fhirtordf.fhir.fhirmetavoc import FHIRMetaVoc


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
    pass
```

Notes:
* `base_uri` this is the URI that will be used with URI fragments.  As an example, if a [Patient](http://fhir.org/fhir/patient.html) resource has a link in the form:
```text
  "link": [
    {
      "other": {
        "reference": "Patient/pat2"
      },
      "type": "seealso"
    }
  ]
```
the generated RDF will use `base_uri` it to create the `fhir:link`:
```text
   fhir:Patient.link [
        fhir:index "0"^^xsd:integer ;
        fhir:Patient.link.other [
            fhir:link <http://hl7.org/fhir/Patient/pat2> ;
            fhir:Reference.reference [
                fhir:value "Patient/pat2"
            ]
        ] ;
        fhir:Patient.link.type [
            fhir:value "seealso"
        ]
    ] ;
```
* `add_ontology_header` - if `True`, an additional ontology declaration will be added to the output graph:
```text
<http://hl7.org/fhir/Patient/pat1.ttl> a owl:Ontology ;
    owl:imports fhir:fhir.ttl .
```
Note: We anticipate that the ontololgy URI may be changed at a later date.  Note also, that if there is versioninfo in the metadata, this information will be added to the ontology declaration.

## How it works

## Fragile bits
The items below list points where there are dependencies on specific versions of libraries or resources that are prone to break.

1) **FHIR URI Regular Expression**:
This parser depends heavily on the regular expression for a FHIR resource, as published in [http://hl7.org/fhir/references.html](http://hl7.org/fhir/references.html).  Any changes to this will need to be reflected in [fhirresourcere.py](fhirtordf/rdfsupport/fhirresourcere.py)
2) **`rdflib` URI Parser**: We have to weaken the rules for parsing URI's in `rdflib`, as, technically, "http://snomed.info/id/74400008" is not a valid URI because a path cannot start with a number.  We include the following code fragment in [fhirgraphutils.py](fhirtordf/rdfsupport/fhirgraphutils.py):
```python
from rdflib.namespace import NAME_START_CATEGORIES
NAME_START_CATEGORIES.append('Nd')
```
3) **`rdflib` turtle printer**: For reasons that we don't fully understand, rdflib version 4.2.2 makes a mess of printing nested turtle.  [fhirgraphutils.py](fhirtordf/rdfsupport/fhirgraphutils.py) overrides two methods in `TurtleSerializer` -- `p_squared` and `label`.  It is quite likely that subsequent versions of `rdflib` will not be compatible with these changes.  We can hope, however, that the rdflib group will grow weary of unreadable turtle and fix this problem.

  

## Issues and incomplete tasks

### Which FHIR Metadata Vocabulary?
We have encountered a number of bugs and issues with the HL7 STU3 FHIR Metadata Vocabulary ([http://hl7.org/fhir/fhir.ttl]()). These problems are serious enough that the`fhirtordf` conversion utility will not work correctly with that item as a resource.  The latest 
build of the FMV, ([http://build.fhir.org/fhir.ttl]()), has all of the significant conversion issues fixed.  For this reason, all of the defaults in this package currently point at the latest.

### Numeric precision representation
1) The FHIR specification requires a non standard JSON parser -- one that preserves the textual representation of numeric objects.  As an example, in JSON,  "5", "5.", "5.0" and "5.00" all represent exactly the same value and will all be serialized as "5".  The FHIR specification requires that the difference in these values be preserved.   Not unexpectedly, the [Python Json encoder and decoder](https://docs.python.org/3.6/library/json.html) does not preserve this distinction.  We may be able to code a work-around, but, at the moment, currency and diopter values that use trailing zeroes fail this test.
### Recursive representation of paths
1) There is some sort of a bug -- either in the way that the FHIR Metadata Vocabulary is being generated or in our interpretation of it that results in path errors of the sort. As an example, the native FHIR converter represents (http://hl7.org/fhir/ValueSet/example-intensional.json):
```text
    "compose": {
        ...
        "exclude": [
          {
            "system": "http://loinc.org",
            "concept": [
              {
                "code": "5932-9",
                "display": "Cholesterol [Presence] in Blood by Test strip"
              }
            ]
          }
        ],
         ...
    }
```

as:

```text
fhir:ValueSet.compose [
        ...
     fhir:ValueSet.compose.exclude [
       fhir:index 0;
       fhir:ValueSet.compose.include.system [ fhir:value "http://loinc.org" ];
       fhir:ValueSet.compose.include.concept [
         fhir:index 0;
         fhir:ValueSet.compose.include.concept.code [ fhir:value "5932-9" ];
         fhir:ValueSet.compose.include.concept.display [ fhir:value "Cholesterol [Presence] in Blood by Test strip" ]
       ...
```

while the `fhirtordf` tool represents it as:

```text
    fhir:ValueSet.compose [
            ...
        fhir:ValueSet.compose.exclude [
            fhir:index "0"^^xsd:integer ;
            fhir:ValueSet.compose.exclude.concept [
                fhir:index "0"^^xsd:integer ;
                fhir:ValueSet.compose.exclude.concept.code [fhir:value "5932-9"] ;
                 fhir:ValueSet.compose.exclude.concept.display [fhir:value "Cholesterol [Presence] in Blood by Test strip"]
          ...
```
 
 We currently believe that tis is a bug in the native FHIR conversion, but further discussion is needed.

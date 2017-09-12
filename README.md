# FHIR JSON to RDF conversion utility

A tool to convert FHIR Resources from the JSON format to their equivalent in the FHIR RDF format.  This tool can be used to convert FHIR queries, bundles and individual FHIR resources.  It can be used to load an `rdflib` instance of the resource(s) for further processing and/or to create RDF output files.

Example:

```bash
> fhirrdf -i http://hl7.org/fhir/Patient/f201 -nn
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

## Command Line Tool
The `fhirtordf` command line tool can:
* Convert a list of FHIR DSTU2 or STU3 JSON resources, bundles or collections to their RDF equivalents.  The input(s) be a URL or a file.
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
* **`-u URIBASE, --uribase URIBASE`**: Base URI for the output RDF identifiers (default://hl7.org/fhir/)
* **`-mv METADATAVOC, --metadatavoc METADATAVOC`**: Location of the FHIR metadata vocabulary (fhir.ttl) (default: )
* **`-no, --noontology`**: Do not emit the OWL ontology declaration for the target resources.
* **`-nn, --nonarrative`**: Remove the content of the `fhir:narrative` text if it is greater than ?? bytes in length
* **`-nc, --nocontinuation`**: Don't follow FHIR navigation next page links.  Normally the service will load all of the pages in a resource 
* **`--nocache `**: Load the FHIR Metadata Vocabulary (fhir.ttl) from the `METADATVOC` location.
* **`--fmvcache FMVCACHE`**: Location of the FMB cache. (default: `$HOME/.cache`)
* **`--maxsize MAXSIZE`**: Maximum sensible file size in KB. 0 means no size check (default: 800)

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

## How it works

## Issues and incomplete tasks
### FHIR Bundle Entries
1) The native FHIR to RDF converter uses the `fullUrl` of each [entry](http://hl7.org/fhir/bundle-definitions.html#Bundle.entry) in the FHIR [Bundle](http://hl7.org/fhir/bundle.html) Resource as the subject of the entry itself. The `fhirtordf` tool currently represents each entry as a BNode.
2) `search`, `request` and/or `response` elements in the FHIR Bundle entry are not currently converted.  This is a bug in the conversion tool and is scheduled to be fixed.
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
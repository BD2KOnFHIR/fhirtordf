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
import os
import sys
from argparse import Namespace, ArgumentParser
from typing import List

import dirlistproc
from rdflib import Graph

from fhirtordf.fhir.fhirmetavoc import FHIRMetaVoc
from fhirtordf.fhir.picklejar import picklejarfactory
from fhirtordf.loaders.fhirjsonloader import fhir_json_to_rdf
from fhirtordf import __version__
from fhirtordf.rdfsupport.rdflibformats import known_formats, suffix_for

dirname, _ = os.path.split(os.path.abspath(__file__))

DEFAULT_FHIR_URI = "http://hl7.org/fhir/"
DEFAULT_RDF_DIR = "rdf"
DEFAULT_FHIR_MV = os.path.abspath(os.path.join(dirname, '..', 'tests', 'data', 'fhir_metadata_vocabulary', 'fhir.ttl'))
DEFAULT_FMV_CACHE_DIR = os.path.abspath(os.path.join(os.path.expanduser('~'), ".cache"))

output_formats = known_formats()
output_formats.remove('nquads')         # Only makes sense for context-aware stores
output_formats.remove('trix')


def load_fhir_ontology(opts: Namespace) -> Graph:
    if opts.nocache:
        picklejarfactory.cache_directory = None
    else:
        picklejarfactory.cache_directory = os.path.abspath(opts.fmvcache)
    if opts.outfile:
        print("Loading FHIR metadata vocabulary...", end='')
    mv = FHIRMetaVoc(opts.metadatavoc)
    if opts.outfile:
        print("loaded from local cache" if mv.from_cache else "loaded from {}".format(opts.metadatavoc))
    return mv.g


def add_argument(parser: ArgumentParser, *args, **kwargs):
    defhelp = kwargs.pop("help", None)
    default = kwargs.pop("default", None)
    if not defhelp or default is None:
        return parser.add_argument(*args, help=defhelp, default=default, **kwargs)
    else:
        return parser.add_argument(*args, help=defhelp + " (default: {})".format(default), default=default, **kwargs)


def proc_file(infile: str, outfile: str, opts: Namespace) -> bool:
    """
    Process infile.
    :param infile: input file to be processed
    :param outfile: target output file.
    :param opts:
    :return:
    """
    g = fhir_json_to_rdf(infile, opts.uribase, opts.graph, add_ontology_header=not opts.noontology,
                         do_continuations=not opts.nocontinuation, replace_narrative_text=bool(opts.nonarrative),
                         metavoc=opts.fhir_metavoc)

    # If we aren't carrying graph in opts, we're doing a file by file transformation
    if g:
        if not opts.graph:
            serialize_graph(g, outfile, opts)
        return True
    else:
        print("{} : Not a FHIR collection or resource".format(infile))
        return False


def serialize_graph(g: Graph, outfile: str, opts: Namespace) -> None:
    if outfile:
        g.serialize(outfile, format=opts.format)
    else:
        print(g.serialize(format=opts.format).decode())


def file_filter(ifn: str, indir: str, opts: Namespace) -> bool:
    """
    Determine whether to process ifn.  We con't process:
        1) Anything in a directory having a path element that begins with "_"
        2) Really, really big files
        3) Temporary lists of know errors
    :param ifn: input file name
    :param indir: input directory
    :param opts: argparse options
    :return: True if to be processed, false if to be skipped
    """
    # If it looks like we're processing a URL as an input file, skip the suffix check
    if '://' in ifn:
        return True

    if not ifn.endswith('.json'):
        return False

    if indir and (indir.startswith("_") or "/_" in indir or any(dn in indir for dn in opts.skipdirs)):
        return False

    if opts.skipfns and any(sfn in ifn for sfn in opts.skipfns):
        return False

    infile = os.path.join(indir, ifn)
    if not opts.infile and opts.maxsize and os.path.getsize(infile) > (opts.maxsize * 1000):
        return False

    return True


def addargs(parser: ArgumentParser) -> None:
    parser.prog = os.path.basename(__file__).split(".")[0]
    add_argument(parser, "-v", "--version", help="Current version number", action="store_true")
    add_argument(parser, "-u", "--uribase", help="Base URI for RDF identifiers", default=DEFAULT_FHIR_URI)
    add_argument(parser, "-mv", "--metadatavoc", help="FHIR metadata vocabulary", default=DEFAULT_FHIR_MV)
    add_argument(parser, "-no", "--noontology", help="Omit owl ontology header", action="store_true")
    add_argument(parser, "-nn", "--nonarrative", help="Omit narrative text on output", action="store_true")
    add_argument(parser, "-nc", "--nocontinuation", help="Don't follow URL continuations", action="store_true")
    add_argument(parser, "--nocache", help="Do not use FMV Cache", action="store_true")
    add_argument(parser, "--fmvcache", help="Metadata vocabluary cache directory",
                 default=DEFAULT_FMV_CACHE_DIR)
    add_argument(parser, "--maxsize", help="Maximum sensible file size in KB.  0 means no size check",
                 type=int, default=800)
    add_argument(parser, "-sd", "--skipdirs", help="Skip directories", nargs='*')
    add_argument(parser, "-sf", "--skipfns", help="Skip file names containing text", nargs='*')
    add_argument(parser, "--format", help="Output format", choices=output_formats, default="turtle")
    parser.fromfile_prefix_chars = "@"


def postparse(opts: Namespace) -> bool:
    # If we have a single outfile, we will collect everything into a single graph
    opts.graph = Graph() if opts.outfile else None
    opts.fhir_metavoc = load_fhir_ontology(opts)
    return True


def fhirtordf(argv: List[str], default_exit: bool = True) -> bool:
    """ Entry point for command line utility """
    dlp = dirlistproc.DirectoryListProcessor(argv,
                                             description="Convert FHIR JSON into RDF",
                                             infile_suffix=".json",
                                             outfile_suffix=".ttl",
                                             addargs=addargs,
                                             noexit=not default_exit)

    if not dlp.successful_parse:
        return False

    # Version
    if dlp.opts.version:
        print("FHIR to RDF Conversion Tool -- Version {}".format(__version__))

    # We either have to have an input file or an input directory
    if not dlp.opts.infile and not dlp.opts.indir:
        if not dlp.opts.version:
            dlp.parser.error("Either an input file or an input directory must be supplied")
        return dlp.opts.version

    # Create the output directory if needed
    if dlp.opts.outdir and not os.path.exists(dlp.opts.outdir):
        os.makedirs(dlp.opts.outdir)

    # If we are going to a single output file or stdout, gather all the input
    dlp.opts.graph = Graph() if (not dlp.opts.outfile and not dlp.opts.outdir) or\
                                (dlp.opts.outfile and len(dlp.opts.outfile) == 1) else None
    dlp.opts.fhir_metavoc = load_fhir_ontology(dlp.opts)

    # If it looks like we're processing a URL as an input file, skip the suffix check
    if dlp.opts.infile and len(dlp.opts.infile) == 1 and not dlp.opts.indir and "://" in dlp.opts.infile[0]:
        dlp.infile_suffix = ""
    dlp.outfile_suffix = '.' + suffix_for(dlp.opts.format)
    nfiles, nsuccess = dlp.run(proc=proc_file, file_filter_2=file_filter)
    if nfiles:
        if dlp.opts.graph:
            serialize_graph(dlp.opts.graph, dlp.opts.outfile[0] if dlp.opts.outfile else None, dlp.opts)
        return nsuccess > 0
    return False


if __name__ == "__main__":
    sys.path.append(os.path.join(os.path.join(os.getcwd(), os.path.dirname(__file__)), '..'))
    fhirtordf(sys.argv[1:])

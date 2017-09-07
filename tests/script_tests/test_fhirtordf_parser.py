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
import io
import unittest

import sys

import os
from rdflib import Graph

from fhirtordf.rdfsupport.rdfcompare import rdf_compare

help_text = """usage: fhirtordf [-h] [-i [INFILE [INFILE ...]]] [-id INDIR]
                 [-o [OUTFILE [OUTFILE ...]]] [-od OUTDIR] [-f] [-s]
                 [-u URIBASE] [-mv METADATAVOC] [-no] [-nn] [-nc] [--nocache]
                 [--fmvcache FMVCACHE] [--maxsize MAXSIZE]

Convert FHIR JSON into RDF

optional arguments:
  -h, --help            show this help message and exit
  -i [INFILE [INFILE ...]], --infile [INFILE [INFILE ...]]
                        Input file(s)
  -id INDIR, --indir INDIR
                        Input directory
  -o [OUTFILE [OUTFILE ...]], --outfile [OUTFILE [OUTFILE ...]]
                        Output file(s)
  -od OUTDIR, --outdir OUTDIR
                        Output directory
  -f, --flatten         Flatten output directory
  -s, --stoponerror     Stop on processing error
  -u URIBASE, --uribase URIBASE
                        Base URI for RDF identifiers (default:
                        http://hl7.org/fhir/)
  -mv METADATAVOC, --metadatavoc METADATAVOC
                        FHIR metadata vocabulary (default: /Users/mrf7578/Deve
                        lopment/git/BD2KOnFHIR/fhirtordf/tests/data/fhir_metad
                        ata_vocabulary/fhir.ttl)
  -no, --noontology     Omit owl ontology header
  -nn, --nonarrative    Omit narrative text on output
  -nc, --nocontinuation
                        Don't follow URL continuations
  --nocache             Do not use FMV Cache
  --fmvcache FMVCACHE   Metadata vocabluary cache directory (default:
                        /Users/mrf7578/.cache)
  --maxsize MAXSIZE     Maximum sensible file size in KB. 0 means no size
                        check (default: 800)
"""

save_sample_output = False           # True means create a fres text copy for sample patient


class FHIRToRDFParserTestCase(unittest.TestCase):
    save_stdout = []

    def _push_stdout(self) -> io:
        self.save_stdout.append(sys.stdout)
        output = io.StringIO()
        sys.stdout = output
        return output

    def _pop_stdout(self) -> None:
        if self.save_stdout:
            sys.stdout = self.save_stdout.pop()

    def tearDown(self):
        self._pop_stdout()

    def test_no_args(self):
        from fhirtordf.fhirtordf import fhirtordf
        args = ""
        output = self._push_stdout()
        fhirtordf(args.split(), default_exit=False)
        self._pop_stdout()
        self.assertEqual("Either an input file or an input directory must be supplied\n", output.getvalue())

    def test_help(self):
        from fhirtordf.fhirtordf import fhirtordf
        args = "-h"
        output = self._push_stdout()
        fhirtordf(args.split(), default_exit=False)
        self._pop_stdout()
        self.assertEqual(help_text, output.getvalue())

    def bester_tester(self, args: str, test_fname: str):
        from fhirtordf.fhirtordf import fhirtordf
        output = self._push_stdout()
        fhirtordf(args.split(), default_exit=False)
        g2 = Graph()
        g2.parse(data=output.getvalue(), format="turtle")
        self._pop_stdout()
        if save_sample_output:
            with open(test_fname, 'w') as f:
                f.write(output.getvalue())
        g1 = Graph()
        g1.parse(test_fname, format="turtle")
        comp_result = rdf_compare(g1, g2)

        if len(comp_result):
            print(comp_result)
        self.assertTrue(len(comp_result) == 0)
        self.assertFalse(save_sample_output, "save_sample_output is True -- test not applied")

    def test_narrative_text(self):
        test_fname = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'data', 'patient-example-2_nn.ttl')
        args = "-i http://hl7.org/fhir/Patient/f201 -nn"
        self.bester_tester(args, test_fname)

    def test_sample_patient(self):
        test_fname = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'data', 'patient-example-2.ttl')
        args = "-i http://hl7.org/fhir/Patient/f201"
        self.bester_tester(args, test_fname)

if __name__ == '__main__':
    unittest.main()

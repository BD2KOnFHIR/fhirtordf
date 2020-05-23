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
import unittest
from datetime import datetime, timedelta
from typing import Union

from dateutil.parser import parse
from rdflib import Graph, Literal, XSD

from tests.utils import test_fhir_server, test_fmv_loc


class FHIRGraph(Graph):
    message_printed = False

    def __init__(self, do_print=True):
        super().__init__()
        if do_print and not FHIRGraph.message_printed:
            print("***** Testing from fhir server: {}".format(test_fhir_server))
            print("***** Using FMV: {}".format(test_fmv_loc))
            FHIRGraph.message_printed = True

        if do_print:
            print("Loading graph...", end="")
        self.load(test_fmv_loc, format="turtle")
        if do_print:
            print("done\n")


def make_and_clear_directory(directory: str):
    """
    Create the supplied directory if needed and clear its contents.  Because this is a sufficiently dangerous function,
    it will only clear the contents of the directory if there is a file named 'generated' in it.
    :param directory:
    :return:
    """
    import shutil

    safety_file = os.path.join(directory, "generated")
    if os.path.exists(directory):
        if not os.path.exists(safety_file):
            raise FileExistsError("{} not found in test directory".format(safety_file))
        shutil.rmtree(directory)
    os.makedirs(directory)
    with open(safety_file, "w") as f:
        f.write("Generated for safety.  Must be present for test to clear this directory.")

def fhir_decimal_issue_filter(in_both: Graph, in_first: Graph, in_second: Graph) -> None:
    """ FHIR currently requires a non-standard JSON parser that can differentiate between '"x": 1.0' and '"x": 1.00'
        The filter below treats RDF representation of both as the same, and is used to make decimal values
        pass unit tests
    """
    for s, p, o in list(in_first):
        o_2 = in_second.value(s, p)
        if o_2 is not None and isinstance(o_2, Literal) and o_2.datatype == XSD.decimal and \
                               isinstance(o, Literal) and o.datatype == XSD.decimal:
            if o.value == o_2.value:
                in_both.add((s, p, o))
                in_first.remove((s, p, o))
                in_second.remove((s, p, o_2))

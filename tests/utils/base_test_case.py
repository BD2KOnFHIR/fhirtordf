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

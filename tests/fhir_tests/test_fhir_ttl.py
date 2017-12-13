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

import unittest

from rdflib import Graph, RDFS, BNode, OWL, XSD, URIRef

from fhirtordf.rdfsupport.namespaces import FHIR
from tests.utils.base_test_case import FHIRGraph


class FHIRTTLTestCase(unittest.TestCase):

    @staticmethod
    def is_xsd_primitive(prim: URIRef, g: Graph) -> bool:
        for node in g.objects(prim, RDFS.subClassOf):
            if isinstance(node, BNode) and g.value(node, OWL.onProperty) == FHIR.value:
                # Older versions of fhir.ttl used allValuesFrom (incorrect, btw)
                base_type = g.value(node, OWL.allValuesFrom)
                if not base_type:
                    base_node = g.value(node, OWL.someValuesFrom)
                    if isinstance(base_node, BNode):
                        base_type = g.value(base_node, OWL.onDatatype)
                if not str(base_type).startswith(str(XSD)):
                    print("type failure - {} : {}".format(prim, base_type))
                    return False
                return True
        print("No base type defined for {}".format(prim))
        return False

    def test_primitives(self):
        """
        FHIR periodically makes changes to the fhir data types.  This test determines whether there are any FHIR
        primitive types that aren't anchored in the XML space
        """
        g = FHIRGraph()
        tests = [self.is_xsd_primitive(p, g) for p in g.subjects(RDFS.subClassOf, FHIR.Primitive)]
        self.assertTrue(all(tests))


if __name__ == '__main__':
    unittest.main()

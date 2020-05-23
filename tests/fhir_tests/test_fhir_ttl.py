
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
                    # TODO: Remove this once FHIRCat issue #35 (https://github.com/fhircat/FHIRCat/issues/35) is fixed
                    if base_type == FHIR.integer64:
                        print("integer64 issue still needs fixing")
                    else:
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

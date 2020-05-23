
from rdflib import Namespace, URIRef


class DottedNamespace(Namespace):
    """
    An RDF namespace that supports the FHIR dotted notation (e.g. fhir:Patient.status)
    """
    def __new__(cls, value):
        return Namespace.__new__(cls, value)

    def __getattribute__(self, item: str) -> "DottedURIRef":
        if item == 'index':
            return DottedURIRef(str(self) + item)
        else:
            return super().__getattribute__(item)

    def __getattr__(self, item: str) -> "DottedURIRef":
        return DottedURIRef(str(self) + item)

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()


class DottedURIRef(URIRef):
    """
    A URIRef that supports the FHIR dotted notation
    """
    def __new__(cls, value, base=None):
        return URIRef.__new__(cls, value, base)

    def __getattr__(self, item: str) -> "DottedURIRef":
        return DottedURIRef(str(self) + '.' + item)

    def __eq__(self, other):
        if isinstance(self, URIRef) and isinstance(other, URIRef):
            return str(self) == str(other)
        else:
            return False

    def __hash__(self):
        return super().__hash__()

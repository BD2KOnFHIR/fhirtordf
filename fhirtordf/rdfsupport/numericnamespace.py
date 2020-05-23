from typing import Optional, Any

from rdflib import Namespace, URIRef


class NumericNamespace(Namespace):
    """
    An RDF namespace that supports numeric identifiers (e.g. sct:74400008).
    Notation for use: SCT.C74400008
    """
    def __new__(cls, value):
        return Namespace.__new__(cls, value)

    def __getattr__(self, item: str) -> "URIRef":
        return URIRef(str(self) + item[1:])

    def __getitem__(self, item, default=None) -> URIRef:
        return super().__getitem__(str(item) if isinstance(item, int) else item)

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()

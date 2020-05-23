
import unittest

import rdflib
from rdflib import XSD

from fhirtordf.rdfsupport.namespaces import FHIR


class FHIRMetaVocTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from tests.utils.base_test_case import FHIRGraph
        cls.fhir_ontology = FHIRGraph()

    def test1(self):
        from fhirtordf.fhir.fhirmetavoc import FHIRMetaVocEntry

        m = FHIRMetaVocEntry(self.fhir_ontology, "Account")
        self.assertEqual({
             'contained': rdflib.term.URIRef('http://hl7.org/fhir/DomainResource.contained'),
             'coverage': rdflib.term.URIRef('http://hl7.org/fhir/Account.coverage'),
             'description': rdflib.term.URIRef('http://hl7.org/fhir/Account.description'),
             'extension': rdflib.term.URIRef('http://hl7.org/fhir/DomainResource.extension'),
             'guarantor': rdflib.term.URIRef('http://hl7.org/fhir/Account.guarantor'),
             'id': rdflib.term.URIRef('http://hl7.org/fhir/Resource.id'),
             'identifier': rdflib.term.URIRef('http://hl7.org/fhir/Account.identifier'),
             'implicitRules': rdflib.term.URIRef('http://hl7.org/fhir/Resource.implicitRules'),
             'language': rdflib.term.URIRef('http://hl7.org/fhir/Resource.language'),
             'meta': rdflib.term.URIRef('http://hl7.org/fhir/Resource.meta'),
             'modifierExtension': rdflib.term.URIRef('http://hl7.org/fhir/DomainResource.modifierExtension'),
             'name': rdflib.term.URIRef('http://hl7.org/fhir/Account.name'),
             'nodeRole': rdflib.term.URIRef('http://hl7.org/fhir/nodeRole'),
             'owner': rdflib.term.URIRef('http://hl7.org/fhir/Account.owner'),
             'partOf': rdflib.term.URIRef('http://hl7.org/fhir/Account.partOf'),
             'servicePeriod': rdflib.term.URIRef('http://hl7.org/fhir/Account.servicePeriod'),
             'status': rdflib.term.URIRef('http://hl7.org/fhir/Account.status'),
             'subject': rdflib.term.URIRef('http://hl7.org/fhir/Account.subject'),
             'text': rdflib.term.URIRef('http://hl7.org/fhir/DomainResource.text'),
             'type': rdflib.term.URIRef('http://hl7.org/fhir/Account.type')}, m.predicates())

    def test2(self):
        from fhirtordf.fhir.fhirmetavoc import FHIRMetaVocEntry
        m = FHIRMetaVocEntry(self.fhir_ontology, "Account")
        preds = m.predicates()
        v = []
        for name in sorted(preds.keys()):
            pred = preds[name]
            t = m.predicate_type(pred)
            v.append((name, str(t), 'A' if m.is_atom(pred) else 'P' if m.is_primitive(t) else 'C'))
        self.assertEqual([
             ('contained', 'http://hl7.org/fhir/Resource', 'C'),
             ('coverage', 'http://hl7.org/fhir/Account.CoverageComponent', 'C'),
             ('description', 'http://hl7.org/fhir/string', 'P'),
             ('extension', 'http://hl7.org/fhir/Extension', 'C'),
             ('guarantor', 'http://hl7.org/fhir/Account.GuarantorComponent', 'C'),
             ('id', 'http://hl7.org/fhir/id', 'P'),
             ('identifier', 'http://hl7.org/fhir/Identifier', 'C'),
             ('implicitRules', 'http://hl7.org/fhir/uri', 'P'),
             ('language', 'http://hl7.org/fhir/code', 'P'),
             ('meta', 'http://hl7.org/fhir/Meta', 'C'),
             ('modifierExtension', 'http://hl7.org/fhir/Extension', 'C'),
             ('name', 'http://hl7.org/fhir/string', 'P'),
             ('nodeRole', 'http://hl7.org/fhir/treeRoot', 'A'),
             ('owner', 'http://hl7.org/fhir/Reference', 'C'),
             ('partOf', 'http://hl7.org/fhir/Reference', 'C'),
             ('servicePeriod', 'http://hl7.org/fhir/Period', 'C'),
             ('status', 'http://hl7.org/fhir/code', 'P'),
             ('subject', 'http://hl7.org/fhir/Reference', 'C'),
             ('text', 'http://hl7.org/fhir/Narrative', 'C'),
             ('type', 'http://hl7.org/fhir/CodeableConcept', 'C')], v)

    def test3(self):
        from fhirtordf.fhir.fhirmetavoc import FHIRMetaVocEntry
        m = FHIRMetaVocEntry(self.fhir_ontology, "Narrative")
        preds = m.predicates()
        v = []
        for name in sorted(preds.keys()):
            pred = preds[name]
            t = m.predicate_type(pred)
            v.append((name, str(t), 'A' if m.is_atom(pred) else 'P' if m.is_primitive(t) else 'C'))
        self.assertEqual([
            ('div', 'http://hl7.org/fhir/xhtml', 'A'),
            ('extension', 'http://hl7.org/fhir/Extension', 'C'),
            ('id', 'http://hl7.org/fhir/string', 'P'),
            ('index', 'http://www.w3.org/2001/XMLSchema#nonNegativeInteger', 'A'),
            ('status', 'http://hl7.org/fhir/code', 'P')], v)

    def test_valuetype(self):
        from fhirtordf.fhir.fhirmetavoc import FHIRMetaVocEntry
        m = FHIRMetaVocEntry(self.fhir_ontology, "Account")

        self.assertEqual(XSD.base64Binary, m.primitive_datatype(FHIR.base64Binary))
        self.assertEqual(XSD.boolean, m.primitive_datatype(FHIR.boolean))
        self.assertEqual(XSD.string, m.primitive_datatype(FHIR.code))
        self.assertEqual(XSD.dateTime, m.primitive_datatype(FHIR.date))
        self.assertEqual(XSD.dateTime, m.primitive_datatype(FHIR.dateTime))
        self.assertEqual(XSD.decimal, m.primitive_datatype(FHIR.decimal))
        self.assertEqual(XSD.string, m.primitive_datatype(FHIR.id))
        self.assertEqual(XSD.dateTime, m.primitive_datatype(FHIR.instant))
        self.assertEqual(XSD.integer, m.primitive_datatype(FHIR.integer))
        self.assertEqual(XSD.string, m.primitive_datatype(FHIR.markdown))
        self.assertEqual(XSD.anyURI, m.primitive_datatype(FHIR.oid))
        self.assertEqual(XSD.positiveInteger, m.primitive_datatype(FHIR.positiveInt))
        self.assertEqual(XSD.string, m.primitive_datatype(FHIR.string))
        self.assertEqual(XSD.string, m.primitive_datatype(FHIR.time))
        self.assertEqual(XSD.nonNegativeInteger, m.primitive_datatype(FHIR.unsignedInt))
        self.assertEqual(XSD.anyURI, m.primitive_datatype(FHIR.uri))
        self.assertEqual(XSD.anyURI, m.primitive_datatype(FHIR.uuid))
        self.assertEqual(None, m.primitive_datatype(FHIR.Quantity))

    def test_nostring_valuetype(self):
        from fhirtordf.fhir.fhirmetavoc import FHIRMetaVocEntry
        m = FHIRMetaVocEntry(self.fhir_ontology, "Account")

        self.assertEqual(XSD.base64Binary, m.primitive_datatype_nostring(FHIR.base64Binary))
        self.assertEqual(XSD.boolean, m.primitive_datatype_nostring(FHIR.boolean))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.code))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.date))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.dateTime))
        self.assertEqual(XSD.decimal, m.primitive_datatype_nostring(FHIR.decimal))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.id))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.instant))
        self.assertEqual(XSD.integer, m.primitive_datatype_nostring(FHIR.integer))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.markdown))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.oid))
        self.assertEqual(XSD.positiveInteger, m.primitive_datatype_nostring(FHIR.positiveInt))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.string))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.time))
        self.assertEqual(XSD.nonNegativeInteger, m.primitive_datatype_nostring(FHIR.unsignedInt))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.uri))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.uuid))
        self.assertEqual(None, m.primitive_datatype_nostring(FHIR.Quantity))

    def test_fhir_dates(self):
        from fhirtordf.fhir.fhirmetavoc import FHIRMetaVocEntry

        m = FHIRMetaVocEntry(self.fhir_ontology, "Account")

        FHIRMetaVocEntry.fhir_dates = False
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.dateTime, "2009"))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11"))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11-30"))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11-30T09:00:00Z"))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11-30+10"))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11-30-9"))

        FHIRMetaVocEntry.fhir_dates = True
        self.assertEqual(XSD.gYear, m.primitive_datatype_nostring(FHIR.dateTime, "2009"))
        self.assertEqual(XSD.gYearMonth, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11"))
        self.assertEqual(XSD.date, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11-30"))
        self.assertEqual(XSD.dateTime, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11-30T09:00:00Z"))
        self.assertEqual(XSD.date, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11-30+10"))
        self.assertEqual(XSD.date, m.primitive_datatype_nostring(FHIR.dateTime, "2009-11-30-9"))


if __name__ == '__main__':
    unittest.main()

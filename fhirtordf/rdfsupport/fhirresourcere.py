import re


# Taken from http://build.fhir.org/references.html (2.3.0.1).
#   Note 1: Additional set of parenthesis placed after the closing slash on _history and end
#   Note 2: '$' added to the end of of the string
#   Note 3: Additional set of parenthesis placed on the resource identifier portion
# TODO: Find a mechanism to keep this current...
_fhir_resource_re = "((http|https)://([A-Za-z0-9\\.:%$]*/)*)?" \
                   "(Account|ActivityDefinition|AdverseEvent|AllergyIntolerance|Appointment|AppointmentResponse" \
                   "|AuditEvent|Basic|Binary|BodyStructure|Bundle|CapabilityStatement|CarePlan|CareTeam|ChargeItem" \
                   "|Claim|ClaimResponse|ClinicalImpression|CodeSystem|Communication|CommunicationRequest" \
                   "|CompartmentDefinition|Composition|ConceptMap|Condition|Consent|Contract|Coverage|DetectedIssue" \
                   "|Device|DeviceComponent|DeviceMetric|DeviceRequest|DeviceUseStatement|DiagnosticReport" \
                   "|DocumentManifest|DocumentReference|EligibilityRequest|EligibilityResponse|Encounter|Endpoint" \
                   "|EnrollmentRequest|EnrollmentResponse|EpisodeOfCare|EventDefinition|ExpansionProfile" \
                   "|ExplanationOfBenefit|FamilyMemberHistory|Flag|Goal|GraphDefinition|Group|GuidanceResponse" \
                   "|HealthcareService|ImagingManifest|ImagingStudy|Immunization|ImmunizationRecommendation" \
                   "|ImplementationGuide|Library|Linkage|List|Location|Measure|MeasureReport|Media|Medication" \
                   "|MedicationAdministration|MedicationDispense|MedicationRequest|MedicationStatement" \
                   "|MessageDefinition|MessageHeader|NamingSystem|NutritionOrder|Observation|OperationDefinition" \
                   "|OperationOutcome|Organization|Patient|PaymentNotice|PaymentReconciliation|Person|PlanDefinition" \
                   "|Practitioner|PractitionerRole|Procedure|ProcedureRequest|ProcessRequest|ProcessResponse" \
                   "|Provenance|Questionnaire|QuestionnaireResponse|RelatedPerson|RequestGroup|ResearchStudy" \
                   "|ResearchSubject|RiskAssessment|Schedule|SearchParameter|Sequence|ServiceDefinition|Slot|Specimen" \
                   "|StructureDefinition|StructureMap|Subscription|Substance|SupplyDelivery|SupplyRequest|Task" \
                   "|TestReport|TestScript|ValueSet|VisionPrescription)" \
                   "/([A-Za-z0-9.-]{1,64})(/_history/([A-Za-z0-9.-]{1,64}))?$"
FHIR_RESOURCE_RE = re.compile(_fhir_resource_re)

# Group indices  (FHIR_RESOURCE_RE.match(str).group(index) -- group(0) is the entire thing)
FHIR_RE_BASE = 1
FHIR_RE_RESOURCE = 4
FHIR_RE_ID = 5
FHIR_RE_VERSION = 7

# Not really a part of the regular expression, but a convenient place to keep it.  What to replace narrative text
# with
REPLACED_NARRATIVE_TEXT = '<div xmlns="http://www.w3.org/1999/xhtml">(removed)</div>'

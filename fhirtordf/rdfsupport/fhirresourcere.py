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

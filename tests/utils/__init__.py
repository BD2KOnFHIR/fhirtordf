import os

test_directory = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], '..'))
test_data_directory = os.path.join(test_directory, 'data')

USE_BUILD_SERVER = True
USE_LOCAL_FMV = True
if USE_BUILD_SERVER:
    test_fhir_server = "http://build.fhir.org/"
else:
    test_fhir_server = "http://hl7.org/fhir/"

if USE_LOCAL_FMV:
    test_fmv_loc = os.path.join(test_data_directory, 'fhir_metadata_vocabulary', 'fhir.ttl')
else:
    test_fmv_loc = f"{test_fhir_server}fhir.ttl"

SKIP_CONTINUATION_TESTS = True          # Skip the continuation test (takes a lot of time)
SKIP_ALL_FHIR_ELEMENTS = True           # Skip the fhir server tests (takes a really big lot of time)

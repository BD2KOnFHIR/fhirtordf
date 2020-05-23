import os

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_DATA_DIR = os.path.join(TEST_DIR, 'data')
FHIR_R4_TTL = os.path.join(TEST_DATA_DIR, 'fhir_metadata_vocabulary', 'fhir_r4.ttl')

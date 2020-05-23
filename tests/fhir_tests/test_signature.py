
import unittest

import time

from fhirtordf.fhir.signature import *


class SignatureTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = "http://build.fhir.org/w5.ttl"
        cls.url2 = "http://build.fhir.org/fhir.ttl"
        cls.file = os.path.join(os.path.split(os.path.abspath(__file__))[0], '..', 'data', 'sig_file')

    def test_type(self):
        self.assertTrue(is_url(self.url))
        self.assertFalse(is_file(self.url))
        self.assertFalse(is_url(self.file))
        self.assertTrue(is_file(self.file))
        self.assertFalse(is_url(""))
        self.assertFalse(is_file(""))

    def test_sigs(self):
        if os.path.exists(self.file):
            os.remove(self.file)
        sig = signature(self.url)
        self.assertIsNotNone(sig)
        self.assertEqual(sig, signature(self.url))
        sig2 = signature(self.url2)
        self.assertIsNotNone(sig2)
        self.assertNotEqual(sig, sig2)
        self.assertIsNone(signature(self.url + 'z'))
        self.assertIsNone(signature(self.file))
        with open(self.file, 'w') as f:
            f.write("test")
        sig = signature(self.file)
        self.assertIsNotNone(sig)
        time.sleep(1)
        with open(self.file, 'a') as f:
            f.write("a")
        sig2 = signature(self.file)
        self.assertNotEqual(sig, sig2)
        self.assertNotEqual(sig[2], sig2[2])
        os.remove(self.file)


if __name__ == '__main__':
    unittest.main()

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

import os

from fhirtordf.fhir.picklejar import picklejar, picklejarfactory
from tests.utils.base_test_case import make_and_clear_directory


class TestObj:
    pass


class PickleJarTestCase(unittest.TestCase):
    current_cache_directory = None

    @classmethod
    def setUpClass(cls):
        picklejar().clear()
        cls.current_cache_directory = picklejarfactory.cache_directory
        o = TestObj()
        o.cls = "CLASS"
        picklejar().add("cls", (1,), o)

    @classmethod
    def tearDownClass(cls):
        picklejar().clear()

    def setUp(self):
        # Recover if there is an error when we're not working with the default
        picklejarfactory.cache_directory = self.current_cache_directory

    def test_pickled_file(self):
        o = TestObj()
        o.foo = 42
        picklejar().add('o1', (1,), o)
        o2 = picklejar().get('o1', (1,))
        self.assertIsNotNone(o2)
        self.assertEqual(42, o2.foo)

    def test_singleton(self):
        o = picklejar().get('cls', (1,))
        self.assertIsNotNone(o)
        self.assertEqual("CLASS", o.cls)

    def test_cache_loc(self):
        current_cache_directory = picklejarfactory.cache_directory
        test_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')
        picklejarfactory.cache_directory = os.path.abspath(os.path.join(test_directory, 'pjcache'))
        make_and_clear_directory(picklejarfactory.cache_directory)
        o1 = TestObj()
        o1.foo = "bagels"
        picklejar().add('o1', (2, 3), o1)
        o2 = TestObj()
        o2.foo = "cheese"
        picklejar().add('o2', (2, 5), o2)
        ot1 = picklejar().get('o1', (2, 3))
        ot2 = picklejar().get('o2', (2, 5))
        self.assertEqual("bagels", ot1.foo)
        self.assertEqual("cheese", ot2.foo)
        picklejar().clear()
        picklejarfactory.cache_directory = current_cache_directory
        ot1 = picklejar().get('o1', (2, 3))
        ot2 = picklejar().get('o2', (2, 5))
        self.assertIsNone(ot1)
        self.assertIsNone(ot2)
        self.assertIsNotNone(picklejar().get('cls', (1,)))

    def test_no_cache(self):
        current_cache_directory = picklejarfactory.cache_directory
        picklejarfactory.cache_directory = None
        o = picklejar().get('cls', (1,))
        self.assertIsNone(o)
        o1 = TestObj()
        o1.foo = "bagels"
        picklejar().add('o1', (2, 3), o1)
        ot1 = picklejar().get('o1', (2, 3))
        self.assertIsNone(ot1)
        picklejarfactory.cache_directory = current_cache_directory
        o = picklejar().get('cls', (1,))
        self.assertEqual("CLASS", o.cls)

if __name__ == '__main__':
    unittest.main()

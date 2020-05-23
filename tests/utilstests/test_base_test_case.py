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

from tests.utils import test_data_directory


class BaseTestCaseTestCase(unittest.TestCase):

    def test_fhir_graph(self):
        from tests.utils.base_test_case import FHIRGraph
        from fhirtordf.rdfsupport.namespaces import FHIR, W5
        g = FHIRGraph()
        self.assertTrue(FHIR.Account in g.subjects())
        # self.assertTrue(W5.where in g.subjects())

    def test_make_and_clear_directory(self):
        from tests.utils.base_test_case import make_and_clear_directory
        test_dir = os.path.join(test_data_directory, 'mcd_test')
        safety_file = os.path.join(test_dir, "generated")
        test_file = os.path.join(test_dir, "test.txt")
        
        self.assertFalse(os.path.exists(test_dir), "mcd_test directory should not exist at this point")
        make_and_clear_directory(test_dir)
        self.assertTrue(os.path.exists(test_dir))
        self.assertTrue(os.path.exists(safety_file))
        with open(test_file, "w") as f:
            f.write("Test file")
        make_and_clear_directory(test_dir)
        self.assertFalse(os.path.exists(test_file))
        with open(test_file, "w") as f:
            f.write("Test file")
        os.remove(safety_file)
        with self.assertRaises(FileExistsError):
            make_and_clear_directory(test_dir)
        os.remove(test_file)
        os.removedirs(test_dir)
        


if __name__ == '__main__':
    unittest.main()

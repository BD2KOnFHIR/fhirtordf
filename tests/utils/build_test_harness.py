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
import os
import unittest
from typing import Optional, List, Callable


class ValidationTestCase(unittest.TestCase):
    """
    A test case builder.  Iterates over all of the files in input_directory with suffix file_suffix, invoking
    validation_function with the input file and optional output directory.

    """
    longMessage = True

    input_directory = None          # type: str
    output_directory = None         # type: Optional[str]
    file_filter = None              # type: Optional[Callable[str, str], bool]
    file_suffix = None              # type: str
    start_at = ""                   # type: Optional[str]
    skip = []                       # type: List[str]
    validation_function = None      # type: Callable[["ValidationTestCase", str, str, Optional[str]], bool]
    single_file = False             # type: bool
    max_size = 0                    # type: int
    no_tests = True                 # type: bool

    @classmethod
    def make_test_function(cls, directory: str, fname: str):
        @unittest.skipIf(cls.no_tests, "Omitted")
        def test(self):
            self.assertTrue(cls.validation_function(self, directory, fname))
        return test

    @classmethod
    def build_test_harness(cls) -> None:
        started = not bool(cls.start_at)
        test_generated = False

        for dirpath, _, filenames in os.walk(cls.input_directory):
            for fname in filenames:
                if fname.endswith(cls.file_suffix):
                    if fname not in cls.skip and (started or fname >= cls.start_at) and \
                            (not cls.file_filter or cls.file_filter(dirpath, fname)) and \
                            (not cls.max_size or os.path.getsize(os.path.join(dirpath, fname)) <= (cls.max_size * 1000)):
                        started = True
                        test_func = cls.make_test_function(dirpath, fname)
                        setattr(cls, 'test_{0}'.format(fname.rsplit('.', 1)[0]), test_func)
                        test_generated = True
                        if cls.single_file:
                            break
            if cls.single_file and test_generated:
                break

    def blank_test(self):
        self.assertTrue(True)

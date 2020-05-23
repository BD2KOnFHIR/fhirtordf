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

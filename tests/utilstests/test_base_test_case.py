
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

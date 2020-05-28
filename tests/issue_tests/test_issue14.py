import os
import unittest
from contextlib import redirect_stdout
from io import StringIO
from tempfile import mktemp

from fhirtordf.fhirtordf import main


class SDIssueUseCase(unittest.TestCase):
    def test_sd_issue(self):

        test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        of = mktemp()
        fhir_ttl = os.path.join(test_dir, 'fhir_metadata_vocabulary', 'fhir.ttl')
        args = f"-id {test_dir} -mv {fhir_ttl} -u http://dss.cora/ -no -o {of}"
        print(args)
        output = StringIO()
        with redirect_stdout(output):
            main(args.split())
        print(output.getvalue())
        # passes if we get here
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()

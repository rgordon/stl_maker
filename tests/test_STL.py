import unittest
from tempfile import NamedTemporaryFile
from pathlib import Path

"""
import sys
import os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(os.path.dirname(__file__))
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
"""
from main import STL as stl

"""To run this within your environment just 'python -m unittest discover -s tests' from project directory"""

class STLTestCase(unittest.TestCase):

    def setUp(self):
        # points are tuples (x, y, z)
        self.pt_1 = (0.0, 0.0, 0.0)
        self.pt_2 = (0.0, 10.0, 3.0)
        self.pt_3 = (5.0, 10.0, 2.0)

    def test_stl_facet(self):
        x = stl.STLFacet(self.pt_1, self.pt_2, self.pt_3)
        self.assertIsNotNone(x)
        self.assertEqual(x.normal_a, 10.0)
        self.assertEqual(x.normal_b, -15.0)
        self.assertEqual(x.normal_c, 50.0)

    def test_stl_file_text(self):

        # make a temporary file we can use for output and keep the empty file around
        test_file = NamedTemporaryFile(mode="w", delete=False)
        test_file_name = test_file.name
        test_file.close()

        # open the object and write to it
        with stl.STLFile(test_file_name, stl.TEXT_ENCODING, num_facets=1, solid_name='test') as sf:
            x = stl.STLFacet(self.pt_1, self.pt_2, self.pt_3)
            sf.append_facet(x)

        # some basic checks on the file: its here and it has something it
        check_file = Path(test_file_name)
        self.assertTrue(check_file.exists())
        self.assertTrue(check_file.is_file())
        self.assertNotEqual(check_file.stat().st_size, 0)

        # and let's clean it up manually
        check_file.unlink()
        self.assertFalse(check_file.exists())

    def test_stl_file_binary(self):

        # make a temporary file we can use for output and keep the empty file around
        test_file = NamedTemporaryFile(mode="wb", delete=False)
        test_file_name = test_file.name
        test_file.close()

        # open the object and write to it
        with stl.STLFile(test_file_name, stl.BINARY_ENCODING, num_facets=1, solid_name='test') as sf:
            x = stl.STLFacet(self.pt_1, self.pt_2, self.pt_3)
            sf.append_facet(x)

        # some basic checks on the file: its here and it has something it
        check_file = Path(test_file_name)
        self.assertTrue(check_file.exists())
        self.assertTrue(check_file.is_file())
        self.assertNotEqual(check_file.stat().st_size, 0)

        # and let's clean it up manually
        check_file.unlink()
        self.assertFalse(check_file.exists())


if __name__ == '__main__':
    unittest.main()

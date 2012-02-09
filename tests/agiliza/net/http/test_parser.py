import unittest
from agiliza.net.http.exceptions import AcceptHeaderException
from agiliza.net.http.parser import parse_accept_header


class AcceptMediaRangeTest(unittest.TestCase):
    def setUp(self):
        self.example1 = 'Accept:*/*'
        self.example2 = 'Accept:text/html'
        self.example3 = 'Accept :audio/*; q=0.2, audio/basic'
        self.example4 = 'Accept : text/plain; q=0.5, text/html, text/x-dvi; q=0.8, text/x-c'
        self.example5 = 'Accept: text/x-dvi; q=0.8, text/x-c; q = 0.6, text/x-dvi ; q =0.2'
        self.example6 = 'Some text'

        self.example1_result = {
            '*/*': 1.0,
        }
        self.example2_result = {
            'text/html': 1.0,
        }
        self.example3_result = {
            'audio/*': 0.2,
            'audio/basic': 1.0,
        }
        self.example4_result = {
            'text/plain': 0.5,
            'text/html': 1.0,
            'text/x-dvi': 0.8,
            'text/x-c': 1.0,
        }
        self.example5_result = {
            'text/x-dvi': 0.8,
            'text/x-c': 0.6,
            'text/x-dvi': 0.2,
        }

    def tearDown(self):
        self.example1 = None
        self.example2 = None
        self.example3 = None
        self.example4 = None
        self.example5 = None
        self.example6 = None

        self.example1_result = None
        self.example2_result = None
        self.example3_result = None
        self.example4_result = None
        self.example5_result = None

    def test_example1(self):
        result = parse_accept_header(self.example1)
        self.assertDictEqual(self.example1_result, result)

    def test_example2(self):
        result = parse_accept_header(self.example2)
        self.assertDictEqual(self.example2_result, result)

    def test_example3(self):
        result = parse_accept_header(self.example3)
        self.assertDictEqual(self.example3_result, result)

    def test_example4(self):
        result = parse_accept_header(self.example4)
        self.assertDictEqual(self.example4_result, result)

    def test_example5(self):
        result = parse_accept_header(self.example5)
        self.assertDictEqual(self.example5_result, result)

    def test_example6(self):
        with self.assertRaises(AcceptHeaderException):
            parse_accept_header(self.example6)


if __name__ == '__main__':
    unittest.main()

"""
Test internal classes
"""

import unittest


class TestParserBase(unittest.TestCase):
    def setUp(self):
        self.zone = u"{0}-parser-unittest.zone.".format(type(self).__name__.lower())


class TestParserBaseClass(TestParserBase):
    def test_class(self):
        from pypdnsrest.parsers import RecordParser
        p = RecordParser()
        with self.assertRaises(NotImplementedError) as context:
            p.parse("", [], 0)

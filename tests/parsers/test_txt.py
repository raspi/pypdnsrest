from pypdnsrest.parsers import TxtRecordParser
from pypdnsrest.dnsrecords import DNSTxtRecord
from tests.parsers.test_parsers import TestParserBase


class TestTxtParser(TestParserBase):
    def test_parser(self):
        p = TxtRecordParser()
        rec = p.parse(self.zone, u"test", 3600)
        self.assertIsInstance(rec, DNSTxtRecord)
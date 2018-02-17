from pypdnsrest.parsers import MxRecordParser
from pypdnsrest.dnsrecords import DNSMxRecord
from tests.parsers.test_parsers import TestParserBase


class TestMxParser(TestParserBase):
    def test_parser(self):
        p = MxRecordParser()
        rec = p.parse(self.zone, u"10 mail.{0}".format(self.zone), 3600)
        self.assertIsInstance(rec, DNSMxRecord)
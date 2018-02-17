from pypdnsrest.parsers import CnameRecordParser
from pypdnsrest.dnsrecords import DNSCNameRecord
from tests.parsers.test_parsers import TestParserBase


class TestCNameParser(TestParserBase):
    def test_parser(self):
        p = CnameRecordParser()
        rec = p.parse(self.zone, u"alias.{0}".format(self.zone), 3600)
        self.assertIsInstance(rec, DNSCNameRecord)
from pypdnsrest.parsers import AaaaRecordParser
from pypdnsrest.dnsrecords import DNSAaaaRecord
from tests.parsers.test_parsers import TestParserBase


class TestAaaaParser(TestParserBase):
    def test_parser(self):
        p = AaaaRecordParser()
        rec = p.parse(self.zone, u"fd12:3456:789a:bcde:f012:3456:789a:bcde", 3600)
        self.assertIsInstance(rec, DNSAaaaRecord)
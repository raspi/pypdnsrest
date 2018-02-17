from pypdnsrest.parsers import NsRecordParser
from pypdnsrest.dnsrecords import DNSNsRecord
from pypdnsrest.dnsrecords import InvalidDNSRecordException
from tests.parsers.test_parsers import TestParserBase


class TestNsParser(TestParserBase):
    def test_parser(self):
        p = NsRecordParser()
        rec = p.parse(self.zone, u"ns1.{0}".format(self.zone), 3600)
        self.assertIsInstance(rec, DNSNsRecord)

    def test_empty(self):
        p = NsRecordParser()
        with self.assertRaises(InvalidDNSRecordException) as context:
            p.parse(self.zone, u"", 3600)

    def test_empty2(self):
        p = NsRecordParser()
        with self.assertRaises(InvalidDNSRecordException) as context:
            p.parse(self.zone, None, 3600)

    def test_invalid_ipv6(self):
        p = NsRecordParser()
        with self.assertRaises(InvalidDNSRecordException) as context:
            p.parse(self.zone, u"fd12:3456:789a:bcde:f012:3456:789a:bcde", 3600)
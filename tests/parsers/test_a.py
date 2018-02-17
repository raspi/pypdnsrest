from pypdnsrest.parsers import ARecordParser
from pypdnsrest.dnsrecords import DNSARecord
from tests.parsers.test_parsers import TestParserBase
from ipaddress import AddressValueError


class TestAParser(TestParserBase):
    def test_parser(self):
        p = ARecordParser()
        rec = p.parse(self.zone, u"192.168.0.1", 3600)
        self.assertIsInstance(rec, DNSARecord)

    def test_empty(self):
        p = ARecordParser()
        with self.assertRaises(AddressValueError) as context:
            p.parse(self.zone, u"", 3600)

    def test_empty2(self):
        p = ARecordParser()
        with self.assertRaises(AddressValueError) as context:
            p.parse(self.zone, None, 3600)

    def test_invalid(self):
        p = ARecordParser()
        with self.assertRaises(AddressValueError) as context:
            p.parse(self.zone, u"invalid", 3600)